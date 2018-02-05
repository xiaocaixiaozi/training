#!/usr/bin/env python
# coding=utf-8
# Author: bloke

import socket

client = socket.socket()
client.connect(('localhost', 8080))

try:
    while True:
        data_send = input('> ').strip()
        if not data_send: continue
        client.sendall(bytes(data_send, 'utf-8'))
        data_recv = client.recv(1024).decode('utf-8')
        print(data_recv)
except Exception as e:
    print(e)
    client.close()


