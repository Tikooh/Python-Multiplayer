import socket
import threading

# hostname = socket.gethostname()
# HOST = socket.gethostbyname(hostname)

# print(f'running on host {HOST}')
HOST = '192.168.0.64'
PORT = 1234 # use any port between 0 to 65535
LISTENER_LIMIT = 5 # amount of connections

active_clients = [] #list of all connected users

#function is threaded and listens to upcoming messages from a client
def listen_for_messages(client, username):

    while 1:
        response = client.recv(2048).decode()
        print(f'Response is {response}')

        if response[0] == "~":
            file_size = client.recv(2048).decode()
            if file_size == 0:
                print("File is empty")
            else:
                print(f'File size is {file_size}')

            file = open(response, "wb")
            file_bytes = b""

            done = False
            while not done:
                data = client.recv(2048)
                if file_bytes[-5:] == b"<END>": #once <END> reachedall data received for response
                    print("All data received")
                    done = True
                else:
                    file_bytes += data
            
            file.write(file_bytes)
            file.close()

        else:
            final_msg = username + '¬' + response
            send_messages_to_all(final_msg)


def send_message_to_client(client, message):

    client.sendall(message.encode())

def send_messages_to_all(message):
    print(active_clients)
    for user in active_clients:

        send_message_to_client(user[1], message)

#function to handle client

def client_handler(client):
    #server will listen for client message that will contain username
    

    while 1:
        username = client.recv(2048).decode('utf-8')
        if username != '':
            active_clients.append((username, client))
            break
        else:    
            print("Client username is empty")

    threading.Thread(target = listen_for_messages, args=(client, username, )).start()

    

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((HOST, PORT))
        print(f'Running the server on {HOST}')
    except:
        print(f'Unable to bind to host {HOST} and port {PORT}')

    server.listen(LISTENER_LIMIT)

    while 1:
        client, address = server.accept() # client represents socket of client

        threading.Thread(target=client_handler, args=(client, )).start()

if __name__ == '__main__':
    main()