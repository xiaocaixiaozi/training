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
                self.data = self.request.recv(8192)
            except (ConnectionResetError, ConnectionAbortedError) as e:
                break
            if not self.data:
                break
            print('Recv:', self.data)
            self.request.sendall(self.data.upper())

    def finish(self):
        print('[%s:%s] is disconnected.' % self.client_address)


def server_main(host, port):
    server = socketserver.ThreadingTCPServer((host, port), MyTCPHandler)
    with server:
        server.serve_forever()


if __name__ == "__main__":
    host, port = 'localhost', 9999
    server_main(host, port)




