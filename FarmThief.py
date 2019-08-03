from PySide2 import QtGui, QtCore, QtWidgets
from io import BytesIO
import urllib.request
import urllib.parse
import gzip

import os
import sys
import math
import re
import time

from design import FtUi
from WorldsData import TWData
from CustomDesign import Validator
from Functions import resource_path

class FarmThiefDialog(QtWidgets.QDialog, FtUi):

    def __init__(self, other_window, world_data):
        super(FarmThiefDialog, self).__init__()
        self.world_data = world_data
        self.other_window = other_window
        self.setupUi()

    def closeEvent(self, event):
        self.other_window.show()
        event.accept()

    def showEvent(self, event):
        geom = self.frameGeometry()
        geom.moveCenter(QtGui.QCursor.pos())
        self.setGeometry(geom)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.return_function()
            event.accept()

    def return_function(self):
        self.other_window.show()
        self.close()