#!/usr/bin/env python3
"""
Scan the follower networks of tech journal listings for course code signals.

This script mirrors the parsing flow of `detect_courses.py`, but instead of
scraping content referenced in the table it traverses the GitHub social graph.
For each person listed in `other-folks.astro`, the script:

1. Extracts GitHub usernames from the row.
2. Fetches the followers and following for each username (their network).
3. Inspects those network accounts for Champlain-style course codes
   (pattern: XYZ-###) across profile metadata and repository catalog data.
4. Presents a terminal UI so you can review candidates and note which
   connections to investigate further for affiliation.

Use `--no-tui` to emit a simple text report instead of launching the interface.
Run with `--write` to append your selections into the Astro table once the review ends.
Provide a personal access token with `--token` or the `GITHUB_TOKEN` env var to
raise the GitHub rate limits; anonymous calls are heavily throttled.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from dataclasses import dataclass
from html import escape
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Optional, Sequence, Set, Tuple
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

try:
    import curses
except ImportError:  # pragma: no cover - Windows without curses support
    curses = None


COURSE_REGEX = re.compile(r"\b[A-Z]{3}-\d{3}\b")
DEFAULT_USER_AGENT = "TechJournalNetworkBot/1.0 (+https://github.com/)"


# --- Shared parsing helpers (adapted from detect_courses.py) -----------------

def extract_cells(row_html: str) -> List[str]:
    """Return the <td> cell contents for the provided table row."""
    return re.findall(r"<td>(.*?)</td>", row_html, flags=re.DOTALL)


def unique_order(items: Iterable[str]) -> Iterator[str]:
    """Yield unique items while preserving their first-seen order."""
    seen: Set[str] = set()
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        yield item


def find_course_codes(text: Optional[str]) -> Set[str]:
    """Return all matching course codes within the supplied text."""
    if not text:
        return set()
    return set(COURSE_REGEX.findall(text))


# --- Data models -------------------------------------------------------------

@dataclass
class PersonEntry:
    """A person defined in the Astro table."""

    name: str
    role: str
    year: str
    github_usernames: Set[str]


@dataclass
class ScanConfig:
    """Runtime knobs for the network scan."""

    token: Optional[str] = None
    max_network: int = 200
    max_repos: int = 40
    per_page: int = 100
    timeout: float = 10.0
    pause: float = 0.35
    user_agent: str = DEFAULT_USER_AGENT
    verbose: bool = False
    include_self: bool = False


@dataclass
class AccountMatches:
    """Course code matches detected for a GitHub account."""

    username: str
    profile_url: str
    display_name: Optional[str]
    codes: Set[str]
    sources: Set[str]  # Names from the Astro table that surfaced this account
    details: List[str]

    def merge(self, other: "AccountMatches") -> None:
        self.codes.update(other.codes)
        self.sources.update(other.sources)
        self.details.extend(detail for detail in other.details if detail not in self.details)
        if not self.display_name and other.display_name:
            self.display_name = other.display_name


# --- Astro parsing -----------------------------------------------------------

def parse_people(astro_path: Path) -> List[PersonEntry]:
    """Return all table rows with at least one GitHub username."""
    raw = astro_path.read_text(encoding="utf-8")
    tbody_match = re.search(r"(<tbody>)(.*?)(</tbody>)", raw, re.DOTALL)
    if not tbody_match:
        raise RuntimeError("Unable to locate <tbody> in Astro file.")

    people: List[PersonEntry] = []
    for match in re.finditer(r"(\s*<tr>.*?</tr>)", tbody_match.group(2), re.DOTALL):
        row_text = match.group(1).strip()
        cells = extract_cells(row_text)
        if len(cells) < 4:
            continue

        name, role, year, links_html = cells[:4]
        usernames = set()
        for href in re.findall(r'href="([^"]+)"', links_html):
            username = extract_github_username(href)
            if username:
                usernames.add(username)
        if not usernames:
            continue

        people.append(
            PersonEntry(
                name=strip_html(name),
                role=strip_html(role),
                year=strip_html(year),
                github_usernames=usernames,
            )
        )

    return people


def extract_github_username(url: str) -> Optional[str]:
    """Return the GitHub username from the supplied URL, if present."""
    try:
        parsed = urlparse(url)
    except ValueError:
        return None
    host = parsed.netloc.lower()
    if host not in {"github.com", "www.github.com"}:
        return None

    parts = [segment for segment in parsed.path.split("/") if segment]
    if not parts:
        return None
    return parts[0]


def strip_html(text: str) -> str:
    """Remove basic HTML tags from cell content."""
    return re.sub(r"<.*?>", "", text).strip()


# --- GitHub API client -------------------------------------------------------

class GitHubClient:
    """Minimal GitHub REST client with simplistic pagination handling."""

    api_root = "https://api.github.com"

    def __init__(self, config: ScanConfig) -> None:
        self.config = config
        self._user_cache: Dict[str, dict] = {}
        self._repos_cache: Dict[str, List[dict]] = {}
        self._network_cache: Dict[Tuple[str, str], List[str]] = {}

    def _headers(self) -> Dict[str, str]:
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": self.config.user_agent,
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self.config.token:
            headers["Authorization"] = f"Bearer {self.config.token}"
        return headers

    def fetch_user(self, username: str) -> Optional[dict]:
        username = username.strip()
        if username in self._user_cache:
            return self._user_cache[username]

        data = self._request_json(f"/users/{username}")
        self._user_cache[username] = data or {}
        return data

    def fetch_network(self, username: str, relation: str) -> List[str]:
        """Return followers or following usernames."""
        key = (username, relation)
        if key in self._network_cache:
            return list(self._network_cache[key])

        path = f"/users/{username}/{relation}?per_page={self.config.per_page}"
        usernames: List[str] = []
        for item in self._paginate(path):
            if not isinstance(item, dict):
                continue
            login = item.get("login")
            if login:
                usernames.append(login)
            if len(usernames) >= self.config.max_network:
                break

        self._network_cache[key] = list(usernames)
        return usernames

    def fetch_repositories(self, username: str) -> List[dict]:
        username = username.strip()
        if username in self._repos_cache:
            return list(self._repos_cache[username])

        repos: List[dict] = []
        params = f"?per_page={self.config.per_page}&type=owner&sort=updated"
        for item in self._paginate(f"/users/{username}/repos{params}"):
            if not isinstance(item, dict):
                continue
            repos.append(item)
            if len(repos) >= self.config.max_repos:
                break

        self._repos_cache[username] = list(repos)
        return repos

    # -- Core request helpers -------------------------------------------------

    def _request_json(self, path: str) -> Optional[dict]:
        url = f"{self.api_root}{path}"
        payload = self._request_raw(url)
        if payload is None:
            return None
        try:
            return json.loads(payload)
        except json.JSONDecodeError:
            return None

    def _paginate(self, path: str) -> Iterator[dict]:
        url: Optional[str] = f"{self.api_root}{path}"
        fetched = 0
        while url:
            payload, headers = self._request_with_headers(url)
            if payload is None:
                return
            try:
                data = json.loads(payload)
            except json.JSONDecodeError:
                return
            if isinstance(data, list):
                for item in data:
                    fetched += 1
                    yield item
                    if fetched >= self.config.max_network:
                        return
            next_url = self._next_link(headers)
            url = next_url
            if url and self.config.pause:
                time.sleep(self.config.pause)

    def _request_raw(self, url: str) -> Optional[str]:
        payload, _ = self._request_with_headers(url)
        return payload

    def _request_with_headers(self, url: str) -> Tuple[Optional[str], Dict[str, str]]:
        headers = self._headers()
        request = Request(url, headers=headers)

        if self.config.verbose:
            print(f"[github] GET {url}")

        try:
            with urlopen(request, timeout=self.config.timeout) as response:
                payload = response.read().decode("utf-8", errors="replace")
                header_map = {key: value for key, value in response.headers.items()}
        except HTTPError as error:
            if error.code == 404:
                return None, {}
            if error.code == 403:
                reset = error.headers.get("X-RateLimit-Reset")
                remaining = error.headers.get("X-RateLimit-Remaining")
                if self.config.verbose:
                    print(
                        f"[github] rate limited: remaining={remaining} reset={reset}",
                        file=sys.stderr,
                    )
            if self.config.verbose:
                print(f"[github] HTTP error {error.code} for {url}", file=sys.stderr)
            return None, {}
        except URLError as error:
            if self.config.verbose:
                print(f"[github] URL error for {url}: {error}", file=sys.stderr)
            return None, {}

        if self.config.pause:
            time.sleep(self.config.pause)
        return payload, header_map

    @staticmethod
    def _next_link(headers: Dict[str, str]) -> Optional[str]:
        link_header = headers.get("Link")
        if not link_header:
            return None
        parts = [part.strip() for part in link_header.split(",")]
        for part in parts:
            if 'rel="next"' not in part:
                continue
            match = re.search(r"<([^>]+)>", part)
            if match:
                return match.group(1)
        return None


# --- Account inspection ------------------------------------------------------

class AccountInspector:
    """Inspect GitHub accounts for course code matches."""

    def __init__(self, client: GitHubClient, config: ScanConfig) -> None:
        self.client = client
        self.config = config
        self._result_cache: Dict[str, AccountMatches] = {}

    def inspect(self, username: str, source_label: str) -> Optional[AccountMatches]:
        username = username.strip()
        if not username:
            return None

        cached = self._result_cache.get(username.lower())
        if cached:
            cached.sources.add(source_label)
            return cached

        profile = self.client.fetch_user(username)
        if not profile:
            return None

        codes: Set[str] = set()
        details: List[str] = []

        for field in ("name", "bio", "company", "location"):
            value = profile.get(field)
            detected = find_course_codes(value)
            if detected:
                codes.update(detected)
                label = field.title()
                details.append(f"{label}: {value}")

        repos = self.client.fetch_repositories(username)
        for repo in repos:
            repo_name = repo.get("name", "")
            full_name = repo.get("full_name", repo_name)
            description = repo.get("description")

            detected_name = find_course_codes(repo_name)
            if detected_name:
                codes.update(detected_name)
                details.append(f"Repo name: {full_name}")

            detected_desc = find_course_codes(description)
            if detected_desc:
                codes.update(detected_desc)
                details.append(f"Repo desc: {full_name} -> {description}")

        if not codes:
            return None

        matches = AccountMatches(
            username=username,
            profile_url=profile.get("html_url") or f"https://github.com/{username}",
            display_name=profile.get("name"),
            codes=codes,
            sources={source_label},
            details=details,
        )
        self._result_cache[username.lower()] = matches
        return matches


# --- TUI ---------------------------------------------------------------------

class ReviewTUI:
    """Simple curses interface for reviewing matched accounts."""

    def __init__(self, matches: Sequence[AccountMatches]) -> None:
        self.matches = list(matches)
        self.selected = 0
        self.marked: Set[int] = set()

    def run(self) -> List[int]:
        if curses is None:
            raise RuntimeError("curses is not available on this system.")
        return curses.wrapper(self._main)

    def _main(self, stdscr: "curses._CursesWindow") -> List[int]:
        curses.curs_set(0)
        stdscr.nodelay(False)

        while True:
            stdscr.erase()
            height, width = stdscr.getmaxyx()

            title = (
                "Course Code Candidate Review (↑/↓ move, space toggle, enter details, a all, c clear, q quit)"
            )
            stdscr.addnstr(0, 0, title.ljust(width), width, curses.A_REVERSE)

            visible_rows = max(1, height - 4)
            start = max(0, self.selected - visible_rows // 2)
            end = min(len(self.matches), start + visible_rows)
            start = max(0, end - visible_rows)

            for idx in range(start, end):
                match = self.matches[idx]
                row = idx - start + 1
                prefix = "▶" if idx == self.selected else " "
                marker = "✓" if idx in self.marked else " "
                codes = ", ".join(sorted(match.codes))
                sources = ", ".join(sorted(match.sources))
                summary = f"{prefix} [{marker}] {match.username:<18} codes: {codes:<20} via: {sources}"
                attr = curses.A_BOLD if idx == self.selected else curses.A_NORMAL
                stdscr.addnstr(row, 0, summary.ljust(width), width, attr)

            detail_lines = self.matches[self.selected].details if self.matches else []
            detail_y = height - 3
            if detail_y > 1:
                stdscr.hline(detail_y - 1, 0, "-", width)
                stdscr.addnstr(detail_y, 0, "Details:", width, curses.A_UNDERLINE)
                max_detail_rows = max(0, height - detail_y - 2)
                for offset, detail in enumerate(detail_lines[:max_detail_rows]):
                    safe_detail = detail.replace("\n", " ")
                    stdscr.addnstr(detail_y + 1 + offset, 0, safe_detail.ljust(width), width)

            key = stdscr.getch()
            if key in (ord("q"), 27):
                return sorted(self.marked)
            if key in (curses.KEY_DOWN, ord("j")):
                self.selected = min(self.selected + 1, len(self.matches) - 1)
            elif key in (curses.KEY_UP, ord("k")):
                self.selected = max(self.selected - 1, 0)
            elif key in (ord(" "), ord("x")):
                if self.selected in self.marked:
                    self.marked.remove(self.selected)
                else:
                    self.marked.add(self.selected)
            elif key in (curses.KEY_ENTER, 10, 13):
                self._show_popup(stdscr, self.matches[self.selected])
            elif key in (ord("a"),):
                # Quick toggle to select all
                self.marked = set(range(len(self.matches)))
            elif key in (ord("c"),):
                self.marked.clear()

    def _show_popup(self, stdscr: "curses._CursesWindow", match: AccountMatches) -> None:
        height, width = stdscr.getmaxyx()
        popup_height = min(10, height - 4)
        popup_width = min(70, width - 4)
        top = (height - popup_height) // 2
        left = (width - popup_width) // 2

        window = stdscr.subwin(popup_height, popup_width, top, left)
        window.box()
        window.addnstr(0, 2, f" {match.username} ", popup_width - 4, curses.A_REVERSE)
        window.addnstr(1, 2, f"URL: {match.profile_url}", popup_width - 4)
        window.addnstr(2, 2, f"Codes: {', '.join(sorted(match.codes))}", popup_width - 4)
        window.addnstr(3, 2, f"Sources: {', '.join(sorted(match.sources))}", popup_width - 4)
        window.addnstr(5, 2, "Details:", popup_width - 4, curses.A_UNDERLINE)

        for idx, detail in enumerate(match.details[: popup_height - 7]):
            window.addnstr(6 + idx, 2, detail, popup_width - 4)

        window.addnstr(popup_height - 2, 2, "Press any key to close", popup_width - 4, curses.A_DIM)
        stdscr.refresh()
        window.refresh()
        window.getch()


# --- Reporting ---------------------------------------------------------------

def print_report(matches: Sequence[AccountMatches]) -> None:
    if not matches:
        print("No course code matches found within the scanned networks.")
        return

    for match in matches:
        print(f"- {match.username}: {', '.join(sorted(match.codes))}")
        print(f"  URL     : {match.profile_url}")
        print(f"  Sources : {', '.join(sorted(match.sources))}")
        for detail in match.details:
            print(f"    - {detail}")
        print()


# --- Main orchestration ------------------------------------------------------

def scan_networks(people: Sequence[PersonEntry], config: ScanConfig) -> List[AccountMatches]:
    client = GitHubClient(config)
    inspector = AccountInspector(client, config)
    aggregated: Dict[str, AccountMatches] = {}
    seed_accounts = {username.lower() for person in people for username in person.github_usernames}

    for person in people:
        if config.verbose:
            print(f"[scan] {person.name} ({', '.join(person.github_usernames)})")

        for username in sorted(person.github_usernames):
            followers = client.fetch_network(username, "followers")
            following = client.fetch_network(username, "following")
            network = list(unique_order(followers + following))

            for account in network:
                if not config.include_self and account.lower() in seed_accounts:
                    continue

                source_label = f"{person.name} ({username})"
                matches = inspector.inspect(account, source_label)
                if not matches:
                    continue
                key = matches.username.lower()
                existing = aggregated.get(key)
                if existing:
                    existing.merge(matches)
                else:
                    aggregated[key] = AccountMatches(
                        username=matches.username,
                        profile_url=matches.profile_url,
                        display_name=matches.display_name,
                        codes=set(matches.codes),
                        sources=set(matches.sources),
                        details=list(matches.details),
                    )

    return sorted(aggregated.values(), key=lambda m: (m.username.lower()))


def build_row_payloads(
    matches: Sequence[AccountMatches], existing_usernames: Set[str]
) -> List[Tuple[str, str, str]]:
    """
    Convert account matches into HTML rows while skipping existing usernames.

    Returns a list of tuples: (display_name, username, row_html).
    """
    rows: List[Tuple[str, str, str]] = []
    seen = {username.lower() for username in existing_usernames}

    for match in matches:
        username_lower = match.username.lower()
        if username_lower in seen:
            continue

        display_name = (match.display_name or match.username).strip() or match.username
        safe_name = escape(display_name)

        profile_url = match.profile_url or f"https://github.com/{match.username}"
        safe_url = escape(profile_url, quote=True)
        link_html = f'<a href="{safe_url}">{safe_url}</a>'

        row_html = f'<tr><td>{safe_name}</td><td></td><td></td><td>{link_html}</td><td></td><td></td></tr>'
        rows.append((display_name, match.username, row_html))
        seen.add(username_lower)

    return rows


def append_rows_to_table(astro_path: Path, row_payloads: Sequence[Tuple[str, str, str]]) -> None:
    """
    Append the supplied rows to the manual (unsorted) table so the primary
    listings remain untouched by automation.
    """
    if not row_payloads:
        return

    content = astro_path.read_text(encoding="utf-8")
    manual_match = re.search(
        r"(<details\s+class=\"manual-entries\"[^>]*>.*?<tbody>)(.*?)(</tbody>)",
        content,
        re.DOTALL,
    )
    if not manual_match:
        raise RuntimeError("Unable to append rows: manual-entries table not found.")

    indent = "          "
    insertion = "".join(f"{indent}{row}\n" for _, _, row in row_payloads)
    insert_at = manual_match.start(3)

    if not content[:insert_at].endswith("\n"):
        insertion = "\n" + insertion

    updated = content[:insert_at] + insertion + content[insert_at:]
    astro_path.write_text(updated, encoding="utf-8")


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scan GitHub networks for course code matches and review in a TUI."
    )
    parser.add_argument(
        "--file",
        default="src/pages/techjournals/other-folks.astro",
        help="Astro file containing the listings table.",
    )
    parser.add_argument(
        "--token",
        default=os.getenv("GITHUB_TOKEN"),
        help="GitHub personal access token. Falls back to GITHUB_TOKEN env var.",
    )
    parser.add_argument(
        "--max-network",
        type=int,
        default=200,
        help="Maximum follower/following accounts to inspect per seed username.",
    )
    parser.add_argument(
        "--max-repos",
        type=int,
        default=40,
        help="Maximum repositories to inspect per network account.",
    )
    parser.add_argument("--timeout", type=float, default=10.0, help="Request timeout in seconds.")
    parser.add_argument("--pause", type=float, default=0.35, help="Delay between HTTP requests.")
    parser.add_argument("--per-page", type=int, default=100, help="GitHub pagination size.")
    parser.add_argument(
        "--no-tui",
        action="store_true",
        help="Print a text report instead of launching the review interface.",
    )
    parser.add_argument(
        "--include-self",
        action="store_true",
        help="Inspect the listed accounts themselves in addition to their networks.",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Append selected matches to the Astro table after review.",
    )
    parser.add_argument("--verbose", action="store_true", help="Enable progress logging.")
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    astro_path = Path(args.file)
    if not astro_path.exists():
        print(f"File not found: {astro_path}", file=sys.stderr)
        return 1

    config = ScanConfig(
        token=args.token,
        max_network=max(args.max_network, 1),
        max_repos=max(args.max_repos, 1),
        per_page=max(args.per_page, 1),
        timeout=max(args.timeout, 1.0),
        pause=max(args.pause, 0.0),
        verbose=args.verbose,
        include_self=args.include_self,
    )

    try:
        people = parse_people(astro_path)
    except RuntimeError as error:
        print(str(error), file=sys.stderr)
        return 1
    if not people:
        print("No GitHub usernames found in the Astro table.", file=sys.stderr)
        return 1

    matches = scan_networks(people, config)
    if not matches:
        print("No course code matches discovered within the scanned networks.")
        return 0

    existing_usernames = {username.lower() for person in people for username in person.github_usernames}

    selected_matches: List[AccountMatches]

    if args.no_tui:
        print_report(matches)
        selected_matches = list(matches)
    else:
        try:
            marked_indexes = ReviewTUI(matches).run()
            selected_matches = [matches[idx] for idx in marked_indexes]
        except RuntimeError as error:
            print(f"{error}\nFalling back to text report.\n", file=sys.stderr)
            print_report(matches)
            selected_matches = list(matches)

    if args.write:
        row_payloads = build_row_payloads(selected_matches, existing_usernames)
        if not row_payloads:
            if not selected_matches:
                print("No candidates selected for insertion; no changes made.")
            else:
                print("All selected candidates already exist in the table; no changes made.")
            return 0

        append_rows_to_table(astro_path, row_payloads)
        summaries = [f"{name} (@{username})" for name, username, _ in row_payloads]
        print(f"Appended {len(row_payloads)} row(s) to {astro_path}:")
        for summary in summaries:
            print(f"  - {summary}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
