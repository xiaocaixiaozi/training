import os
import sys
import json
import selectors
import socket
import time
import errno
import random

BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from conf import setting
sel = selectors.DefaultSelector()

class selectors_ftp(object):
    '''selectors_ftp服务端'''
    def __init__(self):
        '''
        构造函数
        '''
        self.sock = socket.socket()

    def upload(self,conn,mask):
        '''
        服务器upload函数
        :param conn:
        :param mask
        :return:
        '''
        os.chdir(setting.upload_path)
        self.conn.send(b'Server receive upload %s request'%self.file_name.encode())
        new = random.randint(1, 100000) #并发测试使用random生成新文件名
        file_object = open((self.file_name+'.'+(str(new))), 'wb')
        received_size = 0
        while received_size < self.file_size:
            try:
                if self.file_size - received_size > 1024:
                    size = 1024
                elif self.file_size < 1024:
                    size = self.file_size
                else:
                    size = self.file_size - received_size
                recv_data = conn.recv(size)
                received_size += len(recv_data)
                file_object.write(recv_data)
            except BlockingIOError as e:
                if e.errno != errno.EAGAIN:
                    raise
            else:
              time.sleep(0.00001)
            #   #print(received_size, file_size)
        else:
            file_object.close()

    def download(self,conn,mask):
        '''
        服务器下载函数
        :param conn:
        :param mask:
        :return:
        '''
        while True:
            os.chdir(setting.download_path)
            if os.path.isfile(self.file_name) and os.path.exists(self.file_name):
                try:
                    file_size = os.path.getsize(self.file_name)
                    self.conn.send(str(file_size).encode())
                    client_file_size = 0
                    with open(self.file_name, "rb") as file_obj:
                        for line in file_obj:
                            client_file_size += len(line)  # 记录已经传送的文件大小
                            self.conn.sendall(line)
                    file_obj.close()
                    if client_file_size >= int(file_size):  # 文件传送完毕
                        break
                except BlockingIOError as e:
                    if e.errno != errno.EAGAIN:  # errno.EAGAIN 缓冲区满 等待下
                        raise
                else:
                    time.sleep(0.00001)  # 等待0.1s进行下一次读取
            else:
                conn.send(b'404')
                break

    def accept(self,sock,mask):
        '''
        服务器监听函数
        :param sock:
        :param mask:
        :return:
        '''
        self.conn, self.addr = sock.accept()
        print(time.strftime("%Y-%m-%d %X", time.localtime()), ': accepted',self.conn,'from', self.addr, mask)
        self.conn.setblocking(False)
        sel.register(self.conn, selectors.EVENT_READ, self.read)

    def read(self,conn,mask):
        '''
        服务器读取命令信息函数
        :param conn:
        :param mask:
        :return:
        '''
        self.data = conn.recv(1024)
        if self.data:
            self.data_receive = json.loads(self.data.decode())
            self.action = self.data_receive['client']['action']
            self.file_name = self.data_receive['client']['file_name']
            self.file_size = self.data_receive['client']['size']
            print(time.strftime("%Y-%m-%d %X", time.localtime()), ': echoing', repr(self.data), 'to', self.conn, mask)
            if self.action == 'put':
                self.upload(self.conn, mask)
                conn.send(b'[+]server: -bash : Server receive upload %s done ' % self.file_name.encode())
                print(time.strftime("%Y-%m-%d %X", time.localtime()), ': client :', self.addr,
                      ': upload %s done' % self.file_name)
            elif self.action == 'get':
                self.download(self.conn, mask)
                print(time.strftime("%Y-%m-%d %X", time.localtime()), ': client :', self.addr,
                      ': download %s done' % self.file_name)
        else:
            print(time.strftime("%Y-%m-%d %X", time.localtime()), ': closing:', self.conn, mask)
            sel.unregister(conn)
            conn.close()

    def register(self,sock):
        '''
        注册函数
        :return:
        '''
        sel.register(self.sock, selectors.EVENT_READ, self.accept)
        while True:
            events = sel.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj,mask)


    def start(self,ip,port):
        '''
        启动函数
        :return:
        '''
        self.sock.bind((ip,port))
        self.sock.listen(500)
        self.sock.setblocking(False)
        self.register(self.sock)