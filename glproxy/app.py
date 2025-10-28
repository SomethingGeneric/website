from __future__ import annotations

import logging
import os
import re
import textwrap
from datetime import datetime, timezone
from html import escape
from typing import Any, Dict, Optional
from uuid import uuid4

import requests
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator


LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=LOG_LEVEL, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger(__name__)

GITLAB_API_BASE = os.getenv("GITLAB_API_BASE", "https://gitlab.goober.cloud/api/v4").rstrip("/")
GITLAB_PROJECT_PATH = os.getenv("GITLAB_PROJECT_PATH", "matt/website")
GITLAB_API_TOKEN = os.getenv("GITLAB_API_TOKEN")
ISSUE_LABELS = os.getenv("ISSUE_LABELS", "")
ALLOWED_ORIGINS_RAW = os.getenv("ALLOWED_ORIGINS", "")

ENABLE_MERGE_REQUESTS = os.getenv("ENABLE_MERGE_REQUESTS", "true").lower() in {"1", "true", "yes"}
GITLAB_MR_TARGET_BRANCH = os.getenv("GITLAB_MR_TARGET_BRANCH", "main")
GITLAB_MR_FILE_DIR = os.getenv("GITLAB_MR_FILE_DIR", "incoming-techjournals")
OTHER_FOLKS_FILE_PATH = "src/pages/techjournals/other-folks.astro"

if not GITLAB_API_TOKEN:
	def _missing_token() -> None:
		raise RuntimeError("GITLAB_API_TOKEN env var is required")

	_missing_token()

ALLOWED_ORIGINS = {origin.strip() for origin in ALLOWED_ORIGINS_RAW.split(",") if origin.strip()}

app = FastAPI(title="Techjournal Submission Proxy", version="2.0.0")

if ALLOWED_ORIGINS:
	app.add_middleware(
		CORSMiddleware,
		allow_origins=list(ALLOWED_ORIGINS),
		allow_methods=["POST", "OPTIONS"],
		allow_headers=["Content-Type"],
	)
else:
	app.add_middleware(
		CORSMiddleware,
		allow_origins=["*"],
		allow_methods=["POST", "OPTIONS"],
		allow_headers=["Content-Type"],
	)

_session = requests.Session()
_session.headers.update({"PRIVATE-TOKEN": GITLAB_API_TOKEN})
DEFAULT_TIMEOUT = 15


ROLE_LABELS = {"student": "Student", "staff": "Staff"}


class Submission(BaseModel):
	model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)

	name: str
	link: HttpUrl
	role: Optional[str] = None
	grad_year: Optional[str] = Field(None, alias="gradYear")

	@field_validator("name")
	@classmethod
	def _strip_name(cls, value: str) -> str:
		value = value.strip()
		if not value:
			raise ValueError("name must not be blank")
		return value

	@field_validator("role")
	@classmethod
	def _validate_role(cls, value: Optional[str]) -> Optional[str]:
		if value is None or value == "":
			return None
		normalized = value.strip().lower()
		if normalized not in {"student", "staff"}:
			raise ValueError("role must be either 'student' or 'staff'")
		return normalized

	@field_validator("grad_year", mode="before")
	@classmethod
	def _validate_grad_year(cls, value: Optional[str]) -> Optional[str]:
		if value is None or value == "":
			return None
		value = str(value).strip()
		if not re.fullmatch(r"\d{4}", value):
			raise ValueError("gradYear must be four digits (e.g., 2026)")
		return value


def _gitlab_request(method: str, endpoint: str, **kwargs: Any) -> requests.Response:
	url = f"{GITLAB_API_BASE.rstrip('/')}/{endpoint.lstrip('/')}"
	if "timeout" not in kwargs:
		kwargs["timeout"] = DEFAULT_TIMEOUT
	logger.debug("GitLab request %s %s", method.upper(), url)
	response = _session.request(method=method.upper(), url=url, **kwargs)
	return response


def _project_path_encoded() -> str:
	return requests.utils.quote(GITLAB_PROJECT_PATH, safe="")


def _format_role_label(submission: Submission) -> str:
	return ROLE_LABELS.get(submission.role or "", "")


def _format_display_name(submission: Submission) -> str:
	base = submission.name
	role_label = _format_role_label(submission)
	if submission.role == "student" and submission.grad_year:
		return f"{base} (student, {submission.grad_year})"
	if submission.role == "student":
		return f"{base} (student)"
	if submission.role == "staff":
		return f"{base} (staff)"
	return base


def _fetch_file_contents(file_path: str, ref: str) -> tuple[Optional[str], Optional[str]]:
	encoded_path = requests.utils.quote(file_path, safe="")
	endpoint = f"projects/{_project_path_encoded()}/repository/files/{encoded_path}/raw"
	try:
		response = _gitlab_request("GET", endpoint, params={"ref": ref})
	except requests.RequestException as exc:
		logger.warning("Network error while fetching %s: %s", file_path, exc)
		return None, str(exc)

	if response.status_code == 200:
		return response.text, None

	logger.warning("Failed to fetch %s: status=%s body=%s", file_path, response.status_code, response.text)
	return None, f"status={response.status_code} body={response.text}"


def _render_table_row(submission: Submission) -> str:
	name_html = escape(submission.name)
	role_html = escape(_format_role_label(submission))
	year_html = escape(submission.grad_year or "")
	link_str = str(submission.link)
	link_html = escape(link_str)
	return f'        <tr><td>{name_html}</td><td>{role_html}</td><td>{year_html}</td><td><a href="{link_html}">{link_html}</a></td><td></td></tr>\n'


def _inject_submission_row(existing_content: str, submission: Submission) -> tuple[str, bool]:
	link_html = escape(str(submission.link))
	if link_html in existing_content:
		logger.info("Link %s already present in other-folks.astro; skipping table update", link_html)
		return existing_content, False

	marker = "</tbody>"
	index = existing_content.find(marker)
	if index == -1:
		raise RuntimeError("Unable to locate </tbody> in other-folks.astro")

	row = _render_table_row(submission)
	if not existing_content[:index].endswith("\n"):
		row = "\n" + row

	updated_content = existing_content[:index] + row + existing_content[index:]
	logger.info("Inserted new techjournal row for %s", submission.name)
	return updated_content, True


def _create_gitlab_issue(submission: Submission) -> Dict[str, Any]:
	display_name = _format_display_name(submission)
	role_label = _format_role_label(submission)
	issue_title = f"New techjournal submission: {display_name}"
	issue_body = "\n".join(
		[
			f"**Name:** {submission.name}",
			f"**Link:** {submission.link}",
			*( [f"**Role:** {role_label}"] if role_label else [] ),
			*( [f"**Graduation Year:** {submission.grad_year}"] if submission.grad_year else [] ),
			"",
			"Submitted via techjournals/other-folks modal.",
		]
	)

	payload: Dict[str, Any] = {
		"title": issue_title,
		"description": issue_body,
	}

	if ISSUE_LABELS:
		payload["labels"] = ISSUE_LABELS

	endpoint = f"projects/{_project_path_encoded()}/issues"
	try:
		response = _gitlab_request("POST", endpoint, json=payload)
	except requests.RequestException as exc:  # pragma: no cover - network failure
		logger.exception("Error connecting to GitLab for issue creation")
		raise HTTPException(
			status_code=status.HTTP_502_BAD_GATEWAY,
			detail={"error": "Failed to reach GitLab", "details": str(exc)},
		) from exc

	if response.status_code >= 400:
		logger.warning("GitLab issue creation failed: status=%s body=%s", response.status_code, response.text)
		raise HTTPException(
			status_code=status.HTTP_502_BAD_GATEWAY,
			detail={
				"error": "GitLab rejected the request",
				"status": response.status_code,
				"body": response.text,
			},
		)

	issue = response.json()
	logger.info("Created GitLab issue %s (%s)", issue.get("iid"), issue.get("web_url"))
	return issue


def _build_branch_name(issue_iid: int) -> str:
	base = f"techjournal-submission-{issue_iid}"
	return base[:250]


def _ensure_branch(branch_name: str) -> tuple[Optional[str], Optional[str]]:
	endpoint = f"projects/{_project_path_encoded()}/repository/branches"
	payload = {"branch": branch_name, "ref": GITLAB_MR_TARGET_BRANCH}
	try:
		response = _gitlab_request("POST", endpoint, params=payload)
	except requests.RequestException as exc:
		logger.warning("Network error while creating branch '%s': %s", branch_name, exc)
		return None, str(exc)

	if response.status_code == 409:
		new_branch = f"{branch_name}-{uuid4().hex[:8]}"
		logger.info("Branch %s already exists; retrying with %s", branch_name, new_branch)
		return _ensure_branch(new_branch)

	if response.status_code >= 400:
		logger.warning("Unable to create branch '%s': %s", branch_name, response.text)
		return None, f"status={response.status_code} body={response.text}"

	created_branch = response.json().get("name") or branch_name
	logger.info("Created GitLab branch %s for issue", created_branch)
	return created_branch, None


def _prepare_commit_actions(issue: Dict[str, Any], submission: Submission) -> tuple[Optional[list[Dict[str, Any]]], bool, Optional[str]]:
	other_folks_content, fetch_error = _fetch_file_contents(OTHER_FOLKS_FILE_PATH, GITLAB_MR_TARGET_BRANCH)
	if other_folks_content is None:
		return None, False, f"Unable to fetch {OTHER_FOLKS_FILE_PATH}: {fetch_error}"

	try:
		updated_content, added_row = _inject_submission_row(other_folks_content, submission)
	except RuntimeError as exc:
		logger.error("Failed to update other-folks.astro: %s", exc)
		return None, False, str(exc)

	display_name = _format_display_name(submission)
	timestamp = datetime.now(timezone.utc).isoformat()
	file_path = f"{GITLAB_MR_FILE_DIR.rstrip('/')}/issue-{issue.get('iid')}.md"
	role_label = _format_role_label(submission)
	content = textwrap.dedent(
		f"""\
		# Techjournal Submission

		- **Issue**: #{issue.get('iid')}
		- **Created**: {timestamp}
		- **Name**: {submission.name}
		- **Display Name**: {display_name}
		{"- **Role**: " + role_label if role_label else ""}
		{"- **Graduation Year**: " + submission.grad_year if submission.grad_year else ""}
		- **Link**: {submission.link}

		This file was generated automatically when the submission was received.
		"""
	)

	actions: list[Dict[str, Any]] = []
	if added_row:
		actions.append(
			{
				"action": "update",
				"file_path": OTHER_FOLKS_FILE_PATH,
				"content": updated_content,
			}
		)

	actions.append(
		{
			"action": "create",
			"file_path": file_path,
			"content": content,
		}
	)

	return actions, added_row, None


def _create_submission_commit(branch_name: str, issue: Dict[str, Any], submission: Submission) -> tuple[bool, Optional[str], bool]:
	actions, added_row, preparation_error = _prepare_commit_actions(issue, submission)
	if actions is None:
		return False, preparation_error, False

	display_name = _format_display_name(submission)
	payload = {
		"branch": branch_name,
		"commit_message": f"Add techjournal submission for {display_name}",
		"actions": actions,
	}

	endpoint = f"projects/{_project_path_encoded()}/repository/commits"
	try:
		response = _gitlab_request("POST", endpoint, json=payload)
	except requests.RequestException as exc:
		logger.warning("Network error while committing on %s: %s", branch_name, exc)
		return False, str(exc), added_row

	if response.status_code >= 400:
		logger.warning("Failed to create commit on %s: %s", branch_name, response.text)
		return False, f"status={response.status_code} body={response.text}", added_row

	logger.info("Added submission stub to branch %s (table row added=%s)", branch_name, added_row)
	return True, None, added_row


def _create_merge_request(branch_name: str, issue: Dict[str, Any], submission: Submission) -> tuple[Optional[Dict[str, Any]], Optional[str]]:
	display_name = _format_display_name(submission)
	role_label = _format_role_label(submission)
	title = f"Add techjournal submission: {display_name}"
	description = textwrap.dedent(
		f"""\
		Auto-generated techjournal submission for **{display_name}**.

		- Link: {submission.link}
		{"- Role: " + role_label if role_label else ""}
		{"- Graduation Year: " + submission.grad_year if submission.grad_year else ""}
		- Issue: #{issue.get('iid')}

		Closes #{issue.get('iid')}.
		"""
	)

	payload = {
		"source_branch": branch_name,
		"target_branch": GITLAB_MR_TARGET_BRANCH,
		"title": title,
		"description": description,
		"remove_source_branch": True,
	}

	endpoint = f"projects/{_project_path_encoded()}/merge_requests"
	try:
		response = _gitlab_request("POST", endpoint, json=payload)
	except requests.RequestException as exc:
		logger.warning("Network error while creating merge request: %s", exc)
		return None, str(exc)

	if response.status_code == 409:
		logger.warning("Merge request already exists for branch %s: %s", branch_name, response.text)
		return None, f"status=409 body={response.text}"

	if response.status_code >= 400:
		logger.warning("Failed to create merge request: %s", response.text)
		return None, f"status={response.status_code} body={response.text}"

	merge_request = response.json()
	logger.info("Created merge request !%s (%s)", merge_request.get("iid"), merge_request.get("web_url"))
	return merge_request, None


def _attempt_merge_request(issue: Dict[str, Any], submission: Submission) -> Dict[str, Any]:
	if not ENABLE_MERGE_REQUESTS:
		return {"enabled": False}

	branch_name = _build_branch_name(issue.get("iid"))
	created_branch, branch_error = _ensure_branch(branch_name)
	if not created_branch:
		return {
			"enabled": True,
			"error": "Failed to create feature branch",
			"details": branch_error,
		}

	commit_ok, commit_error, table_row_added = _create_submission_commit(created_branch, issue, submission)
	if not commit_ok:
		return {
			"enabled": True,
			"error": "Failed to add submission commit",
			"details": commit_error,
			"tableRowAdded": table_row_added,
		}

	merge_request, merge_error = _create_merge_request(created_branch, issue, submission)
	if not merge_request:
		return {
			"enabled": True,
			"error": "Failed to create merge request",
			"details": merge_error,
			"tableRowAdded": table_row_added,
		}

	return {
		"enabled": True,
		"web_url": merge_request.get("web_url"),
		"iid": merge_request.get("iid"),
		"tableRowAdded": table_row_added,
	}


@app.post("/techjournal", status_code=status.HTTP_201_CREATED)
def create_techjournal_issue(submission: Submission) -> Dict[str, Any]:
	logger.info("Received submission for %s", _format_display_name(submission))
	issue = _create_gitlab_issue(submission)
	response: Dict[str, Any] = {
		"issueId": issue.get("iid"),
		"issueUrl": issue.get("web_url"),
	}

	try:
		mr_result = _attempt_merge_request(issue, submission)
	except Exception:  # pragma: no cover - defensive catch
		logger.exception("Unexpected error while attempting merge request")
		mr_result = {"enabled": ENABLE_MERGE_REQUESTS, "error": "Unexpected merge request error"}

	if mr_result.get("enabled") and "web_url" in mr_result:
		response["mergeRequestUrl"] = mr_result["web_url"]
	elif mr_result.get("enabled") and mr_result.get("error"):
		response["mergeRequestError"] = mr_result["error"]
		if mr_result.get("details"):
			response["mergeRequestDetails"] = mr_result["details"]
	if mr_result.get("enabled") and "tableRowAdded" in mr_result:
		response["tableRowAdded"] = mr_result["tableRowAdded"]

	return response


def run() -> None:
	import uvicorn

	port = int(os.getenv("PORT", "8080"))
	uvicorn.run("app:app", host="0.0.0.0", port=port, reload=False)


if __name__ == "__main__":
	run()
