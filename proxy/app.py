from __future__ import annotations

import logging
import os
from typing import Optional

import requests
from flask import Flask, jsonify, request
from urllib.parse import quote_plus


logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

GITLAB_API_BASE = os.getenv("GITLAB_API_BASE", "https://gitlab.goober.cloud/api/v4").rstrip("/")
GITLAB_PROJECT_PATH = os.getenv("GITLAB_PROJECT_PATH", "matt/website")
GITLAB_API_TOKEN = os.getenv("GITLAB_API_TOKEN")
ISSUE_LABELS = os.getenv("ISSUE_LABELS", "")
ALLOWED_ORIGINS_RAW = os.getenv("ALLOWED_ORIGINS", "")

if not GITLAB_API_TOKEN:
    raise RuntimeError("GITLAB_API_TOKEN env var is required")

ALLOWED_ORIGINS = {origin.strip() for origin in ALLOWED_ORIGINS_RAW.split(",") if origin.strip()}

app = Flask(__name__)


def _apply_cors(response):
    origin = request.headers.get("Origin")
    if ALLOWED_ORIGINS:
        if origin in ALLOWED_ORIGINS:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Vary"] = "Origin"
    else:
        response.headers["Access-Control-Allow-Origin"] = "*"

    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    return response


@app.after_request
def add_cors_headers(response):
    return _apply_cors(response)


@app.route("/techjournal", methods=["POST", "OPTIONS"])
def create_techjournal_issue():
    if request.method == "OPTIONS":
        response = app.make_response(("", 204))
        return _apply_cors(response)

    payload = request.get_json(force=True, silent=True)
    if not isinstance(payload, dict):
        return jsonify({"error": "Request body must be JSON"}), 400

    name = str(payload.get("name", "")).strip()
    link = str(payload.get("link", "")).strip()

    if not name or not link:
        return jsonify({"error": "Both name and link are required"}), 400

    if not link.startswith(("http://", "https://")):
        return jsonify({"error": "Link must start with http:// or https://"}), 400

    issue_title = f"New techjournal submission: {name}"
    issue_body = "\n".join(
        [
            f"**Name:** {name}",
            f"**Link:** {link}",
            "",
            "Submitted via techjournals/other-folks modal.",
        ]
    )

    issue_payload = {
        "title": issue_title,
        "description": issue_body,
    }

    if ISSUE_LABELS:
        issue_payload["labels"] = ISSUE_LABELS

    project_path_encoded = quote_plus(GITLAB_PROJECT_PATH)
    issues_url = f"{GITLAB_API_BASE}/projects/{project_path_encoded}/issues"

    try:
        response = requests.post(
            issues_url,
            headers={
                "PRIVATE-TOKEN": GITLAB_API_TOKEN,
                "Content-Type": "application/json",
            },
            json=issue_payload,
            timeout=15,
        )
    except requests.RequestException as exc:
        logger.exception("Error connecting to GitLab")
        return jsonify({"error": "Failed to reach GitLab", "details": str(exc)}), 502

    if response.status_code >= 400:
        logger.warning(
            "GitLab issue creation failed: status=%s body=%s",
            response.status_code,
            response.text,
        )
        return (
            jsonify(
                {
                    "error": "GitLab rejected the request",
                    "status": response.status_code,
                    "body": response.text,
                }
            ),
            502,
        )

    issue = response.json()
    return (
        jsonify(
            {
                "issueId": issue.get("iid"),
                "issueUrl": issue.get("web_url"),
            }
        ),
        201,
    )


def run() -> None:
    port = int(os.getenv("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)


if __name__ == "__main__":
    run()
