__version__ = "0.6.1"
__author__ = "ZeX2"

from PySide import QtGui, QtCore
from design import MainUi
import sys
import os
from WorldsData import TWData
from datetime import datetime
from CoordExtractor import CoordExtractorDialog
from VillageFinder import VillageFinderDialog
from BacktimingCalculator import BacktimingCalculatorDialog
from FarmThief import FarmThiefDialog
from ServersData import servers
from Functions import modified_time, app_data, resource_path, world_dir, update_needed
from CustomDialogs import ServersDownloadDialog
import collections
import json
import requests

app_data_path = app_data()

class DownloadThread(QtCore.QThread):

    def __init__(self, url):
        QtCore.QThread.__init__(self)
        self.url = url

    def __del__(self):
        self.wait()

    def run(self):
        """
        Villages and players data
        Creates a dict of all players in the world
        """

        """Gets URL from the GUI and adds on the needed extension"""
        world_directory = world_dir(app_data_path, self.url)

        villages_data_path = os.path.join(world_directory, "village.txt.gz")
        players_data_path = os.path.join(world_directory, "player.txt.gz")
        odd_data_path = os.path.join(world_directory, "kill_def.txt.gz")
        config_path = os.path.join(world_directory, "config.xml")

        """Checks for files and downloads them if needed"""
        files_exist = (os.path.isfile(villages_data_path)) and (os.path.isfile(players_data_path)) and (os.path.isfile(config_path)) and (os.path.isfile(odd_data_path))

        if not (files_exist):
            try:
                TWData.download_data(world_directory, self.url)
            except requests.exceptions.ConnectionError:
                error_text = "Please check your internet connection. For further help contact the author."
                self.emit(QtCore.SIGNAL("download_error(PyObject)"), error_text)
                return
            except requests.exceptions.Timeout:
                error_text = "The connection timed out. Please try again.."
                self.emit(QtCore.SIGNAL("download_error(PyObject)"), error_text)
                return
            except requests.exceptions.HTTPError as e:
                print(e)
                error_text = "An invalid HTTP response occured, check your internet connection. For further help contact the author."
                self.emit(QtCore.SIGNAL("download_error(PyObject)"), error_text)
                return
            except requests.exceptions.RequestException as e:
                print(e)
                error_text = "An unknown network error occured, contact the author of the program on the Tribal Wars forums."
                self.emit(QtCore.SIGNAL("download_error(PyObject)"), error_text)
                return
        else:
            villages_modified_time = modified_time(villages_data_path)
            players_modified_time = modified_time(players_data_path)
            odd_modified_time = modified_time(odd_data_path)
            current_time = datetime.now()
            difference1 = current_time - villages_modified_time
            difference2 = current_time - players_modified_time
            difference3 = current_time - odd_modified_time

            two_hours = 7200

            outdated = (difference1.total_seconds() > two_hours) or (difference2.total_seconds() > two_hours) or (difference3.total_seconds() > two_hours)

            if outdated:
                try:
                    TWData.download_data(world_directory, self.url)
                except requests.exceptions.ConnectionError:
                    error_text = "Please check your internet connection. For further help contact the author."
                    self.emit(QtCore.SIGNAL("download_error(PyObject)"), error_text)
                    return
                except requests.exceptions.Timeout:
                    error_text = "The connection timed out. Please try again."
                    self.emit(QtCore.SIGNAL("download_error(PyObject)"), error_text)
                    return
                except requests.exceptions.HTTPError as e:
                    print(e)
                    error_text = "An invalid HTTP response occured, check your internet connection. For further help contact the author."
                    self.emit(QtCore.SIGNAL("download_error(PyObject)"), error_text)
                    return
                except requests.exceptions.RequestException as e:
                    print(e)
                    error_text = "An unknown network error occured, contact the author of the program on the Tribal Wars forums."
                    self.emit(QtCore.SIGNAL("download_error(PyObject)"), error_text)
                    return

        try:
            villages_dict = TWData.get_villages_dict(villages_data_path)
            players_dict = TWData.get_players_dict(players_data_path)
            odd_dict = TWData.get_odd_dict(odd_data_path)
        except:
            error_text = "An unknown error occured. Contact the author if needed."
            self.emit(QtCore.SIGNAL("download_error(PyObject)"), error_text)
            return

        """Emits signal with world data"""
        world_data = [villages_dict, players_dict, odd_dict, config_path]
        self.emit(QtCore.SIGNAL("get_world_data(PyObject)"), world_data)

class Window(QtGui.QMainWindow, MainUi):

    def __init__(self):
        super(Window, self).__init__()
        self.update_message()
        self.servers_dict = {}
        self.serverItems = servers
        self.setupUi()
        self.show()

        self.world_data = None
        self.servers_update()
        self.on_combo_activated(self.serverItems[0])

    def update_message(self):
        if update_needed(__version__):
            QtGui.QMessageBox.information(
                self,
                "A new version is available!",
                "A new version is available. Click <a href='https://forum.tribalwars.net/index.php?threads/zezes-twtools.278433/'>here</a> to update. ")

    def village_finder(self):
        self.dialog = VillageFinderDialog(self, self.world_data)
        self.dialog.show()
        self.hide()

    def coord_extractor(self):
        self.dialog = CoordExtractorDialog(self)
        self.dialog.show()
        self.hide()

    def backtiming_calculator(self):
        if self.world_data != None:
            config = self.world_data[3]
        else:
            config = None
        self.dialog = BacktimingCalculatorDialog(self, config)
        self.dialog.show()
        self.hide()

    def farm_thief(self):
        self.dialog = FarmThiefDialog(self, self.world_data)
        self.dialog.show()
        self.hide()

    def coming_soon(self):
        QtGui.QMessageBox.critical(
            self,
            "Coming Soon",
            "This feature isn't available yet!",
            QtGui.QMessageBox.Ok)

    def on_combo_activated(self, server):
        self.worldBox.clear()
        self.worldBox.addItems(list(self.servers_dict[server].keys()))

    def servers_update(self):
        servers_json_path = os.path.join(app_data_path, "servers.json")
        one_week = 604800

        if not os.path.exists(servers_json_path):
            download_dialog = ServersDownloadDialog(servers_json_path)
            download_dialog.exec_()
        else:
            servers_json_modified_time = modified_time(servers_json_path)
            current_time = datetime.now()
            difference = current_time - servers_json_modified_time

            if difference.total_seconds() > one_week:
                download_dialog = ServersDownloadDialog(servers_json_path)
                download_dialog.exec_()

        self.get_servers_dict()

    def get_servers_dict(self):
        servers_json_path = os.path.join(app_data_path, "servers.json")
        with open(servers_json_path) as f:
            self.servers_dict = json.load(f, object_pairs_hook=collections.OrderedDict)

    def download_function(self):
        self.downloadButton.setEnabled(False)
        self.downloadButton.setText("Downloading....")
        server = self.serverBox.currentText()
        world = self.worldBox.currentText()
        url = self.servers_dict[server][world]

        self.get_download_thread = DownloadThread(url)
        self.connect(self.get_download_thread, QtCore.SIGNAL("get_world_data(PyObject)"), self.get_world_data)
        self.connect(self.get_download_thread, QtCore.SIGNAL("download_error(PyObject)"), self.download_error)
        self.get_download_thread.start()

    def download_error(self, error_text):
        QtGui.QMessageBox.critical(self, "Download Error", error_text)
        self.downloadButton.setText("Download World Data")
        self.downloadButton.setEnabled(True)

    def get_world_data(self, world_data):
        self.world_data = world_data
        self.downloadButton.setEnabled(True)
        self.downloadButton.setText("Download World Data")

def main():
    app = QtGui.QApplication(sys.argv)
    MainWindow = Window()
    app.exec_()

if __name__ == "__main__":
    main()