import cv2 as cv
import numpy as np
import socket
import sys
from timeit import default_timer as timer
from keras.preprocessing import image
from keras.utils import np_utils
from keras import models
import datetime

def make_string(balls):
    s = str(len(balls)) + ' '
    for i in balls:
        for j in i:
            s += str(j) + ' '
    return s

json_file = open("model.json", "r")
js_model = json_file.read()
json_file.close()

model = models.model_from_json(js_model)

model.load_weights('model.h5')
model.compile(loss="binary_crossentropy", optimizer='adam', metrics=['accuracy'])


def prediction(frame, balls):
    result = []
    for (x, y, w, h) in balls:
        im = frame[y:y+h, x:x+w]
        im = cv.cvtColor(im, cv.COLOR_BGR2RGB)
        im = cv.resize(im, (150, 150))
        img = image.img_to_array(im)
        img /= 255
        img = np.expand_dims(im, axis=0)
        res = model.predict(img)
        if res < 0.5:
            # print(res)
            cv.circle(frame, (x + w // 2, y + h // 2), w // 2, (0, 0, 255), 2)
            result.append((x, y, w, h))
    return result


def resizing(frame, balls):
    if len(balls) == 0:
        return None, (0, 0)
    (x, y, w, h) = balls[0]
    y1 = y - 100
    h1 = 100
    if y1 < 0:
        y1 = 0
        # h1 = y -y1
    x1 = x - 100
    w1 = 100
    if x1 < 0:
        x1 = 0
        # w1 = x -x1
    cv.rectangle(frame, (x1, y1), (x1 + (2 * h1) + h, y1 + (2 * w1) + w), (0, 255, 0), 2)
    return frame[y1: y1 + (w1 * 2), x1: x1 + (h1 * 2)], (h, w)
    # delta = radius // 2
    # x = int(round(center[0] - radius - delta))
    # if x < 0:
    #     x = 0
    # y = int(round(center[1] - radius - delta))
    # if y < 0:
    #     y = 0
    # xm = int(round(center[0] + radius + delta))
    # if xm > frame.shape[1]:
    #     xm = frame.shape[1]
    # ym = int(round(center[1] + radius + delta))
    # if ym > frame.shape[0]:
    #     ym = frame.shape[0]
    # im = frame[y:ym, x:xm]
    # im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    # im = cv2.resize(im, (150, 150))
    # img = image.image.img_to_array(im)
    # img /= 255
    # img = np.expand_dims(im, axis=0)
    # res = model.predict(img)
    # if res > 0.5:
    #     print(res)
    #     cv2.circle(frame, center, radius, (0, 0, 255), 2)
    # # print(timer() - t)

# ball_cascade = sys.argv[1]
# ball_cascade =  '/home/boris-zverkov/images/data/cascade.xml'
ball_cascade =  'cascade/cascade.xml'
cascade = cv.CascadeClassifier()
cascade.load(ball_cascade)

host = ''
port = 3333
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind((host, port))
serv.listen(1)
clien, addr = serv.accept()
# try:
capture = cv.VideoCapture(0)
balls = []

while True:
    while True:
        if clien.recv(1024).decode('utf-8') == 'get':
            break
    ok, frame = capture.read()
    if not ok:
      break

    im, (h, w) = resizing(frame, balls)
    if type(im) != type(None):
        t = timer()
        balls = cascade.detectMultiScale(im, minSize=(h - 20, w - 20), maxSize=(h + 20, w + 20))
        print('small', timer() -t)
    else:
        t = timer()
        balls = cascade.detectMultiScale(frame, scaleFactor=2)
        print('full', timer() - t)
    t = timer()
    balls = prediction(frame, balls)
    print('nn', timer() - t)
    frame = frame.flatten()
    data = frame.tostring()
    clien.send(data)
# except:
capture.release()
serv.close()
