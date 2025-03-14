import supabase

import os
from dotenv import load_dotenv

class SupabaseService:
    def __init__(self) -> None:
        load_dotenv()

        theURL = os.getenv("SUPABASE_URL")
        theKey = os.getenv("SUPABASE_KEY")

        if not theURL or not theKey:
            raise ValueError("Supabase URL or Key is missing in environment variables.")

        self.theClient: supabase.Client = supabase.create_client(theURL, theKey)

    def isConnected(self) -> bool:
        try:
            response = self.theClient.table('users').select("*").limit(1).execute()
            if response.data is not None:  
                return True
            return False
        except Exception as e:
            print(f"Supabase connection test failed: {e}")
            return False
    
    def fetchData(self, aTableName: str) -> list[dict]:
        theQuery = self.theClient.table(aTableName).select("*")
        theResponse = theQuery.execute()
        return theResponse