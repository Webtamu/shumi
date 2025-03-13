from PyQt6.QtCore import QThread, pyqtSignal
import time

from helpers.signals import Signal
from helpers.helpers import Items, ViewState, Actions

class Timer(QThread):
    theTimerSignal = pyqtSignal(Signal)

    def __init__(self, aTimeLimit: int) -> None:
        super(Timer, self).__init__()
        self.theTimeLimit = aTimeLimit
        self.isRunning = True  

    def run(self) -> None:
        i = self.theTimeLimit
        while i >= 0 and self.isRunning:
            self.theTimerSignal.emit(Signal(theText=str(i), 
                                            theItem=Items.TIMER,
                                            theActionType=Actions.LABEL_SET,
                                            theSource=ViewState.SESSION))
            time.sleep(1)
            i -= 1
        if self.isRunning:  
            self.theTimerSignal.emit(Signal(theItem=Items.STOP,
                                            theActionType=Actions.LABEL_SET,
                                            theSource=ViewState.SESSION))

    def stop(self):
        self.isRunning = False 
