import subprocess
from pathlib import Path


def clone_repo(repo_url: str, clone_dir: Path) -> None:
    """Clone GitHub repo to given path if not already exists."""
    if clone_dir.exists():
        print(f"[git_runner] Repo already exists at {clone_dir}")
        return
    subprocess.run(
        ["git", "clone", repo_url, str(clone_dir)],
        check=True,
    )
    print(f"[git_runner] Cloned into {clone_dir}")


def checkout_commit(
    repo_path: Path, commit_sha: str, worktree_dir: Path,
) -> None:
    """Checkout a commit into a separate directory using git worktree."""
    subprocess.run(
        ["git", "worktree", "add", str(worktree_dir), commit_sha],
        cwd=repo_path,
        check=True,
    )
    print(f"[git_runner] Checked out {commit_sha} into {worktree_dir}")


def get_diff_lines(
    repo_path: Path, base_sha: str, head_sha: str,
) -> dict[str, set[int]]:
    """
    Get a dictionary of {filename: set(modified_line_numbers)}.

    The result reflects lines changed between base_sha and head_sha.
    """
    result = subprocess.run(
        ["git", "diff", "--unified=0", base_sha, head_sha],
        cwd=repo_path,
        stdout=subprocess.PIPE,
        text=True,
        check=True,
    )

    diff_lines: dict[str, set[int]] = {}
    current_file = ""

    for line in result.stdout.splitlines():
        if line.startswith("+++ b/"):
            current_file = line[6:]
        elif line.startswith("@@"):
            if current_file == "":
                continue

            parts = line.split(" ")
            new_info = next(p for p in parts if p.startswith("+"))
            new_line_info = new_info[1:]  # remove '+'

            if "," in new_line_info:
                start, count = map(int, new_line_info.split(","))
            else:
                start = int(new_line_info)
                count = 1

            changed_lines = set(range(start, start + count))
            diff_lines.setdefault(current_file, set()).update(changed_lines)

    return diff_lines
