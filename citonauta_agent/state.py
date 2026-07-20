from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from .catalog import SubjectRef


class AgentState:
    def __init__(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(path)
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS courses (
                subject_id TEXT PRIMARY KEY,
                area_id TEXT NOT NULL,
                title TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                attempts INTEGER NOT NULL DEFAULT 0,
                branch TEXT,
                pr_url TEXT,
                last_error TEXT,
                updated_at TEXT NOT NULL
            )
            """
        )
        self.connection.commit()

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()

    def register(self, subjects: list[SubjectRef]) -> None:
        for subject in subjects:
            self.connection.execute(
                """
                INSERT INTO courses(subject_id, area_id, title, status, updated_at)
                VALUES (?, ?, ?, 'pending', ?)
                ON CONFLICT(subject_id) DO UPDATE SET
                    area_id=excluded.area_id,
                    title=excluded.title
                """,
                (subject.id, subject.area_id, subject.title, self._now()),
            )
        self.connection.commit()

    def status(self, subject_id: str) -> str:
        row = self.connection.execute(
            "SELECT status FROM courses WHERE subject_id = ?", (subject_id,)
        ).fetchone()
        return str(row[0]) if row else "pending"

    def update(
        self,
        subject_id: str,
        status: str,
        *,
        branch: str | None = None,
        pr_url: str | None = None,
        error: str | None = None,
        increment_attempt: bool = False,
    ) -> None:
        self.connection.execute(
            """
            UPDATE courses
            SET status = ?,
                branch = COALESCE(?, branch),
                pr_url = COALESCE(?, pr_url),
                last_error = ?,
                attempts = attempts + ?,
                updated_at = ?
            WHERE subject_id = ?
            """,
            (
                status,
                branch,
                pr_url,
                error,
                1 if increment_attempt else 0,
                self._now(),
                subject_id,
            ),
        )
        self.connection.commit()

    def reset_failed(self) -> int:
        cursor = self.connection.execute(
            "UPDATE courses SET status='pending', last_error=NULL, updated_at=? WHERE status='failed'",
            (self._now(),),
        )
        self.connection.commit()
        return int(cursor.rowcount)

    def summary(self) -> dict[str, int]:
        rows = self.connection.execute(
            "SELECT status, COUNT(*) FROM courses GROUP BY status ORDER BY status"
        ).fetchall()
        return {str(status): int(count) for status, count in rows}

    def close(self) -> None:
        self.connection.close()
