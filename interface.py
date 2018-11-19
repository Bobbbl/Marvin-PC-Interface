import sys
import glob
import serial
import time
import PyQt5
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QThread 

comm_dict = "__Start_Session__", "__End_Session__","__Send_Toolpath__", "__Empfang_Besteatigt__",  "__Receive_Error__", "__Receive_Successfull__"

comm_enum = {"Start_Session" : 0, "End_Session" : 1, "Start_Homing" : 2, "Send_Toolpath" : 3, "Empfang_Bestaetigt" : 4, "Receive_Error" : 5, "Receive_Successfull" : 6, "No_Message" : -1}


class Listener_Thread(QThread):

    newMessage = QtCore.Signal(str)
    readTimeout = QtCore.Signal()
    write_flag = False
    read_flag = False

    def __init__(self, port, read_timeout, write_timeout):
        QThread.__init__(self)  # Ruft den Mutterklassenkonstruktor auf
        self.port = serial.Serial(port, 115200, timeout=read_timeout, write_timeout=write_timeout)
        self.seep(1)


    def __del__(self):
        self.wait()

    @QtCore.Slot(str)
    def sendMessage(str)
        self.sendBuffer = str
        self.write_flag = True
    
    @QtCore.Slot()
    def receiveMessage():
        self.read_flag = True

    def run(self):
        # Listener Code Here
        while(1):
            if write_flag == True:
                self.port.write(write_message)
                self.write_flag = False
            elif read_flag == True:
                msg = self.port.readline()
                self.write_flag = False
                if not msg:
                    self.readTimeout.emit()



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


if __name__ == '__main__':
    serial_ports_list = list_serial_ports()
    if not serial_ports_list:
        print("No Ports available")
    else:
        #port.write(comm_dict[comm_enum["Start_Session"]].encode())
        port.write(b"__Start_Session__")


            