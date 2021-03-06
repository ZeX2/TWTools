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

from design import VfUi
from WorldsData import TWData
from CustomDesign import Validator
from Functions import resource_path


class GoThread(QtCore.QThread):

    def __init__(self, search_coord, type_, min_points, max_points, min_range, max_range, world_data):
        QtCore.QThread.__init__(self)
        self.search_coord = search_coord
        self.type_ = type_
        self.min_points = min_points
        self.max_points = max_points
        self.min_range = min_range
        self.max_range = max_range
        self.world_data = world_data

    def __del__(self):
        self.wait()

    def run(self):
        """Data obtained from the main window"""
        try:
            villages_data = self.world_data[0]
            players_data = self.world_data[1]
        except TypeError:
            self.emit(QtCore.SIGNAL("no_data_error()"))
            return

        filtered_by_type = None
        filtered_by_points = None
        filtered_by_range = {}

        """Filers by village type"""
        if self.type_ == 1:
            filtered_by_type = {key: value for key, value in villages_data.items() if int(value[4]) == 0}
        elif self.type_ == 0:
            filtered_by_type = {key: value for key, value in villages_data.items() if int(value[4]) > 0}
        else:
            filtered_by_type = villages_data
        villages_data = None

        """Filters by points"""
        filtered_by_points = {key: value for key, value in filtered_by_type.items() if int(value[5]) >= int(self.min_points) and int(value[5]) <= int(self.max_points)}
        filtered_by_type = None

        """Filters by range"""
        search_coord = self.search_coord.split("|")
        search_x = search_coord[0]
        search_y = search_coord[1]

        for key, value in filtered_by_points.items():
            village_x = value[2]
            village_y = value[3]

            x = int(village_x) - int(search_x)
            y = int(village_y) - int(search_y)

            actual_max_range_squared = (x ** 2) + (y ** 2)

            actual_range = math.sqrt(actual_max_range_squared)

            if int(actual_range) <= int(self.max_range) and int(actual_range) >= int(self.min_range):
                filtered_by_range[key] = value
        filtered_by_points = None

        """Adds player names"""
        table_data = []
        if self.type_ == 1:
            for key, value in filtered_by_range.items():
                coord = value[2] + "|" + value[3]
                points = value[5]
                table_data.append(["", "Barbarian village", coord, points])
        else:
            for key, value in filtered_by_range.items():
                player_id = int(value[4])
                player_name = ""

                if player_id != 0:
                    player_data = players_data[player_id]
                    player_name = player_data[1]

                village_name = value[1]
                coord = value[2] + "|" + value[3]
                points = value[5]

                table_data.append([player_name, village_name, coord, points])

        """Emits data for the table"""
        self.emit(QtCore.SIGNAL("get_gui_data(PyObject)"), table_data)


class TableThread(QtCore.QThread):

    def __init__(self, table_data):
        QtCore.QThread.__init__(self)
        self.table_data = table_data

    def __del__(self):
        self.wait()

    def run(self):
        self.emit(QtCore.SIGNAL("reset_rows()"))

        for row in self.table_data:
            self.emit(QtCore.SIGNAL("update_table(PyObject)"), row)

        self.emit(QtCore.SIGNAL("get_coords_data(PyObject)"), self.table_data)


class CoordsThread(QtCore.QThread):

    def __init__(self, table_data, option, number, player, points):
        QtCore.QThread.__init__(self)
        self.table_data = table_data
        self.option = option
        self.number = number
        self.player = player
        self.points = points

    def __del__(self):
        self.wait()

    def run(self):
        """table_data = [player_name, village_name, coord, points]"""
        coord_chunks = []

        n = 1
        for village in self.table_data:
            player_name = village[0]
            village_name = village[1]
            coord = village[2]
            points = village[3]

            if self.option == 1:
                village_data_chunks = []

                if self.number:
                    village_data_chunks.append("[b]" + str(n) + "." + "[/b]")
                    n += 1

                village_data_chunks.append(coord)

                if self.player:
                    if player_name == "":
                        village_data_chunks.append("- " + "Barbarian")
                    else:
                        village_data_chunks.append(
                            "- " + "[player]" + player_name + "[/player]")

                if self.points:
                    village_data_chunks.append("- " + str(points))

                village_data = " ".join(village_data_chunks)
                coord_chunks.append(village_data)
            else:
                coord_chunks.append(coord)

        """Converts coord_chunks list into a string"""
        coords = ""
        if self.option == 1:
            coords = "\n".join(coord_chunks)
        else:
            coords = " ".join(coord_chunks)

        self.emit(QtCore.SIGNAL("update_coords(PyObject)"), coords)


class VillageFinderDialog(QtWidgets.QDialog, VfUi, Validator):

    def __init__(self, other_window, world_data):
        super(VillageFinderDialog, self).__init__()
        self.world_data = world_data
        self.other_window = other_window
        self.gui_data = None
        self.setupUi()

        self.searchEdit.textChanged.connect(self.check_coord_state)

        self.min_pointsEdit.setValidator(self.points_validator())
        self.min_pointsEdit.textChanged.connect(self.check_points_state)
        self.max_pointsEdit.setValidator(self.points_validator())
        self.max_pointsEdit.textChanged.connect(self.check_points_state)

    def go_function(self):
        self.goButton.setEnabled(False)

        search_coord = self.searchEdit.text()
        filter_ = self.filterBox.currentIndex()
        min_points = self.min_pointsEdit.text()
        max_points = self.max_pointsEdit.text()
        min_range = self.min_rangeEdit.text()
        max_range = self.max_rangeEdit.text()

        coord_pattern = re.compile("\d{3}\|\d{3}")
        coord_validity = coord_pattern.match(search_coord)

        if self.world_data is None:
            self.no_data_error()
            return

        if coord_validity is None:
            QtWidgets.QMessageBox.critical(
                self,
                "Search Around Error",
                "Please enter a valid coordinate such as 556|494",
                QtWidgets.QMessageBox.Ok)
            self.goButton.setEnabled(True)
            return

        try:
            if int(min_points) < 0 or int(max_points) < 0:
                QtWidgets.QMessageBox.critical(
                    self,
                    "Points Error",
                    "Please enter a number greater than or equal to 0.",
                    QtWidgets.QMessageBox.Ok)
                self.goButton.setEnabled(True)
                return
        except ValueError:
            QtWidgets.QMessageBox.critical(
                self,
                "Points Error",
                "Please enter a valid number",
                QtWidgets.QMessageBox.Ok)
            self.goButton.setEnabled(True)
            return

        try:
            if int(min_range) < 0 or int(max_range) < 0:
                QtWidgets.QMessageBox.critical(
                    self,
                    "Range Error",
                    "Please enter a number greater than or equal to 0.",
                    QtWidgets.QMessageBox.Ok)
                self.goButton.setEnabled(True)
                return
        except ValueError:
            QtWidgets.QMessageBox.critical(
                self,
                "Range Error",
                "Please enter a valid number",
                QtWidgets.QMessageBox.Ok)
            self.goButton.setEnabled(True)
            return

        self.get_go_thread = GoThread(search_coord, filter_, min_points, max_points, min_range, max_range, self.world_data)
        self.connect(self.get_go_thread, QtCore.SIGNAL("get_gui_data(PyObject)"), self.get_gui_data)
        self.connect(self.get_go_thread, QtCore.SIGNAL("no_data_error()"), self.no_data_error)
        self.get_go_thread.start()

    def get_gui_data(self, gui_data):
        self.gui_data = gui_data
        self.table_function()

    def table_function(self):
        self.get_table_thread = TableThread(self.gui_data)
        self.connect(self.get_table_thread, QtCore.SIGNAL("update_table(PyObject)"), self.update_table)
        self.connect(self.get_table_thread, QtCore.SIGNAL("reset_rows()"), self.reset_rows)
        self.connect(self.get_table_thread, QtCore.SIGNAL("get_coords_data(PyObject)"), self.get_coords_data)
        self.get_table_thread.start()

    def get_coords_data(self):
        if self.gui_data is None:
            return

        option = None
        if self.listRadio.isChecked():
            option = 1
        else:
            option = 0

        number = self.numberCheck.isChecked()
        player = self.playerCheck.isChecked()
        points = self.pointsCheck.isChecked()

        self.get_coords_thread = CoordsThread(self.gui_data, option, number, player, points)
        self.connect(self.get_coords_thread, QtCore.SIGNAL("update_coords(PyObject)"), self.update_coords)
        self.get_coords_thread.start()

    def reset_rows(self):
        self.tableWidget.setRowCount(0)
        self.tableWidget.setUpdatesEnabled(False)

    def update_table(self, row):
        rowPosition = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowPosition)

        player = row[0]
        name = row[1]
        coord = row[2]
        points = int(row[3])

        self.tableWidget.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(player))
        self.tableWidget.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(name))
        self.tableWidget.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(coord))

        points_item = QtWidgets.QTableWidgetItem()
        points_item.setData(QtCore.Qt.DisplayRole, points)
        self.tableWidget.setItem(rowPosition, 3, points_item)

    def update_coords(self, coords):
        self.tableWidget.setUpdatesEnabled(True)
        self.coordsEdit.setText(coords)
        self.goButton.setEnabled(True)

    def no_data_error(self):
        QtWidgets.QMessageBox.critical(
            self,
            "World Data Error",
            "There is no world data! Please return to the main window and download the world data.",
            QtWidgets.QMessageBox.Ok)
        self.goButton.setEnabled(True)

    def plain_function(self):
        pass

    def list_options_toggle(self, state):
        self.formWidget.setVisible(not state)

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