import socket
import os
import threading

HOST, PORT = '192.168.0.64', 4999
LISTENER_LIMIT = 5

active_clients = []

def send_webserver(c):

    with open('site.html') as html:
        content = html.read()
        
    
    response = 'HTTP/1.0 200 OK\n\n' + content
    c.sendall(response.encode())

def Main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((HOST, PORT))
        print(f'Running server on HOST : {HOST} and PORT : {PORT}')
    except:
        print(f"Unable to bind to HOST : {HOST} and PORT : {PORT}")
    
    s.listen(LISTENER_LIMIT)

    c, addr = s.accept()


    send_webserver(c)



if __name__ == "__main__":
    Main()