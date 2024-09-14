import sys
import socket
import selectors
#https://docs.python.org/3/library/selectors.html

import types

sel = selectors.DefaultSelector()

HOST, PORT = '', 4999
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST, PORT))

s.listen()

s.setblocking(False) # methods that block app include recv, send etc

sel.register(s, selectors.EVENT_READ, data=None) # registers socket to be monitored with sel.select for events you're interested in

def accept_wrapper(s):
    c, addr = s.accept()
    print(f'Accepted connection from {addr}')

    c.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"") #include data to know when client is ready #simple namespace is a class which only holds attributes

    events = selectors.EVENT_READ or selectors.EVENT_WRITE #events are reading and writing

    sel.register(c, events, data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ: #mask contains information on which event is ready
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            data.outb += recv_data
        else:
            sel.unregister(sock) #if read event ready and no data received, client has closed connection so server closes connection also
            sock.close()
    if mask & selectors.EVENT_WRITE: 
        if data.outb:
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]
try:
    while True:
        events = sel.select(timeout=None) # blocks until sockets ready for I/O returns list of tuples
        #A SelectorKey is a namedtuple used to associate a file object to its underlying file descriptor, selected event mask and attached data. It is returned by several BaseSelector methods.

        for key,mask in events:
            if key.data is None: # from listening socket with an oepn connection
                pass
            else: #client socket that's already been accepted.
                service_connection(key, mask)
except KeyboardInterrupt:
    print("Caught Keyboard Interrupt")


