"""FastAPI endpoints for normalized GitHub data."""

from __future__ import annotations

import re

from fastapi import APIRouter, Depends

from backend.github.client import GitHubClient
from backend.github.comments import get_issue_comments, get_pr_comments, get_pr_reviews
from backend.github.commits import get_commits
from backend.github.files import get_repository_files
from backend.github.issues import get_issues
from backend.github.pull_requests import get_pr_commits, get_pr_files, get_pull_requests
from backend.github.client import GitHubIntegrationError
from backend.github.repositories import get_repository
from backend.models.github_models import NormalizedDocument, RepositoryContext
from backend.services.context_service import collect_repository_context


router = APIRouter(prefix="/repository", tags=["github"])


def get_client(owner: str, repo: str) -> GitHubClient:
    """Build the client per request so missing configuration does not break startup."""

    name_pattern = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,99}$")
    if not name_pattern.fullmatch(owner) or not name_pattern.fullmatch(repo):
        raise GitHubIntegrationError("Invalid GitHub owner or repository name.", 400)
    return GitHubClient()


@router.get("/{owner}/{repo}", response_model=NormalizedDocument)
def repository(owner: str, repo: str, client: GitHubClient = Depends(get_client)) -> NormalizedDocument:
    return get_repository(client, owner, repo)


@router.get("/{owner}/{repo}/issues", response_model=list[NormalizedDocument])
def issues(owner: str, repo: str, client: GitHubClient = Depends(get_client)) -> list[NormalizedDocument]:
    return get_issues(client, owner, repo)


@router.get("/{owner}/{repo}/issues/{issue_number}/comments", response_model=list[NormalizedDocument])
def issue_comments(owner: str, repo: str, issue_number: int, client: GitHubClient = Depends(get_client)) -> list[NormalizedDocument]:
    return get_issue_comments(client, owner, repo, issue_number)


@router.get("/{owner}/{repo}/pulls", response_model=list[NormalizedDocument])
def pull_requests(owner: str, repo: str, client: GitHubClient = Depends(get_client)) -> list[NormalizedDocument]:
    return get_pull_requests(client, owner, repo)


@router.get("/{owner}/{repo}/pulls/{pr_number}/comments", response_model=list[NormalizedDocument])
def pull_request_comments(owner: str, repo: str, pr_number: int, client: GitHubClient = Depends(get_client)) -> list[NormalizedDocument]:
    return get_pr_comments(client, owner, repo, pr_number)


@router.get("/{owner}/{repo}/pulls/{pr_number}/reviews", response_model=list[NormalizedDocument])
def pull_request_reviews(owner: str, repo: str, pr_number: int, client: GitHubClient = Depends(get_client)) -> list[NormalizedDocument]:
    return get_pr_reviews(client, owner, repo, pr_number)


@router.get("/{owner}/{repo}/pulls/{pr_number}/commits", response_model=list[NormalizedDocument])
def pull_request_commits(owner: str, repo: str, pr_number: int, client: GitHubClient = Depends(get_client)) -> list[NormalizedDocument]:
    return get_pr_commits(client, owner, repo, pr_number)


@router.get("/{owner}/{repo}/pulls/{pr_number}/files", response_model=list[NormalizedDocument])
def pull_request_files(owner: str, repo: str, pr_number: int, client: GitHubClient = Depends(get_client)) -> list[NormalizedDocument]:
    return get_pr_files(client, owner, repo, pr_number)


@router.get("/{owner}/{repo}/commits", response_model=list[NormalizedDocument])
def commits(owner: str, repo: str, client: GitHubClient = Depends(get_client)) -> list[NormalizedDocument]:
    return get_commits(client, owner, repo)


@router.get("/{owner}/{repo}/files", response_model=list[NormalizedDocument])
def files(owner: str, repo: str, client: GitHubClient = Depends(get_client)) -> list[NormalizedDocument]:
    return get_repository_files(client, owner, repo)


@router.get("/{owner}/{repo}/context", response_model=RepositoryContext)
def context(owner: str, repo: str, client: GitHubClient = Depends(get_client)) -> RepositoryContext:
    return collect_repository_context(client, owner, repo)