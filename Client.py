import socket
import sys
import threading

from PyQt5.QtCore import pyqtSignal, QObject

'''import threading
import time

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore, QtWidgets

from ClientGUI import ClientGUI'''
'''
class Client:
    def __init__(self, gui):
        self.gui = gui
        self.__server_ip = None
        self.__server_port = None
        self.server_socket = None
        self.conn_listener = None

    def start_listen(self):
        self.listener_thread = threading.Thread(target=self.listen)
        self.listener_thread.start()

    def listen(self):
        while True:
            if gui.btnConn.isChecked():
                self.__server_ip = self.gui.teIP.toPlainText()
                self.__server_port = self.gui.tePort.toPlainText()
                break
        self.listener_thread.join()
        print(self.__server_ip)
        print(self.__server_port)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    gui = ClientGUI()
    gui.show()

    client = Client(gui)
    #client.start_GUI()
    #client.set_param()
    client.start_listen()
    # server.stop_listen()

    sys.exit(app.exec_())

'''

class Client(QObject):
    sig_transfer = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.server_ip = None
        self.server_port = None
        self.client_socket = None
        self.listener = threading.Thread(target=self.listen)

    def connect(self, server_ip: str, server_port: int) -> str:
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((self.server_ip, self.server_port))
            self.listener.start()
        except Exception as e: return str(e)

    def send(self, msg: str):
        self.client_socket.sendall(str.encode(msg))

    def listen(self):
        while True:
            recv = self.client_socket.recv(16)
            self.sig_transfer.emit(str(recv.decode("utf-8")))
            break



if __name__ == '__main__':
    pass
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 7)
        client_socket.connect(server_address)
        print('Connected to {} on port {}'.format(server_address[0], server_address[1]))
    except:
        print("Connection not found :(")
        exit(1)

    try:
        while(1):
            message = input("Enter message: ")
            if message == 'q': break
            print('sending "%s"' % message)
            client_socket.sendall(str.encode(message))

            # Look for the response
            amount_received = 0
            amount_expected = len(message)

            while amount_received < amount_expected:
                data = client_socket.recv(16)
                amount_received += len(data)
                print(sys.stderr, 'received "%s"' % data)

    finally:
        print(sys.stderr, 'closing socket')
        client_socket.close()