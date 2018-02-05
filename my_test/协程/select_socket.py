#!/usr/bin/env python
# coding=utf-8
# Author: bloke
# Subject: select版本Socket server

import socket
import select
import queue

local_addr = ('localhost', 8080)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(local_addr)
server.setblocking(False)
server.listen(1)
print('Start server [%s: %s]' % local_addr)

inputs = [server]
outputs = []
msg_dict = {}

while True:
    readable, writable, exception = select.select(inputs, outputs, inputs)

    for r in readable:
        if r is server:
            conn, addr = r.accept()
            print('Client [%s: %s] is connected.' % conn.getpeername())
            inputs.append(conn)
            msg_dict[conn] = queue.Queue()
        else:
            try:
                recv_data = r.recv(1024)
            except ConnectionResetError as e:
                recv_data = None
            if not recv_data:
                inputs.remove(r)
                if r in outputs:
                    outputs.remove(r)
                print('Client [%s: %s] is disconnected.' % r.getpeername())
            else:
                print('Recv:', recv_data)
                outputs.append(r)
                msg_dict[r].put(recv_data.upper())

    for w in writable:
        try:
            send_data = msg_dict[w].get_nowait()
            w.sendall(send_data)
            print('Send:', send_data)
        except queue.Empty:
            outputs.remove(w)
        except Exception as e:
            print(e)

    for e in exception:
        inputs.remove(e)
        if e in outputs:
            outputs.remove(e)
        del msg_dict[e]


