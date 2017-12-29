#!/usr/bin/env python
# coding=utf-8
# Author: bloke

import socketserver
import subprocess
import os
import json
import shutil
from .ftp_tools import check_auth, hash_password


class MyTCPHandler(socketserver.BaseRequestHandler):

    BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    AUTHDIR = BASEDIR + os.sep + 'conf'
    transfer_count = 4096  # 全局变量，网络传输大小，字节
    comm_dict = {
        'cd': 'Change Dir',
        'dir': 'List Dir',
        'get': 'Download File',
        'put': 'Upload File',
        'help': 'Show This Page',
        'del': 'Delete file or directory',
        'bye': 'Exit.'
    }
    error_dict = {
        'comm_error': 'Invalid Commands',
    }

    def setup(self):
        print('%s is connected.' % str(self.client_address))
        auth_info = self.request.recv(self.transfer_count).decode('utf-8')  # 接受client端账号密码
        self.account, password = auth_info.split()
        self.password = hash_password(password)     # 加密
        auth = check_auth(self.account, self.password, os.path.join(self.AUTHDIR, 'shadow'))    # 鉴权
        if not auth:    # 鉴权失败，发送1
            self.request.sendall(bytes(str(1), encoding='utf-8'))
        else:   # 鉴权成功，发送0
            self.request.sendall(bytes(str(0), encoding='utf-8'))
        self.client_sign = self.request.recv(self.transfer_count).decode('utf-8')

    def handle(self):
        check = True
        if self.client_sign == 'bye':
            print('%s auth failed.' % str(self.client_address))
            self.finish()
            check = False
        else:
            print('[%s:%s] is connected.' % self.client_address)
        self.request.sendall(bytes('Welcome %s, Please enter "help" to help.' % str(self.client_address), \
                                   encoding='utf-8'))
        while check:
            try:
                count = 0
                recv_list = []
                num = self.request.recv(self.transfer_count)
                try:
                    print('Num: ', num)
                    num = float(num.decode('utf-8'))
                except ValueError as e:
                    print(e)
                    break
                except Exception as e:
                    print(e)
                    break
                while count < num:
                    recv_data = self.request.recv(self.transfer_count)
                    print(recv_data)
                    recv_list.append(recv_data.decode('utf-8'))
                    count += self.transfer_count
                self.recv = ''.join(recv_list)
                print('Recv:', self.recv)
                try:
                    action = self.recv.split()[0]
                except IndexError as e:
                    print(e)
                    continue
                if action == 'bye':
                    self.finish()
                if action not in self.comm_dict:
                    self.request.sendall(bytes('Invalid Command.', encoding='utf-8'))
                    continue
                func = getattr(self, '_%s' % action, self._comm)
                print('_%s' % action)
                func()
                continue
            except (ConnectionResetError, ConnectionAbortedError) as e:
                print(e)
                continue
            except FileNotFoundError as e:
                print(e)
                self.request.sendall(bytes('Error...[File Not Found]', encoding='utf-8'))
                continue

    def finish(self):
        print('[%s:%s] is disconnected.' % self.client_address)

    def _put(self):
        action, filename, filesize = self.recv.split()[0], self.recv.split()[1], int(self.recv.split()[2])
        self.request.sendall(bytes('Ready...', encoding='utf-8'))
        filecount = 0
        w_file = open(os.path.basename(filename), 'wb')
        while 1:
            if filecount < filesize:
                recv_data = self.request.recv(self.transfer_count)
                w_file.write(recv_data)
                filecount += self.transfer_count
                continue
            else:
                w_file.flush()
                w_file.close()
                break

    def _get(self):
        action, filename = self.recv.split()[0], self.recv.split()[1]
        filesize = os.path.getsize(filename)
        self.request.send(bytes(str(filesize), encoding='utf-8'))
        try:
            with open(filename, 'rb') as f:
                self.request.sendall(f.read())
                print(os.path.getsize(filename))
        except FileNotFoundError as e:
            print(e)

    def _help(self):
        send_data = json.dumps(self.comm_dict)
        self.request.sendall(bytes(send_data, encoding='utf-8'))

    def _cd(self, recv_data):
        e = ''
        action, dirname = recv_data
        try:
            subprocess.os.chdir(dirname)
            self.request.sendall(bytes('Operate Success.', encoding='utf-8'))
        except Exception as e:
            self.request.sendall(bytes(str(e), encoding='utf-8'))

    def _dir(self):
        dirname = '.'
        if len(self.recv.split()) > 1:
            dirname = self.recv.split()[1]
        data = os.listdir(dirname)
        self.request.sendall(bytes('\n'.join(data), encoding='utf-8'))

    def _del(self):
        action, file_dir = self.recv.split()[0], self.recv.split()[1]
        if not os.path.exists(file_dir):
            self.request.sendall(bytes('File Not Found.', encoding='utf-8'))
            return False
        elif os.path.isfile(file_dir):
            os.remove(file_dir)
            self.request.sendall(bytes('Delete Success.', encoding='utf-8'))
        elif os.path.isdir(file_dir):
            shutil.rmtree(file_dir)
            self.request.sendall(bytes('Delete Success.', encoding='utf-8'))

    def _comm(self):
        try:
            data = subprocess.getoutput(self.recv)
            self.request.sendall(bytes(data, encoding='utf-8'))
        except Exception as e:
            self.request.sendall(bytes(str(e), 'utf-8'))



def run(host, port):
    server = socketserver.ThreadingTCPServer((host, port), MyTCPHandler)
    with server:
        ip, addr = server.server_address
        server.serve_forever()


if __name__ == "__main__":
    host, port = 'localhost', 9999
    run(host, port)



