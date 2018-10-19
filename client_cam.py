#!/usr/bin/env python3

import numpy as np
import socket
import os
import sys
host = os.popen("./connect.sh").read()
port = 3333
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))
name = 1
path = sys.argv[1]
sock.send('begin'.encode('utf-8'))
try:
	while True:
		data = int(sock.recv(16).decode('utf-8').strip())
		print(data)
		if not data:
			break
		image = b''
		while data > len(image):
			image += sock.recv(1024)
		filename = os.path.join(path, str(name) + '.jpg')
		out = open(filename, 'wb')
		out.write(image)
		out.close()
		name += 1
except:
	sock.close()
