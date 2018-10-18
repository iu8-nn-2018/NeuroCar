#!/usr/bin/env python3

import socket
import os
host = os.popen("./connect.sh").read()
print(host)
port = 3333
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))
data = 1
while int(data) != 0:
	data = input()
	sock.send(data.encode('utf-8'))
sock.close()

