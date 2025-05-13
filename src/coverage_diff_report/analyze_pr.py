from __future__ import annotations

import shutil
import sys
import tempfile
from pathlib import Path

from src.coverage_diff_report.coverage_runner.coverage_runner import (
    load_coverage_data,
    run_coverage_scan,
)
from src.coverage_diff_report.diff_analyzer.diff_analyzer import (
    analyze_diff_coverage,
)
from src.coverage_diff_report.git_runner.git_runner import (
    checkout_commit,
    clone_repo,
    get_diff_lines,
)
from src.coverage_diff_report.github_util.github_util import (
    get_pr_metadata,
    parse_pr_url,
)
from src.coverage_diff_report.pdf_generator.pdf_generator import (
    generate_pdf_report,
)


def analyze_pr(pr_url: str, output_pdf: str) -> None:

    repo_fullname, pr_number = parse_pr_url(pr_url)
    pr_meta = get_pr_metadata(repo_fullname, pr_number)

    base_sha: str = pr_meta["merge_base"]
    head_sha: str = pr_meta["head_sha"]
    repo_https_url = f"https://github.com/{repo_fullname}.git"

    tmp_root = Path(tempfile.mkdtemp(prefix="pr-analysis-"))
    print(f"[INFO] Using temp directory: {tmp_root}")

    repo_path = tmp_root / "repo"
    clone_repo(repo_https_url, repo_path)

    base_dir = tmp_root / "base"
    head_dir = tmp_root / "head"
    checkout_commit(repo_path, base_sha, base_dir)
    checkout_commit(repo_path, head_sha, head_dir)
    diff_lines_all = get_diff_lines(repo_path, base_sha, head_sha)
    diff_lines = {f: lines for f, lines in diff_lines_all.items() if f.endswith(".py")}
    base_json = base_dir / "coverage.json"
    head_json = head_dir / "coverage.json"
    run_coverage_scan(base_dir, base_json)
    run_coverage_scan(head_dir, head_json)
    base_cov = load_coverage_data(base_json)
    head_cov = load_coverage_data(head_json)
    diff_results = analyze_diff_coverage(diff_lines, base_cov, head_cov)
    generate_pdf_report(diff_results, output_pdf)
    print(f"[DONE] Report saved to {output_pdf}")
    shutil.rmtree(tmp_root)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(
            "Usage: python -m src.coverage_diff_report.analyze_pr "
            "<PR_URL> <output.pdf>",
        )
        sys.exit(1)

    analyze_pr(sys.argv[1], sys.argv[2])
