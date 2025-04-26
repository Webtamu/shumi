from PyQt6.QtWidgets import QStackedWidget
from PyQt6.QtCore import QObject

from ..views import View
from ..helpers import Signal, ViewState, Items, Logger


class NavigationManager(QObject):
    def __init__(self) -> None:
        super().__init__()
        self.stacked_widget = QStackedWidget()
        self.view_map: dict[ViewState, int] = {}
        self.counter = 0

    def add_views(self, view_list: list[View]) -> None:
        for view in view_list:
            self.stacked_widget.addWidget(view.window)
            self.view_map[view.view_state] = self.counter
            self.counter += 1
            view.nav_signal.connect(self.handle_navigation)

    def navigate_to(self, view_state: ViewState) -> None:
        if view_state in self.view_map:
            self.stacked_widget.setCurrentIndex(self.view_map[view_state])

    def get_current_view(self) -> View:
        return self.stacked_widget.currentWidget()

    def do_show(self) -> None:
        self.stacked_widget.show()

    def handle_navigation(self, signal: Signal) -> None:
        nav_map = {
            Items.SETTINGS: ViewState.SETTINGS,
            Items.HOME: ViewState.HOME,
            Items.STATS: ViewState.STATS,
            Items.PROFILE: ViewState.PROFILE,
            Items.START: ViewState.SESSION,
            Items.STOP: ViewState.SUMMARY,
            Items.BEGIN_TAKE: ViewState.HOME,
            Items.LOGIN_LOGIN: ViewState.HOME,
            Items.PROFILE_LOGOUT: ViewState.LOGIN,
            Items.LOGIN_CREATE_ACCOUNT: ViewState.CREATE,
            Items.CREATE_ACCOUNT_ALREADY_HAVE_ACCOUNT: ViewState.LOGIN,
        }
        destination = nav_map.get(signal.item)

        if not destination:
            return

        self.navigate_to(destination)
