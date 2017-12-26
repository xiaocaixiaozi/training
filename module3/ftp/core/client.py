#!/usr/bin/env python
# coding=utf-8
# Author: bloke

import socket

host, port = 'localhost', 9999

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

while 1:
    data_list = []
    data = input('Sent: ').strip()
    if not data: continue
    client.sendall(bytes(data, 'utf-8'))
    # while 1:
    recv_data = client.recv(1024)
    print('Recv:', recv_data.decode('utf-8'))
        # if recv_data:
        #     data_list.append(recv_data)
        #     continue
        # else:
        #     print('Recv:', ''.join(data_list))
        #     break



# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
#     client.connect((host, port))
#     while 1:
#         recv_list = []
#         data = input('Send: ').strip()
#         if not data: continue
#         client.sendall(bytes(data, 'utf-8'))
#         # while 1:
#         #     recv = client.recv(2)
#         #     if len(recv) > 0:
#         #         recv_list.append(data)
#         #         continue
#         #     else:
#         #         print('break..')
#         #         break
#         # full_data = ''.join(recv_list)
#         recv = client.recv(1024)
#         print('Recv:', recv)







