import sys
import tester
from PyQt5 import QtGui, QtWidgets, QtCore



class Tester_Mainwindow(QtWidgets.QDialog, tester.Ui_Form):
    def __init__(self, parent=None):
        super(Tester_Mainwindow, self).__init__(parent)
        self.setupUi(self)

        # Set Fixed Size W:250 H:230
        self.setFixedSize(250, 230)

        # Connections
        # Buttons
        self.pushButtonDown.clicked(self.pushButtonDown_Clicked)
        self.pushButtonUp.clicked(self.pushButtonUp_Clicked)
        self.pushButtonLeft.clicked(self.pushButtonLeft_Clicked)
        self.pushButtonDown.clicked(self.pushButtonDown_Clicked)
        self.pushButtonSend.clicked(self.pushButtonSend_Clicked)

    def pushButtonDown_Clicked(self):
        pass

    def pushButtonUp_Clicked(self):
        pass

    def pushButtonLeft_Clicked(self):
        pass

    def pushButtonRight_Clicked(self):
        pass

    def pushButtonSend_Clicked(self):
        pass
