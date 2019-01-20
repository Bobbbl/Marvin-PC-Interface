import sys
import tester
from PyQt5 import QtGui, QtWidgets, QtCore



class Tester_Mainwindow(QtWidgets.QDialog, tester.Ui_Form):
    def __init__(self, parent=None):
        super(Tester_Mainwindow, self).__init__(parent)
        self.setupUi(self)
