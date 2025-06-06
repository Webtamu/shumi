from PyQt6.QtWidgets import QWidget, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
from abc import abstractmethod

from ..helpers import Signal, Items, Actions, ViewState
from ..widgets import QWebWindow
from datetime import datetime, timedelta
import json
from collections import defaultdict


class View(QWidget):

    @abstractmethod
    def __init__(self) -> None:
        super().__init__()
        self.view_state = ViewState.DEFAULT
        self.window = None
        self.item_map = {}
        self.action_map = {
            Actions.BTN_PRESS: self.update_button,
            Actions.BOX_CHECK: self.update_box,
            Actions.LABEL_SET: self.update_label,
            Actions.COMBO_SET: self.update_combo,
            Actions.WEB_COMPONENT_SET: self.update_web_component
        }
        self.setup()
        self.initialize_style()
        self.initialize_buttons()

    @abstractmethod
    def setup(self) -> None:
        pass

    def initialize_buttons(self) -> None:
        for item_data in self.item_map.values():
            widget = item_data["instance"]
            if isinstance(widget, QPushButton):
                widget.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

    def initialize_style(self) -> None:
        with open("app/frontend/resources/light_mode.qss", "r") as file:
            self.window.setStyleSheet(file.read())

    def update_view(self, signal: Signal) -> None:
        if signal.item == Items.DARK_MODE:
            self.toggle_dark_mode(signal)

        item_entry = self.item_map.get(signal.item)
        if not item_entry:
            return

        if action := self.action_map.get(signal.action):
            action(item_entry["instance"], signal)

    def toggle_dark_mode(self, signal: Signal) -> None:
        stylesheet_path = (
            "app/frontend/resources/dark_mode.qss" if signal.state else "app/frontend/resources/light_mode.qss"
        )
        with open(stylesheet_path, "r") as file:
            self.window.setStyleSheet(file.read())

    def update_button(self, item: QWidget, signal: Signal) -> None:
        pass

    def update_box(self, item: QWidget, signal: Signal) -> None:
        was_blocked = item.blockSignals(True)
        item.setChecked(signal.state)
        item.setText(signal.text)
        item.blockSignals(was_blocked)

    def update_label(self, item: QWidget, signal: Signal) -> None:
        item.setText(signal.text)

    def update_combo(self, item: QWidget, signal: Signal) -> None:
        was_blocked = item.blockSignals(True)
        if signal.data:
            item.addItems(signal.data)
        if signal.text:
            item.setCurrentText(signal.text)
        item.blockSignals(was_blocked)

    def update_web_component(self, item: QWebWindow, signal: Signal) -> None:
        if signal.item == Items.HOME_HEATMAP:
            self.update_heatmap(item, signal)
        elif signal.item == Items.STATS_GRAPH:
            self.update_graph(item, signal)

    def update_graph(self, item: QWebWindow, signal: Signal) -> None:
        try:
            raw_data = json.loads(signal.data)

            today = datetime.now().date()
            seven_days_ago = today - timedelta(days=6)
            session_totals = defaultdict(float)

            for entry in raw_data:
                try:
                    start = datetime.fromisoformat(entry["timestamp_start"])
                    stop = datetime.fromisoformat(entry["timestamp_stop"])
                    date_str = start.date().isoformat()

                    if seven_days_ago <= start.date() <= today:
                        duration = (stop - start).total_seconds()  # in seconds
                        session_totals[date_str] += duration
                except Exception as e:
                    print(f"Error parsing session: {e}")

            # Ensure all 7 days are represented
            result = []
            for i in range(7):
                day = seven_days_ago + timedelta(days=i)
                date_str = day.isoformat()
                result.append({
                    "date": date_str,
                    "value": round(session_totals.get(date_str, 0), 2)
                })
            item.update_chart_data(json.dumps({"data": result}))

        except Exception as e:
            print(f"Error in update_graph: {e}")

    def update_heatmap(self, item: QWebWindow, signal: Signal) -> None:
        raw_data = json.loads(signal.data)
        session_count = defaultdict(int)

        for entry in raw_data:
            start = datetime.fromisoformat(entry["timestamp_start"])
            date_str = start.strftime("%Y-%m-%d")
            session_count[date_str] += 1

        normalized_data = {
            date: min(10, count)
            for date, count in session_count.items()
        }
        item.update_chart_data(json.dumps(normalized_data))
