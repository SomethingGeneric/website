# Techjournal Submission Proxy

Small Flask service that accepts techjournal submissions from the static site and opens a GitLab issue on your behalf. The GitLab access token stays on the server, so the public frontend never exposes it.

## Configuration

Set the following environment variables (they can be supplied via `docker run -e` or a `.env` file):

| Variable | Required | Default | Purpose |
| --- | --- | --- | --- |
| `GITLAB_API_TOKEN` | ✅ | — | Personal/project access token with “create issue” scope. |
| `GITLAB_PROJECT_PATH` | | `matt/website` | GitLab project namespace/path. |
| `GITLAB_API_BASE` | | `https://gitlab.goober.cloud/api/v4` | GitLab API base URL. |
| `ISSUE_LABELS` | | *(unset)* | Optional comma-separated labels for the created issue. |
| `ALLOWED_ORIGINS` | | *(wildcard)* | Comma-separated list of origins that may call the API. Enables restrictive CORS if set. |
| `PORT` | | `8080` | Port to bind when running with `python app.py`. Ignored by the Docker CMD (Gunicorn uses 8080). |

## Local development

```bash
cd proxy
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export GITLAB_API_TOKEN=glpat-...           # required
python app.py
```

The service listens on `http://localhost:8080/techjournal` for `POST` requests with JSON:

```json
{
  "name": "Jane Doe",
  "link": "https://example.com/my-tech-journal"
}
```

## Docker

```bash
cd proxy
docker build -t techjournal-proxy .
docker run -p 8080:8080 \
  -e GITLAB_API_TOKEN=glpat-... \
  -e GITLAB_PROJECT_PATH=matt/website \
  techjournal-proxy
```

Deploy the container wherever you host services (Fly.io, Render, a VPS, etc.), then set `PUBLIC_TECHJOURNAL_PROXY_BASE` in the Astro site to the proxy’s public URL (e.g. `https://proxy.mattcompton.dev`).
