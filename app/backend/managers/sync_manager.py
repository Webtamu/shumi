from ..helpers import Logger, Signal
from ..services import DuckDBService, SupabaseService
from ..managers import ContextManager


class SyncManager:
    def __init__(self, local_database: DuckDBService, cloud_database: SupabaseService, context: ContextManager):
        self.local_database = local_database
        self.cloud_database = cloud_database

    def sync_to_cloud(self, signal: Signal = None) -> None:
        """
        Sync unsynced data from the local database to the cloud.
        """

        unsynced_rows = self.local_database.collect_unsynced()

        if not unsynced_rows:
            Logger.info('No unsynced sessions to upload.')
            return

        synced_rows = self.cloud_database.upload_unsynced_sessions(unsynced_rows)

        if synced_rows:
            self.local_database.mark_as_synced(synced_rows)
            Logger.info(f'Synced {len(synced_rows)} session(s) to Supabase.')
        else:
            Logger.error('Failed to sync any sessions.')

    def sync_from_cloud(self) -> None:
        """
        Sync cloud data to local DuckDB.
        """
        return




