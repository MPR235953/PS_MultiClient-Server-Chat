import socket
import threading

from utils import logger, cfg
from PyQt5.QtCore import pyqtSignal, QObject

class Client(QObject):
    # TODO: try to use only one signal
    sig_transfer = pyqtSignal(str)
    sig_server_down = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.__server_ip = None
        self.__server_port = None
        self.__client_socket = None
        self.__listener = None
        self.__connection = False

    def get_connection_status(self):
        return self.__connection

    def connect(self, server_ip: str, server_port: int) -> str:
        logger.info("Set up web stuff")
        self.__server_ip = server_ip
        self.__server_port = server_port
        self.__client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            logger.info("Try to connect to server")
            self.__client_socket.connect((self.__server_ip, self.__server_port))
            self.__connection = True
            self.__listener = threading.Thread(target=self.__listen)
            self.__listener.start()
            logger.info("Connected to server - start listen ")
        except Exception as e: return str(e)

    def disconnect(self):
        self.__connection = False
        self.__client_socket.sendto(str.encode('close'), (self.__server_ip, self.__server_port))
        self.__client_socket.close()
        logger.info("Disconnected")

    def send(self, msg: str):
        self.__client_socket.sendto(str.encode(msg), (self.__server_ip, self.__server_port))
        logger.info("Message was sent")

    # TODO: change disconn sig text
    def __listen(self):
        while self.__connection:
            recv = self.__client_socket.recv(cfg['max_transfer'])
            recv_len = len(recv)
            if recv_len > 0:
                if recv.decode("utf-8") == 'close':
                    self.sig_server_down.emit("Server down")
                    break
                self.sig_transfer.emit(str(recv.decode("utf-8")) + ' - {} bytes'.format(recv_len))
            else: break
        logger.info("Listener task was finished")