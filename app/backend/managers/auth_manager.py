from ..helpers import Logger, Signal
from ..services import SupabaseService
from ..managers import ContextManager


class AuthManager:
    def __init__(self, auth_service: SupabaseService, context: ContextManager):
        self.auth_service = auth_service
        self.context = context

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

        self.auth_service.create_account(email, password, username)

    def login(self, signal: Signal) -> None:
        self.auth_service.login(email="testuser@gmail.com", password="testpass")

        if self.auth_service.is_connected():
            user_info = self.auth_service.get_user_info()
            # Update the context instead of local storage
            self.context.user_id = user_info.user.id
            signal.nav = True
