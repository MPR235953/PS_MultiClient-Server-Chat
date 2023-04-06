from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication
from PyQt5 import QtCore, QtWidgets
import sys

from Logger import logger
from Client import Client

class ClientGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__receiver_memory = ""
        self.__connection = False

        self.__width = 700
        self.__height = 400
        self.__perc = (0.1, 0.8)

        self.__setup_GUI()

        self.__client = Client()
        self.__client.sig_transfer.connect(self.__receive)

    def __setup_GUI(self):

        self.setWindowTitle("Client")
        self.resize(self.__width, self.__height)

        self.__set_conn()
        self.__set_send()
        self.__set_receive()
        self.__set_status()

        self.__connection_GUI_setter(connection=self.__connection)

    def __set_IP(self):

        self.__lbIP = QtWidgets.QLabel(self)
        self.__lbIP.setGeometry(QtCore.QRect(60, 20, 100, 15))
        self.__lbIP.setObjectName("lbIP")
        self.__lbIP.setText("Enter IP")

        self.__teIP = QtWidgets.QTextEdit(self)
        self.__teIP.setGeometry(QtCore.QRect(60, 40, 100, 30))
        self.__teIP.setObjectName("teIP")
        self.__teIP.setPlaceholderText("127.0.0.1")
        self.__teIP.setText("127.0.0.1")  # TODO: change it, only for debug

    def __set_port(self):

        self.__lbPort = QtWidgets.QLabel(self)
        self.__lbPort.setGeometry(QtCore.QRect(60, 75, 100, 15))
        self.__lbPort.setObjectName("lbPort")
        self.__lbPort.setText("Enter Port")

        self.__tePort = QtWidgets.QTextEdit(self)
        self.__tePort.setGeometry(QtCore.QRect(60, 95, 100, 30))
        self.__tePort.setObjectName("tePort")
        self.__tePort.setPlaceholderText("5000")
        self.__tePort.setText("5000") # TODO: change it, only for debug

    def __set_conn(self):

        self.__set_IP()
        self.__set_port()

        self.__btnConn = QtWidgets.QPushButton(self)
        self.__btnConn.setGeometry(QtCore.QRect(60, 130, 100, 25))
        self.__btnConn.setObjectName("btnConn")
        self.__btnConn.setText("Connect")
        self.__btnConn.clicked.connect(self.__connect)

        self.__btnDisconn = QtWidgets.QPushButton(self)
        self.__btnDisconn.setGeometry(QtCore.QRect(60, 160, 100, 25))
        self.__btnDisconn.setObjectName("btnDisconn")
        self.__btnDisconn.setText("Disconnect")
        self.__btnDisconn.clicked.connect(self.__disconnect)

    def __set_send(self):

        self.__lbSend = QtWidgets.QLabel(self)
        self.__lbSend.setGeometry(QtCore.QRect(60, 200, 100, 15))
        self.__lbSend.setObjectName("lbSend")
        self.__lbSend.setText("Text to send")
        self.__lbSend.setDisabled(True)

        self.__teSend = QtWidgets.QTextEdit(self)
        self.__teSend.setGeometry(QtCore.QRect(60, 220, 200, 100))
        self.__teSend.setObjectName("teSend")
        self.__teSend.setDisabled(True)

        self.__btnSend = QtWidgets.QPushButton(self)
        self.__btnSend.setGeometry(QtCore.QRect(60, 325, 100, 25))
        self.__btnSend.setObjectName("btnSend")
        self.__btnSend.setText("SEND")
        self.__btnSend.setCheckable(True)
        self.__btnSend.clicked.connect(self.__send)
        self.__btnSend.setDisabled(True)

    def __set_receive(self):

        self.__lbReceive = QtWidgets.QLabel(self)
        self.__lbReceive.setGeometry(QtCore.QRect(320, 200, 100, 15))
        self.__lbReceive.setObjectName("lbReceive")
        self.__lbReceive.setText("Received text")
        self.__lbReceive.setDisabled(True)

        self.__teReceive = QtWidgets.QTextEdit(self)
        self.__teReceive.setGeometry(QtCore.QRect(320, 220, 360, 100))
        self.__teReceive.setObjectName("teReceive")
        self.__teReceive.setReadOnly(True)
        self.__teReceive.setDisabled(True)

    def __set_status(self):

        self.__lbConnState = QtWidgets.QLabel(self)
        self.__lbConnState.setGeometry(QtCore.QRect(int(0.8 * self.__width), int(0.025 * self.__width), 100, 15))
        self.__lbConnState.setObjectName("lbConnState")
        self.__lbConnState.setText("State")

        self.__teConnState = QtWidgets.QTextEdit(self)
        self.__teConnState.setGeometry(QtCore.QRect(int(0.8 * self.__width), int(0.1 * self.__height), 120, 30))
        self.__teConnState.setObjectName("teConnState")
        self.__teConnState.setReadOnly(True)

    def __connection_GUI_setter(self, connection) -> None:
        ''' Method to update client GUI, set it to connected or not connected view'''
        if not connection:
            self.__teConnState.setTextColor(QColor(255, 0, 0))
            self.__teConnState.setText("Not connected")
        else:
            self.__teConnState.setTextColor(QColor(0, 127, 0))
            self.__teConnState.setText("Connected")

        self.__lbSend.setEnabled(connection)
        self.__lbReceive.setEnabled(connection)
        self.__teSend.setEnabled(connection)
        self.__teReceive.setEnabled(connection)
        self.__btnSend.setEnabled(connection)
        self.__lbIP.setEnabled(not connection)
        self.__teIP.setEnabled(not connection)
        self.__lbPort.setEnabled(not connection)
        self.__tePort.setEnabled(not connection)

        self.__btnConn.setEnabled(not connection)
        self.__btnDisconn.setEnabled(connection)

        self.__receiver_memory = ""
        self.__teReceive.setText(self.__receiver_memory)

    def __show_popup_fail(self, msg: str) -> None:

        popup = QMessageBox(self)
        popup.setWindowTitle("Info")
        popup.setText(msg)
        popup.setStandardButtons(QMessageBox.Retry | QMessageBox.Ok)
        popup.setDefaultButton(QMessageBox.Retry)
        popup.exec_()
        if popup.standardButton(popup.clickedButton()) == QMessageBox.Retry:
            self.__connect()

    def __connect(self):
        logger.info("Called connect method")
        ip = self.__teIP.toPlainText()
        port = int(self.__tePort.toPlainText())
        msg = self.__client.connect(server_ip=ip, server_port=port)
        if msg is not None: self.__show_popup_fail(msg=msg)
        else:
            self.__connection = True
            self.__connection_GUI_setter(connection=self.__connection)

    def __disconnect(self):
        logger.info("Called disconnect method")
        self.__client.disconnect()
        self.__connection = False
        self.__connection_GUI_setter(connection=self.__connection)

    def __send(self):
        msg = self.__teSend.toPlainText()
        self.__client.send(msg)
        self.__teSend.setText("")  # clear QTextEdit after send

    @pyqtSlot(str)
    def __receive(self, msg: str):
        self.__receiver_memory += msg + '\n'
        self.__teReceive.setText(self.__receiver_memory)
        self.__teReceive.verticalScrollBar().setValue(self.__teReceive.verticalScrollBar().maximum())

    def __closeEvent(self, event) -> None:
        ''' close app by X '''
        self.__client.disconnect()
        QApplication.quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ClientGUI()
    window.show()
    sys.exit(app.exec_())