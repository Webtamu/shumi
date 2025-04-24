import supabase
import os
from dotenv import load_dotenv
from typing import List, Dict

from ..helpers import Logger


class SupabaseService:
    def __init__(self) -> None:
        load_dotenv()

        url: str = os.getenv("SUPABASE_URL")
        key: str = os.getenv("SUPABASE_KEY")

        if not url or not key:
            raise ValueError("Supabase URL or Key is missing in environment variables.")

        self.client: supabase.Client = supabase.create_client(url, key)

    def is_connected(self) -> bool:
        try:
            response = self.client.table('DuckDB').select("*").limit(1).execute()
            return bool(response.data)
        except Exception as e:
            Logger.error(f"Supabase connection test failed: {e}")
            return False

    def fetch_data(self, table_name: str) -> dict:
        try:
            response = self.client.table(table_name).select("*").execute()
            return response
        except Exception as e:
            Logger.error(f"Data fetch failed: {e}")
            return {}

    def create_account(self, email: str, password: str, username: str) -> bool:
        try:
            response = self.client.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": {
                        "full_name": username
                    }
                }
            })
            if response.user and response.user.id:
                Logger.info(f"User registered successfully: {email}")
                return True
        except Exception as e:
            Logger.error(f"Account creation failed: {e}")
        return False

    def login(self, email: str, password: str) -> None:
        try:
            response = self.client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            Logger.info("Login successful.")
            self.client.auth.set_session(response.session.access_token,
                                         response.session.refresh_token)
        except Exception as e:
            Logger.error(f"Login failed: {e}")

    def get_user_info(self) -> str:
        return self.client.auth.get_user()

    def logout(self) -> None:
        self.client.auth.sign_out()
        Logger.info("Logged out successfully.")

    def upload_unsynced_sessions(self, session_rows: List[Dict]) -> List[str]:
        """
        Upload unsynced session rows to Supabase.
        Returns a list of session_ids that were successfully uploaded.
        """
        synced_ids: List[str] = []

        for row in session_rows:
            try:
                row["timestamp_start"] = row["timestamp_start"].isoformat()
                row["timestamp_stop"] = row["timestamp_stop"].isoformat()
                response = self.client.table("sync_test").insert(row).execute()
                if response.data:
                    synced_ids.append(row["session_id"])
            except Exception as e:
                Logger.error(f"Failed to sync session {row.get('session_id')}: {e}")

        return synced_ids
