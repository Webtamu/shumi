from PyQt6.QtCore import QThread, pyqtSignal
import time
import datetime

from helpers.signals import Signal
from helpers.helpers import Items, ViewState, Actions


class Timer(QThread):
    theTimerSignal = pyqtSignal(Signal)
    theTimeModelSignal = pyqtSignal(Signal)

    def __init__(self, aTimeLimit: int) -> None:
        super(Timer, self).__init__()
        self.theTimeLimit = aTimeLimit
        self.isRunning = True  
        self.theStartTime = None
        self.stopTime = None
        

    def run(self) -> None:
        self.theStartTime = datetime.datetime.utcnow()
        i = self.theTimeLimit
        while i >= 0 and self.isRunning:
            self.theTimerSignal.emit(Signal(theText=str(i), 
                                            theItem=Items.TIMER,
                                            theActionType=Actions.LABEL_SET,
                                            theSource=ViewState.SESSION))
            time.sleep(1)
            i -= 1

        
        self.theTimerSignal.emit(Signal(theItem=Items.STOP,
                                        theActionType=Actions.LABEL_SET,
                                        theSource=ViewState.SESSION,
                                        theData=[]))

        


    def stop(self):
        self.theStopTime = datetime.datetime.utcnow()
        self.isRunning = False 

