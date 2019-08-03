from PySide2 import QtGui, QtCore, QtWidgets
import os
from CustomDesign import PicButton
from Functions import resource_path

class MainUi(object):

    def setupUi(self):
        """Bruh"""
        self.setWindowTitle("ZeZe's TWTools")
        self.setWindowIcon(QtGui.QIcon(resource_path("images/icon.png")))

        """Background color"""
        self.backgroundPalette = QtGui.QPalette()
        self.backgroundColor = QtGui.QColor(238, 217, 174)
        self.backgroundPalette.setColor(QtGui.QPalette.Background, self.backgroundColor)
        self.setPalette(self.backgroundPalette)

        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)

        """Spacer to the left"""
        self.leftSpacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout.addItem(self.leftSpacer)

        """Main content"""
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.horizontalLayout.addLayout(self.verticalLayout)

        """Main text picture"""
        self.horizontalLayout_1 = QtWidgets.QHBoxLayout()
        self.logo_textScene = QtWidgets.QGraphicsScene()
        self.logo_textScene.addPixmap(QtGui.QPixmap(resource_path("images/logo_text.png")))
        self.logo_textView = QtWidgets.QGraphicsView(self.logo_textScene, self.centralwidget)
        self.logo_textView.setFixedSize(565, 175)
        self.logo_textView.setStyleSheet("border: 0px; background-color: transparent;")

        self.horizontalLayout_1.addWidget(self.logo_textView)
        self.verticalLayout.addLayout(self.horizontalLayout_1)

        self.mainSpacer = QtWidgets.QSpacerItem(50, 50, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(self.mainSpacer)

        """Download options"""
        self.downloadGrid = QtWidgets.QGridLayout(self.centralwidget)
        self.serverLabel = QtWidgets.QLabel("Tribal Wars Servers", self.centralwidget)
        self.serverBox = QtWidgets.QComboBox(self.centralwidget)

        self.serverBox.addItems(self.serverItems)
        self.serverBox.activated[str].connect(self.on_combo_activated)

        self.worldLabel = QtWidgets.QLabel("Worlds", self.centralwidget)
        self.worldBox = QtWidgets.QComboBox(self.centralwidget)

        self.downloadButton = QtWidgets.QPushButton("Download World Data", self.centralwidget)
        self.downloadButton.clicked.connect(self.download_function)

        self.downloadGrid.addWidget(self.serverLabel, 1, 1)
        self.downloadGrid.addWidget(self.serverBox, 2, 1)
        self.downloadGrid.addWidget(self.worldLabel, 1, 2)
        self.downloadGrid.addWidget(self.worldBox, 2, 2)
        self.downloadGrid.addWidget(self.downloadButton, 2, 3)

        self.verticalLayout.addLayout(self.downloadGrid)

        """Spacer line"""
        self.lineSpacer = QtWidgets.QSpacerItem(50, 50, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(self.lineSpacer)

        """Options row"""
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.vfButton = PicButton(
            QtGui.QPixmap(
                resource_path("images/village_finder.png")),
            QtGui.QPixmap(
                resource_path("images/village_finder.png")),
            QtGui.QPixmap(
                resource_path("images/village_finder.png")))
        self.vfButton.clicked.connect(self.village_finder)
        self.horizontalLayout_3.addWidget(self.vfButton)

        self.spacer = QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout_3.addItem(self.spacer)

        self.ceButton = PicButton(
            QtGui.QPixmap(
                resource_path("images/coordinates_extractor.png")),
            QtGui.QPixmap(
                resource_path("images/coordinates_extractor.png")),
            QtGui.QPixmap(
                resource_path("images/coordinates_extractor.png")))
        self.ceButton.clicked.connect(self.coord_extractor)
        self.horizontalLayout_3.addWidget(self.ceButton)

        self.spacer_1 = QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout_3.addItem(self.spacer_1)

        self.bcButton = PicButton(
            QtGui.QPixmap(
                resource_path("images/backtiming_calculator.png")),
            QtGui.QPixmap(
                resource_path("images/backtiming_calculator.png")),
            QtGui.QPixmap(
                resource_path("images/backtiming_calculator.png")))
        self.bcButton.clicked.connect(self.backtiming_calculator)
        self.horizontalLayout_3.addWidget(self.bcButton)

        """Spacer buttons"""
        self.spacer_buttons = QtWidgets.QSpacerItem(
            5, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(self.spacer_buttons)

        """Options row 2"""
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.ftButton = PicButton(
            QtGui.QPixmap(
                resource_path("images/farm_thief.png")),
            QtGui.QPixmap(
                resource_path("images/farm_thief.png")),
            QtGui.QPixmap(
                resource_path("images/farm_thief.png")))
        self.ftButton.clicked.connect(self.farm_thief)
        self.horizontalLayout_4.addWidget(self.ftButton)

        self.spacer_2 = QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout_4.addItem(self.spacer_2)

        self.vpButton = PicButton(
            QtGui.QPixmap(
                resource_path("images/village_planner.png")),
            QtGui.QPixmap(
                resource_path("images/village_planner.png")),
            QtGui.QPixmap(
                resource_path("images/village_planner.png")))
        self.vpButton.clicked.connect(self.coming_soon)
        self.horizontalLayout_4.addWidget(self.vpButton)

        self.spacer_3 = QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout_4.addItem(self.spacer_3)

        self.eButton = PicButton(
            QtGui.QPixmap(
                resource_path("images/empty.png")),
            QtGui.QPixmap(
                resource_path("images/empty.png")),
            QtGui.QPixmap(
                resource_path("images/empty.png")))
        self.horizontalLayout_4.addWidget(self.eButton)

        """Spacer2 to the right"""
        self.horizontalSpacer_2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout.addItem(self.horizontalSpacer_2)


class VfUi(object):

    def setupUi(self):
        """Bruh"""
        self.setGeometry(50, 50, 850, 425)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("ZeZe's TWTools")
        self.setWindowIcon(QtGui.QIcon(resource_path("images/icon.png")))

        """Set background color"""
        self.backgroundPalette = QtGui.QPalette()
        self.backgroundColor = QtGui.QColor(217, 204, 170)
        self.backgroundPalette.setColor(QtGui.QPalette.Background, self.backgroundColor)
        self.setPalette(self.backgroundPalette)

        """Layout for dialog"""
        self.verticalLayout = QtWidgets.QVBoxLayout(self)

        """Return button"""
        self.buttonLayout = QtWidgets.QHBoxLayout(self)
        self.verticalLayout.addLayout(self.buttonLayout)
        self.returnButton = QtWidgets.QPushButton("  Return to the Main Menu  ", self)
        self.returnButton.clicked.connect(self.return_function)
        self.buttonLayout.addWidget(self.returnButton)
        self.buttonSpacer = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.buttonLayout.addItem(self.buttonSpacer)

        """Line Spacer and line"""
        self.lineSpacer = QtWidgets.QSpacerItem(40, 5, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(self.lineSpacer)
        self.line = QtWidgets.QFrame(self)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.verticalLayout.addWidget(self.line)

        """Layout for form and table"""
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.verticalLayout.addLayout(self.horizontalLayout)

        """Layout for form"""
        self.formLayout = QtWidgets.QFormLayout()
        self.horizontalLayout.addLayout(self.formLayout)

        """Search around Form[0]"""
        self.searchLabel = QtWidgets.QLabel("Search around", self)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.searchLabel)

        self.searchEdit = QtWidgets.QLineEdit(self)
        self.searchEdit.setText("500|500")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.searchEdit)

        """Spacer Form[1]"""
        self.Spacer1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.formLayout.setItem(1, QtWidgets.QFormLayout.FieldRole, self.Spacer1)

        """Filter by Form[2]"""
        self.filterLabel = QtWidgets.QLabel("Filter by", self)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.filterLabel)

        self.filterBox = QtWidgets.QComboBox(self)
        self.filterBox.addItem("Players")
        self.filterBox.addItem("Barbarian Villages")
        self.filterBox.addItem("Players and Barbarians")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.filterBox)

        """Spacer Form[3]"""
        self.Spacer2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.formLayout.setItem(3, QtWidgets.QFormLayout.FieldRole, self.Spacer2)

        """Min points Form[4]"""
        self.min_pointsLabel = QtWidgets.QLabel("Min points", self)
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.min_pointsLabel)

        self.min_pointsEdit = QtWidgets.QLineEdit(self)
        self.min_pointsEdit.setText("26")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.min_pointsEdit)

        """Max points Form"""
        self.max_pointsLabel = QtWidgets.QLabel("Max points", self)
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.max_pointsLabel)

        self.max_pointsEdit = QtWidgets.QLineEdit(self)
        self.max_pointsEdit.setText("12393")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.max_pointsEdit)

        """Range Form[6]"""
        self.min_rangeLabel = QtWidgets.QLabel("Min range", self)
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.min_rangeLabel)

        self.min_rangeEdit = QtWidgets.QLineEdit(self)
        self.min_rangeEdit.setText("0")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.min_rangeEdit)

        """Range Form[7]"""
        self.max_rangeLabel = QtWidgets.QLabel("Max range", self)
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.max_rangeLabel)

        self.max_rangeEdit = QtWidgets.QLineEdit(self)
        self.max_rangeEdit.setText("25")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.max_rangeEdit)

        """Picture Form[8]"""
        self.testLabel = QtWidgets.QLabel(self)
        self.pixmap = QtGui.QPixmap(resource_path("images/pic.jpg"))
        self.testLabel.setPixmap(self.pixmap)
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.testLabel)

        """Go button Form[9]"""
        self.goButton = QtWidgets.QPushButton("Go", self)
        self.goButton.clicked.connect(self.go_function)
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.FieldRole, self.goButton)

        """Table widget & options"""
        self.tableWidget = QtWidgets.QTableWidget(self)
        self.horizontalLayout.addWidget(self.tableWidget)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.setWordWrap(False)
        self.tableWidget.setCornerButtonEnabled(False)
        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)

        """Table columns"""
        self.tableWidget.setColumnCount(4)
        item = QtWidgets.QTableWidgetItem("Player")
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem("Name")
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem("Coordinates")
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem("Points")
        self.tableWidget.setHorizontalHeaderItem(3, item)

        """Spacer, line and layout for coords output options panel"""
        self.Spacer = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(self.Spacer)

        self.line = QtWidgets.QFrame(self)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.verticalLayout.addWidget(self.line)

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.Spacer1 = QtWidgets.QSpacerItem(10, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout_2.addItem(self.Spacer1)

        """Radio buttons for output options"""
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.outputLabel = QtWidgets.QLabel("Output as: ", self)
        self.verticalLayout_2.addWidget(self.outputLabel)

        self.plainRadio = QtWidgets.QRadioButton("Plain coordinates (useful for scripts)", self)
        self.plainRadio.toggled.connect(self.list_options_toggle)
        self.plainRadio.toggled.connect(self.get_coords_data)

        self.verticalLayout_2.addWidget(self.plainRadio)

        self.listRadio = QtWidgets.QRadioButton("Formatted list (BB-code)", self)
        self.listRadio.toggled.connect(self.get_coords_data)
        self.verticalLayout_2.addWidget(self.listRadio)

        """Checkbox for list output options"""
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)

        self.Spacer2 = QtWidgets.QSpacerItem(5, 1.75, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(self.Spacer2)

        self.formWidget = QtWidgets.QWidget()
        self.verticalLayout_3.addWidget(self.formWidget)

        self.formLayout = QtWidgets.QFormLayout()
        self.formWidget.setLayout(self.formLayout)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)

        self.numberCheck = QtWidgets.QCheckBox("Incrementing number", self)
        self.numberCheck.toggled.connect(self.get_coords_data)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.numberCheck)

        self.playerCheck = QtWidgets.QCheckBox("Player names", self)
        self.playerCheck.toggled.connect(self.get_coords_data)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.playerCheck)

        self.pointsCheck = QtWidgets.QCheckBox("Village points", self)
        self.pointsCheck.toggled.connect(self.get_coords_data)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.pointsCheck)

        self.plainRadio.toggle()

        """Coords edit box"""
        self.coordsEdit = QtWidgets.QTextEdit(self)
        self.verticalLayout.addWidget(self.coordsEdit)


class CeUi(object):

    def setupUi(self):
        """Bruh"""
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setGeometry(50, 50, 850, 425)
        self.setWindowTitle("ZeZe's TWTools - Coord Extractor")
        self.setWindowIcon(QtGui.QIcon(resource_path("images/icon.png")))

        """Background color"""
        self.backgroundPalette = QtGui.QPalette()
        self.backgroundColor = QtGui.QColor(217, 204, 170)
        self.backgroundPalette.setColor(QtGui.QPalette.Background, self.backgroundColor)
        self.setPalette(self.backgroundPalette)

        """Main layout & return to main menu button"""
        self.verticalLayout = QtWidgets.QVBoxLayout(self)

        self.buttonLayout = QtWidgets.QHBoxLayout(self)
        self.verticalLayout.addLayout(self.buttonLayout)
        self.returnButton = QtWidgets.QPushButton("  Return to the Main Menu  ", self)
        self.returnButton.clicked.connect(self.return_function)
        self.buttonLayout.addWidget(self.returnButton)
        self.buttonSpacer = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.buttonLayout.addItem(self.buttonSpacer)

        """Line Spacer and line"""
        self.lineSpacer = QtWidgets.QSpacerItem(40, 5, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(self.lineSpacer)
        self.line = QtWidgets.QFrame(self)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.verticalLayout.addWidget(self.line)

        """Text input label and edit"""
        self.Spacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(self.Spacer)
        self.inputLabel = QtWidgets.QLabel("Input text with coordinates here:")
        self.verticalLayout.addWidget(self.inputLabel)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self)
        self.verticalLayout.addWidget(self.plainTextEdit)

        """Coordinates output label and edit"""
        self.Spacer1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(self.Spacer1)
        self.outputLabel = QtWidgets.QLabel("Output coordinates magically appear here:")
        self.verticalLayout.addWidget(self.outputLabel)
        self.plainTextEdit_2 = QtWidgets.QPlainTextEdit(self)
        self.verticalLayout.addWidget(self.plainTextEdit_2)

        """Extract coordinates button"""
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.Spacer2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(self.Spacer2)
        self.extractButton = QtWidgets.QPushButton("  Extract Coordinates  ", self)
        self.extractButton.clicked.connect(self.extract_function)
        self.horizontalLayout.addWidget(self.extractButton)


class BcUi(object):

    def setupUi(self):
        """Bruh"""
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setGeometry(50, 50, 600, 300)
        self.setWindowTitle("ZeZe's TWTools - Backtiming Calculator")
        self.setWindowIcon(QtGui.QIcon(resource_path("images/icon.png")))

        """Background color"""
        self.backgroundPalette = QtGui.QPalette()
        self.backgroundColor = QtGui.QColor(217, 204, 170)
        self.backgroundPalette.setColor(
            QtGui.QPalette.Background, self.backgroundColor)
        self.setPalette(self.backgroundPalette)

        """Main layout & return to main menu button"""
        self.verticalLayout = QtWidgets.QVBoxLayout(self)

        self.buttonLayout = QtWidgets.QHBoxLayout(self)
        self.verticalLayout.addLayout(self.buttonLayout)
        self.returnButton = QtWidgets.QPushButton("  Return to the Main Menu  ", self)
        self.returnButton.clicked.connect(self.return_function)
        self.buttonLayout.addWidget(self.returnButton)
        self.buttonSpacer = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.buttonLayout.addItem(self.buttonSpacer)

        """Line Spacer and line"""
        self.lineSpacer = QtWidgets.QSpacerItem(40, 5, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(self.lineSpacer)
        self.line = QtWidgets.QFrame(self)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.verticalLayout.addWidget(self.line)

        """Settings radio buttons"""
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.selected_worldRadio = QtWidgets.QRadioButton("Use Selected World", self)
        self.selected_worldRadio.toggled.connect(self.selected_function)
        self.verticalLayout_2.addWidget(self.selected_worldRadio)

        self.manual_speedRadio = QtWidgets.QRadioButton("Input Speed Manually", self)
        self.manual_speedRadio.toggled.connect(self.manual_function)
        self.verticalLayout_2.addWidget(self.manual_speedRadio)

        """Speed labels"""
        self.speed_labelsLayout = QtWidgets.QVBoxLayout()
        self.horizontalLayout_2.addLayout(self.speed_labelsLayout)

        self.world_speedLabel = QtWidgets.QLabel(self)
        self.world_speedLabel.setText("World Speed:")
        self.speed_labelsLayout.addWidget(self.world_speedLabel)

        self.unit_speedLabel = QtWidgets.QLabel(self)
        self.unit_speedLabel.setText("Unit Speed:")
        self.speed_labelsLayout.addWidget(self.unit_speedLabel)

        """Spacer"""
        self.Spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(self.Spacer)

        """Botton layout"""
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        """Bottom left layout"""
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.horizontalLayout_3.addLayout(self.verticalLayout_4)

        """Settings layout"""
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)

        """Origin and destination"""
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.horizontalLayout_4.addLayout(self.verticalLayout_6)

        self.originLabel = QtWidgets.QLabel(self)
        self.originLabel.setText("Origin:")
        self.verticalLayout_6.addWidget(self.originLabel)

        self.originEdit = QtWidgets.QLineEdit(self)
        self.originEdit.setText("500|500")
        self.verticalLayout_6.addWidget(self.originEdit)

        self.destinationLabel = QtWidgets.QLabel(self)
        self.destinationLabel.setText("Destination:")
        self.verticalLayout_6.addWidget(self.destinationLabel)

        self.destinationEdit = QtWidgets.QLineEdit(self)
        self.destinationEdit.setText("550|550")
        self.verticalLayout_6.addWidget(self.destinationEdit)

        """Unit and arrival"""
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.horizontalLayout_4.addLayout(self.verticalLayout_7)

        self.unitLabel = QtWidgets.QLabel(self)
        self.unitLabel.setText("Unit:")
        self.verticalLayout_7.addWidget(self.unitLabel)

        self.unitBox = QtWidgets.QComboBox(self)
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

        self.arrivalLabel = QtWidgets.QLabel(self)
        self.arrivalLabel.setText("Arrival:")
        self.verticalLayout_7.addWidget(self.arrivalLabel)

        self.arrivalEdit = QtWidgets.QDateTimeEdit(self)
        self.verticalLayout_7.addWidget(self.arrivalEdit)

        """Button and text edit"""
        self.calculateButton = QtWidgets.QPushButton(self)
        self.calculateButton.setText("Calculate Backtime")
        self.calculateButton.clicked.connect(self.backtime_function)
        self.verticalLayout_4.addWidget(self.calculateButton)

        self.backtimeEdit = QtWidgets.QTextEdit(self)
        self.horizontalLayout_3.addWidget(self.backtimeEdit)

class SidUi(object):

    def setupUi(self):
        """Bruh"""
        self.setGeometry(50, 50, 300, 150)
        self.setWindowTitle("ZeZe's TWTools - Input Speeds")
        self.setWindowIcon(QtGui.QIcon(resource_path("images/icon.png")))

        """Background color"""
        self.backgroundPalette = QtGui.QPalette()
        self.backgroundColor = QtGui.QColor(217, 204, 170)
        self.backgroundPalette.setColor(QtGui.QPalette.Background, self.backgroundColor)
        self.setPalette(self.backgroundPalette)

        """Form layout"""
        self.formLayout = QtWidgets.QFormLayout(self)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)

        """World speed label & input box"""
        self.world_speedLabel = QtWidgets.QLabel("World Speed:", self)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.world_speedLabel)

        self.world_speedBox = QtWidgets.QDoubleSpinBox(self)
        self.world_speedBox.setDecimals(1)
        self.world_speedBox.setMaximum(1000.0)
        self.world_speedBox.setSingleStep(0.5)
        self.world_speedBox.setProperty("value", 1.0)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.world_speedBox)

        """Unit speed label & input box"""
        self.unit_speedLabel = QtWidgets.QLabel("Unit Speed:", self)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.unit_speedLabel)

        self.unit_speedBox = QtWidgets.QDoubleSpinBox(self)
        self.unit_speedBox.setDecimals(1)
        self.unit_speedBox.setMaximum(1000.0)
        self.unit_speedBox.setSingleStep(0.5)
        self.unit_speedBox.setProperty("value", 1.0)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.unit_speedBox)

        """Spacer"""
        self.Spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.formLayout.setItem(2, QtWidgets.QFormLayout.FieldRole, self.Spacer)

        """Ok button"""
        self.okButton = QtWidgets.QPushButton("Ok", self)
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.okButton)
        self.okButton.clicked.connect(self.get_data)

class DdUi(object):

    def setupUi(self):
        """Bruh"""
        self.setGeometry(50, 50, 450, 250)
        self.setWindowTitle("ZeZe's TWTools - Updating Servers")
        self.setWindowIcon(QtGui.QIcon(resource_path("images/icon.png")))

        """Background color"""
        self.backgroundPalette = QtGui.QPalette()
        self.backgroundColor = QtGui.QColor(217, 204, 170)
        self.backgroundPalette.setColor(QtGui.QPalette.Background, self.backgroundColor)
        self.setPalette(self.backgroundPalette)

        """Layout"""
        self.verticalLayout = QtWidgets.QVBoxLayout(self)

        self.text = QtWidgets.QLabel("Updating server list:")
        self.verticalLayout.addWidget(self.text)

        """Download bar"""
        self.progress_bar = QtWidgets.QProgressBar(self)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(self.servers_amount)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("%v / %m")
        self.verticalLayout.addWidget(self.progress_bar)

        """Text browser for progress"""
        self.progress_text = QtWidgets.QTextBrowser(self)
        self.verticalLayout.addWidget(self.progress_text)

        """Button"""
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.Spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(self.Spacer)

        self.cancelButton = QtWidgets.QPushButton("Cancel")
        self.horizontalLayout.addWidget(self.cancelButton)
        self.cancelButton.clicked.connect(self.cancel_function)

class FtUi(object):

    def setupUi(self):
        """Bruh"""
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setGeometry(50, 50, 600, 300)
        self.setWindowTitle("ZeZe's TWTools - Backtiming Calculator")
        self.setWindowIcon(QtGui.QIcon(resource_path("images/icon.png")))

        """Background color"""
        self.backgroundPalette = QtGui.QPalette()
        self.backgroundColor = QtGui.QColor(217, 204, 170)
        self.backgroundPalette.setColor(
            QtGui.QPalette.Background, self.backgroundColor)
        self.setPalette(self.backgroundPalette)

        """Main layout & return to main menu button"""
        self.verticalLayout = QtWidgets.QVBoxLayout(self)

        self.buttonLayout = QtWidgets.QHBoxLayout(self)
        self.verticalLayout.addLayout(self.buttonLayout)
        self.returnButton = QtWidgets.QPushButton("  Return to the Main Menu  ", self)
        self.returnButton.clicked.connect(self.return_function)
        self.buttonLayout.addWidget(self.returnButton)
        self.buttonSpacer = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.buttonLayout.addItem(self.buttonSpacer)