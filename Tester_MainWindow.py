import sys
import tester
from PyQt5 import QtGui, QtWidgets, QtCore
import serial
import glob
from interface import Listener_Thread



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
          self._Port = Listener_Thread(serial_ports_list[0], read_timeout=7)
          self._Port.start()



        # Connections
        # Buttons
        self.pushButtonDown.clicked(self.pushButtonDown_Clicked)
        self.pushButtonUp.clicked(self.pushButtonUp_Clicked)
        self.pushButtonLeft.clicked(self.pushButtonLeft_Clicked)
        self.pushButtonDown.clicked(self.pushButtonDown_Clicked)
        self.pushButtonSend.clicked(self.pushButtonSend_Clicked)

    def pushButtonDown_Clicked(self):
        self._Port.sendMessage("XYF 0 -100 " + self.PreFeed)

    def pushButtonUp_Clicked(self):
        self._Port.sendMessage("XYF 0 100 " + self.PreFeed)

    def pushButtonLeft_Clicked(self):
        self._Port.sendMessage("XYF -100 0 " + self.PreFeed)

    def pushButtonRight_Clicked(self):
        self._Port.sendMessage("XYF 100 0 " + self.PreFeed)

    def pushButtonSend_Clicked(self):
        x = self.lineEditX.text()
        y = self.lineEditY.text()
        self._Port.sendMessage("XYF " + x + " " + y + self.PreFeed)


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
