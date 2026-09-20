"""FastAPI application entry point for Context Recovery."""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from backend.github.client import GitHubIntegrationError
from backend.routes.github_routes import router as github_router


app = FastAPI(
    title="Context Recovery GitHub Data Layer",
    version="0.1.0",
    description="GitHub integration and normalized project context collection.",
)


@app.exception_handler(GitHubIntegrationError)
async def github_error_handler(request: Request, error: GitHubIntegrationError) -> JSONResponse:
    """Return safe, consistent HTTP errors for GitHub integration failures."""

    return JSONResponse(status_code=error.status_code, content={"detail": error.message})


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(github_router)