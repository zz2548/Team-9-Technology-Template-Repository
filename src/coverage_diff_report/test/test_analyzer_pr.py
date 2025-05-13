from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch

from src.coverage_diff_report.analyze_pr import analyze_pr


class TestAnalyzePr(unittest.TestCase):
    """Unit-tests for analyze_pr.analyze_pr()."""

    @patch("src.coverage_diff_report.analyze_pr.generate_pdf_report")
    @patch("src.coverage_diff_report.analyze_pr.analyze_diff_coverage")
    @patch("src.coverage_diff_report.analyze_pr.load_coverage_data")
    @patch("src.coverage_diff_report.analyze_pr.run_coverage_scan")
    @patch("src.coverage_diff_report.analyze_pr.get_diff_lines")
    @patch("src.coverage_diff_report.analyze_pr.checkout_commit")
    @patch("src.coverage_diff_report.analyze_pr.clone_repo")
    @patch("src.coverage_diff_report.analyze_pr.get_pr_metadata")
    @patch("src.coverage_diff_report.analyze_pr.parse_pr_url")
    def test_happy_path(  # noqa: PLR0913
        self,
        mock_parse_pr_url: MagicMock,
        mock_get_pr_meta: MagicMock,
        _mock_clone_repo: MagicMock,  # noqa: PT019
        _mock_checkout: MagicMock,  # noqa: PT019
        mock_get_diff_lines: MagicMock,
        _mock_run_cov: MagicMock,  # noqa: PT019
        mock_load_cov: MagicMock,
        mock_analyze_diff: MagicMock,
        mock_pdf: MagicMock,
    ) -> None:
        pr_url = "https://github.com/foo/bar/pull/42"
        out_pdf = "dummy.pdf"

        mock_parse_pr_url.return_value = ("foo/bar", 42)

        mock_get_pr_meta.return_value = {
            "merge_base": "deadbeef",
            "head_sha": "faceb00c",
        }

        mock_get_diff_lines.return_value = {
            "src/a.py": {1, 2},
            "README.md": {3},
        }

        mock_load_cov.side_effect = [
            {"src/a.py": {1}},           # base coverage
            {"src/a.py": {1, 2}},        # head coverage
        ]

        dummy_result = [
            {"file": "src/a.py", "line": 2,
             "before": "not_covered", "after": "covered"},
        ]
        mock_analyze_diff.return_value = dummy_result

        analyze_pr(pr_url, out_pdf)

        passed_diff_lines = mock_analyze_diff.call_args.args[0]
        self.assertEqual(passed_diff_lines, {"src/a.py": {1, 2}})

        mock_pdf.assert_called_once_with(dummy_result, out_pdf)


if __name__ == "__main__":
    unittest.main(verbosity=2)
