import pytest

from src.coverage_diff_report.github_util.github_util import (
    get_pr_metadata,
    parse_pr_url,
)


def test_parse_pr_url_valid() -> None:
    url = "https://github.com/zz2548/Team-9-Technology-Template-Repository/pull/12"
    repo, pr_number = parse_pr_url(url)
    assert repo == "zz2548/Team-9-Technology-Template-Repository"
    assert pr_number == 12


def test_parse_pr_url_invalid() -> None:
    with pytest.raises(ValueError, match="Invalid GitHub PR URL"):
        parse_pr_url("https://invalid-url.com/just/some/page")


def test_get_pr_metadata_public_repo() -> None:
    url = "https://github.com/zz2548/Team-9-Technology-Template-Repository/pull/12"
    repo, pr_number = parse_pr_url(url)

    meta = get_pr_metadata(repo, pr_number)

    assert meta["repo"] == repo
    assert meta["pr_number"] == pr_number
    required_keys = ["base_ref", "head_ref", "base_sha", "head_sha", "merge_base"]
    assert all(key in meta for key in required_keys)
