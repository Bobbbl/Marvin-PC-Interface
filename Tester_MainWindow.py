import sys
from PyQt5.QtWidgets import QFileDialog
import tester
from PyQt5 import QtGui, QtWidgets, QtCore
import serial
import glob
from interface import Listener_Thread
import pandas as pd


# noinspection PyPep8Naming
class Tester_Mainwindow(QtWidgets.QDialog, tester.Ui_Form):
    def __init__(self, parent=None):
        super(Tester_Mainwindow, self).__init__(parent)
        self.setupUi(self)

        # Set Fixed Size W:250 H:230
        self.setFixedSize(250, 230)

        # Pre
        self.PreFeed = 100

        # Serial Port
        serial_ports_list = self.list_serial_ports()
        if not serial_ports_list:
            print("No Ports Available")
        else:
            self._Port = Listener_Thread(serial_ports_list[0], read_timeout=7, write_timeout=7)
            self._Port.start()

        # Connections
        # Buttons
        self.pushButtonDown.clicked.connect(self.pushButtonDown_Clicked)
        self.pushButtonUp.clicked.connect(self.pushButtonUp_Clicked)
        self.pushButtonLeft.clicked.connect(self.pushButtonLeft_Clicked)
        self.pushButtonRight.clicked.connect(self.pushButtonDown_Clicked)
        self.pushButtonSend.clicked.connect(self.pushButtonSend_Clicked)
        self.pushButtonSpindel.clicked.connect(self.pushButtonSpindel_Clicked)
        self.pushButtonPumpe.clicked.connect(self.pushButtonPumpe_Clicked)
        self.pushButtonStop.clicked.connect(self.pushButtonStop_Clicked)
        self.pushButtonExcel.clicked.connect(self.pushButtonExcel_Clicked)

    def pushButtonExcel_Clicked(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\', "Image files (*.csv)")
        pd.read_csv(fname)

    def pushButtonStop_Clicked(self):
        tmp = "STOP@"
        self._Port.sendMessage(tmp)

    def pushButtonSpindel_Clicked(self):
        tmp = "S;" + str(self.lineEditSpindel.text()) + "@"
        self._Port.sendMessage(tmp)

    def pushButtonPumpe_Clicked(self):
        tmp = "P;" + str(self.lineEditPolierpumpe.text()) + "@"
        self._Port.sendMessage(tmp)

    def pushButtonDown_Clicked(self):
        self._Port.sendMessage("XYF;0;1;" + str(self.PreFeed) + "@")

    def pushButtonUp_Clicked(self):
        self._Port.sendMessage("XYF;0;-1;" + str(self.PreFeed) + "@")

    def pushButtonLeft_Clicked(self):
        self._Port.sendMessage("XYF;-1;0;" + str(self.PreFeed) + "@")

    def pushButtonRight_Clicked(self):
        self._Port.sendMessage("XYF;1;0;" + str(self.PreFeed) + "@")

    def pushButtonSend_Clicked(self):
        if any(char.isdigit() for char in self.lineEditX.text()):
            x = self.lineEditX.text()
        if any(char.isdigit() for char in self.lineEditY.text()):
            y = self.lineEditY.text()
        if any(char.isdigit() for char in self.lineEditFeed.text()):
            feed = self.lineEditFeed.text()
        self._Port.sendMessage("XYF;" + x + ";" + y + ";" + feed + "@")

    def list_serial_ports(self):
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result
