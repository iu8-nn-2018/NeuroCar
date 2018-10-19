#!/usr/bin/env python

import videocam
import socket
import sys
import time

capture = videocam.start()
host = ''
port = 3333
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind((host, port))
serv.listen(1)
clien, addr = serv.accept()
data = clien.recv(1024).decode('utf-8')
while data != 'begin':
        data = clien.recv(1024).decode('utf-8')
time.sleep(1)
try:
        while True:
                dat = videocam.read_picture(capture)
                print(len(dat))
                clien.send('%16d'.encode('utf-8') % len(dat))
                clien.send(dat)
                time.sleep(1)
except:
        videocam.end(capture)
serv.close()
