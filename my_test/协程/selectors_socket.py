#!/usr/bin/env python
# coding=utf-8
# Author: bloke

import selectors
import socket


def accept(sock):
    conn, addr = sock.accept()
    print('Client [%s: %s] is connected.' % conn.getpeername())
    sel.register(conn, selectors.EVENT_READ, read)


def read(conn):
    data = conn.recv(1024)
    if data:
        print('Recv:', data.decode('utf-8'))
        conn.sendall(data.upper())
    else:
        print('Client [%s: %s] is disconnected.' % conn.getpeername())
        sel.unregister(conn)
        conn.close()


if __name__ == '__main__':
    sel = selectors.DefaultSelector()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 8888))
    server.listen(10)
    sel.register(server, selectors.EVENT_READ, accept)

    while True:
        events = sel.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj)

