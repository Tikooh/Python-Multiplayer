import socket
import threading


HOST = '127.0.0.1'
PORT = 1234

def listen_for_messages_from_server(client):
    while 1:
        message = client.recv(2048).decode('utf-8')
        username = message.split('¬')[0]
        content = message.split('¬')[1]

        print(f'[{username}] {content}')


def send_message_to_server(client):
    while 1:
        message = input(("Message: "))
        client.sendall(message.encode())

def communicate_to_server(client):

    username = input("Enter username: ")

    client.sendall(username.encode())

    threading.Thread(target = listen_for_messages_from_server, args=(client, )).start()

    send_message_to_server(client)

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((HOST,PORT))
        print("successfully connected")
    except:
        print(f'Unable to connect to server {HOST}')
    
    communicate_to_server(client)

if __name__ == '__main__':
    print("hi")
    main()