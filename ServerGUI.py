import sys

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore, QtWidgets

class ServerGUI(QMainWindow):

    def __init__(self):

        self.app = QtWidgets.QApplication(sys.argv)
        super().__init__()
        self.__width = 600
        self.__height = 400
        self.__perc = (0.1, 0.8)

        self.teLog = None
        self.teIP = None
        self.tePort = None

        self.__setup_GUI()

    def __setup_GUI(self):

        self.setWindowTitle("lab1")
        self.resize(self.__width, self.__height)

        self.__set_logs()
        self.__set_IP()
        self.__set_port()

    def __set_logs(self):

        self.lbLog = QtWidgets.QLabel(self)
        self.lbLog.setGeometry(QtCore.QRect(60, 20, 100, 15))
        self.lbLog.setObjectName("lbLog")
        self.lbLog.setText("Server Logs")

        self.teLog = QtWidgets.QTextEdit(self)
        self.teLog.setGeometry(QtCore.QRect(60, 40, 300, 300))
        self.teLog.setObjectName("teLog")
        self.teLog.setEnabled(False)
        self.teLog.setTextColor(QColor(0, 0, 0))

    def __set_IP(self):

        self.lbIP = QtWidgets.QLabel(self)
        self.lbIP.setGeometry(QtCore.QRect(400, 20, 100, 15))
        self.lbIP.setObjectName("lbIP")
        self.lbIP.setText("IP")

        self.teIP = QtWidgets.QTextEdit(self)
        self.teIP.setGeometry(QtCore.QRect(400, 40, 100, 30))
        self.teIP.setObjectName("teIP")
        self.teIP.setEnabled(False)
        self.teIP.setTextColor(QColor(0, 0, 0))

    def __set_port(self):

        self.lbPort = QtWidgets.QLabel(self)
        self.lbPort.setGeometry(QtCore.QRect(400, 75, 100, 15))
        self.lbPort.setObjectName("lbPort")
        self.lbPort.setText("Port")

        self.tePort = QtWidgets.QTextEdit(self)
        self.tePort.setGeometry(QtCore.QRect(400, 95, 100, 30))
        self.tePort.setObjectName("tePort")
        self.tePort.setEnabled(False)
        self.tePort.setTextColor(QColor(0, 0, 0))
