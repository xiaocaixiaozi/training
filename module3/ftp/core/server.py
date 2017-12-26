#!/usr/bin/env python
# coding=utf-8
# Author: bloke

import socketserver
import subprocess
import os
import json


class MyTCPHandler(socketserver.BaseRequestHandler):

    transfer_count = 4096  # 全局变量，网络传输大小，字节

    def myinit(self):
        self.comm_dict = {
            'cd': 'Change Dir',
            'dir': 'List Dir',
            'get': 'Download File',
            'put': 'Upload File'
        }
        self.error_dict = {
            'comm_error': 'Invalid Commands',
        }

    def setup(self):
        self.myinit()
        print('[%s:%s] is connected.' % self.client_address)
        self.request.sendall(bytes('Welcome %s, Please enter "help" to help.' % str(self.client_address), \
                                   encoding='utf-8'))

    def handle(self):
        try:
            while 1:
                count = 0
                recv_list = []
                num = self.request.recv(self.transfer_count)
                while count < int(num.decode('utf-8')):
                    recv_data = self.request.recv(self.transfer_count).decode('utf-8')
                    recv_list.append(recv_data)
                    count += self.transfer_count
                else:
                    recv = ''.join(recv_list)
                    print('Recv:', recv)
                    if recv == 'help':
                        send_data = json.dumps(self.comm_dict)
                        self.request.sendall(bytes(send_data, encoding='utf-8'))
                        continue
                    if recv.split()[0] == 'put':
                        action, filename, filesize = recv.split()[0], recv.split()[1], recv.split()[2]
                        self.transfer_file(action, filename, filesize)
                        continue
                    elif recv.split()[0] == 'get':
                        action, filename = recv.split()[0], recv.split()[1]
                        filesize = os.path.getsize(filename)
                        self.request.send(bytes(str(filesize), encoding='utf-8'))
                        self.transfer_file(action, filename, filesize)
                        continue

                    data = subprocess.getoutput(recv)
                    self.request.sendall(bytes(data, encoding='utf-8'))
        except ConnectionResetError as e:
            print(e)

    def finish(self):
        print('[%s:%s] is disconnected.' % self.client_address)

    def transfer_file(self, action, filename, filesize):
        filecount = 0
        if action == 'put':
            with open(filename, 'wb') as f:
                while filecount < filesize:
                    recv_data = self.request.recv(self.transfer_count)
                    f.write(recv_data)
        elif action == 'get':
            with open(filename, 'rb') as f:
                for line in f:
                    self.request.sendall(line)


if __name__ == "__main__":
    host, port = 'localhost', 9999
    server = socketserver.ThreadingTCPServer((host, port), MyTCPHandler)
    with server:
        ip, addr = server.server_address
        server.serve_forever()




