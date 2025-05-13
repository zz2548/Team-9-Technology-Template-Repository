import re
from typing import Any

import requests

GITHUB_API = "https://api.github.com"


def parse_pr_url(url: str) -> tuple[str, int]:
    match = re.match(r"https://github\.com/([^/]+/[^/]+)/pull/(\d+)", url)
    if not match:
        raise ValueError("Invalid GitHub PR URL")
    return match.group(1), int(match.group(2))


def get_pr_metadata(
    repo: str, pr_number: int, github_token: str | None = None,
) -> dict[str, Any]:
    headers = {"Accept": "application/vnd.github+json"}
    if github_token:
        headers["Authorization"] = f"Bearer {github_token}"

    pr_url = f"{GITHUB_API}/repos/{repo}/pulls/{pr_number}"
    resp = requests.get(pr_url, headers=headers, timeout=10)
    if resp.status_code != 200:
        msg = f"Failed to fetch PR info: {resp.status_code} - {resp.text}"
        raise RuntimeError(msg)

    pr_data = resp.json()
    base_sha = pr_data["base"]["sha"]
    base_ref = pr_data["base"]["ref"]
    head_sha = pr_data["head"]["sha"]
    head_ref = pr_data["head"]["ref"]

    compare_url = (
        f"{GITHUB_API}/repos/{repo}/compare/{base_sha}...{head_sha}"
    )
    resp2 = requests.get(compare_url, headers=headers, timeout=10)
    if resp2.status_code != 200:
        msg = f"Failed to fetch compare info: {resp2.status_code} - {resp2.text}"
        raise RuntimeError(msg)

    merge_base = resp2.json()["merge_base_commit"]["sha"]

    return {
        "repo": repo,
        "pr_number": pr_number,
        "base_ref": base_ref,
        "head_ref": head_ref,
        "base_sha": base_sha,
        "head_sha": head_sha,
        "merge_base": merge_base,
    }
