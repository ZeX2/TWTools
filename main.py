__version__ = "0.5"
__author__ = "ZeX2"

from PySide import QtGui, QtCore
from design import MainUi
import sys
import os
from Data import Files, TWData, Config_XML
from datetime import datetime
from CoordExtractor import CoordExtractorDialog
from VillageFinder import VillageFinderDialog
from BacktimingCalculator import BacktimingCalculatorDialog

class DownloadThread(QtCore.QThread):
	def __init__(self, url):
		QtCore.QThread.__init__(self)
		self.url = url

	def __del__(self):
		self.wait()

	def run(self):
		"""
		Villages and players data
		Gets URL from the GUI and adds on the needed extension
		Gets the villages and players data
		Creates a dict of all players in the world
		"""

		app_data_path = Files.app_data_path()
		directory = Files.make_data_dir(app_data_path, self.url)

		villages_data = directory + "\\" + "village.txt.gz"
		players_data = directory + "\\" + "player.txt.gz"
		config = directory + "\\" + "config.xml"

		two_hours = 7200

		if not (os.path.isfile(villages_data) and os.path.isfile(players_data)):
			try:
				TWData.download_data(directory, self.url)
			except:
				self.emit(QtCore.SIGNAL("download_error()"))
				return
		else:
			villages_modified_time = Files.modified_time(villages_data)
			players_modified_time = Files.modified_time(players_data)
			current_time = datetime.now()
			difference1 = current_time - villages_modified_time
			difference2 = current_time - players_modified_time

			if difference1.seconds > two_hours or difference2.seconds > two_hours:
				try:
					TWData.download_data(directory, self.url)
				except:
					self.emit(QtCore.SIGNAL("download_error()"))
					return

		try:
			villages_dict = TWData.get_villages_dict(villages_data)
			players_dict = TWData.get_players_dict(players_data)
		except:
			self.emit(QtCore.SIGNAL("download_error()"))
			return

		"""Emits signal with world data"""
		world_data = [villages_dict, players_dict, config]
		self.emit(QtCore.SIGNAL("get_world_data(PyObject)"), world_data)

class Window(QtGui.QMainWindow, MainUi):
	def __init__(self):
		super(Window, self).__init__()
		self.setWindowTitle("ZeZe's TWTools")
		self.setWindowIcon(QtGui.QIcon(Files.resource_path("images/icon.png")))
		self.serverItems = Config_XML.server_box_items(Files.resource_path("config.xml"))
		self.worldItems = Config_XML.world_box_items(Files.resource_path("config.xml"))

		self.setupUi()
		self.on_combo_activated(self.serverItems[0])
		self.app_data_folder()
		self.world_data = None

		self.show()

	def app_data_folder(self):
		directory = Files.app_data_path()
		if not os.path.exists(directory):
			os.makedirs(directory)

	def village_finder(self):
		self.hide()
		self.dialog = VillageFinderDialog(self, self.world_data)
		self.dialog.show()

	def coord_extractor(self):
		self.dialog = CoordExtractorDialog(self)
		self.dialog.show()
		self.hide()

	def backtiming_calculator(self):
		try:
			config = self.world_data[2]
		except:
			config = None
		self.dialog = BacktimingCalculatorDialog(self, config)
		self.dialog.show()
		self.hide()

	def coming_soon(self):
		QtGui.QMessageBox.critical(self, "Coming Soon", "This feature isn't available yet!", QtGui.QMessageBox.Ok)

	def on_combo_activated(self, server):
		self.worldBox.clear()
		self.worldBox.addItems(self.worldItems[server])

	def download_function(self):
		self.downloadButton.setEnabled(False)
		server = self.serverBox.currentText()
		world = Config_XML.get_world_url(Files.resource_path("config.xml"), server , self.worldBox.currentText())
		url = "https://" + world + "." + server

		self.get_download_thread = DownloadThread(url)
		self.connect(self.get_download_thread, QtCore.SIGNAL("get_world_data(PyObject)"), self.get_world_data)
		self.connect(self.get_download_thread, QtCore.SIGNAL("download_error()"), self.download_error)
		self.get_download_thread.start()

	def download_error(self):
		QtGui.QMessageBox.critical(self, "Download Error", "Please check your internet connection and try again.")
		self.downloadButton.setEnabled(True)

	def get_world_data(self, world_data):
		self.world_data = world_data
		self.downloadButton.setEnabled(True)

def main():
	app = QtGui.QApplication(sys.argv)
	MainWindow = Window()
	app.exec_()

if __name__ == "__main__":
	main()