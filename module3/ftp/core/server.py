#!/usr/bin/env python
# coding=utf-8
# Author: bloke

import socketserver
import subprocess
import os
import json
import shutil
import hashlib
import sys
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASEDIR)
from core.ftp_tools import check_auth, hash_password, record_log, replace_relative_path
from core.read_config import GetConfig


class MyTCPHandler(socketserver.BaseRequestHandler):

    BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    AUTHDIR = BASEDIR + os.sep + 'conf'
    transfer_count = 4096  # 全局变量，网络传输大小，字节
    change_dir_error = 'due to can not change directory.'
    comm_dict = {
        'cd': 'Change Dir',
        'dir': 'List Dir',
        'get': 'Download File',
        'put': 'Upload File',
        'help': 'Show This Page',
        'del': 'Delete file or directory',
        'bye': 'Exit.'
    }
    loglevel = GetConfig(os.path.join(AUTHDIR, 'config.ini')).get_config('server')['loglevel']
    logger = record_log(int(loglevel))

    def setup(self):
        if not self.logger:
            return False
        self.logger.info('[{0}] {0} is connected.'.format(str(self.client_address)))
        auth_info = self.request.recv(self.transfer_count).decode('utf-8')  # 接受client端账号密码
        self.account, password = auth_info.split()
        self.password = hash_password(password)     # 加密
        self.logger.info('[%s] Account: %s' % (str(self.client_address), self.account))
        # 用户家目录
        auth = check_auth(self.account, self.password, os.path.join(self.AUTHDIR, 'shadow'))    # 鉴权
        if not auth:    # 鉴权失败，发送1
            self.request.sendall(bytes(str(1), encoding='utf-8'))
        else:   # 鉴权成功，发送0
            self.request.sendall(bytes(str(0), encoding='utf-8'))
        self.client_sign = self.request.recv(self.transfer_count).decode('utf-8')

    def handle(self):
        check = True
        if self.client_sign == 'bye':
            self.logger.warning('[%s] "%s" Auth failed.' % (str(self.client_address), self.account))
            check = False
        else:
            self.logger.info('[{0}] "{1}" Auth success.'.format(str(self.client_address), self.account))
        self.request.sendall(bytes('Welcome %s, Please enter "help" to help.' % \
                                   str(self.client_address), encoding='utf-8'))
        self.basedir = self.BASEDIR + os.sep + 'dirs' + os.sep + self.account
        # os.chdir(self.basedir)  # 切换目录到用户家目录
        while check:
            try:
                count = 0
                recv_list = []
                num = self.request.recv(self.transfer_count)
                if not num: break
                try:
                    self.logger.debug('[%s] Recive data length: %s' % (str(self.client_address), num))
                    num = float(num.decode('utf-8'))
                except ValueError as e:
                    self.logger.error('[%s] %s' % (str(self.client_address), e))
                    break
                except Exception as e:
                    self.logger.error('[%s] %s' % (str(self.client_address), e))
                    break
                while count < num:
                    recv_data = self.request.recv(self.transfer_count)
                    recv_list.append(recv_data.decode('utf-8'))
                    count += self.transfer_count
                self.recv = ''.join(recv_list)
                self.logger.info('[%s] Command: %s' % (str(self.client_address), self.recv))
                try:
                    action = self.recv.split()[0]
                except IndexError as e:
                    self.logger.error('[%s] %s' % (str(self.client_address), e))
                    continue
                if action == 'bye':
                    self.finish()
                if action not in self.comm_dict:
                    self.logger.debug('[%s] Invalid command: %s' % (str(self.client_address), self.recv))
                    self.request.sendall(bytes('Invalid Command.', encoding='utf-8'))
                    continue
                func = getattr(self, '_%s' % action, self._comm)
                self.logger.debug('[%s] Action: _%s' % (str(self.client_address), action))
                func()
                continue
            except (ConnectionResetError, ConnectionAbortedError) as e:
                self.logger.error('[%s] %s' % (self.client_address, e))
                continue
            except FileNotFoundError as e:
                self.logger.error('[%s] %s' % (self.client_address, e))
                self.request.sendall(bytes('Error...[File Not Found]', encoding='utf-8'))
                continue

    def finish(self):
        self.logger.warning('[{0}] {0} is disconnected.'.format(str(self.client_address)))

    def _put(self):
        recv_data = self.recv.split()
        action, filename, filesize = recv_data[0], recv_data[1], int(recv_data[2])
        self.request.sendall(bytes('Ready...', encoding='utf-8'))
        filecount = 0
        w_file = open(os.path.join(self.basedir, filename), 'wb')
        file_md5 = hashlib.md5()
        while filecount < filesize:
            lave_count = filesize - filecount
            if lave_count < self.transfer_count:
                recv_data = self.request.recv(lave_count)
                file_md5.update(recv_data)
            else:
                recv_data = self.request.recv(self.transfer_count)
                file_md5.update(recv_data)
            w_file.write(recv_data)
            filecount += len(recv_data)
        else:
            w_file.flush()
            w_file.close()
            put_file_md5 = self.request.recv(self.transfer_count)
            local_file_md5 = file_md5.hexdigest()
            if put_file_md5.decode('utf-8') != local_file_md5:
                self.request.sendall(bytes('File md5 value is wrong.', encoding='utf-8'))
                self.logger.warning('[%s] File md5 value is wrong. [%s]' % \
                                    (str(self.client_address), filename))
            else:
                self.request.sendall(bytes('File md5 value is correct.', encoding='utf-8'))
                self.logger.warning('[%s] File md5 value is correct. [%s]' % \
                                    (str(self.client_address), filename))

    def _get(self):
        expect_file = replace_relative_path(self.basedir, os.getcwd(), self.recv)
        filesize = os.path.getsize(expect_file)
        self.request.send(bytes(str(filesize), encoding='utf-8'))
        file_md5 = hashlib.md5()
        try:
            with open(expect_file, 'rb') as f:
                for line in f:
                    self.request.sendall(line)
                    file_md5.update(line)
                else:
                    self.request.sendall(bytes(file_md5.hexdigest(), encoding='utf-8'))     # 发送md5值
                    self.logger.debug('[%s] File size: %s' % \
                                      (str(self.client_address), os.path.getsize(expect_file)))
        except FileNotFoundError as e:
            self.logger.error('[%s] %s' % (str(self.client_address), e))

    def _help(self):
        send_data = json.dumps(self.comm_dict)
        self.request.sendall(bytes(send_data, encoding='utf-8'))

    def _cd(self):
        e = ''
        dirname = replace_relative_path(self.basedir, os.getcwd(), self.recv)
        if not os.path.exists(dirname):
            self.request.sendall(bytes('Can not change directory.', encoding='utf-8'))
            self.logger.warning('[%s] Change dir "%s" failed, %s' % \
                                (str(self.client_address), os.path.abspath(dirname), self.change_dir_error))
            return False
        try:
            subprocess.os.chdir(dirname)
            self.request.sendall(bytes('Operate Success.', encoding='utf-8'))
        except Exception as e:
            self.request.sendall(bytes(str(e), encoding='utf-8'))

    def _dir(self):
        dirname = replace_relative_path(self.basedir, os.getcwd(), self.recv)
        data = os.listdir(dirname)
        if not data:
            self.request.sendall(bytes(' ', encoding='utf-8'))
        else:
            self.request.sendall(bytes('\n'.join(data), encoding='utf-8'))

    def _del(self):
        file_dir = replace_relative_path(self.basedir, os.getcwd(), self.recv)
        if file_dir == self.basedir:
            self.logger.error('[%s] Invalid command: %s' % \
                              (str(self.client_address), self.recv))
            self.request.sendall(bytes('Invalid command.', encoding='utf-8'))
            return False
        if not os.path.exists(file_dir):
            self.request.sendall(bytes('File Not Found.', encoding='utf-8'))
            self.logger.debug('[%s] Delete "%s" failed: file not found.' % \
                              (str(self.client_address), file_dir))
            return False
        elif os.path.isfile(file_dir):
            os.remove(file_dir)
            self.request.sendall(bytes('Delete Success.', encoding='utf-8'))
            self.logger.debug('[%s] Delete success: %s' % (str(self.client_address), file_dir))
        elif os.path.isdir(file_dir):
            shutil.rmtree(file_dir)
            self.request.sendall(bytes('Delete Success.', encoding='utf-8'))
            self.logger.debug('[%s] Delete success: %s' % (str(self.client_address), file_dir))

    def _comm(self):
        try:
            data = subprocess.getoutput(self.recv)
            self.request.sendall(bytes(data, encoding='utf-8'))
        except Exception as e:
            self.request.sendall(bytes(str(e), 'utf-8'))
            self.logger.error('[%s] %s' % (str(self.client_address), e))


def run(host, port):
    server = socketserver.ThreadingTCPServer((host, port), MyTCPHandler)
    with server:
        ip, addr = server.server_address
        MyTCPHandler.logger.info('Start server. [%s:%s]' % (ip, addr))
        server.serve_forever()


if __name__ == "__main__":
    host, port = 'localhost', 9999
    run(host, port)

