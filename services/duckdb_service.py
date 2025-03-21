import duckdb
import os
from helpers.helpers import Colors

class DuckDBService:
    def __init__(self, db_path: str = "local_data.duckdb"):
        """Initialize DuckDB connection."""
        self.con = duckdb.connect(db_path)
        self.con.execute(
            '''
            CREATE TABLE IF NOT EXISTS session (
                session_id TEXT PRIMARY KEY DEFAULT uuid(),
                user_id TEXT, 
                timestamp_start TIMESTAMP, 
                timestamp_stop TIMESTAMP
            )
            '''
        )

    

    def insert_data(self, aUserID, aStartTime, aStopTime):
        """Insert data into local DuckDB."""

        self.con.execute(
            """
            INSERT INTO session (user_id, timestamp_start, timestamp_stop)
            VALUES (?, ?, ?)
            """,
            (aUserID, aStartTime, aStopTime)
        )


        result = self.con.execute("SELECT * FROM session").fetchall()
        for row in result:
            print(row)
