import sys
import socket
import selectors
#https://docs.python.org/3/library/selectors.html

import types

sel = selectors.DefaultSelector()

HOST, PORT = '192.168.0.64', 4999
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST, PORT))

s.listen()

s.setblocking(False) # methods that block app include recv, send etc

sel.register(s, selectors.EVENT_READ, data=None) # registers socket to be monitored with sel.select for events you're interested in

try:
    while True:
        events = sel.select(timeout=None) # blocks until sockets ready for I/O returns list of tuples
        #A SelectorKey is a namedtuple used to associate a file object to its underlying file descriptor, selected event mask and attached data. It is returned by several BaseSelector methods.

        for key,mask in events:
            if key.data is None: # from listening socket with an oepn connection
                pass
            else: #client socket that's already been accepted.



