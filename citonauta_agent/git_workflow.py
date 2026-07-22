from __future__ import annotations

import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from .catalog import SubjectRef
from .config import GitConfig


class GitWorkflow:
    def __init__(self, root: Path, config: GitConfig):
        self.root = root
        self.config = config

    def _run(self, command: list[str], timeout: int = 900) -> str:
        completed = subprocess.run(
            command,
            cwd=self.root,
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
        output = (completed.stdout + "\n" + completed.stderr).strip()
        if completed.returncode != 0:
            raise RuntimeError(
                f"Falló el comando ({completed.returncode}): {' '.join(command)}\n{output}"
            )
        return output

    def preflight(self) -> None:
        for executable in ("git", "gh", "ollama"):
            if shutil.which(executable) is None:
                raise RuntimeError(f"No se encontró el ejecutable requerido: {executable}")
        self._run(["git", "rev-parse", "--show-toplevel"])
        self._run(["gh", "auth", "status"])
        if self.config.require_clean_worktree:
            status = self._run(["git", "status", "--porcelain"])
            if status.strip():
                raise RuntimeError(
                    "El repositorio contiene cambios sin guardar. El agente no continuará para no mezclarlos."
                )

    def checkout_base(self) -> None:
        self._run(["git", "checkout", self.config.default_branch])
        self._run(
            ["git", "pull", "--ff-only", self.config.remote, self.config.default_branch]
        )

    def create_branch(self, subject: SubjectRef) -> str:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        branch = f"{self.config.branch_prefix}-{subject.id}-{stamp}"
        self._run(["git", "checkout", "-b", branch])
        return branch

    def changed_files(self) -> list[str]:
        output = self._run(["git", "status", "--porcelain"])
        paths: list[str] = []
        for line in output.splitlines():
            if len(line) >= 4:
                paths.append(line[3:].strip())
        return paths

    def ensure_expected_changes(self, expected: set[str]) -> None:
        actual = set(self.changed_files())
        unexpected = actual - expected
        missing = expected - actual
        if unexpected:
            raise RuntimeError(
                "El agente modificó archivos no autorizados: " + ", ".join(sorted(unexpected))
            )
        if missing:
            raise RuntimeError(
                "No se generaron los archivos esperados: " + ", ".join(sorted(missing))
            )

    def commit(self, paths: list[str], message: str) -> str:
        self._run(["git", "add", "--", *paths])
        self._run(["git", "commit", "-m", message])
        return self._run(["git", "rev-parse", "HEAD"])

    def push(self, branch: str) -> None:
        self._run(["git", "push", "-u", self.config.remote, branch], timeout=1200)

    def create_pr(self, branch: str, title: str, body_path: Path) -> str:
        output = self._run(
            [
                "gh",
                "pr",
                "create",
                "--base",
                self.config.default_branch,
                "--head",
                branch,
                "--title",
                title,
                "--body-file",
                str(body_path),
            ]
        )
        for token in output.split():
            if token.startswith("https://"):
                return token.strip()
        return output.strip()

    def wait_for_checks(self, pr_url: str) -> None:
        self._run(["gh", "pr", "checks", pr_url, "--watch", "--fail-fast"], timeout=3600)

    def merge(self, pr_url: str) -> None:
        command = ["gh", "pr", "merge", pr_url, f"--{self.config.merge_method}"]
        if self.config.delete_branch:
            command.append("--delete-branch")
        self._run(command, timeout=1200)

    def recover_base(self) -> None:
        self._run(["git", "reset", "--hard"])
        self._run(["git", "checkout", self.config.default_branch])
        self._run(
            ["git", "pull", "--ff-only", self.config.remote, self.config.default_branch]
        )

    def repository_identity(self) -> str:
        raw = self._run(["gh", "repo", "view", "--json", "nameWithOwner"])
        return str(json.loads(raw)["nameWithOwner"])
