from ..helpers import Logger, Signal, Items, Actions, ViewState
from ..services import SupabaseService
from ..managers import ContextManager

from typing import Callable


class AuthManager:
    def __init__(self, auth_service: SupabaseService, callback: Callable, context: ContextManager):
        self.auth_service = auth_service
        self.context = context
        self.callback = callback

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

    def login(self, signal: Signal) -> None:
        # Auth takes email for now, might need to make it interchangeable (login with both email and user)
        self.auth_service.login(email=signal.data.get("username"), password=signal.data.get("password"))
        # self.auth_service.login(email="testuser@gmail.com", password="testpass")

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
            welcome_signal = Signal(
                                item=Items.HOME_CURRENT_STREAK,
                                text=f"Current Streak: {1} day",
                                action=Actions.LABEL_SET,
                                source=ViewState.HOME,
                            )
            self.callback(welcome_signal)
            welcome_signal = Signal(
                                item=Items.HOME_HIGHEST_STREAK,
                                text=f"Highest Streak: {2} days",
                                action=Actions.LABEL_SET,
                                source=ViewState.HOME,
                            )
            self.callback(welcome_signal)
            welcome_signal = Signal(
                                item=Items.HOME_DAILY_AVERAGE,
                                text=f"Daily Average: {3} hours",
                                action=Actions.LABEL_SET,
                                source=ViewState.HOME,
                            )
            self.callback(welcome_signal)
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

