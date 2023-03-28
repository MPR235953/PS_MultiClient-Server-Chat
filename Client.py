import socket
import sys

if __name__ == '__main__':
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 2137)
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