import sys
import glob
import serial
import time
import PyQt5
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QThread 
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QTimer, QEventLoop

comm_dict = "__Start_Session__", "__End_Session__","__Send_Toolpath__", "__Empfang_Besteatigt__",  "__Receive_Error__", "__Receive_Successfull__"

comm_enum = {"Start_Session" : 0, "End_Session" : 1, "Start_Homing" : 2, "Send_Toolpath" : 3, "Empfang_Bestaetigt" : 4, "Receive_Error" : 5, "Receive_Successfull" : 6, "No_Message" : -1}

class Listener_Helper_Class(QThread):


    sessionStarted = QtCore.pyqtSignal()
    sessionEnded = QtCore.pyqtSignal()
    
    homing_flag = False

    def __init__(self, port):
        QThread.__init__(self)  # Ruft den Mutterklassenkonstruktor auf
        self.port = port
    

    def __del__(self):
        self.wait()

    def doHoming(self):
        self.homing_flag = True
    
    def startHoming(self):
        self.sessionStarted.emit()
        self.port.sendMessage(b"__Start_Session__")

        while 1:
            if self.port.messagesAvailable:
                print(self.port.getMessage())
                break
        
        self.port.sendMessage(b"__Start_Homing__")

        while 1:
            if self.port.messagesAvailable:
                tmp = self.port.getMessage()
                if tmp == "__End_Session__\r\n":
                    print("Homing Successfull")
                    break
                else:
                    print(tmp)

        self.port.homing_flag = False
        self.homing_flag = False
        self.sessionEnded.emit()
    

    def run(self):
        while 1:
            if self.homing_flag == True:
                self.startHoming()
            else:
                self.sleep(1)



class Listener_Thread(QThread):

    newMessage = QtCore.pyqtSignal(str)
    readTimeout = QtCore.pyqtSignal()



    lastMessage = ""
    receiveBuffer = []

    write_flag = False
    read_flag = False
    homing_flag = False
    messagesAvailable = False

    def __init__(self, port, read_timeout=None, write_timeout=None):
        QThread.__init__(self)  # Ruft den Mutterklassenkonstruktor auf
        self.port = serial.Serial(port, 115200, timeout=read_timeout, write_timeout=write_timeout)
        self.resetTimer = QTimer()
        self.resetTimer.timeout.connect(self.doReset)
        self.sleep(1)
        self.helper = helper = Listener_Helper_Class(self)
        self.helper.start()


    def __del__(self):
        self.wait()

    def sendMessage(self, str):
        self.sendBuffer = str
        self.port.write(str)
        self.port.flush()
    
    def doHoming(self):
        self.homing_flag = True
        self.helper.doHoming()
    
    def doReset(self):
        self.homing_flag = False
        print("Timeout")

    def getMessage(self):
        if self.receiveBuffer:
            if len(self.receiveBuffer) <= 1:
                self.messagesAvailable = False
            return self.receiveBuffer.pop(0)
        else:
            self.messagesAvailable = False
            return None


    def run(self):
        # Listener Code Here
        while(1):
            self.lastMessage = self.port.readline()
            if self.lastMessage:
                self.receiveBuffer.append(self.lastMessage.decode('ascii'))

            if self.receiveBuffer:
                self.messagesAvailable = True
            else:
                self.messagesAvailable = False



def list_serial_ports():

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

def newMessageHandler(message):
    print(message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    serial_ports_list = list_serial_ports()
    if not serial_ports_list:
        print("No Ports available")
    else:
        # loop = QEventLoop()
        port = Listener_Thread(serial_ports_list[0], read_timeout=7)
        port.start()
        port.doHoming()
        port.doToolpath()
        while 1:
            time.sleep(1)

        print("End reached")





            