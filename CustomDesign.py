from PySide2 import QtGui, QtCore, QtWidgets

from Functions import resource_path


class PicButton(QtWidgets.QAbstractButton):

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