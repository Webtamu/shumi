import cv2
from PyQt6 import uic
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QImage, QPixmap

from ..views import View
from ..helpers import Items, Actions, ViewState
from PyQt6.QtWidgets import QPushButton, QPlainTextEdit, QLabel


class SummaryView(View):
    def setup(self) -> None:
        self.view_state = ViewState.SUMMARY
        self.window = uic.loadUi("app/frontend/qtdesigner/summary_design.ui")

        self.item_map = {
            Items.BEGIN_TAKE: {
                "instance": self.window.findChild(QPushButton, "btnBeginTake"),
                "action": Actions.BTN_PRESS
            },
            Items.SUMMARY_NOTES: {
                "instance": self.window.findChild(QPlainTextEdit, "editNotes"),
                "action": Actions.NONE
            }
        }

        self.video_label = self.window.findChild(QLabel, "videoLabel")
        self.cap = cv2.VideoCapture(0)  # 0 = default webcam

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # ~30 FPS

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            qt_img = QImage(frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_img)
            self.video_label.setPixmap(pixmap.scaled(
                self.video_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            ))

    def close(self):
        self.cap.release()
        self.timer.stop()
