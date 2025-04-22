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
        Logger.debug(self.local_database.fetch_data('session'))

        unsynced_rows = self.local_database.collect_unsynced()
        synced_rows = self.cloud_database.upload_unsynced_sessions(unsynced_rows)
        self.local_database.mark_as_synced(synced_rows)

        Logger.debug(self.local_database.fetch_data('session'))

    def sync_to_cloud_test(self) -> None:
        """
        Sync local DuckDB unsynced sessions to Supabase.
        """
        unsynced_sessions = self.local_database.collect_unsynced()

        if not unsynced_sessions:
            Logger.info('No unsynced sessions to upload.')
            return

        synced_ids = self.cloud_database.upload_unsynced_sessions(unsynced_sessions)

        if synced_ids:
            self.local_database.mark_as_synced(synced_ids)
            Logger.info(f'Synced {len(synced_ids)} session(s) to Supabase.')
        else:
            Logger.error('Failed to sync any sessions.')
