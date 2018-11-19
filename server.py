import cv2 as cv
import subprocess
import socket
import sys
import time

host = ''
port = 3333
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind((host, port))
serv.listen(1)
clien, addr = serv.accept()
#data = clien.recv(1024).decode('utf-8')
#while data != 'begin':
#        data = clien.recv(1024).decode('utf-8')
#time.sleep(1)
try:
    capture = cv.VideoCapture(0)

    while True:
        ok,frame = capture.read()
        if not ok:
          break
        #frame = cv.resize(frame, (320, 240))
        frame = frame.flatten()
        print(frame, frame.size)
        data = frame.tostring()
        print(len(data))
                #print(len(dat))
                #clien.send('%16d'.encode('utf-8') % len(dat))
        clien.send(data)
except:
    capture.release()
    serv.close()
