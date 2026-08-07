import unittest
from types import SimpleNamespace
from unittest.mock import patch

from multiarch_publish._command_runner import run_command
from multiarch_publish._errors import CommandError


class CommandRunnerTests(unittest.TestCase):
    def test_run_command_returns_stdout(self) -> None:
        completed = SimpleNamespace(
            stdout="ok",
        )

        with patch(
            "multiarch_publish._command_runner.subprocess.run", return_value=completed
        ):
            self.assertEqual(run_command(["tool", "arg"]), "ok")

    def test_run_command_raises_for_missing_binary(self) -> None:
        with patch(
            "multiarch_publish._command_runner.subprocess.run",
            side_effect=FileNotFoundError(),
        ):
            with self.assertRaisesRegex(CommandError, "required command not found"):
                run_command(["tool"])


if __name__ == "__main__":
    unittest.main()
