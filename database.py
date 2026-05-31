import sqlite3
from datetime import datetime


class Database:
    def __init__(self, db_path: str = "requests.db"):
        self.db_path = db_path
        self._create_table()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _create_table(self):
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS requests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    full_name TEXT,
                    username TEXT,
                    date TEXT
                )
            """)
            conn.commit()

    def add_request(self, user_id: int, full_name: str, username: str):
        date = datetime.now().strftime("%d.%m.%Y %H:%M")
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO requests (user_id, full_name, username, date) VALUES (?, ?, ?, ?)",
                (user_id, full_name, username, date)
            )
            conn.commit()

    def get_all_requests(self) -> list[dict]:
        with self._connect() as conn:
            cursor = conn.execute(
                "SELECT user_id, full_name, username, date FROM requests ORDER BY id DESC"
            )
            rows = cursor.fetchall()
        return [
            {"user_id": r[0], "full_name": r[1], "username": r[2], "date": r[3]}
            for r in rows
        ]
