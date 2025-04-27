from PyQt6.QtCore import QObject, QEvent
from PyQt6.QtWidgets import QWidget
from ..helpers import KeyAction, Items


class KeyEventFilter(QObject):
    def __init__(self, view_instance, key_bindings):
        super().__init__()
        self.view_instance = view_instance
        self.key_bindings = key_bindings

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.KeyPress:
            key = event.key()

            for key_action, item in self.key_bindings.items():
                if key == key_action.value and item in self.view_instance.item_map:
                    target = self.view_instance.item_map[item]["instance"]
                    if hasattr(target, 'click'):
                        target.click()
                        return True
        return super().eventFilter(obj, event)


class KeybindManager:
    bindings = {}
    active_filters = {}

    @classmethod
    def add_keybind(cls, view, key_action: KeyAction, item: Items):
        if view not in cls.bindings:
            cls.bindings[view] = {}
        cls.bindings[view][key_action] = item

    @classmethod
    def activate_keybinds(cls, view_instance):
        view_state = view_instance.view_state

        if view_state not in cls.bindings:
            return

        window = view_instance.window

        if view_instance in cls.active_filters:
            window.removeEventFilter(cls.active_filters[view_instance])

        event_filter = KeyEventFilter(view_instance, cls.bindings[view_state])
        window.installEventFilter(event_filter)

        for child in window.findChildren(QWidget):
            child.installEventFilter(event_filter)

        cls.active_filters[view_instance] = event_filter
