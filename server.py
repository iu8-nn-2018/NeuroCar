#!/usr/bin/env python3

import socket
import sys
import wiringpi as wiringpi

host = ''
port = 3333
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
wiringpi.wiringPiSetupGpio()
wiringpi.pinMode(18,2)
wiringpi.pwmSetMode(0)
wiringpi.pwmSetClock(400)
wiringpi.pwmSetRange(1024)
wiringpi.pwmWrite(18, 0)
serv.bind((host, port))
serv.listen(1)
clien, addr = serv.accept()
while True:
        data = int(clien.recv(1024).decode('utf-8').strip())
        if not data:
                break
        if data > 255 or data < 0:
                wiringpi.pwmWrite(18, 0)
        else:
                wiringpi.pwmWrite(18, data)
serv.close()
wiringpi.pwmWrite(18, 0)
