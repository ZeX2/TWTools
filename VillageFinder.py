from PySide import QtGui, QtCore
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
from Data import TWData
from Data import Files
from CustomDesign import Validator

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
		coord_chunks = []
		if self.type_ == 1:
			for key, value in filtered_by_range.items():
				coord = value[2] + "|" + value[3]
				points = value[5]
				table_data.append(["", "Barbarian village", coord, points])
				coords = coords + coord + " "
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
				coord_chunks.append(coord)
		coords = " ".join(coord_chunks)

		"""Emits data for the table"""
		gui_data = [table_data, coords]
		self.emit(QtCore.SIGNAL("get_gui_data(PyObject)"), gui_data)

class TableThread(QtCore.QThread):
	def __init__(self, gui_data):
		QtCore.QThread.__init__(self)
		self.table_data = gui_data[0]
		self.coords = gui_data[1]

	def __del__(self):
		self.wait()

	def run(self):
		self.emit(QtCore.SIGNAL("reset_rows()"))
		
		for row in self.table_data:
			self.emit(QtCore.SIGNAL("update_table(PyObject)"), row)

		self.emit(QtCore.SIGNAL("update_coords(PyObject)"), self.coords)

class VillageFinderDialog(QtGui.QDialog, VfUi, Validator):
	def __init__(self, other_window, world_data):
		super(VillageFinderDialog, self).__init__()
		self.setGeometry(50, 50, 850, 425)
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		self.setWindowTitle("ZeZe's TWTools")
		self.setWindowIcon(QtGui.QIcon(Files.resource_path("images/icon.png")))
		self.world_data = world_data
		self.other_window = other_window
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

		if self.world_data == None:
			self.no_data_error()
			return

		if coord_validity == None:
			QtGui.QMessageBox.critical(self, "Search Around Error", "Please enter a valid coordinate such as 556|494", QtGui.QMessageBox.Ok)
			self.goButton.setEnabled(True)
			return

		try:
			if int(min_points) < 0 or int(max_points) < 0:
				QtGui.QMessageBox.critical(self, "Points Error", "Please enter a number greater than or equal to 0.", QtGui.QMessageBox.Ok)
				self.goButton.setEnabled(True)
				return
		except ValueError:
			QtGui.QMessageBox.critical(self, "Points Error", "Please enter a valid number", QtGui.QMessageBox.Ok)
			self.goButton.setEnabled(True)
			return

		try:
			if int(min_range) < 0 or int(max_range) < 0:
				QtGui.QMessageBox.critical(self, "Range Error", "Please enter a number greater than or equal to 0.", QtGui.QMessageBox.Ok)
				self.goButton.setEnabled(True)
				return
		except ValueError:
			QtGui.QMessageBox.critical(self, "Range Error", "Please enter a valid number", QtGui.QMessageBox.Ok)
			self.goButton.setEnabled(True)
			return

		self.get_go_thread = GoThread(search_coord, filter_, min_points, max_points, min_range, max_range, self.world_data)
		self.connect(self.get_go_thread, QtCore.SIGNAL("get_gui_data(PyObject)"), self.get_gui_data)
		self.connect(self.get_go_thread, QtCore.SIGNAL("no_data_error()"), 	self.no_data_error)
		self.get_go_thread.start()


	def get_gui_data(self, gui_data):
		self.get_table_thread = TableThread(gui_data)
		self.connect(self.get_table_thread, QtCore.SIGNAL("update_coords(PyObject)"), self.update_coords)
		self.connect(self.get_table_thread, QtCore.SIGNAL("update_table(PyObject)"), self.update_table)
		self.connect(self.get_table_thread, QtCore.SIGNAL("reset_rows()"), self.reset_rows)
		self.get_table_thread.start()

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

		self.tableWidget.setItem(rowPosition , 0, QtGui.QTableWidgetItem(player))
		self.tableWidget.setItem(rowPosition , 1, QtGui.QTableWidgetItem(name))
		self.tableWidget.setItem(rowPosition , 2, QtGui.QTableWidgetItem(coord))

		points_item = QtGui.QTableWidgetItem()
		points_item.setData(QtCore.Qt.DisplayRole, points)
		self.tableWidget.setItem(rowPosition, 3, points_item)

	def update_coords(self, coords):
		self.tableWidget.setUpdatesEnabled(True)
		self.coordsEdit.setText(coords)
		self.goButton.setEnabled(True)

	def no_data_error(self):
		QtGui.QMessageBox.critical(self, "World Data Error", "There is no world data! Please return to the main window and download the world data.", QtGui.QMessageBox.Ok)
		self.goButton.setEnabled(True)

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