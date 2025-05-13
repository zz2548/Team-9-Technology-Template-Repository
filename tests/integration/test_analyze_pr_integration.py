import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from PyPDF2 import PdfReader

from src.coverage_diff_report.analyze_pr import analyze_pr


class TestAnalyzePRIntegration(unittest.TestCase):

    @patch("src.coverage_diff_report.analyze_pr.clone_repo")
    @patch("src.coverage_diff_report.analyze_pr.checkout_commit")
    @patch("src.coverage_diff_report.analyze_pr.run_coverage_scan")
    @patch("src.coverage_diff_report.analyze_pr.load_coverage_data")
    @patch("src.coverage_diff_report.analyze_pr.get_diff_lines")
    @patch("src.coverage_diff_report.analyze_pr.get_pr_metadata")
    @patch("src.coverage_diff_report.analyze_pr.parse_pr_url")
    def test_end_to_end_report_generated(
        self,
        mock_parse_pr: MagicMock,
        mock_get_meta: MagicMock,
        mock_diff_lines: MagicMock,
        mock_load_cov: MagicMock,
        _mock_run_coverage: MagicMock,  # noqa: PT019
        _mock_checkout: MagicMock,  # noqa: PT019
        _mock_clone: MagicMock,  # noqa: PT019
    ) -> None:
        """Simulate a complete PR analysis run and check PDF is generated."""
        pr_url = "https://github.com/fake/fake-repo/pull/99"

        # Setup fake PR info
        mock_parse_pr.return_value = ("fake/fake-repo", 99)
        mock_get_meta.return_value = {
            "merge_base": "abc123",
            "head_sha": "def456",
        }

        # Setup fake diff (Python only)
        mock_diff_lines.return_value = {
            "src/foo.py": {1, 2},
            "README.md": {5},  # Will be filtered out
        }

        # Setup fake coverage
        mock_load_cov.side_effect = [
            {"src/foo.py": {1}},          # base
            {"src/foo.py": {1, 2}},       # head
        ]

        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "report.pdf"
            analyze_pr(pr_url, str(out))

            # ✅ Check PDF exists and has content
            self.assertTrue(out.exists())
            self.assertGreater(out.stat().st_size, 100)

            # ✅ Check PDF contains expected filename and line
            reader = PdfReader(str(out))
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
            self.assertIn("src/foo.py", text)
            self.assertIn("2", text)
            self.assertIn("covered", text)

    @patch("src.coverage_diff_report.analyze_pr.clone_repo")
    @patch("src.coverage_diff_report.analyze_pr.checkout_commit")
    @patch("src.coverage_diff_report.analyze_pr.run_coverage_scan")
    @patch("src.coverage_diff_report.analyze_pr.get_diff_lines", return_value={})
    @patch("src.coverage_diff_report.analyze_pr.load_coverage_data", return_value={})
    @patch("src.coverage_diff_report.analyze_pr.get_pr_metadata",
           return_value={"merge_base": "old", "head_sha": "new"})
    @patch("src.coverage_diff_report.analyze_pr.parse_pr_url",
           return_value=("fake/fake", 7))
    def test_empty_diff_produces_empty_report(
            self,
            _mock_parse: MagicMock,  # noqa: PT019
            _mock_meta: MagicMock,  # noqa: PT019
            _mock_load: MagicMock,  # noqa: PT019
            _mock_diff: MagicMock,  # noqa: PT019
            _mock_run: MagicMock,  # noqa: PT019
            _mock_checkout: MagicMock,  # noqa: PT019
            _mock_clone: MagicMock,  # noqa: PT019
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pdf_path = Path(tmp) / "empty.pdf"
            analyze_pr("http://dummy/pr/7", str(pdf_path))

            self.assertTrue(pdf_path.exists())
            reader = PdfReader(str(pdf_path))
            text = "\n".join(p.extract_text() or "" for p in reader.pages)
            self.assertIn("No changes found in diff.", text)


if __name__ == "__main__":
    unittest.main()
