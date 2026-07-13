"""
database.py

Stores scan history using SQLite.
"""

import sqlite3
from datetime import datetime
from pathlib import Path


class Database:

    def __init__(self):

        base_dir = Path(__file__).resolve().parent.parent

        db_folder = base_dir / "output"

        db_folder.mkdir(exist_ok=True)

        self.db_path = db_folder / "scanner.db"

        self.connection = sqlite3.connect(self.db_path)

        self.create_table()

    def create_table(self):

        cursor = self.connection.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS scan_history(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            target_url TEXT,

            scan_date TEXT,

            pages_scanned INTEGER,

            overall_score INTEGER,

            overall_risk TEXT
        )
        """)

        self.connection.commit()

    def save_scan(
        self,
        target_url,
        pages_scanned,
        overall_score,
        overall_risk
    ):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO scan_history(
                target_url,
                scan_date,
                pages_scanned,
                overall_score,
                overall_risk
            )
            VALUES(?,?,?,?,?)
            """,
            (
                target_url,
                datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                pages_scanned,
                overall_score,
                overall_risk
            )
        )

        self.connection.commit()

    def get_history(self):

        cursor = self.connection.cursor()

        cursor.execute("""
        SELECT * FROM scan_history
        ORDER BY id DESC
        """)

        return cursor.fetchall()

    def close(self):
        self.connection.close()