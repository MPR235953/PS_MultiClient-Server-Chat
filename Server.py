import ipaddress
import socket
import threading
import netifaces

import time

from PyQt5.QtCore import pyqtSignal, QObject

import utils
from utils import logger, CONFIG

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
        self.threads = []

    def start(self, server_ip: str, server_port: str):
        try:
            logger.info("Set up web stuff")
            self.__server_down = False

            self.__server_ip = server_ip
            self.__server_port = int(server_port)
            self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.__server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # to reuse address
            self.__server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # enable broadcast
            self.__server_socket.bind((self.__server_ip, self.__server_port))

            self.__connection_listener = threading.Thread(target=self.__connection_listen)
            self.__connection_listener.start()

            logger.info("Server configured")
        except Exception as e: return str(e)

    def stop(self):
        self.__server_down = True
        diss_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        diss_socket.sendto("".encode("UTF-8"), (self.__server_ip, self.__server_port))
        diss_socket.close()
        for cli in self.__client_list:
            self.__server_socket.sendto(utils.SERVER_DISCONNECT_KEY.encode("UTF-8"), cli['address'])
        self.sig_update_clients.emit(str("DEL,ALL"))
        self.__client_list = []
        self.__server_socket.close()
        logger.info("Disconnected")

    def __get_id(self) -> int | None:
        occupied_ids = set(client['id'] for client in self.__client_list)  # get all occupied ids
        avail_ids = set(i for i in range(CONFIG['client_max']))  # get all available ids based on client max
        free_ids = list(avail_ids - occupied_ids)
        if not free_ids: return None    # if there is no free ids it means that server is full
        else: return free_ids[0]  # get first free id

    def __connection_listen(self):
        logger.info("Server is listening for connection")
        while True:
            data, client_address = self.__server_socket.recvfrom(utils.CONFIG['max_transfer'])
            decoded_data = data.decode('utf-8')
            if self.__server_down:
                logger.info("Server finished listen for connection")
                return

            if client_address not in [client['address'] for client in self.__client_list]:  # in case of a new client
                id = self.__get_id()
                if id is None:  # when server is full
                    if decoded_data == utils.CLIENT_DISCONNECT_KEY: continue  # to prevent 2 the same messages
                    logger.info("Server busy")
                    self.__server_socket.sendto(utils.SERVER_BUSY_KEY.encode('utf-8'), client_address)
                    self.sig_update_terminal.emit(str("Client - {}:{} want to join, but no id available\n").format(client_address[0],client_address[1]))
                    continue
                else:
                    client_data = {
                        "id": id,
                        "address": client_address,
                    }
                    self.__client_list.append(client_data)
                    self.sig_update_terminal.emit(str("Client - #{} {}:{} joined\n").format(id, client_address[0], client_address[1]))
                    self.sig_update_clients.emit(str("ADD,#{} {}:{}\n").format(id, client_address[0], client_address[1]))

            if decoded_data == utils.CLIENT_DISCONNECT_KEY:  # delete client from list if he wants to disconnect
                for client in self.__client_list:
                    if client_address == client['address']:
                        self.__client_list.remove(client)
                        break
                self.sig_update_terminal.emit(str("Client - #{} {}:{} left\n").format(client['id'], client['address'][0], client['address'][1]))
                self.sig_update_clients.emit(str("DEL,#{} {}:{}\n").format(client['id'], client['address'][0], client['address'][1]))
            else:
                for client in self.__client_list:   # send to all
                    self.__server_socket.sendto(data, client['address'])
