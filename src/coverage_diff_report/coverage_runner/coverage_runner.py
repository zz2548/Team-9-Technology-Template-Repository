import json
import subprocess
from pathlib import Path


def run_coverage_scan(source_dir: Path, coverage_json_path: Path) -> None:
    """
    Run nose2 + coverage in a given directory and generate coverage.json.

    Assumes that the source already contains tests.
    """
    subprocess.run(["coverage", "erase"], cwd=source_dir, check=True)

    subprocess.run(
        ["coverage", "run", "--source=src", "--source=.", "-m", "nose2", "-v"],
        cwd=source_dir,
        check=True,
    )

    subprocess.run(
        ["coverage", "json", "--ignore-errors", "-o", str(coverage_json_path)],
        cwd=source_dir,
        check=False,
    )


def load_coverage_data(coverage_json_path: Path) -> dict[str, set[int]]:
    """Return {relative_path_from_repo_root: set(covered_lines)}."""
    with coverage_json_path.open() as f:
        data = json.load(f)

    result: dict[str, set[int]] = {}
    repo_root = Path.cwd().resolve()

    for file, info in data.get("files", {}).items():
        path_obj = Path(file).resolve()
        try:
            rel_path = str(path_obj.relative_to(repo_root))
        except ValueError:
            rel_path = file  # fallback
        result[rel_path] = set(info.get("executed_lines", []))
    return result


