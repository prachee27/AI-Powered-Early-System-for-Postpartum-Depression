"""Persist and enforce the one-week EPDS screening interval.

The journal check-in may happen every day.  The ten EPDS questions are a
weekly screening, so this small repository deliberately stores only the date
on which a participant last completed them.  SQLite is part of Python, which
makes this usable locally without requiring a separate database server.
"""

from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path
import sqlite3


EPDS_INTERVAL_DAYS = 7
DEFAULT_DATABASE_PATH = Path(__file__).resolve().parents[3] / "data" / "assessments.db"


class EPDSSchedule:
    def __init__(self, database_path: Path | str = DEFAULT_DATABASE_PATH):
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._create_table()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.database_path)

    def _create_table(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS epds_submissions (
                    patient_id TEXT NOT NULL,
                    completed_on TEXT NOT NULL,
                    PRIMARY KEY (patient_id, completed_on)
                )
                """
            )

    def next_due_date(self, patient_id: str) -> date | None:
        with self._connect() as connection:
            row = connection.execute(
                """SELECT MAX(completed_on) FROM epds_submissions
                   WHERE patient_id = ?""",
                (patient_id,),
            ).fetchone()
        if not row or row[0] is None:
            return None
        return date.fromisoformat(row[0]) + timedelta(days=EPDS_INTERVAL_DAYS)

    def submit(self, patient_id: str, completed_on: date) -> date:
        """Record a weekly EPDS submission or reject an early submission.

        Returns the date on which the next EPDS questionnaire is due.
        """
        due_date = self.next_due_date(patient_id)
        if due_date is not None and completed_on < due_date:
            raise ValueError(
                "EPDS is a weekly questionnaire. "
                f"The next assessment is due on {due_date.isoformat()}."
            )

        with self._connect() as connection:
            connection.execute(
                "INSERT OR IGNORE INTO epds_submissions(patient_id, completed_on) VALUES (?, ?)",
                (patient_id, completed_on.isoformat()),
            )
        return completed_on + timedelta(days=EPDS_INTERVAL_DAYS)
