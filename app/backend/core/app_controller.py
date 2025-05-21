from PyQt6.QtCore import QTimer, QObject
from ..models import Model
from ..views import View
from ..helpers import Logger, Connections, Signal, ViewState, KeyAction, Items
from ..managers import ExtractorManager, NavigationManager, KeybindManager
from .eventbus import event_bus


class ApplicationController(QObject):
    def __init__(self, model_list: list[Model], view_list: list[View]) -> None:
        super().__init__()
        self.model_list: list[Model] = model_list
        self.view_map: dict[ViewState, View] = {}
        self.extractor = ExtractorManager(view_map=self.view_map)
        self.navigator = NavigationManager()

        # QTimer to poll the event bus every 100ms
        self.initialize_event_polling()
        self.initialize_keybinds()

        # Wiring up Model signals to Controller
        for model in self.model_list:
            model.model_signal.connect(self.handle_model_response)

        self.initialize_views(view_list)

    def initialize_event_polling(self, interval_ms: int = 100) -> None:
        self.event_poll_timer = QTimer()
        self.event_poll_timer.timeout.connect(self.dispatch_queued_signals)
        self.event_poll_timer.start(interval_ms)

    def initialize_views(self, view_list: list[View]) -> None:
        for view in view_list:
            self.connect_items(view)
            self.view_map[view.view_state] = view
            self.navigator.add_view(view)
            KeybindManager.activate_keybinds(view)

        self.navigator.do_show()

    def initialize_keybinds(self):
        KeybindManager.add_keybind(ViewState.LOGIN, KeyAction.PRESS_ENTER, Items.LOGIN_LOGIN)
        KeybindManager.add_keybind(ViewState.HOME, KeyAction.PRESS_S, Items.SETTINGS)

    def dispatch_queued_signals(self) -> None:
        while event_bus.has_signals():
            signal = event_bus.get_next_signal()
            if signal and not self.route_to_model(signal):
                Logger.error(f"No model could handle signal: {signal.item}")

    def route_to_model(self, signal: Signal) -> bool:
        for model in self.model_list:
            if model.can_handle(signal):
                model.update_model(signal)
                return True
        return False

    # Connect items based on action types
    def connect_items(self, view: View) -> None:
        for name, data in view.item_map.items():
            signal = Signal(item=name, source=view.view_state, action=data["action"])
            Connections.connect_item(data["instance"], signal, self.handle_view_response)

    # Response from View (Initial Trigger), sending to Model for processing
    def handle_view_response(self, signal: Signal) -> None:
        signal.data = self.extractor.extract(signal.item)
        if signal and not self.route_to_model(signal):
            Logger.error(f"No model could handle signal: {signal.item}")

    # Response from Model (Compute Response), sending to View for presentation
    def handle_model_response(self, signal: Signal) -> None:
        if signal.nav:
            self.navigator.handle_navigation(signal)

        if signal.source == ViewState.ALL:
            targets = self.view_map.values()
        else:
            targets = [self.view_map[signal.source]]

        for view in targets:
            view.update_view(signal)
