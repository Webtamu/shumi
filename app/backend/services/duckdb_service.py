import duckdb
import pytz
from datetime import datetime, timedelta
from typing import List, Dict, Any

from ..helpers import Logger


class DuckDBService:
    def __init__(self, db_path: str = "local_data.duckdb") -> None:
        """Initialize DuckDB connection."""
        self.con = duckdb.connect(db_path)
        self.con.execute(
            '''
            CREATE TABLE IF NOT EXISTS session (
                session_id TEXT PRIMARY KEY DEFAULT uuid(),
                user_id TEXT,
                timestamp_start TIMESTAMP,
                timestamp_stop TIMESTAMP,
                synced BOOLEAN DEFAULT FALSE
            )
            '''
        )

    def insert_data(self,
                    user_id: str,
                    start_time: Any,
                    stop_time: Any,
                    synced: bool = False) -> None:

        """Insert data into local DuckDB."""
        self.con.execute(
            """
            INSERT INTO session (user_id, timestamp_start, timestamp_stop, synced)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, start_time.isoformat(), stop_time.isoformat(), synced)
        )

        self.con.execute("SELECT * FROM session").fetchall()

    def collect_unsynced(self) -> List[Dict[str, Any]]:
        """Return all unsynced session rows as list of dicts."""
        result = self.con.execute(
            "SELECT session_id, user_id, timestamp_start, timestamp_stop FROM session WHERE synced = FALSE"
        ).fetchall()
        cols = [desc[0] for desc in self.con.description]
        return [dict(zip(cols, row)) for row in result]

    def mark_as_synced(self, session_ids: List[str]) -> None:
        """Mark given session_ids as synced."""
        if not session_ids:
            return

        placeholders = ", ".join("?" for _ in session_ids)
        query = f"""
            UPDATE session
            SET synced = TRUE
            WHERE session_id IN ({placeholders})
        """
        self.con.execute(query, session_ids)

    def get_current_streak(self, user_id: str, timezone_str: str = 'UTC') -> int:
        """
        Calculate user's current daily streak based on their timezone.

        Args:
            user_id (str): The ID of the user.
            timezone_str (str): Timezone like 'Asia/Tokyo', 'America/Los_Angeles'.

        Returns:
            int: Number of consecutive days user has activity including today.
        """
        try:
            tz = pytz.timezone(timezone_str)

            # Fetch all session start timestamps for the user
            rows = self.con.execute(
                """
                SELECT timestamp_start FROM session
                WHERE user_id = ?
                ORDER BY timestamp_start DESC
                """, (user_id,)
            ).fetchall()

            # Convert timestamps to dates in the user's time zone
            date_set = set()
            for row in rows:
                utc_time = row[0].replace(tzinfo=pytz.utc)
                local_date = utc_time.astimezone(tz).date()
                date_set.add(local_date)

            # Check streak backwards from today
            today = datetime.now(tz).date()
            streak = 0
            while today in date_set:
                streak += 1
                today -= timedelta(days=1)
            Logger.debug(f"Streak calculated as {streak}")
            return streak

        except Exception as e:
            Logger.error(f"Failed to calculate streak: {e}")
            return 0

    def get_highest_streak(self, user_id: str, timezone_str: str = 'UTC') -> int:
        """
        Calculate the highest streak the user ever achieved.

        Args:
            user_id (str): The ID of the user.
            timezone_str (str): Timezone like 'Asia/Tokyo', 'America/Los_Angeles'.

        Returns:
            int: Highest streak achieved.
        """
        try:
            tz = pytz.timezone(timezone_str)

            rows = self.con.execute(
                """
                SELECT timestamp_start FROM session
                WHERE user_id = ?
                ORDER BY timestamp_start ASC
                """, (user_id,)
            ).fetchall()

            if not rows:
                return 0

            date_list = []
            for row in rows:
                utc_time = row[0].replace(tzinfo=pytz.utc)
                local_date = utc_time.astimezone(tz).date()
                date_list.append(local_date)

            if not date_list:
                return 0

            date_list = sorted(set(date_list))
            highest_streak = 1
            current_streak = 1

            for i in range(1, len(date_list)):
                if (date_list[i] - date_list[i - 1]).days == 1:
                    current_streak += 1
                    highest_streak = max(highest_streak, current_streak)
                else:
                    current_streak = 1

            Logger.debug(f"Highest streak calculated as {highest_streak}")
            return highest_streak

        except Exception as e:
            Logger.error(f"Failed to calculate highest streak: {e}")
            return 0

    def get_average_session_minutes(self, user_id: str) -> float:
        """
        Calculate average session duration in hours.

        Args:
            user_id (str): The ID of the user.

        Returns:
            float: Average hours per session.
        """
        try:
            rows = self.con.execute(
                """
                SELECT timestamp_start, timestamp_stop FROM session
                WHERE user_id = ?
                """, (user_id,)
            ).fetchall()

            if not rows:
                return 0.0

            total_duration = timedelta(0)
            session_count = 0

            for start, stop in rows:
                if start and stop:
                    duration = stop - start
                    total_duration += duration
                    session_count += 1

            if session_count == 0:
                return 0.0

            average_minutes = total_duration.total_seconds() / 60 / session_count
            Logger.debug(f"Average session minutes calculated as {average_minutes:.2f}")
            return average_minutes

        except Exception as e:
            Logger.error(f"Failed to calculate average session time: {e}")
            return 0.0

    def fetch_data(self, table_name: str) -> List[Dict[str, Any]]:
        """Fetch all data from the given table as list of dictionaries."""
        try:
            result = self.con.execute(f"SELECT * FROM {table_name}").fetchall()
            cols = [desc[0] for desc in self.con.description]
            return [dict(zip(cols, row)) for row in result]
        except Exception as e:
            Logger.error(f"Data fetch failed: {e}")
            return []
