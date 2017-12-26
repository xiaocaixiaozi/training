#!/usr/bin/env python
# coding=utf-8
# Author: bloke

import socket
import os
import json

host, port = 'localhost', 9999
transfer_size = 4096

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((host, port))
    welcome = client.recv(transfer_size)  # 欢迎语
    print(welcome.decode('utf-8'))
    while 1:
        data = input('Send: ').strip()
        if not data: continue
        client.sendall(bytes(str(len(data)), encoding='utf-8'))
        if data == 'help':
            client.sendall(data.encode('utf-8'))
            recv_data = client.recv(transfer_size)
            recv_data = json.loads(recv_data.decode('utf-8'))
            print(''.center(50, '*'))
            for key, value in recv_data.items():
                print(key, ': ', value)
            print(''.center(50, '*'))
            continue

        if data.split()[0] == 'put':    # 上传文件
            action, filename = data.split()[0], data.split()[1]
            filesize = os.path.getsize(filename)
            client.sendall(bytes('%s %s %s' % (action, filename, filesize), encoding='utf-8'))
            with open(filename, 'rb') as f:
                for line in f:
                    client.sendall(line)

        elif data.split()[0] == 'get':  # 下载文件
            filecount = 0
            action, filename = data.split()[0], os.path.basename(data.split()[1])
            client.sendall(data.encode('utf-8'))
            filesize = client.recv(transfer_size)
            with open(filename, 'wb') as f:
                while filecount < int(filesize):
                    recv_data = client.recv(transfer_size)
                    f.write(recv_data)
            continue

        else:
            client.sendall(bytes(data, 'utf-8'))
            print('Recv:')
            recv_data = client.recv(transfer_size)
            print(recv_data.decode('utf-8'))
            continue






