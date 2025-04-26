from PyQt6.QtCore import QSettings
from ..helpers import Logger, Signal, Items, Actions, ViewState
from ..services import SupabaseService
from ..managers import ContextManager

from typing import Callable
import datetime

QSETTINGS_ORG = "WEBTAMU"
QSETTINGS_APP = "SHUMI"


class AuthManager:
    def __init__(self, auth_service: SupabaseService, callback: Callable, context: ContextManager):
        self.auth_service = auth_service
        self.context = context
        self.callback = callback
        self.login(Signal())  # Attempt auto-login on initialization

    def create_account(self, signal: Signal) -> None:
        username = signal.data.get("user")
        email = signal.data.get("email")
        password = signal.data.get("pass")
        password_confirm = signal.data.get("confirm_pass")

        if not username or not email or not password:
            Logger.error("Account creation failed: Missing required fields")
            return

        if password != password_confirm:
            Logger.error("Account creation failed: Passwords do not match")
            return

        if "@" not in email or "." not in email:
            Logger.error("Account creation failed: Invalid email format")
            return

        self.auth_service.create_account(email=email, password=password, username=username)

    def save_auth_token(self, access_token: str, refresh_token: str) -> None:
        settings = QSettings(QSETTINGS_ORG, QSETTINGS_APP)
        settings.setValue("access_token", access_token)
        settings.setValue("refresh_token", refresh_token)
        settings.setValue("last_login", datetime.datetime.now().isoformat())
        Logger.info("Auth tokens saved successfully.")

    def get_auth_token(self) -> dict:
        settings = QSettings(QSETTINGS_ORG, QSETTINGS_APP)
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
        settings = QSettings("Shumi", "Auth")
        settings.remove("access_token")
        settings.remove("refresh_token")
        settings.remove("last_login")
        Logger.info("Auth tokens cleaned successfully.")

    def logout(self, signal: Signal) -> None:
        self.auth_service.logout()
        self.clean_auth_token()
        signal.nav = True
        Logger.info("Logged out successfully.")

    def login(self, signal: Signal = None) -> None:
        creds = self.get_auth_token()
        if creds:
            Logger.info("Found previous auth tokens, attempting auto-sign in.")
            access_token = creds.get("access_token")
            refresh_token = creds.get("refresh_token")
            try:
                self.auth_service.client.auth.set_session(access_token, refresh_token)
                Logger.info("Auto-signing in!")
            except Exception as e:
                Logger.error(f"Auto-sign in failed: {e}")
                self.clean_auth_token()
                creds = None  # Force fallback to manual login

        if not creds:
            Logger.error("No previous auth tokens found, attempting with credentials.")
            response = self.auth_service.login(email=signal.data.get("username"), password=signal.data.get("password"))
            stay_signed_in = signal.data.get("stay_signed_in")
            if stay_signed_in:
                self.save_auth_token(
                    access_token=response.session.access_token,
                    refresh_token=response.session.refresh_token
                )

        if self.auth_service.is_connected():
            user_info = self.auth_service.get_user_info()
            self.context.user_id = user_info.user.id
            self.context.username = user_info.user.user_metadata.get("full_name")
            self.context.email = user_info.user.user_metadata.get("email")
            signal.nav = True

            # Need to callback and update dependent items, ducktape solution for now
            welcome_signal = Signal(
                                item=Items.HOME_WELCOME,
                                text=f"Welcome, {self.context.username} - Let's practice some Instrument today!",
                                action=Actions.LABEL_SET,
                                source=ViewState.HOME,
                            )
            self.callback(welcome_signal)
            current_streak_signal = Signal(
                                item=Items.HOME_CURRENT_STREAK,
                                text=f"Current Streak: {0} day",
                                action=Actions.LABEL_SET,
                                source=ViewState.HOME,
                            )
            self.callback(current_streak_signal)
            highest_streak_signal = Signal(
                                item=Items.HOME_HIGHEST_STREAK,
                                text=f"Highest Streak: {2} days",
                                action=Actions.LABEL_SET,
                                source=ViewState.HOME,
                            )
            self.callback(highest_streak_signal)
            daily_average_signal = Signal(
                                item=Items.HOME_DAILY_AVERAGE,
                                text=f"Daily Average: {3} hours",
                                action=Actions.LABEL_SET,
                                source=ViewState.HOME,
                            )
            self.callback(daily_average_signal)
            profile_username_signal = Signal(
                                item=Items.PROFILE_USERNAME,
                                text=f"{self.context.username}",
                                action=Actions.LABEL_SET,
                                source=ViewState.PROFILE,
                            )
            self.callback(profile_username_signal)
            profile_email_signal = Signal(
                                item=Items.PROFILE_EMAIL,
                                text=f"{self.context.email}",
                                action=Actions.LABEL_SET,
                                source=ViewState.PROFILE,
                            )
            self.callback(profile_email_signal)
        else:
            signal.nav = False
