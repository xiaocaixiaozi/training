#!/usr/bin/env python
# coding=utf-8
# Author: bloke

import paramiko


class My_SSH(object):

    def __init__(self, hostname, port, username, password, key_file):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.key_file = key_file

    def connect(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        client.connect(self.hostname, self.port, self.username, self.password, key_filename=self.key_file)
        self.client = client
        self.sftp = self.client.open_sftp()

    def exec(self, cmd):
        stdin, stdout, stderr = self.client.exec_command(cmd)
        return stdout

    def put(self, local_file, remote_file):
        self.sftp.put(local_file, remote_file)

    def get(self, remote_file, local_file):
        self.sftp.get(remote_file, local_file)

ssh = My_SSH('172.28.8.80', 22, 'root', 'itvitv', 'D:\\id_rsa')
ssh.connect()
ip_info = ssh.exec('ip addr')
for line in ip_info.readlines():
    print(line)

ssh.put('messages', '/home/messages')
ssh.get('/etc/hosts', 'hosts')



