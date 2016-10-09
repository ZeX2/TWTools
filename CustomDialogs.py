from PySide import QtGui, QtCore
from design import SidUi, DdUi
from ServersData import ServersDownloadThread
import sys

class SpeedInputDialog(QtGui.QDialog, SidUi):
    
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi()

    def get_data(self):
        self.accept()
        return self.world_speedBox.value(), self.unit_speedBox.value()

    def showEvent(self, event):
        geom = self.frameGeometry()
        geom.moveCenter(QtGui.QCursor.pos())
        self.setGeometry(geom)


class ServersDownloadDialog(QtGui.QDialog, DdUi):

    def __init__(self, servers_json_path):
        QtGui.QDialog.__init__(self)
        self.downloaded = False
        self.setupUi()
        self.servers_json_path = servers_json_path
        self.servers_download_function()

    def servers_download_function(self):
        self.get_servers_download_thread = ServersDownloadThread(self.servers_json_path)
        self.connect(self.get_servers_download_thread, QtCore.SIGNAL("update_progress_text(PyObject)"), self.update_progress_text)
        self.connect(self.get_servers_download_thread, QtCore.SIGNAL("update_progress_bar(PyObject)"), self.update_progress_bar)
        self.connect(self.get_servers_download_thread, QtCore.SIGNAL("update_button()"), self.update_button)
        self.connect(self.get_servers_download_thread, QtCore.SIGNAL("download_error(PyObject)"), self.download_error)
        self.get_servers_download_thread.start()

    def update_progress_text(self, text):
        self.progress_text.append(text)
    
    def update_progress_bar(self, value):
        self.progress_bar.setValue(value)

    def update_button(self):
        self.horizontalLayout.removeWidget(self.cancelButton)
        self.cancelButton.deleteLater()
        self.cancelButton = None

        self.downloaded = True

        self.okButton = QtGui.QPushButton("Ok")
        self.horizontalLayout.addWidget(self.okButton)
        self.okButton.clicked.connect(self.ok_function)

    def cancel_function(self):
        reply = QtGui.QMessageBox.question(self, 'Message', 
                        "Are you sure that you want to cancel downloading? This will exit the program.", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            sys.exit()
        
    def closeEvent(self, event):
        if self.downloaded:
            return event.accept()

        reply = QtGui.QMessageBox.question(self, 'Message', 
                        "The server config with the worlds is downloading, would you like to exit the program anyway?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
            sys.exit()
        else:
            event.ignore()

    def ok_function(self):
        self.close()

    def download_error(self, error_text):
        QtGui.QMessageBox.critical(self, "Download Error", error_text)
        sys.exit()