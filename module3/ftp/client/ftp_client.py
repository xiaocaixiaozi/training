#!/usr/bin/env python
# coding=utf-8
# Author: bloke

import socket
import os
import json
import hashlib


class Client(object):

    transfer_size = 4096

    def __init__(self, account, password, host, port):
        self.account = account
        self.host = host
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
                    break
                except ConnectionAbortedError as e:
                    print(e)
                    break
                except ConnectionRefusedError as e:
                    print(e)
                    break
                except IndexError as e:
                    print(e)
                    continue
                except Exception as e:
                    print(e)
                    break

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
            self.client.sendall(bytes('bloke_error', encoding='utf-8'))
            print(self.client.recv(self.transfer_size).decode('utf-8'))
            return False
        filesize = os.path.getsize(filename)
        self.client.sendall(bytes('%s %s %s' % (action, filename, filesize), encoding='utf-8'))
        sign = self.client.recv(self.transfer_size)
        file_md5 = hashlib.md5()
        if sign:
            with open(filename, 'rb') as f:
                for line in f:
                    self.client.sendall(line)
                    file_md5.update(line)
                else:
                    self.client.sendall(bytes(file_md5.hexdigest(), encoding='utf-8'))  # 发送md5值
            print('Transafer completed.', file_md5.hexdigest())
            check_md5_result = self.client.recv(self.transfer_size)
            print(check_md5_result.decode('utf-8'))

    def _get(self):
        """下载文件"""
        filecount = 0
        try:
            action, filename = self.data.split()[0], os.path.basename(self.data.split()[1])
        except IndexError as e:
            self.client.sendall(bytes('bloke_error', encoding='utf-8'))
            print(self.client.recv(self.transfer_size).decode('utf-8'))
            return False
        self.client.sendall(self.data.encode('utf-8'))
        num_info = self.client.recv(self.transfer_size)
        try:
            filesize = int(num_info)
        except Exception as e:
            print(num_info)
            return False
        w_file = open(filename, 'wb')
        file_md5 = hashlib.md5()
        self.record = re_conn(self.host, self.account, action, filename)    # 文件传输记录，支持断点续传
        try:
            while filecount < filesize:
                lave_count = filesize - filecount
                if lave_count < self.transfer_size:
                    self.client.sendall(bytes('ok', encoding='utf-8'))
                    recv_data = self.client.recv(lave_count)
                    file_md5.update(recv_data)
                else:
                    recv_data = self.client.recv(self.transfer_size)
                    file_md5.update(recv_data)
                w_file.write(recv_data)
                filecount += len(recv_data)
            else:
                w_file.flush()
                w_file.close()
                print('Transfer completed.')
                get_file_md5 = self.client.recv(self.transfer_size).decode('utf-8')
                if get_file_md5 != file_md5.hexdigest():
                    print('File md5 value is wrong.')
                else:
                    print('File md5 value is correct.')
        except KeyboardInterrupt as e:
            print('pause'.center(50, '*'))
            self.client.sendall(bytes('pause', encoding='utf-8'))   # 暂停
            return False

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


def re_conn(host, account, sign, filename):
    """
    断电续传，隐藏文件记录文件传输进度: ".tmp"，通过json读取数据并返回
    如果文件不存在，则通过对应的一下参数生成字典并返回
    :param host: 服务器地址
    :param account: 登录账户
    :param sign: 操作文件动作，例如<put、get>
    :param filename: 操作的文件名
    :return: 返回记录，字典格式
    """
    record_file = '.tmp'
    if not os.path.exists(record_file):
        the_dict = {host: {account: {'filename': filename, 'schedule': 0}}}
        return the_dict
    else:
        with open(record_file) as f:
            the_dict = json.load(f)
            if host not in the_dict:
                the_dict[host] = {account: {filename: 0}}
                return the_dict
            if account not in the_dict[host]:
                the_dict[host][account] = {filename: 0}
                return the_dict
        return the_dict


if __name__ == '__main__':
    client = Client('user01', 'user01', 'localhost', 9999)
