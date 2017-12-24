#!/usr/bin/env python
# coding=utf-8
# Author: bloke

import socket

host, port = 'localhost', 9999

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((host, port))
    while 1:
        data = input('Send: ').strip()
        if not data: continue
        client.sendall(bytes(data, 'utf-8'))
        recv = client.recv(1024)
        print('Recv:', recv)








