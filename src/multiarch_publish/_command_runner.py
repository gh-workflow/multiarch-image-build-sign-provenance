"""Thin subprocess wrapper with consistent error handling."""

import subprocess  # nosec B404 - controlled internal subprocess wrapper without shell execution

from multiarch_publish._errors import CommandError


def run_command(command: list[str], *, input_text: str | None = None) -> str:
    """Run a command and return stdout or raise CommandError."""
    try:
        result = subprocess.run(
            command,
            check=True,
            input=input_text,
            text=True,
            capture_output=True,
        )  # nosec B603 - command is executed without a shell and arguments are passed as a list
    except FileNotFoundError as exc:
        raise CommandError(f"required command not found: {command[0]}") from exc
    except subprocess.CalledProcessError as exc:
        stderr = exc.stderr.strip()
        stdout = exc.stdout.strip()
        detail = stderr or stdout or "command failed without output"
        joined = " ".join(command)
        raise CommandError(f"command failed: {joined}\n{detail}") from exc

    return result.stdout
