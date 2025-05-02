from ..helpers import Logger, Signal
from ..services import SupabaseService
from ..core.context import app_context
from ..core.settings import get_settings
import datetime


class AuthManager:
    def __init__(self, auth_service: SupabaseService):
        self.auth_service = auth_service
        self.settings = get_settings()
        # self.login()  # Attempt auto-login on initialization

    def validate_creds(self, creds: dict) -> bool:
        username = creds.get("user")
        email = creds.get("email")
        password = creds.get("pass")
        password_confirm = creds.get("confirm_pass")

        if not username or not email or not password:
            Logger.error("Account creation failed: Missing required fields")
            return False

        if password != password_confirm:
            Logger.error("Account creation failed: Passwords do not match")
            return False

        if "@" not in email or "." not in email:
            Logger.error("Account creation failed: Invalid email format")
            return False

        return True

    def create_account(self, signal: Signal) -> None:
        creds = {
            "user": signal.data.get("user"),
            "email": signal.data.get("email"),
            "pass": signal.data.get("pass"),
            "confirm_pass": signal.data.get("confirm_pass")
        }

        if not self.validate_creds(creds):
            return

        self.auth_service.create_account(email=creds["email"],
                                         password=creds["pass"],
                                         username=creds["user"]
                                         )

    def save_auth_token(self, access_token: str, refresh_token: str) -> None:
        self.settings.setValue("access_token", access_token)
        self.settings.setValue("refresh_token", refresh_token)
        self.settings.setValue("last_login", datetime.datetime.now().isoformat())
        Logger.info("Auth tokens saved successfully.")

    def get_auth_token(self) -> dict:
        settings = get_settings()
        access_token = settings.value("access_token", defaultValue=None)
        refresh_token = settings.value("refresh_token", defaultValue=None)
        last_login = settings.value("last_login", defaultValue=None)

        if all([access_token, refresh_token, last_login]):
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "last_login": last_login
            }
        else:
            Logger.error("Auth tokens are missing or incomplete.")
            return {}

    def clean_auth_token(self) -> None:
        self.settings.remove("access_token")
        self.settings.remove("refresh_token")
        self.settings.remove("last_login")
        Logger.info("Auth tokens cleaned successfully.")

    def attempt_token_login(self) -> bool:
        creds = self.get_auth_token()
        if not creds:
            Logger.error("No previous auth tokens found.")
            return False

        Logger.info("Found previous auth tokens, attempting auto-sign in.")
        try:
            self.auth_service.client.auth.set_session(
                creds.get("access_token"), creds.get("refresh_token")
            )
            return True
        except Exception as e:
            Logger.error(f"Auto-sign in failed: {e}")
            self.clean_auth_token()
            return False

    def attempt_manual_login(self, signal: Signal) -> None:
        email = signal.data.get("username")
        password = signal.data.get("password")
        stay_signed_in = signal.data.get("stay_signed_in")

        response = self.auth_service.login(email=email, password=password)

        if stay_signed_in:
            self.save_auth_token(
                access_token=response.session.access_token,
                refresh_token=response.session.refresh_token
            )

    def populate_user_context(self) -> None:
        user_info = self.auth_service.get_user_info()
        app_context.user_id = user_info.user.id
        app_context.username = user_info.user.user_metadata.get("full_name")
        app_context.email = user_info.user.user_metadata.get("email")

    def logout(self, signal: Signal) -> None:
        self.auth_service.logout()
        self.clean_auth_token()
        Logger.info("Logged out successfully.")

    def login(self, signal: Signal = None) -> None:
        if self.attempt_token_login():
            Logger.info("Auto-signing in successful!")
        else:
            Logger.info("Falling back to manual login.")
            self.attempt_manual_login(signal)

        if self.auth_service.is_connected():
            self.populate_user_context()
        else:
            signal.nav = False
