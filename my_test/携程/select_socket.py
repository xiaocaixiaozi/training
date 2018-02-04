#!/usr/bin/env python
# coding=utf-8
# Author: bloke

import select
import queue
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 8080))
server.setblocking(False)
server.listen(100)

inputs = [server]
outputs = []
msg_dict = {}

while True:
    readable, writeable, exception = select.select(inputs, outputs, inputs)
    for itemr in readable:
        if itemr is server:
            conn, addr = itemr.accept()
            inputs.append(conn)
            print('Client -->', addr)
            msg_dict[conn] = queue.Queue()
        else:
            data = itemr.recv(1024)
            print(data.decode('utf-8'))
            msg_dict[itemr].put(data)

    for itemw in writeable:
        try:
            msg = msg_dict[itemw].get_nowait()
        except queue.Empty:
            print('Remove %s from writeable.' % itemw)
            outputs.remove(itemw)
        else:
            itemw.sendall(msg)
            print('Send', msg)

    for iteme in exception:
        print('Exception: %s' % iteme)
        inputs.remove(iteme)
        if iteme in outputs:
            outputs.remove(iteme)
        iteme.close()
        del msg_dict[iteme]











