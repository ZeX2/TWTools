from PySide import QtGui, QtCore
import os
from Data import Files, Config_XML
from CustomDesign import PicButton

class MainUi(object):
	def setupUi(self):
		"""Background color"""
		self.backgroundPalette = QtGui.QPalette()
		#color = QtGui.QColor(217, 204, 170)
		self.backgroundColor = QtGui.QColor(238, 217, 174)
		self.backgroundPalette.setColor(QtGui.QPalette.Background, self.backgroundColor)
		self.setPalette(self.backgroundPalette)

		self.centralwidget = QtGui.QWidget(self)
		self.setCentralWidget(self.centralwidget)
		self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)

		"""Spacer to the left"""
		self.leftSpacer = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
		self.horizontalLayout.addItem(self.leftSpacer)

		"""Main content"""
		self.verticalLayout = QtGui.QVBoxLayout()
		self.horizontalLayout.addLayout(self.verticalLayout)

		"""Main text picture"""
		self.horizontalLayout_1 = QtGui.QHBoxLayout()
		self.logo_textScene = QtGui.QGraphicsScene()
		self.logo_textScene.addPixmap(QtGui.QPixmap(Files.resource_path("images/logo_text.png")))
		self.logo_textView = QtGui.QGraphicsView(self.logo_textScene, self.centralwidget)
		self.logo_textView.setFixedSize(565, 175)
		self.logo_textView.setStyleSheet("border: 0px; background-color: transparent;")

		self.horizontalLayout_1.addWidget(self.logo_textView)
		self.verticalLayout.addLayout(self.horizontalLayout_1)

		self.mainSpacer = QtGui.QSpacerItem(50, 50, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
		self.verticalLayout.addItem(self.mainSpacer)

		"""Download options"""
		self.downloadGrid = QtGui.QGridLayout(self.centralwidget)
		self.serverLabel = QtGui.QLabel("Tribal Wars Servers", self.centralwidget)
		self.serverBox = QtGui.QComboBox(self.centralwidget)

		self.serverBox.addItems(self.serverItems)
		self.serverBox.activated[str].connect(self.on_combo_activated)

		self.worldLabel = QtGui.QLabel("Worlds", self.centralwidget)
		self.worldBox = QtGui.QComboBox(self.centralwidget)

		self.downloadButton = QtGui.QPushButton("Download World Data", self.centralwidget)
		self.downloadButton.clicked.connect(self.download_function)

		self.downloadGrid.addWidget(self.serverLabel, 1, 1)
		self.downloadGrid.addWidget(self.serverBox, 2, 1)
		self.downloadGrid.addWidget(self.worldLabel, 1, 2)
		self.downloadGrid.addWidget(self.worldBox, 2, 2)
		self.downloadGrid.addWidget(self.downloadButton, 2, 3)

		self.verticalLayout.addLayout(self.downloadGrid)

		"""Spacer line"""
		self.lineSpacer = QtGui.QSpacerItem(50, 50, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
		self.verticalLayout.addItem(self.lineSpacer)

		"""Options row"""
		self.horizontalLayout_3 = QtGui.QHBoxLayout()
		self.verticalLayout.addLayout(self.horizontalLayout_3)

		self.vfButton = PicButton(QtGui.QPixmap(Files.resource_path("images/village_finder.png")), QtGui.QPixmap(Files.resource_path("images/village_finder.png")), QtGui.QPixmap(Files.resource_path("images/village_finder.png")))
		self.vfButton.clicked.connect(self.village_finder)
		self.horizontalLayout_3.addWidget(self.vfButton)

		self.spacer = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
		self.horizontalLayout_3.addItem(self.spacer)

		self.ceButton = PicButton(QtGui.QPixmap(Files.resource_path("images/coordinates_extractor.png")), QtGui.QPixmap(Files.resource_path("images/coordinates_extractor.png")), QtGui.QPixmap(Files.resource_path("images/coordinates_extractor.png")))
		self.ceButton.clicked.connect(self.coord_extractor)
		self.horizontalLayout_3.addWidget(self.ceButton)

		self.spacer_1 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
		self.horizontalLayout_3.addItem(self.spacer_1)

		self.bcButton = PicButton(QtGui.QPixmap(Files.resource_path("images/backtiming_calculator.png")), QtGui.QPixmap(Files.resource_path("images/backtiming_calculator.png")), QtGui.QPixmap(Files.resource_path("images/backtiming_calculator.png")))
		self.bcButton.clicked.connect(self.backtiming_calculator)
		self.horizontalLayout_3.addWidget(self.bcButton)

		"""Spacer buttons"""
		self.spacer_buttons = QtGui.QSpacerItem(5, 5, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
		self.verticalLayout.addItem(self.spacer_buttons)

		"""Options row 2"""
		self.horizontalLayout_4 = QtGui.QHBoxLayout()
		self.verticalLayout.addLayout(self.horizontalLayout_4)

		self.ftButton = PicButton(QtGui.QPixmap(Files.resource_path("images/farm_thief.png")), QtGui.QPixmap(Files.resource_path("images/farm_thief.png")), QtGui.QPixmap(Files.resource_path("images/farm_thief.png")))
		self.ftButton.clicked.connect(self.coming_soon)
		self.horizontalLayout_4.addWidget(self.ftButton)

		self.spacer_2 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
		self.horizontalLayout_4.addItem(self.spacer_2)

		self.vpButton = PicButton(QtGui.QPixmap(Files.resource_path("images/village_planner.png")), QtGui.QPixmap(Files.resource_path("images/village_planner.png")), QtGui.QPixmap(Files.resource_path("images/village_planner.png")))
		self.vpButton.clicked.connect(self.coming_soon)
		self.horizontalLayout_4.addWidget(self.vpButton)

		self.spacer_3 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
		self.horizontalLayout_4.addItem(self.spacer_3)

		self.eButton = PicButton(QtGui.QPixmap(Files.resource_path("images/empty.png")), QtGui.QPixmap(Files.resource_path("images/empty.png")), QtGui.QPixmap(Files.resource_path("images/empty.png")))
		self.horizontalLayout_4.addWidget(self.eButton)

		"""Spacer2 to the right"""
		self.horizontalSpacer_2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
		self.horizontalLayout.addItem(self.horizontalSpacer_2)

class VfUi(object):
	def setupUi(self):
		"""Set background color"""
		self.backgroundPalette = QtGui.QPalette()
		self.backgroundColor = QtGui.QColor(217, 204, 170)
		self.backgroundPalette.setColor(QtGui.QPalette.Background, self.backgroundColor)
		self.setPalette(self.backgroundPalette)

		"""Layout for dialog"""
		self.verticalLayout = QtGui.QVBoxLayout(self)

		"""Return button"""
		self.buttonLayout = QtGui.QHBoxLayout(self)
		self.verticalLayout.addLayout(self.buttonLayout)
		self.returnButton = QtGui.QPushButton("  Return to the Main Menu  ", self)
		self.returnButton.clicked.connect(self.return_function)
		self.buttonLayout.addWidget(self.returnButton)
		self.buttonSpacer = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
		self.buttonLayout.addItem(self.buttonSpacer)

		"""Line Spacer and line"""
		self.lineSpacer = QtGui.QSpacerItem(40, 5, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
		self.verticalLayout.addItem(self.lineSpacer)
		self.line = QtGui.QFrame(self)
		self.line.setFrameShape(QtGui.QFrame.HLine)
		self.line.setFrameShadow(QtGui.QFrame.Sunken)
		self.verticalLayout.addWidget(self.line)

		"""Layout for form and table"""
		self.horizontalLayout = QtGui.QHBoxLayout()
		self.verticalLayout.addLayout(self.horizontalLayout)

		"""Layout for form"""
		self.formLayout = QtGui.QFormLayout()
		self.horizontalLayout.addLayout(self.formLayout)
		#self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)

		"""Search around Form[0]"""
		self.searchLabel = QtGui.QLabel("Search around", self)
		self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.searchLabel)

		self.searchEdit = QtGui.QLineEdit(self)
		self.searchEdit.setText("500|500")
		self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.searchEdit)

		"""Spacer Form[1]"""
		self.Spacer1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
		self.formLayout.setItem(1, QtGui.QFormLayout.FieldRole, self.Spacer1)
		
		"""Filter by Form[2]"""
		self.filterLabel = QtGui.QLabel("Filter by", self)
		self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.filterLabel)

		self.filterBox = QtGui.QComboBox(self)
		self.filterBox.addItem("Players")
		self.filterBox.addItem("Barbarian Villages")
		self.filterBox.addItem("Players and Barbarians")
		self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.filterBox)

		"""Spacer Form[3]"""
		self.Spacer2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
		self.formLayout.setItem(3, QtGui.QFormLayout.FieldRole, self.Spacer2)

		"""Min points Form[4]"""
		self.min_pointsLabel = QtGui.QLabel("Min points", self)
		self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.min_pointsLabel)

		self.min_pointsEdit = QtGui.QLineEdit(self)
		self.min_pointsEdit.setText("26")
		self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.min_pointsEdit)

		"""Max points Form"""
		self.max_pointsLabel = QtGui.QLabel("Max points", self)
		self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.max_pointsLabel)

		self.max_pointsEdit = QtGui.QLineEdit(self)
		self.max_pointsEdit.setText("12393")
		self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.max_pointsEdit)

		"""Range Form[6]"""
		self.min_rangeLabel = QtGui.QLabel("Min range", self)
		self.formLayout.setWidget(6, QtGui.QFormLayout.LabelRole, self.min_rangeLabel)

		self.min_rangeEdit = QtGui.QLineEdit(self)
		self.min_rangeEdit.setText("0")
		self.formLayout.setWidget(6, QtGui.QFormLayout.FieldRole, self.min_rangeEdit)

		"""Range Form[7]"""
		self.max_rangeLabel = QtGui.QLabel("Max range", self)
		self.formLayout.setWidget(7, QtGui.QFormLayout.LabelRole, self.max_rangeLabel)

		self.max_rangeEdit = QtGui.QLineEdit(self)
		self.max_rangeEdit.setText("25")
		self.formLayout.setWidget(7, QtGui.QFormLayout.FieldRole, self.max_rangeEdit)

		"""Picture Form[8]"""
		self.testLabel = QtGui.QLabel(self)
		self.pixmap = QtGui.QPixmap(Files.resource_path("images/pic.jpg"))
		self.testLabel.setPixmap(self.pixmap)
		self.formLayout.setWidget(8, QtGui.QFormLayout.FieldRole, self.testLabel)

		"""Go button Form[9]"""
		self.goButton = QtGui.QPushButton("Go", self)
		self.goButton.clicked.connect(self.go_function)
		self.formLayout.setWidget(9, QtGui.QFormLayout.FieldRole, self.goButton)

		"""Table widget & options"""
		self.tableWidget = QtGui.QTableWidget(self)
		self.horizontalLayout.addWidget(self.tableWidget)
		self.tableWidget.setShowGrid(False)
		self.tableWidget.setWordWrap(False)
		self.tableWidget.setCornerButtonEnabled(False)
		self.tableWidget.setSortingEnabled(True)
		self.tableWidget.verticalHeader().setVisible(False)
		self.tableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
		self.tableWidget.setSelectionMode(QtGui.QAbstractItemView.NoSelection)

		"""Table columns"""
		self.tableWidget.setColumnCount(4)
		item = QtGui.QTableWidgetItem("Player")
		self.tableWidget.setHorizontalHeaderItem(0, item)
		item = QtGui.QTableWidgetItem("Name")
		self.tableWidget.setHorizontalHeaderItem(1, item)
		item = QtGui.QTableWidgetItem("Coordinates")
		self.tableWidget.setHorizontalHeaderItem(2, item)
		item = QtGui.QTableWidgetItem("Points")
		self.tableWidget.setHorizontalHeaderItem(3, item)

		"""Coords edit box"""
		self.coordsEdit = QtGui.QTextEdit(self)
		self.verticalLayout.addWidget(self.coordsEdit)

class CeUi(object):
	def setupUi(self):
		"""Background color"""
		self.backgroundPalette = QtGui.QPalette()
		self.backgroundColor = QtGui.QColor(217, 204, 170)
		self.backgroundPalette.setColor(QtGui.QPalette.Background, self.backgroundColor)
		self.setPalette(self.backgroundPalette)

		"""Main layout & return to main menu button"""
		self.verticalLayout = QtGui.QVBoxLayout(self)

		self.buttonLayout = QtGui.QHBoxLayout(self)
		self.verticalLayout.addLayout(self.buttonLayout)
		self.returnButton = QtGui.QPushButton("  Return to the Main Menu  ", self)
		self.returnButton.clicked.connect(self.return_function)
		self.buttonLayout.addWidget(self.returnButton)
		self.buttonSpacer = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
		self.buttonLayout.addItem(self.buttonSpacer)

		"""Line Spacer and line"""
		self.lineSpacer = QtGui.QSpacerItem(40, 5, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
		self.verticalLayout.addItem(self.lineSpacer)
		self.line = QtGui.QFrame(self)
		self.line.setFrameShape(QtGui.QFrame.HLine)
		self.line.setFrameShadow(QtGui.QFrame.Sunken)
		self.verticalLayout.addWidget(self.line)

		"""Text input label and edit"""
		self.Spacer = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
		self.verticalLayout.addItem(self.Spacer)
		self.inputLabel = QtGui.QLabel("Input text with coordinates here:")
		self.verticalLayout.addWidget(self.inputLabel)
		self.plainTextEdit = QtGui.QPlainTextEdit(self)
		self.verticalLayout.addWidget(self.plainTextEdit)

		"""Coordinates output label and edit"""
		self.Spacer1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
		self.verticalLayout.addItem(self.Spacer1)
		self.outputLabel = QtGui.QLabel("Output coordinates magically appear here:")
		self.verticalLayout.addWidget(self.outputLabel)
		self.plainTextEdit_2 = QtGui.QPlainTextEdit(self)
		self.verticalLayout.addWidget(self.plainTextEdit_2)

		"""Extract coordinates button"""
		self.horizontalLayout = QtGui.QHBoxLayout()
		self.verticalLayout.addLayout(self.horizontalLayout)
		self.Spacer2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
		self.horizontalLayout.addItem(self.Spacer2)
		self.extractButton = QtGui.QPushButton("  Extract Coordinates  ", self)
		self.extractButton.clicked.connect(self.extract_function)
		self.horizontalLayout.addWidget(self.extractButton)

class BcUi(object):
	def setupUi(self):
		"""Background color"""
		self.backgroundPalette = QtGui.QPalette()
		self.backgroundColor = QtGui.QColor(217, 204, 170)
		self.backgroundPalette.setColor(QtGui.QPalette.Background, self.backgroundColor)
		self.setPalette(self.backgroundPalette)

		"""Main layout & return to main menu button"""
		self.verticalLayout = QtGui.QVBoxLayout(self)

		self.buttonLayout = QtGui.QHBoxLayout(self)
		self.verticalLayout.addLayout(self.buttonLayout)
		self.returnButton = QtGui.QPushButton("  Return to the Main Menu  ", self)
		self.returnButton.clicked.connect(self.return_function)
		self.buttonLayout.addWidget(self.returnButton)
		self.buttonSpacer = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
		self.buttonLayout.addItem(self.buttonSpacer)

		"""Line Spacer and line"""
		self.lineSpacer = QtGui.QSpacerItem(40, 5, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
		self.verticalLayout.addItem(self.lineSpacer)
		self.line = QtGui.QFrame(self)
		self.line.setFrameShape(QtGui.QFrame.HLine)
		self.line.setFrameShadow(QtGui.QFrame.Sunken)
		self.verticalLayout.addWidget(self.line)

		"""Settings radio buttons"""
		self.horizontalLayout_2 = QtGui.QHBoxLayout()
		self.verticalLayout.addLayout(self.horizontalLayout_2)
		self.verticalLayout_2 = QtGui.QVBoxLayout()
		self.horizontalLayout_2.addLayout(self.verticalLayout_2)

		self.selected_worldRadio = QtGui.QRadioButton(self)
		self.selected_worldRadio.setText("Use Selected World")
		self.selected_worldRadio.toggled.connect(self.selected_function)
		self.verticalLayout_2.addWidget(self.selected_worldRadio)

		self.manual_speedRadio = QtGui.QRadioButton(self)
		self.manual_speedRadio.setText("Input Speed Manually")
		self.manual_speedRadio.toggled.connect(self.manual_function)
		self.verticalLayout_2.addWidget(self.manual_speedRadio)

		"""Speed labels"""
		self.speed_labelsLayout = QtGui.QVBoxLayout()
		self.horizontalLayout_2.addLayout(self.speed_labelsLayout)

		self.world_speedLabel = QtGui.QLabel(self)
		self.world_speedLabel.setText("World Speed: 0")
		self.speed_labelsLayout.addWidget(self.world_speedLabel)

		self.unit_speedLabel = QtGui.QLabel(self)
		self.unit_speedLabel.setText("Unit Speed: 0")
		self.speed_labelsLayout.addWidget(self.unit_speedLabel)

		"""Spacer"""
		self.Spacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
		self.verticalLayout.addItem(self.Spacer)

		"""Botton layout"""
		self.horizontalLayout_3 = QtGui.QHBoxLayout()
		self.verticalLayout.addLayout(self.horizontalLayout_3)

		"""Bottom left layout"""
		self.verticalLayout_4 = QtGui.QVBoxLayout()
		self.horizontalLayout_3.addLayout(self.verticalLayout_4)

		"""Settings layout"""
		self.horizontalLayout_4 = QtGui.QHBoxLayout()
		self.verticalLayout_4.addLayout(self.horizontalLayout_4)

		"""Origin and destination"""
		self.verticalLayout_6 = QtGui.QVBoxLayout()
		self.horizontalLayout_4.addLayout(self.verticalLayout_6)

		self.originLabel = QtGui.QLabel(self)
		self.originLabel.setText("Origin:")
		self.verticalLayout_6.addWidget(self.originLabel)

		self.originEdit = QtGui.QLineEdit(self)
		self.originEdit.setText("500|500")
		self.verticalLayout_6.addWidget(self.originEdit)

		self.destinationLabel = QtGui.QLabel(self)
		self.destinationLabel.setText("Destination:")
		self.verticalLayout_6.addWidget(self.destinationLabel)

		self.destinationEdit = QtGui.QLineEdit(self)
		self.destinationEdit.setText("550|550")
		self.verticalLayout_6.addWidget(self.destinationEdit)

		"""Unit and arrival"""
		self.verticalLayout_7 = QtGui.QVBoxLayout()
		self.horizontalLayout_4.addLayout(self.verticalLayout_7)

		self.unitLabel = QtGui.QLabel(self)
		self.unitLabel.setText("Unit:")
		self.verticalLayout_7.addWidget(self.unitLabel)

		self.unitBox = QtGui.QComboBox(self)
		self.unitBox.addItem("Spear fighter")
		self.unitBox.addItem("Swordsman")
		self.unitBox.addItem("Axeman")
		self.unitBox.addItem("Archer")
		self.unitBox.addItem("Scout")
		self.unitBox.addItem("Light cavalry")
		self.unitBox.addItem("Mounted archer")
		self.unitBox.addItem("Heavy cavalry")
		self.unitBox.addItem("Ram")
		self.unitBox.addItem("Catapult")
		self.unitBox.addItem("Paladin")
		self.unitBox.addItem("Nobleman")

		self.verticalLayout_7.addWidget(self.unitBox)

		self.arrivalLabel = QtGui.QLabel(self)
		self.arrivalLabel.setText("Arrival:")
		self.verticalLayout_7.addWidget(self.arrivalLabel)

		self.arrivalEdit = QtGui.QDateTimeEdit(self)
		self.verticalLayout_7.addWidget(self.arrivalEdit)

		"""Button and text edit"""
		self.calculateButton = QtGui.QPushButton(self)
		self.calculateButton.setText("Calculate Backtime")
		self.calculateButton.clicked.connect(self.backtime_function)
		self.verticalLayout_4.addWidget(self.calculateButton)

		self.backtimeEdit = QtGui.QTextEdit(self)
		self.horizontalLayout_3.addWidget(self.backtimeEdit)