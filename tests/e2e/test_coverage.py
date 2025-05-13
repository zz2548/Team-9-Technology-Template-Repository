import tempfile
from pathlib import Path

from src.coverage_diff_report.analyze_pr import analyze_pr


def test_e2e_real_pr_smoke() -> None:
    """End-to-end test: basic smoke test with real GitHub PR."""
    pr_url = (
        "https://github.com/zz2548/Team-9-Technology-Template-Repository/pull/25"
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        output_pdf = Path(tmpdir) / "report.pdf"

        analyze_pr(pr_url, str(output_pdf))  # let errors propagate naturally

        assert output_pdf.exists(), "Expected output PDF file to exist"
        assert output_pdf.stat().st_size > 0, "Expected output PDF file to be non-empty"
