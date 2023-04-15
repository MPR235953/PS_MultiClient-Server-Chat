import socket
import threading

import time

from PyQt5.QtCore import pyqtSignal, QObject

import utils
from utils import logger, CONFIG

class ClientData:
    def __init__(self, id: int, ip: str, port: int):
        self.id = id
        self.ip = ip
        self.port = port

class Server(QObject):
    sig_update_terminal = pyqtSignal(str)
    sig_update_clients = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.__server_ip = None
        self.__server_port = None
        self.__server_socket = None
        self.__connection_listener = None
        self.__transfer_listener = None
        self.__client_list = []
        self.__server_down = False

    # TODO: add exception ? YES
    # TODO: handle with different IP than localhost
    def start(self, server_ip: str, server_port: int):
        logger.info("Set up web stuff")
        self.__server_down = False

        self.__server_ip = server_ip
        self.__server_port = server_port
        self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # to reuse address
        self.__server_socket.bind((self.__server_ip, self.__server_port))
        self.__server_socket.listen(CONFIG['max_connect_requests'])

        self.__connection_listener = threading.Thread(target=self.__connection_listen)
        self.__connection_listener.start()
        self.__transfer_listener = threading.Thread(target=self.__transfer_listen)
        self.__transfer_listener.start()
        logger.info("Server configured")

    # TODO: refactor
    def stop(self):
        self.__server_down = True
        diss_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        diss_socket.connect((self.__server_ip, self.__server_port))
        diss_socket.close()
        for cli in self.__client_list:
            cli['connection'].sendall(utils.SERVER_DISCONNECT_CLIENT_KEY.encode('utf-8'))
        self.sig_update_clients.emit(str("DEL,ALL"))
        self.__client_list = []
        self.__server_socket.close()
        logger.info("Disconnected")

    def __get_id(self) -> int | None:
        occupied_ids = set(client['id'] for client in self.__client_list)  # get all occupied ids
        avail_ids = set(i for i in range(CONFIG['client_max']))  # get all available ids based on client max
        free_ids = list(avail_ids - occupied_ids)
        if not free_ids: return None
        else: return free_ids[0]  # get first free id

    # TODO: fix handling with ID's
    # TODO: refactor logger infos
    def __connection_listen(self):
        logger.info("Server is listening for connection")
        while True:
            connection, client_address = self.__server_socket.accept()
            if self.__server_down:
                logger.info("Server finished listen for connection")
                return
            id = self.__get_id()
            client_data = {
                "id": id,
                "address": client_address,
                "connection": connection
            }
            if id is None:  # when server is full
                client_data['connection'].sendall(utils.SERVER_DISCONNECT_CLIENT_KEY.encode('utf-8'))
                continue
            self.__client_list.append(client_data)
            self.sig_update_terminal.emit(str("Client - #{} {}:{} joined\n").format(id, client_address[0], client_address[1]))
            self.sig_update_clients.emit(str("ADD,#{} {}:{}\n").format(id, client_address[0], client_address[1]))

    # TODO: maybe simplify ?
    # TODO: Broken pipe when disconnect user which wait for send message
    def __transfer_listen(self):
        logger.info("Server is ready to transfer data")
        while True:
            for client in self.__client_list:
                time.sleep(CONFIG['transfer_delay'])
                data = client['connection'].recv(16)
                if self.__server_down:
                    logger.info("Server finished listen for transfer")
                    return
                decoded_data = data.decode('utf-8')
                if decoded_data != utils.CLIENT_DISCONNECT_FROM_SERVER_KEY:
                    logger.info("Data: | {} | from client: | {} |".format(decoded_data, '#' + str(client['id']) + ' ' + client['address'][0] + ' ' + str(client['address'][1])))
                    for cli in self.__client_list:
                        cli['connection'].sendall(('#' + str(client['id']) + ' ' + decoded_data).encode('utf-8'))
                else:
                    logger.info("Data: | {} | from client: | {} |".format(decoded_data, '#' + str(client['id']) + ' ' + client['address'][0] + ' ' + str(client['address'][1])))
                    self.sig_update_terminal.emit(str("Client - #{} {}:{} left\n").format(client['id'], client['address'][0], client['address'][1]))
                    self.sig_update_clients.emit(str("DEL,#{} {}:{}\n").format(client['id'], client['address'][0], client['address'][1]))
                    self.__client_list.remove(client)
                    logger.info(self.__client_list)
                    break



