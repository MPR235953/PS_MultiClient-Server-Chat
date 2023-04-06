import socket
import threading

import time

from PyQt5.QtCore import pyqtSignal, QObject

from utils import logger, cfg


class ClientData:
    def __init__(self, id: int, ip: str, port: int):
        self.id = id
        self.ip = ip
        self.port = port

class Server(QObject):
    sig_transfer = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.__server_ip = None
        self.__server_port = None
        self.__server_socket = None
        self.__listener = None
        self.__client_data_list = []

    # TODO: add exception ?
    def start(self, server_ip: str, server_port: int) -> str:
        logger.info("Set up web stuff")
        self.__server_ip = server_ip
        self.__server_port = server_port
        self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server_socket.bind((self.__server_ip, self.__server_port))
        self.__server_socket.listen(cfg['max_connect_requests'])
        logger.info("Server configured")
        return None  # tmp

    def stop(self):
        self.__server_socket.close()
        logger.info("Disconnected")



