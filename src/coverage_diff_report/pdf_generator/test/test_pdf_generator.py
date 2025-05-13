import tempfile
import unittest
from pathlib import Path
from typing import TYPE_CHECKING

from PyPDF2 import PdfReader

if TYPE_CHECKING:
    from src.coverage_diff_report.diff_analyzer.diff_analyzer import DiffCoverageResult

from src.coverage_diff_report.pdf_generator.pdf_generator import generate_pdf_report


class TestGeneratePdfReport(unittest.TestCase):

    def test_generate_with_data(self) -> None:
        data: list[DiffCoverageResult] = [
            {"file": "src/foo.py", "line": 10,
             "before": "not_covered", "after": "covered"},
            {"file": "src/bar.py", "line": 5,
             "before": "covered", "after": "not_covered"},
        ]
        with tempfile.TemporaryDirectory() as tmpdir:
            pdf_path = Path(tmpdir) / "report.pdf"
            generate_pdf_report(data, str(pdf_path))

            # Assert file was created and is not empty
            self.assertTrue(pdf_path.exists())
            self.assertGreater(pdf_path.stat().st_size, 100)

            # Open PDF and check content
            reader = PdfReader(str(pdf_path))
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
            self.assertIn("PR Diff Coverage Report", text)
            self.assertIn("src/foo.py", text)
            self.assertIn("10", text)
            self.assertIn("covered", text)

    def test_generate_empty(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            pdf_path = Path(tmpdir) / "report.pdf"
            generate_pdf_report([], str(pdf_path))

            self.assertTrue(pdf_path.exists())
            self.assertGreater(pdf_path.stat().st_size, 100)

            reader = PdfReader(str(pdf_path))
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
            self.assertIn("No changes found in diff.", text)


if __name__ == "__main__":
    unittest.main()
