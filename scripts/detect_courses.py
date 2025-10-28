#!/usr/bin/env python3
"""
Detect course codes referenced from tech journal listings and update the Astro table.

For each person listed in `other-folks.astro`, this script crawls the provided link(s),
collects course codes matching the pattern XYZ-###, and writes them into a new
"Courses Detected" column. The crawl is limited per root URL to avoid runaway recursion.
Use `--verbose` to see progress logs while scraping.
"""
from __future__ import annotations

import argparse
import dataclasses
import re
import sys
import time
from collections import deque
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable, Iterator, List, Optional, Set, Tuple
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse, urldefrag
from urllib.request import Request, urlopen


COURSE_REGEX = re.compile(r"\b[A-Z]{3}-\d{3}\b")
ROW_REGEX = re.compile(
    r"<tr><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td>(?:<td>(.*?)</td>)?</tr>",
    re.DOTALL,
)
HEADER_SENTINEL = "<th>Courses Detected</th>"


def find_course_codes(text: str) -> Set[str]:
    """Return all matching course codes within the supplied text."""
    return set(COURSE_REGEX.findall(text))


def strip_fragment(url: str) -> str:
    """Remove URL fragment identifiers."""
    clean, _ = urldefrag(url)
    return clean


def same_host(url: str, compare: str) -> bool:
    """Check whether the hostnames match (case-insensitive)."""
    a = urlparse(url).netloc.lower()
    b = urlparse(compare).netloc.lower()
    return a == b


class AnchorExtractor(HTMLParser):
    """Collect anchor hrefs from arbitrary HTML snippets."""

    def __init__(self) -> None:
        super().__init__()
        self.links: List[str] = []

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, str]]) -> None:
        if tag.lower() != "a":
            return
        for name, value in attrs:
            if name.lower() == "href" and value:
                self.links.append(value)

    @classmethod
    def extract(cls, html: str) -> List[str]:
        parser = cls()
        parser.feed(html)
        return parser.links


@dataclasses.dataclass
class CrawlConfig:
    max_depth: int = 1
    max_pages: int = 4
    timeout: float = 8.0
    pause: float = 0.25  # polite delay between requests
    user_agent: str = "TechJournalCourseBot/1.0 (+https://github.com/)"
    verbose: bool = False


class CourseCrawler:
    """Breadth-first crawler that gathers course codes from HTML pages."""

    def __init__(self, config: CrawlConfig) -> None:
        self.config = config
        self._result_cache: dict[str, Set[str]] = {}
        self._page_cache: dict[str, Optional[str]] = {}

    def collect_from_links(self, html: str) -> Set[str]:
        codes: Set[str] = set()
        for raw_href in unique_order(AnchorExtractor.extract(html)):
            normalized = self._normalize_url(raw_href)
            if not normalized:
                continue
            codes.update(self.crawl(normalized))
        return codes

    def crawl(self, url: str) -> Set[str]:
        normalized = self._normalize_url(url)
        if not normalized:
            return set()
        if normalized in self._result_cache:
            self._log(f"[cache] {normalized}")
            return set(self._result_cache[normalized])

        visited: Set[str] = set()
        queue: deque[Tuple[str, int]] = deque([(normalized, 0)])
        discovered_codes: Set[str] = set()

        self._log(f"[crawl] start {normalized}")

        while queue and len(visited) < self.config.max_pages:
            current, depth = queue.popleft()
            if current in visited:
                continue
            visited.add(current)

            self._log(f"[fetch] {current} (depth {depth})")
            text = self._fetch(current)
            if text is None:
                self._log(f"[skip] unsupported content {current}")
                continue

            discovered_codes.update(find_course_codes(text))
            if self.config.verbose and find_course_codes(text):
                codes = ", ".join(sorted(find_course_codes(text)))
                self._log(f"[codes] {current}: {codes}")

            if depth >= self.config.max_depth:
                continue

            for href in AnchorExtractor.extract(text):
                next_url = self._normalize_url(urljoin(current, href))
                if not next_url:
                    continue
                if not same_host(normalized, next_url):
                    continue
                if next_url in visited:
                    continue
                queue.append((next_url, depth + 1))

        self._result_cache[normalized] = set(discovered_codes)
        if discovered_codes:
            codes = ", ".join(sorted(discovered_codes))
            self._log(f"[result] {normalized}: {codes}")
        else:
            self._log(f"[result] {normalized}: none")
        return discovered_codes

    def _fetch(self, url: str) -> Optional[str]:

        if url in self._page_cache:
            return self._page_cache[url]

        headers = {"User-Agent": self.config.user_agent, "Accept": "text/html, text/plain"}
        request = Request(url, headers=headers)

        try:
            with urlopen(request, timeout=self.config.timeout) as response:
                content_type = response.headers.get_content_type()
                if content_type not in {"text/html", "text/plain", "application/xhtml+xml"}:
                    self._page_cache[url] = None
                    return None

                charset = response.headers.get_content_charset() or "utf-8"
                raw = response.read(1_500_000)  # cap at ~1.5MB per page
                text = raw.decode(charset, errors="replace")
        except (HTTPError, URLError, TimeoutError, UnicodeDecodeError):
            text = None

        self._page_cache[url] = text
        if text is not None and self.config.pause:
            time.sleep(self.config.pause)
        return text

    def _log(self, message: str) -> None:
        if self.config.verbose:
            print(message)

    @staticmethod
    def _normalize_url(url: Optional[str]) -> Optional[str]:
        if not url:
            return None
        parsed = urlparse(url.strip())
        if not parsed.scheme:
            parsed = urlparse(f"https://{url.strip()}")
        if parsed.scheme not in {"http", "https"}:
            return None
        normalized = parsed._replace(fragment="")
        return normalized.geturl()


def unique_order(items: Iterable[str]) -> Iterator[str]:
    seen: Set[str] = set()
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        yield item


def ensure_header_column(source: str) -> str:
    if HEADER_SENTINEL in source:
        return source
    header_line = "          <th>Best Content*</th>"
    replacement = f"{header_line}\n          {HEADER_SENTINEL}"
    if header_line not in source:
        raise RuntimeError("Unable to locate Best Content header; aborting.")
    return source.replace(header_line, replacement, 1)


def update_rows(source: str, crawler: CourseCrawler, verbose: bool = False) -> str:
    tbody_match = re.search(r"(<tbody>)(.*?)(</tbody>)", source, re.DOTALL)
    if not tbody_match:
        raise RuntimeError("Unable to find <tbody> block.")

    body_content = tbody_match.group(2)
    rebuilt = []
    last_index = 0

    for match in re.finditer(r"(\s*<tr>.*?</tr>)", body_content, re.DOTALL):
        rebuilt.append(body_content[last_index:match.start()])
        row_text = match.group(1)
        leading_ws = row_text[: len(row_text) - len(row_text.lstrip())]
        trimmed = row_text.strip()

        parsed = ROW_REGEX.fullmatch(trimmed)
        if not parsed:
            rebuilt.append(row_text)
            last_index = match.end()
            continue

        name, role, year, links_html, best_html, _existing_courses = parsed.groups()
        link_urls = list(unique_order(re.findall(r'href="([^"]+)"', links_html)))
        if not link_urls:
            courses = set()
        else:
            courses = set()
            for url in link_urls:
                courses.update(crawler.crawl(url))

        sorted_courses = sorted(courses)
        courses_html = "<br/>".join(sorted_courses)

        if verbose:
            summary = ", ".join(sorted_courses) if sorted_courses else "none"
            print(f"[row] {name}: {summary}")

        new_row = (
            f"{leading_ws}<tr>"
            f"<td>{name}</td>"
            f"<td>{role}</td>"
            f"<td>{year}</td>"
            f"<td>{links_html}</td>"
            f"<td>{best_html}</td>"
            f"<td>{courses_html}</td>"
            f"</tr>"
        )
        rebuilt.append(new_row)
        last_index = match.end()

    rebuilt.append(body_content[last_index:])

    inner = "".join(rebuilt)
    return source[:tbody_match.start(2)] + inner + source[tbody_match.end(2):]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scrape tech journal listings for course codes.")
    parser.add_argument(
        "--file",
        default="src/pages/techjournals/other-folks.astro",
        help="Astro file containing the listings table.",
    )
    parser.add_argument("--max-depth", type=int, default=1, help="Maximum crawl depth per starting URL.")
    parser.add_argument(
        "--max-pages",
        type=int,
        default=4,
        help="Maximum number of pages to fetch per starting URL (inclusive).",
    )
    parser.add_argument("--timeout", type=float, default=8.0, help="Request timeout in seconds.")
    parser.add_argument(
        "--pause",
        type=float,
        default=0.25,
        help="Delay between HTTP requests (seconds).",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print progress logs while crawling and updating rows.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    astro_path = Path(args.file)
    if not astro_path.exists():
        print(f"File not found: {astro_path}", file=sys.stderr)
        return 1

    raw_content = astro_path.read_text(encoding="utf-8")
    raw_content = ensure_header_column(raw_content)

    crawler = CourseCrawler(
        CrawlConfig(
            max_depth=max(args.max_depth, 0),
            max_pages=max(args.max_pages, 1),
            timeout=max(args.timeout, 1.0),
            pause=max(args.pause, 0.0),
            verbose=args.verbose,
        )
    )

    updated = update_rows(raw_content, crawler, verbose=args.verbose)
    astro_path.write_text(updated, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
