# This Python file uses the following encoding: utf-8
import os
import glob
import sys
from PySide2.QtQuick import QQuickView
from PySide2.QtCore import QAbstractListModel, Qt, QUrl, QStringListModel, QThread, Signal, QTimer, QObject
from PySide2 import QtCore
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlProperty, QQmlApplicationEngine
import serial


class PortList(QObject):

    listChanged = Signal()

    def __init__(self, llist):
        QObject.__init__(self)
        self.llist = llist

    def _appendPort(self, port):
        self.llist.append(port)
        self.listChanged.emit()


    def _setPortList(self, list):
        self.llist = list
        self.listChanged.emit()

    def _getPortList(self):
        return self.llist

    pList = QtCore.Property('QStringList', _getPortList, '', notify=listChanged)


class PortInterface(QThread, QObject):
    newMessageReceived = Signal(str)
    messageSent = Signal(str)
    portsList = []

    def __init__(self, rootObject, view):
        QObject.__init__(self)
        #self.port = serial.Serial(port, 115200, write_timeout=0.1)
        self.rootObject = rootObject


        # Timer
        self.portTimer = QTimer()

        self.plist = PortList(llist=["1", "2"])

        view.rootContext().setContextProperty("Interface", self.plist)



        # Connections
        self.rootObject.upbutton_pressed.connect(self.upbutton_handler)
        self.rootObject.downbutton_pressed.connect(self.downbutton_handler)
        self.rootObject.leftbutton_pressed.connect(self.leftbutton_handler)
        self.rootObject.rightbutton_pressed.connect(self.rightbutton_handler)
        self.rootObject.stopbutton_pressed.connect(self.stopbutton_handler)
        self.portTimer.timeout.connect(self.portTimer_timeout)
        self.sleep(1)
        self.portTimer.start(500)

    def run(self):
        while (1):
            tmp = self.port.readline()
            self.newMessageReceived.emit(tmp)


    def portTimer_timeout(self):
        list = self.serial_ports()

        self.plist._setPortList(list)



    def serial_ports(self):
        """ Lists serial port names

            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
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
                s = serial.Serial(port, 115200, write_timeout=0.1)
                s.close()
                result.append(port)
            except serial.SerialException:
                pass
        return result

    def sendMessage(self, message):
        if (isinstance(message, str)):
            st_array = bytes(message, 'utf-8')
            self.port.write(st_array)
            self.port.flush()
            self.messageSent.emit(message)

    def setProp(self, objName, propName, value):
        obj = self.rootObject.findChild(QObject, objName)
        p = QQmlProperty(obj, propName)
        p.write(value)


    def setPropList(self, objName, propName, values):
        obj = self.rootObject.findChild(QObject, objName)
        property = QQmlProperty(obj, propName)
        property.write(values)

    def upbutton_handler(self):
        print("Up")

    def downbutton_handler(self):
        print("Down")

    def leftbutton_handler(self):
        print("Left")

    def rightbutton_handler(self):
        print("Right")

    def stopbutton_handler(self):
        print("Stop")


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    view = QQuickView()
    qml_file = os.path.join(os.path.dirname(__file__), 'main.qml')
    view.setSource(QUrl.fromLocalFile(os.path.abspath(qml_file)))
    view.setResizeMode(QQuickView.SizeRootObjectToView)



    # engine = QQmlApplicationEngine()

    # engine.load('QML_Interface\main.qml')

    # rootobject = engine.rootObjects()[0]
    rootObject = view.rootObject()
    interface = PortInterface(rootObject, view)

    if view.status() == QQuickView.Error:
        sys.exit(-1)

    view.show()
    app.exec_()
    del view
    # if not engine.rootObjects():
        # sys.exit(-1)
    # sys.exit(app.exec_())

