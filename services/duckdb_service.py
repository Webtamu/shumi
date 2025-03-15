import duckdb

import os
from helpers.helpers import Colors

class DuckDBService:
    def __init__(self, db_path: str = "local_data.duckdb"):
        """Initialize DuckDB connection."""


        self.con.execute(
            '''
            CREATE TABLE IF NOT EXISTS DuckDB (
                id INT PRIMARY KEY,
                text TEXT
            )
            '''
        )

        self.con = duckdb.connect(db_path)
        self.create_table()

    def insert_data(self, data: list):
        """Insert data into local DuckDB."""
        self.con.executemany("INSERT INTO DuckDB (id, text) VALUES (?, ?)", data)



