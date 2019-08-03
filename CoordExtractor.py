from PySide2 import QtGui, QtCore, QtWidgets
import sys
import re

from design import CeUi
from Functions import resource_path

class ExtractThread(QtCore.QThread):

    def __init__(self, text):
        QtCore.QThread.__init__(self)
        self.text = text

    def __del__(self):
        self.wait()

    def run(self):
        coord_pattern = re.compile("\d{3}\|\d{3}")
        coords_list = list(set(re.findall(coord_pattern, self.text)))
        coords_string = ""
        for coord in coords_list:
            coords_string = coords_string + coord + " "

        coords_string = coords_string[:-1]
        self.emit(QtCore.SIGNAL("get_coords(PyObject)"), coords_string)


class CoordExtractorDialog(QtWidgets.QDialog, CeUi):

    def __init__(self, other_window):
        super(CoordExtractorDialog, self).__init__()
        self.other_window = other_window
        self.setupUi()

    def extract_function(self):
        self.extractButton.setEnabled(False)
        text = self.plainTextEdit.toPlainText()
        self.get_extract_thread = ExtractThread(text)
        self.connect(self.get_extract_thread, QtCore.SIGNAL("get_coords(PyObject)"), self.get_coords)
        self.get_extract_thread.start()

    def get_coords(self, coords):
        self.plainTextEdit_2.clear()
        self.plainTextEdit_2.insertPlainText(coords)
        self.extractButton.setEnabled(True)

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