from PyQt6.QtCore import QTimer
from ..models import Model
from ..views import View
from .controllers import Controller
from ..helpers import Logger, Connections, Signal, ViewState
from ..managers import ExtractorManager
from ..core.eventbus import event_bus


class ApplicationController(Controller):
    def __init__(self, model_list: list[Model], view_list: list[View]) -> None:
        super().__init__(model_list, view_list)

        self.model_list: list[Model] = model_list
        self.view_map: dict[ViewState, View] = {}
        self.extractor = ExtractorManager(view_map=self.view_map)

        # QTimer to poll the event bus every 100ms
        self.event_poll_timer = QTimer()
        self.event_poll_timer.timeout.connect(self.dispatch_queued_signals)
        self.event_poll_timer.start(100)

        # Wiring up Model signals to Controller
        for model in self.model_list:
            model.model_signal.connect(self.handle_model_response)

        # Connecting View items to Controller
        for view in view_list:
            self.connect_items(view)
            self.view_map[view.view_state] = view

    def dispatch_queued_signals(self) -> None:
        while event_bus.has_signals():
            signal = event_bus.get_next_signal()
            if signal:
                for model in self.model_list:
                    if model.can_handle(signal):
                        model.update_model(signal)
                        break

    # Connect items based on action types
    def connect_items(self, view: View) -> None:
        for item_name, item_data in view.item_map.items():
            signal = Signal(
                item=item_name,
                source=view.view_state,
                action=item_data["action"]
            )
            Connections.connect_item(widget=item_data["instance"],
                                     signal=signal,
                                     function=self.handle_view_response)

    # Response from View (Initial Trigger), sending to Model for processing
    def handle_view_response(self, signal: Signal) -> None:
        signal.data = self.extractor.extract(signal.item)
        for model in self.model_list:
            if model.can_handle(signal):
                model.update_model(signal)
                return
        Logger.error(f"Cannot handle request: {signal.item}")

    # Response from Model (Compute Response), sending to View for presentation
    def handle_model_response(self, signal: Signal) -> None:
        if signal.source == ViewState.ALL:
            for view in self.view_map.values():
                view.update_view(signal)
        else:
            view_source = self.view_map[signal.source]
            view_source.update_view(signal)
