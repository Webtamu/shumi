import supabase

import os
from dotenv import load_dotenv
from typing import List, Dict

from helpers.helpers import Colors
from helpers.logger import Logger

class SupabaseService:
    def __init__(self) -> None:
        load_dotenv()

        theURL: str = os.getenv("SUPABASE_URL")
        theKey: str = os.getenv("SUPABASE_KEY")

        if not theURL or not theKey:
            raise ValueError("Supabase URL or Key is missing in environment variables.")

        self.theClient: supabase.Client = supabase.create_client(theURL, theKey)

    def isConnected(self) -> bool:
        try:
            response = self.theClient.table('DuckDB').select("*").limit(1).execute()
            return response.data         
        except Exception as e:
            Logger.error(f"Supabase connection test failed: {e}")
            return False
    
    def fetchData(self, aTableName: str) -> dict:
        try:
            theResponse = self.theClient.table(aTableName).select("*").execute()
            return theResponse
        except Exception as e:
            Logger.error(f"Data fetch failed: {e}")
    
    def login(self, anEmail: str, aPassword: str) -> None:
        try:
            theResponse = self.theClient.auth.sign_in_with_password(
                {
                    "email": anEmail,
                    "password": aPassword
                }
            )
            Logger.info(f"Login successful.")
            self.theClient.auth.set_session(theResponse.session.access_token, theResponse.session.refresh_token)
        except Exception as e:
            Logger.error(f"Login failed: {e}") 
    
    def getUserInfo(self) -> str:
        return self.theClient.auth.get_user()

    def logout(self) -> None:
        theResponse = self.theClient.auth.sign_out()
        Logger.info(f"Logged out successfully.")

    def upload_unsynced_sessions(self, aSessionRows: List[Dict]) -> List[str]:
        """
        Upload unsynced session rows to Supabase.
        Returns a list of session_ids that were successfully uploaded.
        """
        synced_ids: List[str] = []

        for row in aSessionRows:
            try:
                row["timestamp_start"] = row["timestamp_start"].isoformat()
                row["timestamp_stop"] = row["timestamp_stop"].isoformat()
                response = self.theClient.table("sync_test").insert(row).execute()
                if response.data:
                    synced_ids.append(row["session_id"])
            except Exception as e:
                Logger.error(f"Failed to sync session {row.get('session_id')}: {e}")

        return synced_ids

        

