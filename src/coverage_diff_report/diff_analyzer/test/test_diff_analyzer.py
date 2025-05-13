import unittest

from src.coverage_diff_report.diff_analyzer.diff_analyzer import analyze_diff_coverage


class TestAnalyzeDiffCoverage(unittest.TestCase):
    def test_covered_and_not_covered(self) -> None:
        diff_lines = {
            "foo.py": {1, 2, 3, 4},
        }
        base_coverage: dict[str, set[int]] = {
            "foo.py": {1, 3},
        }
        head_coverage: dict[str, set[int]] = {
            "foo.py": {2, 3},
        }

        expected = [
            {"file": "foo.py", "line": 1, "before": "covered", "after": "not_covered"},
            {"file": "foo.py", "line": 2, "before": "not_covered", "after": "covered"},
            {"file": "foo.py", "line": 3, "before": "covered", "after": "covered"},
            {"file": "foo.py", "line": 4,
             "before": "not_covered", "after": "not_covered"},
        ]

        result = analyze_diff_coverage(diff_lines, base_coverage, head_coverage)
        self.assertEqual(result, expected)

    def test_file_only_in_head(self) -> None:
        diff_lines = {
            "bar.py": {10, 11},
        }
        base_coverage: dict[str, set[int]] = {}
        head_coverage: dict[str, set[int]] = {
            "bar.py": {10},
        }

        expected = [
            {"file": "bar.py", "line": 10, "before":
                "not_covered", "after": "covered"},
            {"file": "bar.py", "line": 11, "before":
                "not_covered", "after": "not_covered"},
        ]

        result = analyze_diff_coverage(diff_lines, base_coverage, head_coverage)
        self.assertEqual(result, expected)

    def test_file_not_covered_at_all(self) -> None:
        diff_lines = {
            "baz.py": {5, 6},
        }
        base_coverage: dict[str, set[int]] = {}
        head_coverage: dict[str, set[int]] = {}

        expected = [
            {"file": "baz.py", "line": 5, "before":
                "not_covered", "after": "not_covered"},
            {"file": "baz.py", "line": 6, "before":
                "not_covered", "after": "not_covered"},
        ]

        result = analyze_diff_coverage(diff_lines,
                                       base_coverage, head_coverage)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
