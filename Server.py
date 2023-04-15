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
    sig_terminal = pyqtSignal(str)
    sig_clients = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.__server_ip = None
        self.__server_port = None
        self.__server_socket = None
        self.__connection_listener = None
        self.__transfer_listener = None
        self.__client_list = []

    # TODO: add exception ? YES
    # TODO: handle with different IP than localhost
    def start(self, server_ip: str, server_port: int) -> str:
        logger.info("Set up web stuff")
        self.__server_ip = server_ip
        self.__server_port = server_port
        self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # to reuse address
        self.__server_socket.bind((self.__server_ip, self.__server_port))
        self.__server_socket.listen(cfg['max_connect_requests'])

        self.__connection_listener = threading.Thread(target=self.__connection_listen)
        self.__connection_listener.start()
        self.__transfer_listener = threading.Thread(target=self.__transfer_listen)
        self.__transfer_listener.start()
        logger.info("Server configured")
        return None  # tmp

    # TODO: disconn all user when server is down or stopped
    def stop(self):
        self.__server_socket.close()
        logger.info("Disconnected")

    def __connection_listen(self):
        logger.info("Server is listening for connection")
        while True:
            connection, client_address = self.__server_socket.accept()
            id = len(self.__client_list)
            client_data = {
                "id": id,
                "address": client_address,
                "connection": connection
            }
            self.__client_list.append(client_data)
            self.sig_terminal.emit(str("Client - #{} {}:{} joined\n").format(id, client_address[0], client_address[1]))
            self.sig_clients.emit(str("ADD,#{} {}:{}\n").format(id, client_address[0], client_address[1]))

    # TODO: maybe simplify ?
    def __transfer_listen(self):
        logger.info("Server is ready to transfer data")
        while True:
            for client in self.__client_list:
                time.sleep(cfg['transfer_delay'])
                data = client['connection'].recv(16)
                decoded_data = data.decode('utf-8')
                if decoded_data != 'close':
                    logger.info("Data: | {} | from client: | {} |".format(decoded_data, '#' + str(client['id']) + ' ' + client['address'][0] + ' ' + str(client['address'][1])))
                    for cli in self.__client_list:
                        cli['connection'].sendall(('#' + str(cli['id']) + ' ' + decoded_data).encode('utf-8'))
                else:
                    logger.info("Data: | {} | from client: | {} |".format(decoded_data, '#' + str(client['id']) + ' ' + client['address'][0] + ' ' + str(client['address'][1])))
                    client['connection'].sendall(('#' + str(client['id']) + ' ' + decoded_data + ' disconnected').encode('utf-8'))
                    self.sig_terminal.emit(str("Client - #{} {}:{} left\n").format(client['id'], client['address'][0], client['address'][1]))
                    self.sig_clients.emit(str("DEL,#{} {}:{}\n").format(client['id'], client['address'][0], client['address'][1]))
                    self.__client_list.remove(client)
                    logger.info(self.__client_list)
                    break



