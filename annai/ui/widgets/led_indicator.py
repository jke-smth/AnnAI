from PySide6 import QtWidgets, QtCore, QtGui

class LedIndicator(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._color = QtGui.QColor("red")
        self._is_on = True

        self.setFixedSize(10, 10)

    def set_color(self, color):
        self._color = QtGui.QColor(color)
        self.update()

    def _toggle(self):
        self._is_on = not self._is_on
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        if self._is_on:
            painter.setBrush(self._color)
        else:
            painter.setBrush(QtGui.QColor(30, 30, 30))  # dim/off

        painter.setPen(QtCore.Qt.NoPen)
        painter.drawEllipse(0, 0, self.width(), self.height())