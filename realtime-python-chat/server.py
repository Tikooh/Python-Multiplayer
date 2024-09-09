import socket
import threading

HOST = '127.0.0.1'
PORT = '1234' # use any port between 0 to 65535
LISTENER_LIMIT = 5 # amount of connections

def main():
    server = socket.socket(socket.AF.INET, socket.SOCK_STREAM)

    try:
        server.bind((HOST, PORT))
    except:
        raise(f'Unable to bind to host {HOST} and port {PORT}')

    server.listen(LISTENER_LIMIT)

    while 1:
        client, address = server.accept() # client represents socket of client

if __name__ == '__main__':
    main()