from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication
from PyQt5 import QtCore, QtWidgets
import sys

from Client import Client

class ClientGUI(QMainWindow):

    def __init__(self):

        super().__init__()
        self.__width = 700
        self.__height = 400
        self.__perc = (0.1, 0.8)

        self.__setup_GUI()

        self.client = Client()

    def __setup_GUI(self):

        self.setWindowTitle("lab1")
        self.resize(self.__width, self.__height)

        self.__set_conn()
        self.__set_send()
        self.__set_receive()
        self.__set_status()

        self.__connection_GUI_setter(conn_status=False)

    def __set_IP(self):

        self.lbIP = QtWidgets.QLabel(self)
        self.lbIP.setGeometry(QtCore.QRect(60, 20, 100, 15))
        self.lbIP.setObjectName("lbIP")
        self.lbIP.setText("Enter IP")

        self.teIP = QtWidgets.QTextEdit(self)
        self.teIP.setGeometry(QtCore.QRect(60, 40, 100, 30))
        self.teIP.setObjectName("teIP")
        self.teIP.setPlaceholderText("127.0.0.1")
        self.teIP.setText("127.0.0.1")  # TODO: change it, only for debug

    def __set_port(self):

        self.lbPort = QtWidgets.QLabel(self)
        self.lbPort.setGeometry(QtCore.QRect(60, 75, 100, 15))
        self.lbPort.setObjectName("lbPort")
        self.lbPort.setText("Enter Port")

        self.tePort = QtWidgets.QTextEdit(self)
        self.tePort.setGeometry(QtCore.QRect(60, 95, 100, 30))
        self.tePort.setObjectName("tePort")
        self.tePort.setPlaceholderText("5000")
        self.tePort.setText("5000") # TODO: change it, only for debug

    def __set_conn(self):

        self.__set_IP()
        self.__set_port()

        self.btnConn = QtWidgets.QPushButton(self)
        self.btnConn.setGeometry(QtCore.QRect(60, 130, 100, 25))
        self.btnConn.setObjectName("btnConn")
        self.btnConn.setText("Connect")
        self.btnConn.clicked.connect(self.__connect)

    def __set_send(self):

        self.lbSend = QtWidgets.QLabel(self)
        self.lbSend.setGeometry(QtCore.QRect(60, 200, 100, 15))
        self.lbSend.setObjectName("lbSend")
        self.lbSend.setText("Text to send")
        self.lbSend.setDisabled(True)

        self.teSend = QtWidgets.QTextEdit(self)
        self.teSend.setGeometry(QtCore.QRect(60, 220, 200, 100))
        self.teSend.setObjectName("teSend")
        self.teSend.setDisabled(True)

        self.btnSend = QtWidgets.QPushButton(self)
        self.btnSend.setGeometry(QtCore.QRect(60, 325, 100, 25))
        self.btnSend.setObjectName("btnSend")
        self.btnSend.setText("SEND")
        self.btnSend.setCheckable(True)
        self.btnSend.clicked.connect(self.__show_popup_fail)
        self.btnSend.setDisabled(True)

    def __set_receive(self):

        self.lbReceive = QtWidgets.QLabel(self)
        self.lbReceive.setGeometry(QtCore.QRect(320, 200, 100, 15))
        self.lbReceive.setObjectName("lbReceive")
        self.lbReceive.setText("Received text")
        self.lbReceive.setDisabled(True)

        self.teReceive = QtWidgets.QTextEdit(self)
        self.teReceive.setGeometry(QtCore.QRect(320, 220, 200, 100))
        self.teReceive.setObjectName("teReceive")
        self.teReceive.setReadOnly(True)
        self.teReceive.setDisabled(True)

    def __set_status(self):

        self.lbConnState = QtWidgets.QLabel(self)
        self.lbConnState.setGeometry(QtCore.QRect(int(0.8 * self.__width), int(0.025 * self.__width), 100, 15))
        self.lbConnState.setObjectName("lbConnState")
        self.lbConnState.setText("State")

        self.teConnState = QtWidgets.QTextEdit(self)
        self.teConnState.setGeometry(QtCore.QRect(int(0.8 * self.__width), int(0.1 * self.__height), 120, 30))
        self.teConnState.setObjectName("teConnState")
        self.teConnState.setReadOnly(True)

    def __connection_GUI_setter(self, conn_status) -> None:
        ''' Method to update client GUI, set it to connected or not connected view'''
        if not conn_status:
            self.teConnState.setTextColor(QColor(255, 0, 0))
            self.teConnState.setText("Not connected")
        else:
            self.teConnState.setTextColor(QColor(0, 127, 0))
            self.teConnState.setText("Connected")

        self.lbSend.setEnabled(conn_status)
        self.lbReceive.setEnabled(conn_status)
        self.teSend.setEnabled(conn_status)
        self.teReceive.setEnabled(conn_status)
        self.btnSend.setEnabled(conn_status)

    def __show_popup_fail(self, msg: str) -> None:

        popup = QMessageBox(self)
        popup.setWindowTitle("Info")
        popup.setText(msg)
        popup.setStandardButtons(QMessageBox.Retry | QMessageBox.Ok)
        popup.setDefaultButton(QMessageBox.Retry)
        popup.exec_()
        if popup.standardButton(popup.clickedButton()) == QMessageBox.Retry:
            self.__connect()
    def __show_popup_success(self):

        msg = QMessageBox()
        msg.setWindowTitle("Info")
        msg.setText("Connection successful")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Ok)
        msg.exec_()

    def __connect(self):
        ip = self.teIP.toPlainText()
        port = int(self.tePort.toPlainText())
        msg = self.client.connect(server_ip=ip, server_port=port)
        if msg is not None: self.__show_popup_fail(msg=msg)
        else: self.__connection_GUI_setter(conn_status=True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ClientGUI()
    window.show()
    sys.exit(app.exec_())