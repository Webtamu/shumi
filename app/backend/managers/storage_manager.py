from PyQt6.QtWidgets import QFileDialog
from ..helpers import Signal, Actions, Items, ViewState
import sounddevice
import os

from ..core.eventbus import event_bus
from ..core.settings import (
    get_settings,
    QSETTINGS_STORAGE_KEY,
    QSETTINGS_DARK_MODE_KEY,
    QSETTINGS_INPUT_DEVICE,
    QSETTINGS_OUTPUT_DEVICE
)


class StorageManager:
    def __init__(self):
        self.settings = get_settings()
        self.current_path: str = self.settings.value(QSETTINGS_STORAGE_KEY, defaultValue="")
        self.dark_mode: bool = self.settings.value(QSETTINGS_DARK_MODE_KEY, defaultValue=False, type=bool)
        if self.current_path:
            self.update_path()
        if self.dark_mode:
            self.update_dark_mode()
        self.list_audio_devices()
        self.set_input_output_devices()

    def select_directory(self, signal=None):
        dir_path = QFileDialog.getExistingDirectory(None, "Select Storage Directory", self.current_path or "")
        if dir_path:
            self.set_directory(dir_path)
            self.update_path()

    def update_path(self) -> None:
        path_signal = Signal(
                item=Items.SETTINGS_PATH_SELECTED,
                text=self.current_path,
                action=Actions.LABEL_SET,
                source=ViewState.SETTINGS
            )
        event_bus.publish(path_signal)

    def update_dark_mode(self) -> None:
        dark_mode_signal = Signal(
                item=Items.DARK_MODE,
                text="Dark Mode",
                action=Actions.BOX_CHECK,
                source=ViewState.ALL,
                state=self.dark_mode
                )
        event_bus.publish(dark_mode_signal)

    def set_directory(self, path: str):
        if os.path.isdir(path):
            self.current_path = path
            self.settings.setValue(QSETTINGS_STORAGE_KEY, path)

    def set_dark_mode(self, signal: Signal) -> None:
        self.dark_mode = signal.state
        self.settings.setValue(QSETTINGS_DARK_MODE_KEY, self.dark_mode)

    def get_input_output_devices(self) -> tuple:
        input_device = self.settings.value(QSETTINGS_INPUT_DEVICE, defaultValue=None)
        output_device = self.settings.value(QSETTINGS_OUTPUT_DEVICE, defaultValue=None)
        return input_device, output_device

    def set_input_output_devices(self) -> None:
        input_device, output_device = self.get_input_output_devices()
        input_device_signal = Signal(
            item=Items.SETTINGS_INPUT_DEVICE,
            text=input_device,
            action=Actions.COMBO_SET,
            source=ViewState.ALL
        )
        output_device_signal = Signal(
            item=Items.SETTINGS_OUTPUT_DEVICE,
            text=output_device,
            action=Actions.COMBO_SET,
            source=ViewState.ALL
        )
        event_bus.publish(input_device_signal, output_device_signal)

    def set_input_device(self, signal: Signal) -> None:
        self.settings.setValue(QSETTINGS_INPUT_DEVICE, signal.text)

    def set_output_device(self, signal: Signal) -> None:
        self.settings.setValue(QSETTINGS_OUTPUT_DEVICE, signal.text)

    def list_audio_devices(self) -> None:
        devices = sounddevice.query_devices()

        # Nice-to-have: Set default input/output devices to currently used ones if not set
        # input_index, output_index = sounddevice.default.device

        input_devices = []
        output_devices = []

        for i, device in enumerate(devices):
            name = device['name'].strip()
            if device['max_input_channels'] > 0:
                input_devices.append(name)
            if device['max_output_channels'] > 0:
                output_devices.append(name)

        input_signal = Signal(
            item=Items.SETTINGS_INPUT_DEVICE,
            action=Actions.COMBO_SET,
            source=ViewState.ALL,
            data=input_devices
        )

        output_signal = Signal(
            item=Items.SETTINGS_OUTPUT_DEVICE,
            action=Actions.COMBO_SET,
            source=ViewState.ALL,
            data=output_devices
        )

        event_bus.publish(input_signal, output_signal)
