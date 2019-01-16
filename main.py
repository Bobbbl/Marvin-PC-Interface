import sys
import interface
import PyQt5
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
import tester


class TesterApp(QtWidgets.QMainWindow, tester.Ui_Form):
    def __init__(self, parent=None):
        super(TesterApp, self).__init__(parent)
        self.setupUi(self)
        self.setupSignals()

    def setupSignals(self):
        pass

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    form = TesterApp()
    form.show()
    app.exec_()

