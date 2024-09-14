import sys
import socket
import selectors
import types

sel = selectors.DefaultSelector()
HOST, PORT = '', 4999

messages = [b"Message 1 from client.", b"Message 2 from client."]
#https://stackoverflow.com/questions/67891439/how-exactly-does-registering-and-selecting-a-socket-work


def service_connection(key, mask):
    sock = key.fileobj
    data = key.data #data in simplenamespace

    if mask and selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            print(f'Received data from connection {data.connid}')
            data.recv_total += len(recv_data)
        
        if not recv_data or data.recv_total == data.msg_total: #if whole message received or no data received
            print(f'cloing connection')
            sel.unregister(sock)
            sock.close()
        
        if mask and selectors.EVENT_WRITE:
            if not data.outb and data.messages:
                data.outb = messages.pop(0)
            
            if data.outb:
                sent= sock.send(data.outb)
                data.outb = data.outb[sent:] #can i just use sendall here?

        
def start_connection(num_conns):
    for i in range(0, num_conns): #num_conns read from command line?
        connid = i + 1
        print(f'Starting connection from {connid} to {HOST}')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setblocking(False)
        s.connect_ex((HOST, PORT)) #connect_ex avoids blocking io error
        events = selectors.EVENT_READ or selectors.EVENT_WRITE

        data = types.SimpleNamespace(
            connid=connid,
            msg_total=sum(len(m) for m in messages),
            recv_total=0,
            messages=messages.copy(),
            outb=b"",
        )
        sel.register(s, events, data=data)