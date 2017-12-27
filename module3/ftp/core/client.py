#!/usr/bin/env python
# coding=utf-8
# Author: bloke

import socket
import os
import json


class Client(object):

    transfer_size = 4096

    def __init__(self, host, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.client:
            self.client.connect((host, port))
            welcome = self.client.recv(self.transfer_size)  # 欢迎语
            print(welcome)
            while 1:
                self.data = input('Send: ').strip()
                if not self.data:
                    continue
                self.client.sendall(bytes(str(len(self.data)), encoding='utf-8'))
                action = self.data.split()[0]
                func = getattr(self, '_%s' % action, self._comm)
                func()
                continue

    def _help(self):
        self.client.sendall(self.data.encode('utf-8'))
        recv_data = self.client.recv(self.transfer_size)
        recv_data = json.loads(recv_data.decode('utf-8'))
        print(''.center(50, '*'))
        for key, value in recv_data.items():
            print(key, ': ', value)
        print(''.center(50, '*'))

    def _put(self):
        action, filename = self.data.split()[0], self.data.split()[1]
        filesize = os.path.getsize(filename)
        self.client.sendall(bytes('%s %s %s' % (action, filename, filesize), encoding='utf-8'))
        sign = self.client.recv(self.transfer_size)
        if sign.decode('utf-8') == 'Ready...':
            with open(filename, 'rb') as f:
                self.client.sendall(f.read())

    def _get(self):
        filecount = 0
        action, filename = self.data.split()[0], os.path.basename(self.data.split()[1])
        self.client.sendall(self.data.encode('utf-8'))
        filesize = self.client.recv(self.transfer_size)
        w_file = open(filename, 'wb')
        while 1:
            if filecount < int(filesize):
                recv_data = self.client.recv(self.transfer_size)
                w_file.write(recv_data)
                filecount += len(recv_data)
                w_file.flush()
            else:
                w_file.flush()
                w_file.close()
                print('Transfer completed.')
                break

    def _comm(self):
            self.client.sendall(bytes(self.data, 'utf-8'))
            print('Recv:')
            recv_data = self.client.recv(self.transfer_size)
            print(recv_data.decode('utf-8'))


client = Client('localhost', 9999)



