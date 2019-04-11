# This Python file uses the following encoding: utf-8
import os
import re
import glob
import sys
from PySide2.QtQuick import QQuickView
from PySide2.QtCore import QAbstractListModel, Qt, QUrl, QStringListModel, QThread, Signal, QTimer, QObject
from PySide2 import QtCore
from PySide2.QtGui import QGuiApplication
import serial
import time


class PortList(QObject):
    listChanged = Signal()

    def __init__(self, llist=[]):
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


class LogList(QObject):
    listChanged = Signal()

    def __init__(self, llist=[]):
        QObject.__init__(self)
        self.llist = llist

    def _appendLog(self, port):
        self.llist.append(port)
        self.listChanged.emit()

    def _deleteLog(self, list):
        self.llist = list
        self.listChanged.emit()

    def _getList(self):
        llist = "".join(self.llist)
        return llist

    def _getLastElement(self):
        element = str(self.llist[-1])
        return element

    logList = QtCore.Property('QString', _getList, '', notify=listChanged)
    lastElement = QtCore.Property('QString', _getLastElement, '', notify=listChanged)


class ProgressInterface(QObject):
    valueChanged = Signal()

    def __init__(self, value=[]):
        QObject.__init__(self)
        self.value = value

    def _setNewValue(self, value):
        self.value = value
        self.valueChanged.emit()

    def _getValue(self):
        return self.value

    pValue = QtCore.Property('double', _getValue, '', notify=valueChanged)


class Thread(QThread):
    newMessageReceived = Signal(str)
    newToolpathMessageSent = Signal(float)

    def __init__(self):
        QThread.__init__(self)
        self.ReceiveMessageQueue = []
        self.SendMessageQueue = []
        self.port = None
        self.sendToolpathFlag = False

    def sendMessage(self, message):
        if (isinstance(message, str)):
            st_array = bytes(message, 'utf-8')
            self.port.write(st_array)
            self.port.flush()

    def newMessage(self, message):
        self.ReceiveMessageQueue.append(message)
        self.newMessageReceived.emit(str(message))
        if len(self.ReceiveMessageQueue) > 1000:
            self.ReceiveMessageQueue.pop(0)

    def sendToolpath(self, path):
        if self.sendToolpathFlag is not True:
            self.path = path
            self.sendToolpathFlag = True
        else:
            self.newMessage("Toolpath Already Running - Please Wait Or Disconnect")



    def run(self):
        print("Go")
        while 1:
            if self.sendToolpathFlag is False:
                tmp = self.port.readline()
                self.newMessage(tmp)
                if len(self.SendMessageQueue) > 0:
                    self.sendMessage(self.SendMessageQueue.pop(0))
            elif(self.sendToolpathFlag is True):
                path = re.sub(r'file:///', '', self.path)
                print(path)

                with open(path) as f:
                    content = f.readlines()
                    for i in range(0, len(content) - 1):
                        content[i] = content[i].strip()
                        tmp = content[i]
                        self.sendMessage(tmp)
                        self.newMessage(tmp)
                        r = str(self.port.readline())
                        self.newMessage(r)
                        while True:
                            if "End" in r or "Reached" in r:
                                # self.pValue._setNewValue(i/(len(content)-1))
                                self.newToolpathMessageSent.emit(i / (len(content) - 1))
                                break
                            else:
                                r = str(self.port.readline())
                                self.newMessage(r)
                    self.newToolpathMessageSent.emit(1)
                self.sendToolpathFlag = False


class ToolThread(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.ReceiveMessageQueue = []
        self.SendMessageQueue = []
        self.port = None
        self.path = None

    def sendMessage(self, message):
        if (isinstance(message, str)):
            st_array = bytes(message, 'utf-8')
            self.port.write(st_array)
            self.port.flush()

    def newMessage(self, message):
        self.ReceiveMessageQueue.append(message)
        self.newMessageReceived.emit(str(message))
        if len(self.ReceiveMessageQueue) > 1000:
            self.ReceiveMessageQueue.pop(0)

    def run(self):
        path = re.sub(r'file:///', '', self.path)
        print(path)

        with open(path) as f:
            content = f.readlines()
            for i in range(0, len(content) - 1):
                content[i] = content[i].strip()
                tmp = content[i]
                #self.sendMessage(tmp)
                self.SendMessageQueue.append(tmp)
                r = str(self.port.readline())
                #r = str(self.port.readline())
                print(r)
                while True:
                    if r is not None:
                        if "End" in r or "Reached" in r:
                            #self.pValue._setNewValue(i/(len(content)-1))
                            break
                        else:
                            r = str(self.port.readline())
                            #r = self.getMessage()
                    else:
                        r = self.getMessage()



class PortInterface(QThread, QObject):
    messageSent = Signal(str)
    portsList = []

    def __init__(self, rootObject, view):
        QObject.__init__(self)

        self.port = None
        self.rootObject = rootObject
        self.currentPort = None
        self.connectedFlag = False
        self.Thread = Thread()
        self.toolThread = ToolThread()
        self.zupFlag = True



        #############################################################
        #                       Timer                               #
        #############################################################
        self.portTimer = QTimer()

        #############################################################
        #                     Connections                           #
        #############################################################
        self.rootObject.upbutton_pressed.connect(self.upbutton_handler)
        self.rootObject.downbutton_pressed.connect(self.downbutton_handler)
        self.rootObject.leftbutton_pressed.connect(self.leftbutton_handler)
        self.rootObject.rightbutton_pressed.connect(self.rightbutton_handler)
        self.rootObject.stopbutton_pressed.connect(self.stopbutton_handler)
        self.rootObject.portChanged.connect(self.portsspinbox_handler)
        self.rootObject.connectbutton_pressed.connect(self.connectbutton_handler)
        self.rootObject.sendtoolpathbutton_pressed.connect(self.sendtoolpathbutton_handler)
        self.portTimer.timeout.connect(self.portTimer_timeout)
        self.Thread.newMessageReceived.connect(self.newMessageReceived_Handler)
        self.Thread.newToolpathMessageSent.connect(self.newToolpathMessageSend_Handler)
        self.rootObject.spindelbutton_pressed.connect(self.spindelButtonPressed_Handler)
        self.rootObject.zbuttonactivated.connect(self.activated_Handler)
        self.rootObject.zbuttoncanceld.connect(self.canceled_Handler)

        self.portTimer.start(500)

        self.plist = PortList()
        self.loglist = LogList()
        self.pValue = ProgressInterface(0)

        #############################################################
        #                     Root Context                          #
        #############################################################
        view.rootContext().setContextProperty("PortInterface", self.plist)
        view.rootContext().setContextProperty("LogInterface", self.loglist)
        view.rootContext().setContextProperty("ProgressInterface", self.pValue)

    def activated_Handler(self):
        print("Activated")
        if self.zupFlag is True:
            self.Thread.sendMessage("Z;0@")
        elif self.zupFlag is False:
            self.Thread.sendMessage("Z;1@")

    def canceled_Handler(self):
        print("Canceled")

    def spindelButtonPressed_Handler(self, rpm):
        self.Thread.sendMessage("CS;{}@".format(rpm))


    def newToolpathMessageSend_Handler(self, value):
        self.pValue._setNewValue(value)


    def newMessageReceived_Handler(self, message):
        self.loglist._appendLog(str(message))

    def sendtoolpathbutton_handler(self, path):
        if not self.connectedFlag:
            print("Not Connected")
            return
        self.Thread.sendToolpath(path)

    def getMessage(self):
        if len(self.Thread.ReceiveMessageQueue) > 0:
            return str(self.Thread.ReceiveMessageQueue.pop(0))
        else:
            return None

    def portsspinbox_handler(self, name):
        self.currentPort = name

    def connectbutton_handler(self):
        if self.connectedFlag:
            self.port.close()
            self.loglist._appendLog("Disconnected")
            self.connectedFlag = False
            self.Thread.sendToolpathFlag = False
            return

        if self.currentPort is not None:
            try:
                self.port = serial.Serial(self.currentPort, 115200, write_timeout=0.1)
                self.connectedFlag = True
                self.Thread.port = self.port
                self.Thread.start()
                self.loglist._appendLog("Port Connected")
            except:
                self.connectedFlag = False
                self.Thread.exit(-1)
                self.loglist._appendLog("Not Connected")

    def portTimer_timeout(self):
        list = self.serial_ports()

        self.plist._setPortList(list)

    @staticmethod
    def serial_ports():
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

    def upbutton_handler(self):
        # self.loglist._appendLog("Up")
        self.Thread.sendMessage("XYF;0;1;100@")

    def downbutton_handler(self):
        # self.loglist._appendLog("Down")
        self.Thread.sendMessage("XYF;0;-1;100@")

    def leftbutton_handler(self):
        # self.loglist._appendLog("Left")
        self.Thread.sendMessage("XYF;1;0;100@")

    def rightbutton_handler(self):
        # self.loglist._appendLog("Right")
        self.Thread.sendMessage("XYF;-1;0;100@")

    def stopbutton_handler(self):
        self.Thread.sendMessage("STOP")
        self.loglist._appendLog("Stop")


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    view = QQuickView()
    qml_file = os.path.join(os.path.dirname(__file__), 'main.qml')
    view.setSource(QUrl.fromLocalFile(os.path.abspath(qml_file)))
    view.setResizeMode(QQuickView.SizeRootObjectToView)

    rootObject = view.rootObject()
    interface = PortInterface(rootObject, view)

    if view.status() == QQuickView.Error:
        sys.exit(-1)

    view.show()
    app.exec_()
    del view
