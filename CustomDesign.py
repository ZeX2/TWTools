from PySide import QtGui, QtCore
from Data import Files


class PicButton(QtGui.QAbstractButton):

    def __init__(self, pixmap, pixmap_hover, pixmap_pressed, parent=None):
        super(PicButton, self).__init__(parent)
        self.pixmap = pixmap
        self.pixmap_hover = pixmap_hover
        self.pixmap_pressed = pixmap_pressed

        self.pressed.connect(self.update)
        self.released.connect(self.update)

    def paintEvent(self, event):
        pix = self.pixmap_hover if self.underMouse() else self.pixmap
        if self.isDown():
            pix = self.pixmap_pressed

        painter = QtGui.QPainter(self)
        painter.drawPixmap(event.rect(), pix)

    def enterEvent(self, event):
        self.update()

    def leaveEvent(self, event):
        self.update()

    def sizeHint(self):
        return self.pixmap.size()


class Validator(object):

    def check_points_state(self):
        sender = self.sender()
        text = sender.text()
        validator = sender.validator()
        state = validator.validate(text, 0)[0]
        red = '#f6989d'
        try:
            if int(text) > 12393:
                sender.setText("12393")
            elif int(text) < 26:
                sender.setStyleSheet(
                    'QLineEdit { background-color: %s }' % red)
        except:
            pass

        if state == QtGui.QValidator.Acceptable and int(text) > 26:
            sender.setStyleSheet("")
        else:
            sender.setStyleSheet('QLineEdit { background-color: %s }' % red)

    def points_validator(self):
        return QtGui.QIntValidator()

    def check_coord_state(self):
        sender = self.sender()
        validator = QtGui.QRegExpValidator(QtCore.QRegExp("\d{3}\|\d{3}"))
        state = validator.validate(sender.text(), 0)[0]

        if state == QtGui.QValidator.Acceptable:
            sender.setStyleSheet("")
        else:
            red = '#f6989d'
            sender.setStyleSheet('QLineEdit { background-color: %s }' % red)


class CustomInputDialog(QtGui.QDialog):

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        """Bruh"""
        self.setGeometry(50, 50, 300, 150)
        self.setWindowTitle("ZeZe's TWTools - Input Speeds")
        self.setWindowIcon(QtGui.QIcon(Files.resource_path("images/icon.png")))

        """Background color"""
        self.backgroundPalette = QtGui.QPalette()
        self.backgroundColor = QtGui.QColor(217, 204, 170)
        self.backgroundPalette.setColor(QtGui.QPalette.Background, self.backgroundColor)
        self.setPalette(self.backgroundPalette)

        """Form layout"""
        self.formLayout = QtGui.QFormLayout(self)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)

        """World speed label & input box"""
        self.world_speedLabel = QtGui.QLabel("World Speed:", self)
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.world_speedLabel)

        self.world_speedBox = QtGui.QDoubleSpinBox(self)
        self.world_speedBox.setDecimals(1)
        self.world_speedBox.setMaximum(1000.0)
        self.world_speedBox.setSingleStep(0.5)
        self.world_speedBox.setProperty("value", 1.0)
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.world_speedBox)

        """Unit speed label & input box"""
        self.unit_speedLabel = QtGui.QLabel("Unit Speed:", self)
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.unit_speedLabel)

        self.unit_speedBox = QtGui.QDoubleSpinBox(self)
        self.unit_speedBox.setDecimals(1)
        self.unit_speedBox.setMaximum(1000.0)
        self.unit_speedBox.setSingleStep(0.5)
        self.unit_speedBox.setProperty("value", 1.0)
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.unit_speedBox)

        """Spacer"""
        self.Spacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.formLayout.setItem(2, QtGui.QFormLayout.FieldRole, self.Spacer)

        """Ok button"""
        self.okButton = QtGui.QPushButton("Ok", self)
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.okButton)
        self.okButton.clicked.connect(self.get_data)

        self.show()

    def get_data(self):
        self.accept()
        return self.world_speedBox.value(), self.unit_speedBox.value()

    def showEvent(self, event):
        geom = self.frameGeometry()
        geom.moveCenter(QtGui.QCursor.pos())
        self.setGeometry(geom)
