import socket
import threading

from PyQt5.QtCore import pyqtSignal, QObject

class Client(QObject):
    sig_transfer = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.bytes = 16
        self.server_ip = None
        self.server_port = None
        self.client_socket = None
        self.listener = None
        self.connection = False

    def connect(self, server_ip: str, server_port: int) -> str:
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            print("connect - 2")
            self.client_socket.connect((self.server_ip, self.server_port))
            self.connection = True
            self.listener = threading.Thread(target=self.listen)
            self.listener.start()
        except Exception as e: return str(e)

    def disconnect(self):
        self.connection = False
        self.client_socket.sendall(str.encode('close'))
        self.client_socket.close()
        print("disconnect - 2")

    def send(self, msg: str):
        self.client_socket.sendall(str.encode(msg))

    def listen(self):
        while self.connection:
            recv = self.client_socket.recv(self.bytes)
            recv_len = len(recv)
            if recv_len > 0:
                self.sig_transfer.emit(str(recv.decode("utf-8")) + ' - {} bytes'.format(recv_len))
            else: break
        print("finished - 2")