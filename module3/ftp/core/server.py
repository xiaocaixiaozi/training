#!/usr/bin/env python
# coding=utf-8
# Author: bloke

import socketserver


class MyTCPHandler(socketserver.BaseRequestHandler):

    def setup(self):
        print('[%s:%s] is connected.' % self.client_address)

    def handle(self):
        while 1:
            try:
                self.data = self.request.recv(1)
            except ConnectionResetError as e:
                break
            if not self.data:
                break
            print('Recv:', self.data)
            self.request.sendall(self.data.upper())

    def finish(self):
        print('[%s:%s] is disconnected.' % self.client_address)




if __name__ == "__main__":
    host, port = 'localhost', 9999
    server = socketserver.ThreadingTCPServer((host, port), MyTCPHandler)
    with server:
        ip, addr = server.server_address
        server.serve_forever()




