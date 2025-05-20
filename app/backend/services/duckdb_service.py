import uuid
import pandas as pd
import ibis
import pytz
from datetime import datetime, timedelta
from typing import List, Dict

from ..helpers import Logger

DUCKDB_SESSION_TABLE_NAME = "session"
DUCKDB_LOCAL_FILE = "study_sessions.duckdb"


class DuckDBService:
    def __init__(self, db_path: str = DUCKDB_LOCAL_FILE) -> None:
        self.con = ibis.duckdb.connect(db_path)
        session_schema = ibis.schema({
            "session_id": "string",
            "user_id": "string",
            "timestamp_start": "timestamp",
            "timestamp_stop": "timestamp",
            "synced": "boolean",
        })

        if "session" not in self.con.list_tables():
            self.con.create_table(DUCKDB_SESSION_TABLE_NAME, schema=session_schema)

    def insert_data(self, user_id: str, start_time: str, stop_time: str, synced: bool = False) -> None:
        session_id = str(uuid.uuid4())

        df = pd.DataFrame([{
            "session_id": session_id,
            "user_id": user_id,
            "timestamp_start": pd.to_datetime(start_time),
            "timestamp_stop": pd.to_datetime(stop_time),
            "synced": synced
        }])
        self.con.insert(DUCKDB_SESSION_TABLE_NAME, df)

    def collect_unsynced(self) -> List[Dict]:
        session_table = self.con.table(DUCKDB_SESSION_TABLE_NAME)
        unsynced_sessions = session_table.filter(session_table.synced.isin([False])) \
            .select(session_table.session_id,
                    session_table.user_id,
                    session_table.timestamp_start,
                    session_table.timestamp_stop)

        result = unsynced_sessions.execute()
        # Ensure proper handling of result format
        return [dict(zip(result.columns, row)) for row in result]

    def mark_as_synced(self, session_ids: List[str]) -> None:
        if not session_ids:
            return

        session_table = self.con.table(DUCKDB_SESSION_TABLE_NAME)
        updated_sessions = session_table.filter(session_table.session_id.isin(session_ids)) \
            .mutate(synced=True)
        updated_sessions.execute()

    def get_current_streak(self, user_id: str, timezone_str: str = 'UTC') -> int:
        try:
            tz = pytz.timezone(timezone_str)
            session_table = self.con.table(DUCKDB_SESSION_TABLE_NAME)

            df = session_table.filter(session_table.user_id == user_id) \
                .select(session_table.timestamp_start) \
                .order_by(session_table.timestamp_start.desc()) \
                .execute()

            # Convert timestamps to local dates
            date_set = set()
            for row in df.itertuples(index=False):
                timestamp = row.timestamp_start
                if isinstance(timestamp, str):
                    timestamp = pd.to_datetime(timestamp)
                if timestamp.tzinfo is None:
                    timestamp = timestamp.replace(tzinfo=pytz.utc)
                local_date = timestamp.astimezone(tz).date()
                date_set.add(local_date)

            # Count consecutive days including today
            today = datetime.now(tz).date()
            streak = 0
            while today in date_set:
                streak += 1
                today -= timedelta(days=1)

            Logger.debug(f"Streak calculated as {streak}")
            return streak

        except Exception as e:
            Logger.error(f"Failed to calculate current streak: {e}")
            return 0

    def get_highest_streak(self, user_id: str, timezone_str: str = 'UTC') -> int:
        try:
            tz = pytz.timezone(timezone_str)
            session_table = self.con.table(DUCKDB_SESSION_TABLE_NAME)

            # Query all timestamps for the user, ordered by timestamp_start (ASC)
            df = session_table.filter(session_table.user_id == user_id) \
                .select(session_table.timestamp_start) \
                .order_by(session_table.timestamp_start.asc()) \
                .execute()

            if df.empty:
                return 0

            # Convert timestamps to local dates in the specified timezone
            dates = set()
            for row in df.itertuples(index=False):
                timestamp = row.timestamp_start
                if isinstance(timestamp, str):
                    timestamp = pd.to_datetime(timestamp)
                if timestamp.tzinfo is None:
                    timestamp = timestamp.replace(tzinfo=pytz.utc)
                local_date = timestamp.astimezone(tz).date()
                dates.add(local_date)

            if not dates:
                return 0

            # Sort the dates and calculate the highest streak
            dates = sorted(dates)
            highest_streak = 1
            current_streak = 1
            for i in range(1, len(dates)):
                if (dates[i] - dates[i - 1]).days == 1:
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
        try:
            # Fetch the session table and filter by user_id
            session_table = self.con.table(DUCKDB_SESSION_TABLE_NAME)
            sessions = session_table.filter(session_table.user_id == user_id) \
                .select(session_table.timestamp_start, session_table.timestamp_stop)

            # Execute the query and retrieve the result
            result = sessions.execute()
            if result.empty:
                return 0.0

            # Calculate total duration in minutes and count of sessions
            total_duration_seconds = 0
            session_count = 0

            # Iterate over the DataFrame rows
            for _, row in result.iterrows():
                timestamp_start = row['timestamp_start']
                timestamp_stop = row['timestamp_stop']

                # Convert to datetime if they're in string format
                if isinstance(timestamp_start, str):
                    timestamp_start = pd.to_datetime(timestamp_start)
                if isinstance(timestamp_stop, str):
                    timestamp_stop = pd.to_datetime(timestamp_stop)

                # Ensure that timestamps are in datetime format
                if isinstance(timestamp_start, datetime) and isinstance(timestamp_stop, datetime):
                    duration = (timestamp_stop - timestamp_start).total_seconds() / 60  # Convert to minutes
                    if duration > 0:  # Ignore sessions with negative duration
                        total_duration_seconds += duration
                        session_count += 1

            if session_count == 0:
                return 0.0

            # Calculate average session duration in minutes
            average_minutes = total_duration_seconds / session_count
            Logger.debug(f"Average session minutes calculated as {average_minutes:.2f}")
            return round(average_minutes, 2)

        except Exception as e:
            Logger.error(f"Failed to calculate average session time: {e}")
            return 0.0

    def fetch_data(self, table_name: str) -> List[Dict]:
        try:
            table = self.con.table(table_name)
            df = table.execute()
            return df.to_dict(orient="records")
        except Exception as e:
            Logger.error(f"Data fetch failed: {e}")
            return []
