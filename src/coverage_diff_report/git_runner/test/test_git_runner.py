import unittest
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

from src.coverage_diff_report.git_runner import git_runner


class TestGitRunner(unittest.TestCase):

    @patch("src.coverage_diff_report.git_runner.git_runner.subprocess.run")
    def test_clone_repo_when_not_exists(self, mock_run: Mock) -> None:
        mock_path = MagicMock(spec=Path)
        mock_path.exists.return_value = False

        git_runner.clone_repo("https://github.com/test/repo.git", mock_path)

        mock_run.assert_called_once_with(
            ["git", "clone", "https://github.com/test/repo.git", str(mock_path)],
            check=True,
        )

    @patch("src.coverage_diff_report.git_runner.git_runner.subprocess.run")
    def test_checkout_commit(self, mock_run: Mock) -> None:
        repo_path = Path("/some/repo")
        commit = "abc123"
        worktree_dir = Path("/some/repo/checkout")

        git_runner.checkout_commit(repo_path, commit, worktree_dir)

        mock_run.assert_called_once_with(
            ["git", "worktree", "add", str(worktree_dir), commit],
            cwd=repo_path,
            check=True,
        )

    @patch("src.coverage_diff_report.git_runner.git_runner.subprocess.run")
    def test_get_diff_lines(self, mock_run: Mock) -> None:
        mock_output = """\
diff --git a/file.py b/file.py
index abc..def 100644
--- a/file.py
+++ b/file.py
@@ -0,0 +1,3 @@
+line 1
+line 2
+line 3
"""
        mock_run.return_value = MagicMock(stdout=mock_output)

        result = git_runner.get_diff_lines(Path("/repo"), "abc", "def")
        assert result == {"file.py": {1, 2, 3}}
