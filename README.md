# Context Recovery GitHub Data Layer

This prototype collects GitHub repository history and source files, then converts the results into a common Pydantic document format for a later retrieval or AI layer. It contains no LLM calls, embeddings, vector database, or non-GitHub integrations.

## Setup

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add your own token:

```text
GITHUB_TOKEN=your_token_here
```

The token is loaded with `python-dotenv`, is never hardcoded, and is excluded from Git by `.gitignore`.

## Run

From the project root:

```powershell
venv\Scripts\python.exe -m uvicorn backend.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for the interactive API documentation.

## Endpoints

Replace `OWNER` and `REPO` with a repository you can access:

```text
GET /repository/OWNER/REPO
GET /repository/OWNER/REPO/issues
GET /repository/OWNER/REPO/issues/42/comments
GET /repository/OWNER/REPO/pulls
GET /repository/OWNER/REPO/pulls/42/comments
GET /repository/OWNER/REPO/pulls/42/reviews
GET /repository/OWNER/REPO/pulls/42/commits
GET /repository/OWNER/REPO/pulls/42/files
GET /repository/OWNER/REPO/commits
GET /repository/OWNER/REPO/files
GET /repository/OWNER/REPO/context
```

The `/context` response contains `repository`, `issues`, `pull_requests`, `commits`, `files`, and `comments_reviews`. Every item uses the normalized shape `source`, `repository`, `type`, `id`, `title`, `content`, `author`, `timestamp`, `metadata`, and `url`. Type-specific fields such as labels, branches, changed files, review state, file path, and commit SHA remain in `metadata`.

## Live verification checklist

After adding the token, call each endpoint with PowerShell, curl, or the Swagger UI at `/docs`. Check repository metadata, issue comments, pull request conversation comments and reviews, commit patches, source files, and the complete context response. Responses are JSON-serializable through FastAPI's Pydantic response models.