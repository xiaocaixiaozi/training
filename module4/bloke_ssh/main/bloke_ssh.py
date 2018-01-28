#!/usr/bin/env python
# coding=utf-8
# Author: bloke

import paramiko
import os
import sys
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASEDIR)


class MySSH(object):

    """
    SSH 客户端，接受连接参数为字典格式
    connect方法连接主机
    exec方法执行命令
    put、get方法分别为上传、下载方法
    """

    def __init__(self, sign, **kwargs):
        self.hostname = kwargs['hostname']
        self.port = kwargs['port']
        self.username = kwargs['username']
        self.key_file = kwargs.get('key_file')
        self.password = kwargs.get('password')
        self.tmp_dir = os.path.join(BASEDIR, 'tmp')
        self.sign = ('%s 结果' % sign).center(80, '*')
        self.host = sign

    def connect(self):
        """
        建立SSH链接
        """
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        try:
            if self.key_file:
                self.client.connect(self.hostname, self.port, self.username, key_filename=self.key_file)
            else:
                self.client.connect(self.hostname, self.port, self.username, self.password)
        except Exception as e:
            print(e)

    def exec(self, cmd, queue):
        """
        执行远程命令，将主机标记、标准输出、标准错误全部返回到队列中
        """
        self.connect()
        stdin, stdout, stderr = self.client.exec_command(cmd)
        queue.put((['\n' + self.sign + '\n'], stdout, stderr))

    def put(self, file_args, queue):
        """
        上传文件
        """
        local_file, remote_file = file_args
        self.sftp = self.client.open_sftp()
        self.sftp.put(local_file, remote_file)
        queue.put(['\n' + self.sign + '\n' + 'Done'])

    def get(self, file_args, queue):
        """
        下载文件，在程序根目录的tmp目录下，以每台主机的主机名创建目录，将文件分别下载到对应主机名的目录中
        """
        remote_file, local_file = file_args
        self.sftp = self.client.open_sftp()
        host_tmp_dir = os.path.join(self.tmp_dir, self.host)
        if not os.path.exists(host_tmp_dir):
            os.mkdir(host_tmp_dir)
        self.sftp.get(remote_file, os.path.join(host_tmp_dir, local_file))
        queue.put(['\n' + self.sign + '\n' + 'Done'])


