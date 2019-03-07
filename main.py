import sys
import interface
import PyQt5
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
import Tester_MainWindow


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    form = Tester_MainWindow.Tester_Mainwindow()
    form.show()
    app.exec_()

