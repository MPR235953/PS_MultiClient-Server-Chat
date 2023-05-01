import socket
import threading

import utils
from utils import logger, CONFIG
from PyQt5.QtCore import pyqtSignal, QObject

class Client(QObject):
    sig_update_receiver = pyqtSignal(str)
    sig_handle_event = pyqtSignal(str, bool)
    def __init__(self):
        super().__init__()
        self.__server_ip = None
        self.__server_port = None
        self.__client_socket = None
        self.__listener = None
        self.__connection = False

    def get_connection_status(self):
        return self.__connection

    def connect(self, server_ip: str, server_port: str) -> str:
        try:
            logger.info("Set up web stuff")
            self.__server_ip = server_ip
            self.__server_port = int(server_port)
            self.__client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            # check connection with UDP server
            test_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            test_socket.settimeout(utils.CONFIG['timeout'])
            test_socket.sendto(str.encode(utils.CLIENT_TEST_KEY), (self.__server_ip, self.__server_port))
            _, _ = test_socket.recvfrom(utils.CONFIG['max_transfer'])
            test_socket.close()

            logger.info("Try to connect to server")
            self.__connection = True
            self.__listener = threading.Thread(target=self.__listen)
            self.__listener.start()
            self.__client_socket.sendto(str.encode(utils.CLIENT_CONNECT_KEY), (self.__server_ip, self.__server_port))
            logger.info("Connected to server - start listen ")
        except TimeoutError: return str("Server not ready")
        except Exception as e: return str(e)

    def disconnect(self):
        self.__connection = False
        self.__client_socket.sendto(str.encode(utils.CLIENT_DISCONNECT_KEY), (self.__server_ip, self.__server_port))
        self.__client_socket.close()
        logger.info("Disconnected")

    def send(self, msg: str):
        self.__client_socket.sendto(str.encode(msg), (self.__server_ip, self.__server_port))
        logger.info("Message was sent")

    def __listen(self):
        while self.__connection:
            try:
                recv, addr = self.__client_socket.recvfrom(utils.CONFIG['max_transfer'])
                recv_len = len(recv)
                if recv_len > 0:
                    if recv.decode("utf-8") == utils.SERVER_DISCONNECT_KEY:
                        self.sig_handle_event.emit("Server is down", False)
                        break
                    elif recv.decode("utf-8") == utils.SERVER_BUSY_KEY:
                        self.sig_handle_event.emit("Server is busy", True)
                        break
                    self.sig_update_receiver.emit(str(recv.decode("utf-8")) + ' - {} bytes'.format(recv_len))
                else: break
            except Exception as e:
                break
        logger.info("Listener task was finished")
