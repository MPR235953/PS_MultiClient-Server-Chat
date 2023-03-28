import socket
import sys
import threading

from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore, QtWidgets
import sys
from ServerGUI import ServerGUI


class Server:
    def __init__(self):
        self.gui = ServerGUI()
        self.__server_ip = 'localhost'
        self.__server_port = 2137
        self.server_socket = None
        self.listener_thread = None

    def start_GUI(self):
        self.gui.show()

    def set_param(self):
        server_address = (self.__server_ip, self.__server_port)  # set server data
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # set server socket
        self.server_socket.bind(server_address)
        self.server_socket.listen(1)  # Listen for 1 connection

        self.__update_gui()

    def start_listen(self):
        self.listener_thread = threading.Thread(target=self.listen)
        self.listener_thread.start()

    def stop_listen(self):
        self.listener_thread.join()

    def listen(self):
        while True:
            # Wait for a connection
            self.gui.teLog.append('waiting for a connection...')
            self.gui.show()
            connection, client_address = self.server_socket.accept()

            try:
                self.gui.teLog.append('connection from ' + str(client_address))

                # Receive the data in small chunks and retransmit it
                while True:
                    data = connection.recv(16)
                    self.gui.teLog.append('received: ' + str(data))
                    if data:
                        self.gui.teLog.append('sending data back to the client')
                        connection.sendall(data)
                    else:
                        self.gui.teLog.append('no more data from ' + str(client_address))
                        break

            finally:
                # Clean up the connection
                connection.close()


    def __update_gui(self):
        self.gui.teIP.setText(str(self.__server_ip))
        self.gui.tePort.setText(str(self.__server_port))


if __name__ == '__main__':

    server = Server()
    server.start_GUI()
    server.set_param()
    server.start_listen()

    sys.exit(server.gui.app.exec_())

