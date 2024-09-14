import socket
import threading
import os


HOST = ''
PORT = 1234

def listen_for_messages_from_server(client):
    while 1:
        message = client.recv(2048).decode('utf-8')
        username = message.split('¬')[0]
        content = message.split('¬')[1]

        print(f'[{username}] {content}')


def send_message_to_server(client):
    while 1:
        message_type = input("msg or file?: ")
        if message_type == "msg":
            message = input(("Message: "))
            client.sendall(message.encode())
        else:
            input_file = str(input("Enter file name + extension: "))

            file = open(input_file, "rb") #read bytes mode
            file_size = os.path.getsize(input_file)

            client.sendall("~received_image.png".encode())
            client.sendall(str(file_size).encode())

            data = file.read()
            client.sendall(data)
            client.send(b"<END>")


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