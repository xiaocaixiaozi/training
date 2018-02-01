#!/usr/bin/env python
# coding=utf-8
# Author: bloke

import socket
import gevent
from gevent import monkey


def socket_server(address, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((address, port))
    server.listen()
    while True:
        conn, addr = server.accept()
        print(conn, addr)
        gevent.spawn(socket_handler, conn)


def socket_handler(conn):
    try:
        while True:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                conn.shutdown(socket.SHUT_WR)
            print(data)
            conn.sendall(bytes(data.upper(), 'utf-8'))
    except Exception as e:
        print(e)
    finally:
        conn.close()


if __name__ == '__main__':
    monkey.patch_all()
    socket_server('localhost', 8080)










