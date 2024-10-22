from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication
from PyQt5 import QtCore, QtWidgets
import sys

from utils import logger
from Server import Server


class ServerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__terminal_memory = ""
        self.__clients_memory = ""
        self.__active = False

        self.__width = 800
        self.__height = 400
        self.__perc = (0.1, 0.8)

        self.__setup_GUI()

        self.__server = Server()
        self.__server.sig_update_terminal.connect(self.__update_terminal)
        self.__server.sig_update_clients.connect(self.__update_clients)

    def __setup_GUI(self):

        self.setWindowTitle("Server")
        self.setGeometry(0, 50, self.__width, self.__height)

        self.__set_conn()
        self.__set_terminal()
        self.__set_connection_status()
        self.__set_clients()

        self.__active_GUI_setter(active=self.__active)

    def __set_connection_status(self):

        self.__lbConnState = QtWidgets.QLabel(self)
        self.__lbConnState.setGeometry(QtCore.QRect(60, 20, 100, 15))
        self.__lbConnState.setObjectName("lbConnState")
        self.__lbConnState.setText("State")

        self.__teConnState = QtWidgets.QTextEdit(self)
        self.__teConnState.setGeometry(QtCore.QRect(60, 40, 100, 30))
        self.__teConnState.setObjectName("teConnState")
        self.__teConnState.setReadOnly(True)

    def __set_IP(self):

        self.__lbIP = QtWidgets.QLabel(self)
        self.__lbIP.setGeometry(QtCore.QRect(60, 75, 100, 15))
        self.__lbIP.setObjectName("lbIP")
        self.__lbIP.setText("Enter IP")

        self.__teIP = QtWidgets.QTextEdit(self)
        self.__teIP.setGeometry(QtCore.QRect(60, 95, 100, 30))
        self.__teIP.setObjectName("teIP")
        self.__teIP.setPlaceholderText("127.0.0.1")
        self.__teIP.setText("127.0.0.1")

    def __set_port(self):

        self.__lbPort = QtWidgets.QLabel(self)
        self.__lbPort.setGeometry(QtCore.QRect(60, 130, 100, 15))
        self.__lbPort.setObjectName("lbPort")
        self.__lbPort.setText("Enter Port")

        self.__tePort = QtWidgets.QTextEdit(self)
        self.__tePort.setGeometry(QtCore.QRect(60, 150, 100, 30))
        self.__tePort.setObjectName("tePort")
        self.__tePort.setPlaceholderText("5000")
        self.__tePort.setText("5000")

    def __set_conn(self):

        self.__set_IP()
        self.__set_port()

        self.__btnStart = QtWidgets.QPushButton(self)
        self.__btnStart.setGeometry(QtCore.QRect(60, 185, 100, 25))
        self.__btnStart.setObjectName("btnStart")
        self.__btnStart.setText("Start")
        self.__btnStart.clicked.connect(self.__start)

        self.__btnStop = QtWidgets.QPushButton(self)
        self.__btnStop.setGeometry(QtCore.QRect(60, 215, 100, 25))
        self.__btnStop.setObjectName("btnStop")
        self.__btnStop.setText("Stop")
        self.__btnStop.clicked.connect(self.__stop)

    def __set_terminal(self):

        self.__lbTerminal = QtWidgets.QLabel(self)
        self.__lbTerminal.setGeometry(QtCore.QRect(170, 20, 100, 15))
        self.__lbTerminal.setObjectName("lbTerminal")
        self.__lbTerminal.setText("Terminal")

        self.__teTerminal = QtWidgets.QTextEdit(self)
        self.__teTerminal.setGeometry(QtCore.QRect(170, 40, 460, 340))
        self.__teTerminal.setObjectName("teTerminal")
        self.__teTerminal.setReadOnly(True)

    def __set_clients(self):

        self.__lbClients = QtWidgets.QLabel(self)
        self.__lbClients.setGeometry(QtCore.QRect(int(0.8 * self.__width), int(0.025 * self.__width), 100, 15))
        self.__lbClients.setObjectName("lbClients")
        self.__lbClients.setText("Clients")

        self.__teClients = QtWidgets.QTextEdit(self)
        self.__teClients.setGeometry(QtCore.QRect(int(0.8 * self.__width), int(0.1 * self.__height), 140, 340))
        self.__teClients.setObjectName("teClients")
        self.__teClients.setReadOnly(True)

    def __active_GUI_setter(self, active) -> None:
        ''' Method to update client GUI, set it to connected or not connected view'''
        if not active:
            self.__teConnState.setTextColor(QColor(255, 0, 0))
            self.__teConnState.setText("Not active")
        else:
            self.__teConnState.setTextColor(QColor(0, 127, 0))
            self.__teConnState.setText("Active")

        self.__lbIP.setEnabled(not active)
        self.__teIP.setEnabled(not active)
        self.__lbPort.setEnabled(not active)
        self.__tePort.setEnabled(not active)

        self.__btnStart.setEnabled(not active)
        self.__btnStop.setEnabled(active)

    def __show_popup_fail(self, msg: str) -> None:

        popup = QMessageBox(self)
        popup.setWindowTitle("Info")
        popup.setText(msg)
        popup.setStandardButtons(QMessageBox.Retry | QMessageBox.Ok)
        popup.setDefaultButton(QMessageBox.Retry)
        popup.exec_()
        if popup.standardButton(popup.clickedButton()) == QMessageBox.Retry:
            self.__start()

    def __start(self):
        logger.info("Called start method")
        ip = self.__teIP.toPlainText()
        port = self.__tePort.toPlainText()
        msg = self.__server.start(server_ip=ip, server_port=port)
        if msg is not None: self.__show_popup(msg=msg, retry=False)
        else:
            self.__active = True
            self.__active_GUI_setter(active=self.__active)
            self.__update_terminal("Server has started\n")

    def __stop(self):
        logger.info("Called stop method")
        self.__server.stop()
        self.__active = False
        self.__active_GUI_setter(active=self.__active)
        self.__update_terminal("Server has stopped\n")

    def __show_popup(self, title: str = 'Info', msg: str = '', retry: bool = True) -> None:
        popup = QMessageBox(self)
        popup.setWindowTitle(title)
        popup.setText(msg)
        if retry:
            popup.setStandardButtons(QMessageBox.Retry | QMessageBox.Ok)
            popup.setDefaultButton(QMessageBox.Retry)
        else: popup.setStandardButtons(QMessageBox.Ok)
        popup.exec_()
        if popup.standardButton(popup.clickedButton()) == QMessageBox.Retry:
            self.__connect()

    @pyqtSlot(str)
    def __update_terminal(self, input: str):
        self.__terminal_memory += input
        self.__teTerminal.setText(self.__terminal_memory)
        self.__teTerminal.verticalScrollBar().setValue(self.__teTerminal.verticalScrollBar().maximum())

    @pyqtSlot(str)
    def __update_clients(self, input: str):
        operation, client = input.split(',')
        logger.info(operation)
        logger.info(client)
        logger.info(self.__clients_memory)
        if operation == 'ADD': self.__clients_memory += client
        elif operation == 'DEL':
            if client == 'ALL': self.__clients_memory = ''
            else: self.__clients_memory = self.__clients_memory.replace(client, '')
        logger.info(self.__clients_memory)
        self.__teClients.setText(self.__clients_memory)
        self.__teClients.verticalScrollBar().setValue(self.__teClients.verticalScrollBar().maximum())

    def closeEvent(self, event) -> None:
        ''' close app by X '''
        self.__stop()
        QApplication.quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ServerGUI()
    window.show()
    sys.exit(app.exec_())
