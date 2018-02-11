#!/usr/bin/env python
# coding=utf-8
# Author: bloke

import socket
import selectors
import os


def accept(sock):
    conn, addr = sock.accept()
    print('Client [%s: %s] is connected.' % conn.getpeername())
    sel.register(conn, selectors.EVENT_READ, read)


def read(conn):

    client_addr = conn.getpeername()
    try:
        data = conn.recv(trans_size)
        if not data:
            sel.unregister(conn)
            conn.close()
            print('Client [%s: %s] is disconnected.' % client_addr)
        else:
            client_data = data.decode('utf-8').split()
            client_command = client_data[0]
            if not client_command in ['get', 'put', 'ls']:
                conn.sendall(bytes('Invalid command.', 'utf-8'))
            elif client_command == 'get':
                filename = client_data[1]
                if not os.path.exists(filename):
                    conn.sendall(bytes('File not found. [%s]' % filename, 'utf-8'))
                else:
                    conn.sendall(bytes('ready%s-->%s' % (filename, os.path.getsize(filename)), 'utf-8'))
                    # client_sign = conn.recv(trans_size)
                    # if client_sign.decode('utf-8') == 'ok':
                get(conn, filename, trans_size)
            # elif client_command == 'put':
            #     filename = client_data[1]
            #     put(conn, filename)
            elif client_command == 'ls':
                data = '\n'.join(os.listdir('.'))
                conn.sendall(bytes(data, 'utf-8'))

    except ConnectionResetError as e:
        print('Client [%s: %s] is disconnected.' % client_addr)
        sel.unregister(conn)
        conn.close()


def get(client, filename, trans_size):
    # if not os.path.exists(filename):
    #     client.sendall(bytes('File not found. [%s]' % filename, 'utf-8'))
    # else:
    #     client.sendall(bytes('ready%s-->%s' % (filename, os.path.getsize(filename)), 'utf-8'))
        # client_sign = client.recv(trans_size)
        # if client_sign.decode('utf-8') == 'ok':
        with open(filename, 'rb') as f:
            for line in f:
                client.sendall(line)


if __name__ == '__main__':
    local_addr = ('localhost', 9999)
    trans_size = 4096
    method_dict = {
        'ls': 'List directory',
        'get': 'Download file',
        'put': 'Put file'
    }

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(local_addr)
    server.setblocking(False)
    server.listen(10)

    sel = selectors.DefaultSelector()
    sel.register(server, selectors.EVENT_READ, accept)

    while True:
        readys = sel.select()
        for key, event in readys:
            call = key.data
            call(key.fileobj)


