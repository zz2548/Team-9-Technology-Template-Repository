import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

from src.coverage_diff_report.coverage_runner.coverage_runner import load_coverage_data


class TestLoadCoverageData(unittest.TestCase):

    def make_temp_coverage_json(self, files_section: dict[str, Any]) -> Path:
        temp_dir = tempfile.TemporaryDirectory()
        path = Path(temp_dir.name) / "coverage.json"
        with path.open("w") as f:
            json.dump({
                "meta": {"version": "7.6.0"},
                "files": files_section,
            }, f)
        self.addCleanup(temp_dir.cleanup)
        return path

    def test_single_file_with_executed_lines(self) -> None:
        abs_file = str((Path.cwd() / "src/foo.py").resolve())
        cov_path = self.make_temp_coverage_json({
            abs_file: {"executed_lines": [1, 3, 5]},
        })
        result = load_coverage_data(cov_path)
        self.assertEqual(result, {"src/foo.py": {1, 3, 5}})

    def test_multiple_files(self) -> None:
        abs_a = str((Path.cwd() / "src/a.py").resolve())
        abs_b = str((Path.cwd() / "src/b.py").resolve())
        cov_path = self.make_temp_coverage_json({
            abs_a: {"executed_lines": [2]},
            abs_b: {"executed_lines": [4, 5]},
        })
        result = load_coverage_data(cov_path)
        self.assertEqual(result, {
            "src/a.py": {2},
            "src/b.py": {4, 5},
        })

    def test_no_executed_lines(self) -> None:
        abs_path = str((Path.cwd() / "src/empty.py").resolve())
        cov_path = self.make_temp_coverage_json({
            abs_path: {"executed_lines": []},
        })
        result = load_coverage_data(cov_path)
        self.assertEqual(result, {"src/empty.py": set()})

    def test_relative_path_remains(self) -> None:
        cov_path = self.make_temp_coverage_json({
            "src/manual_relative.py": {"executed_lines": [99]},
        })
        result = load_coverage_data(cov_path)
        self.assertEqual(result, {"src/manual_relative.py": {99}})


if __name__ == "__main__":
    unittest.main()
