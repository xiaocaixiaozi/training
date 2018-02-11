#!/usr/bin/env python
# coding=utf-8
# Author: bloke

import socket


class CLIENT(object):

    def __init__(self):
        self.remote_addr = ('localhost', 9999)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.recv_size = 4096
        self.sign = 'ok'

    def connect(self):
        self.client.connect(self.remote_addr)

    def client_input(self):
        while True:
            send_data = input('>>> ').strip()
            if not send_data:
                continue
            self.client.sendall(bytes(send_data, 'utf-8'))
            recv_sign = self.client.recv(self.recv_size).decode('utf-8')
            if not recv_sign.startswith('ready'):
                print(recv_sign)
                continue
            send_data_split = send_data.split()
            func = send_data_split[0]
            if hasattr(self, func):
                getattr(self, func)(recv_sign.strip('ready'))

    def get(self, recv_data):
        filename, size = recv_data.split('-->')
        size = int(size)
        # self.client.sendall(bytes(self.sign, 'utf-8'))
        total_size = 0
        with open(filename, 'wb') as f:
            while total_size < size:
                data = self.client.recv(self.recv_size)
                total_size += len(data)
                f.write(data)
                print('|', ('>' * int(total_size / size * 50)).ljust(50, '-'), '|', end='\r')
            else:
                print('\nDone.')

if __name__ == '__main__':
    client = CLIENT()
    client.connect()
    client.client_input()
