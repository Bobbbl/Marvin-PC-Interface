import sys
import glob
import serial
import time
import PyQt5
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QThread 
from PyQt5.QtWidgets import QApplication, QWidget

comm_dict = "__Start_Session__", "__End_Session__","__Send_Toolpath__", "__Empfang_Besteatigt__",  "__Receive_Error__", "__Receive_Successfull__"

comm_enum = {"Start_Session" : 0, "End_Session" : 1, "Start_Homing" : 2, "Send_Toolpath" : 3, "Empfang_Bestaetigt" : 4, "Receive_Error" : 5, "Receive_Successfull" : 6, "No_Message" : -1}


class Listener_Thread(QThread):

    newMessage = QtCore.pyqtSignal(str)
    readTimeout = QtCore.pyqtSignal()
    write_flag = False
    read_flag = False

    def __init__(self, port, read_timeout=None, write_timeout=None):
        QThread.__init__(self)  # Ruft den Mutterklassenkonstruktor auf
        self.port = serial.Serial(port, 115200, timeout=read_timeout, write_timeout=write_timeout)
        self.sleep(1)


    def __del__(self):
        self.wait()

    def sendMessage(self, str):
        self.sendBuffer = str
        self.write_flag = True
    
    def receiveMessage(self):
        self.read_flag = True

    def run(self):
        # Listener Code Here
        while(1):
            if self.write_flag == True:
                self.port.write(self.sendBuffer)
                self.write_flag = False
            elif self.read_flag == True:
                msg = self.port.readline()
                if not msg:
                    self.readTimeout.emit()
                    continue
                self.newMessage.emit(str(msg))
                if(msg.decode('ascii') == "__End_Session__\r\n"):
                    self.read_flag = False



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
        port = Listener_Thread(serial_ports_list[0], read_timeout=1)
        time.sleep(1)
        port.newMessage.connect(newMessageHandler)
        port.start()
        port.sendMessage(b"__Start_Session__")
        port.receiveMessage()
        
    sys.exit(app.exec_())





            