#!/usr/bin/env python
# coding=utf-8
# Author: bloke

import socket
import os
import json


class Client(object):

    transfer_size = 4096

    def __init__(self, account, password, host, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.client:
            self.client.connect((host, port))
            self.client.sendall(bytes('%s %s' % (account, password), encoding='utf-8'))
            auth_sign = self.client.recv(self.transfer_size).decode('utf-8')
            if int(auth_sign):
                self.client.sendall(bytes('bye', encoding='utf-8'))
                self.client.close()
                os._exit(1)
            else:
                self.client.sendall(bytes('nice', encoding='utf-8'))
            welcome = self.client.recv(self.transfer_size)  # 欢迎语
            print(welcome.decode('utf-8'))
            while 1:
                try:
                    self.data = input('Send: ').strip()
                    if not self.data:
                        continue
                    self.client.sendall(bytes(str(len(self.data)), encoding='utf-8'))
                    action = self.data.split()[0]
                    if action == 'bye':
                        self.__del__()
                    func = getattr(self, '_%s' % action, self._comm)
                    func()
                    continue
                except ValueError as e:
                    print(e)
                    continue
                except KeyboardInterrupt as e:
                    self.__del__()
                except ConnectionAbortedError as e:
                    print(e)
                    self.__del__()

    def _help(self):
        """帮助命令"""
        self.client.sendall(self.data.encode('utf-8'))
        recv_data = self.client.recv(self.transfer_size)
        recv_data = json.loads(recv_data.decode('utf-8'))
        print(''.center(50, '*'))
        for key, value in recv_data.items():
            print(key, ': ', value)
        print(''.center(50, '*'))

    def _put(self):
        """上传文件"""
        try:
            action, filename = self.data.split()[0], self.data.split()[1]
        except IndexError as e:
            return False
        filesize = os.path.getsize(filename)
        self.client.sendall(bytes('%s %s %s' % (action, filename, filesize), encoding='utf-8'))
        sign = self.client.recv(self.transfer_size)
        if sign:
            with open(filename, 'rb') as f:
                self.client.sendall(f.read())

    def _get(self):
        """下载文件"""
        filecount = 0
        action, filename = self.data.split()[0], os.path.basename(self.data.split()[1])
        self.client.sendall(self.data.encode('utf-8'))
        num_info = self.client.recv(self.transfer_size)
        try:
            filesize = int(num_info)
        except Exception as e:
            print(num_info)
            return False
        w_file = open(filename, 'wb')
        while filecount != filesize:
            recv_data = self.client.recv(self.transfer_size)
            w_file.write(recv_data)
            filecount += len(recv_data)
        else:
            w_file.flush()
            w_file.close()
            print('Transfer completed.')

    def _comm(self):
        """匹配未指定命令"""
        self.client.sendall(bytes(self.data, 'utf-8'))
        print('Recv:')
        recv_data = self.client.recv(self.transfer_size)
        print(recv_data.decode('utf-8'))

    def __del__(self):
        print('Exit.')
        self.client.shutdown(2)
        self.client.close()
        os._exit(1)


if __name__ == '__main__':
    client = Client('user01', 'user01', 'localhost', 9999)


