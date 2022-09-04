from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
import datetime
import sys

class DigitalClock():
    def __init__(self, date, time):
        self.labelClockDate = date
        self.labelClockTime = time
    
    def redrawClock(self):
        now = datetime.datetime.now()
        self.labelClockDate.setText(f"{now.day:02d}/{now.month:02d}/{now.year}")
        self.labelClockTime.setText(f"{now.hour:02d}:{now.minute:02d}")
