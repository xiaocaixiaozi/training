#!/usr/bin/env python
# coding=utf-8
# Author: bloke

import socket

remote_addr = ('localhost', 8888)
sockets = [socket.socket(socket.AF_INET, socket.SOCK_STREAM) for i in range(500)]
messages = [
    'first',
    'second',
    'third',
    'forth',
    'fifth',
    'sixth'
]

for sock in sockets:
    sock.connect(remote_addr)

for msg in messages:
    for s in sockets:
        s.sendall(bytes(msg, 'utf-8'))
        print(('[%s: %s] send:' % s.getpeername()), msg)

    for rs in sockets:
        data = rs.recv(1024)
        if not data:
            print('Socket [%s: %s] is disconnected.' % rs.getpeername())
        else:
            print(('[%s: %s] recv:' % rs.getpeername()), data)

