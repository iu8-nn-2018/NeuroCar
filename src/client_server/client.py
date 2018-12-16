
import cv2
import sys

import numpy as np
import socket
import os
print('start')
from PyQt5 import  QtWidgets, QtCore

from PyQt5.QtWidgets import (QWidget, QHBoxLayout,
    QLabel, QApplication)
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap

def show_balls(s):
    ls = [int(i) for i in s.strip().split(' ')]
    balls = []
    for i in range(ls[0]):
        x = int(ls[i * 3 + 1])
        y = int(ls[i * 3 + 2])
        r = int(ls[i * 3 + 3])
        balls.append([x, y, r])
    return balls

class Thread(QThread):
    changePixmap = pyqtSignal(QImage)

    def run(self):
        # host = '192.168.43.245'
        host =''
        port = 3333

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        while True:
            print('send')
            sock.send('get'.encode('utf-8'))
            data = sock.recv(1024)
            while len(data) != 230400:
                l = sock.recv(1024)
                # print('get l')
                if not l:
                    # print('not l')
                    break
                data += l
                # print('added')
                # print(len(data))
                if 0 < 230400 - len(data) < 1024:
                    # print('low len')
                    data += sock.recv(1024)
                    # print('out')
                    break
            if len(data) != 230400:
                # print('again')
                continue
            frame = np.fromstring(data, dtype=np.uint8)
            frame = np.reshape(frame, (240, 320, 3))
            frame = cv2.resize(frame, (640, 480))
            # rgbImage = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
            p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
            self.changePixmap.emit(p)


class App(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        self.title = 'PyQt5 Video'
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 480
        self.initUI()

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.resize(780, 500)
        # create a label
        self.label = QLabel(self)
        self.label.resize(640, 480)
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(0, 480, 200, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.button = QtWidgets.QPushButton(self)
        self.button.setGeometry(QtCore.QRect(200, 480, 50, 20))
        self.button.setObjectName("Ok")
        self.button.setText("Ok")
        self.button.clicked.connect(self.check)
        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()

    def check(self):
        print(self.lineEdit.text())
        if self.lineEdit.text() == "admin":
            print('ok')
            self.admin()

    def admin(self):
        self.up = QtWidgets.QPushButton(self)
        print('here')
        self.up.setGeometry(QtCore.QRect(640, 0, 120, 120))
        self.up.setObjectName("up")
        self.up.setText("Up")
        self.up.setVisible(True)
        self.down = QtWidgets.QPushButton(self)
        self.down.setGeometry(QtCore.QRect(640, 120, 120, 120))
        self.down.setObjectName("down")
        self.down.setText("Down")
        self.down.setVisible(True)
        self.left = QtWidgets.QPushButton(self)
        self.left.setGeometry(QtCore.QRect(640, 240, 120, 120))
        self.left.setObjectName("left")
        self.left.setText("Left")
        self.left.setVisible(True)
        self.right = QtWidgets.QPushButton(self)
        self.right.setGeometry(QtCore.QRect(640, 360, 120, 120))
        self.right.setObjectName("right")
        self.right.setText("Right")
        self.right.setVisible(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
