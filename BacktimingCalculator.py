from PySide2 import QtGui, QtCore, QtWidgets
import sys
import math
import datetime
import time
import re

from design import BcUi
from CustomDesign import Validator
from CustomDialogs import SpeedInputDialog
from Functions import resource_path
from WorldsData import TWData

class BacktimeThread(QtCore.QThread):
	def __init__(self, world_speed, unit_speed, origin, destination, unit, arrival):
		QtCore.QThread.__init__(self)
		self.world_speed = world_speed
		self.unit_speed = unit_speed
		self.origin = origin
		self.destination = destination
		self.unit = unit
		self.arrival = arrival

	def __del__(self):
		self.wait()

	def run(self):
		speed_dict = {0: 18, 1:22, 2:18, 3:18, 4: 9, 5: 10, 6: 10, 7: 11, 8: 30, 9: 30, 10: 10, 11: 35}
		speed = speed_dict[self.unit]
		one_field_speed = speed * (1 / float(self.unit_speed)) * (1 / float(self.world_speed))
		
		origin = self.origin.split("|")
		origin_x = origin[0]
		origin_y = origin[1]

		destination = self.destination.split("|")
		destination_x = destination[0]
		destination_y = destination[1]

		x = int(origin_x) - int(destination_x)
		y = int(origin_y) - int(destination_y)

		max_range_squared = (x ** 2) + (y ** 2)
		range_ = math.sqrt(max_range_squared)

		minutes = range_ * one_field_speed
		rounded_seconds = round(minutes * 60)

		travel_time = datetime.timedelta(seconds = rounded_seconds)
		arrival_time = self.arrival.toPython()

		backtime = arrival_time + travel_time
		
		data = [backtime, self.origin]
		self.emit(QtCore.SIGNAL("update_backtime(PyObject)"), data)

class BacktimingCalculatorDialog(QtWidgets.QDialog, BcUi, Validator):
	def __init__(self, other_window, config):
		super(BacktimingCalculatorDialog, self).__init__()
		self.other_window = other_window
		self.config = config
		self.setupUi()

		self.originEdit.textChanged.connect(self.check_coord_state)
		self.destinationEdit.textChanged.connect(self.check_coord_state)

		self.world_speed = 1
		self.unit_speed = 1
		self.update_speed_labels()

	def manual_function(self, enabled):
		if enabled:
			input_dialog = SpeedInputDialog()
			if input_dialog.exec_():
				self.world_speed, self.unit_speed = input_dialog.get_data()
				self.update_speed_labels()

	def selected_function(self, enabled):
		if enabled:
			if self.config != None:
				speeds = TWData.get_speed_data(self.config)
				self.world_speed = speeds[0]
				self.unit_speed = speeds[1]
				self.update_speed_labels()

	def update_speed_labels(self):
		self.world_speedLabel.setText("World Speed: " + str(self.world_speed))
		self.unit_speedLabel.setText("Unit Speed: " + str(self.unit_speed))

	def backtime_function(self):
		if ((self.world_speed == 0) and (self.unit_speed == 0)):
			print("asdasd")
			return

		origin_coord = self.originEdit.text()
		destination_coord = self.destinationEdit.text()

		coord_pattern = re.compile("\d{3}\|\d{3}")
		origin_validity = coord_pattern.match(origin_coord)
		destination_validity = coord_pattern.match(destination_coord)

		if ((destination_validity is None) or (origin_validity is None)):
			QtWidgets.QMessageBox.critical(
                self,
                "Search Around Error",
                "Please enter a valid coordinate such as 556|494",
                QtWidgets.QMessageBox.Ok)
			self.calculateButton.setEnabled(True)
			return

		self.calculateButton.setEnabled(False)

		world_speed = self.world_speed
		unit_speed = self.unit_speed
		origin = self.originEdit.text()
		destination = self.destinationEdit.text()
		unit = self.unitBox.currentIndex()
		arrival = self.arrivalEdit.dateTime()

		self.get_backtime_thread = BacktimeThread(world_speed, unit_speed, origin, destination, unit, arrival)
		self.connect(self.get_backtime_thread, QtCore.SIGNAL("update_backtime(PyObject)"), self.update_backtime)
		self.get_backtime_thread.start()

	def update_backtime(self, data):
		backtime = data[0]
		origin = data[1]
	
		text = "The troops return to " + origin + " at " + backtime.strftime("%Y-%m-%d %H:%M:%S")
		self.backtimeEdit.setText(text)

		self.calculateButton.setEnabled(True)

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