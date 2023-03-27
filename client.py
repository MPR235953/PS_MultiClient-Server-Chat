import random
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5 import QtCore, QtWidgets
import sys

class GUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.__width = 600
        self.__height = 400
        self.__perc = (0.1, 0.8)

        self.__setup_GUI()

    def __setup_GUI(self):
        self.setWindowTitle("lab1")
        self.resize(self.__width, self.__height)

        self.__set_conn()
        self.__set_send()
        self.__set_receive()
        self.__set_status()

    def __set_IP(self):

        self.lbIP = QtWidgets.QLabel(self)
        self.lbIP.setGeometry(QtCore.QRect(60, 20, 100, 15))
        self.lbIP.setObjectName("lbIP")
        self.lbIP.setText("Enter IP")

        self.teIP = QtWidgets.QTextEdit(self)
        self.teIP.setGeometry(QtCore.QRect(60, 40, 100, 30))
        self.teIP.setObjectName("teIP")

    def __set_port(self):

        self.lbPort = QtWidgets.QLabel(self)
        self.lbPort.setGeometry(QtCore.QRect(60, 75, 100, 15))
        self.lbPort.setObjectName("lbPort")
        self.lbPort.setText("Enter Port")

        self.tePort = QtWidgets.QTextEdit(self)
        self.tePort.setGeometry(QtCore.QRect(60, 95, 100, 30))
        self.tePort.setObjectName("tePort")

    def __set_conn(self):

        self.__set_IP()
        self.__set_port()

        self.btnConn = QtWidgets.QPushButton(self)
        self.btnConn.setGeometry(QtCore.QRect(60, 130, 100, 25))
        self.btnConn.setObjectName("btnConn")
        self.btnConn.setText("SUBMIT")
        self.btnConn.clicked.connect(self.__show_popup_fail)

    def __set_send(self):

        self.lbSend = QtWidgets.QLabel(self)
        self.lbSend.setGeometry(QtCore.QRect(60, 200, 100, 15))
        self.lbSend.setObjectName("lbSend")
        self.lbSend.setText("Text to send")

        self.teSend = QtWidgets.QTextEdit(self)
        self.teSend.setGeometry(QtCore.QRect(60, 220, 200, 100))
        self.teSend.setObjectName("teSend")

        self.btnSend = QtWidgets.QPushButton(self)
        self.btnSend.setGeometry(QtCore.QRect(60, 325, 100, 25))
        self.btnSend.setObjectName("btnSend")
        self.btnSend.setText("SEND")
        self.btnSend.clicked.connect(self.__show_popup_fail)

    def __set_receive(self):

        self.lbReceive = QtWidgets.QLabel(self)
        self.lbReceive.setGeometry(QtCore.QRect(320, 200, 100, 15))
        self.lbReceive.setObjectName("lbReceive")
        self.lbReceive.setText("Received text")

        self.teReceive = QtWidgets.QTextEdit(self)
        self.teReceive.setGeometry(QtCore.QRect(320, 220, 200, 100))
        self.teReceive.setObjectName("teReceive")

    def __set_status(self):
        
        self.lbConnState = QtWidgets.QLabel(self)
        self.lbConnState.setGeometry(QtCore.QRect(int(0.8 * self.__width), int(0.025 * self.__width), 100, 15))
        self.lbConnState.setObjectName("lbConnState")
        self.lbConnState.setText("State")

        self.teConnState = QtWidgets.QTextEdit(self)
        self.teConnState.setGeometry(QtCore.QRect(int(0.8 * self.__width), int(0.1 * self.__height), 100, 30))
        self.teConnState.setObjectName("teConnState")
        self.teConnState.setEnabled(False)
        self.teConnState.setTextColor(QColor(0, 0, 0))

    def __show_popup_fail(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Info")
        msg.setText("Connection failed")
        msg.setStandardButtons(QMessageBox.Retry | QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Retry)
        msg.exec_()

    def __show_popup_success(self):
        msg = QMessageBox()
        msg.setWindowTitle("Info")
        msg.setText("Connection successful")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Ok)
        msg.exec_()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    gui = GUI()
    gui.show()
    sys.exit(app.exec_())