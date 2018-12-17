import cv2 as cv
from timeit import default_timer as timer
from keras import models
import numpy as np
import socket
import math
from threading import Thread
from multiprocessing import Queue, Pool
# from car import car

def predict(balls, frame, model):
    predicted = []
    for (x, y, w, h) in balls:
        if 4 < x < 315 and 4 < y < 235:
            im = frame[y - 5:y + h + 5, x - 5:x + w + 5]
        else:
            im = frame[y:y + h, x:x + w]
        im = cv.resize(im, (50, 50))
        im = im.astype('float32')
        im /= 255.0
        im = np.expand_dims(im, axis=0)
        res = model.predict(im)
        # print(res)
        # print('predict', timer() - t)
        if res < 0.5:
            predicted.append((x,  y, w, h))
    return predicted


def Set_speed(speed_r, speed_l, last_x, last_y, last_ang, balls, frame):
    # print(balls)
    target_r = 20
    if len(balls) == 0:
        # car.stop()
        return 29, 29, 160, 240, 0, frame
    if len(balls) != 1:
        dist = 10000
        num = 0
        for i in range(len(balls)):
            l = math.sqrt((last_x - balls[i][0]) ** 2 + (last_y - balls[i][1]) ** 2)
            if l < dist:
                num = i
                dist = l
        balls = [balls[num]]
    x, y, w, h = balls[0]
    print(x, y, w, h)
    cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    rad = w // 2
    ang = math.atan(float((x - 160)) / (240 - y))
    print('last(r, l)', speed_r, speed_l)
    ang = math.degrees(ang)
    delta = ang - last_ang
    print(ang, delta)
    if rad == target_r and -25 < ang < 25:
        # car.stop()
        return 29, 29, x, y, ang, frame
    if rad < target_r and y < last_y:  # and rad < 90:
        speed_l += 5
        speed_r += 4
    if rad > target_r and y > last_y:  # last_r and rad > 90:
        speed_l -= 4
        speed_r -= 4

    if 25 < ang:
        if rad < target_r:
            speed_l += 1
        elif rad == target_r:
            speed_l += 1
        else:
            speed_r -= 2
    if ang < -25:
        if rad < target_r:
            speed_r += 1
        elif rad == target_r:
            speed_r += 1
        else:
            speed_l -= 2
    speed_l = min(127, speed_l)
    speed_r = min(127, speed_r)
    speed_l = max(-127, speed_l)
    speed_r = max(-127, speed_r)
    cur_speed_l = 0
    cur_speed_r = 0
    if speed_l < 0:
        cur_speed_l = -1 * speed_l
    elif speed_l != 0:
        cur_speed_l = (128 - speed_l) * 2 + speed_l
    if speed_r < 0:
        cur_speed_r = -1 * speed_r
    elif speed_r != 0:
        cur_speed_r = (128 - speed_r) * 2 + speed_r
    print('get(r, l)', speed_r, speed_l)
    if not 29 < cur_speed_l < 221:
        cur_speed_l = 29
    if not 29 < cur_speed_r < 221:
        cur_speed_r = 29
    if cur_speed_l != 29 or cur_speed_r != 29:
        print('l, r', cur_speed_l, cur_speed_r)
        # car.set_speed(cur_speed_r, cur_speed_l)
    else:
        print('stop')
        # car.stop()
    return speed_r, speed_l, x, y, ang, frame


def check(balls):
    res = []
    # print(balls)
    flag = True
    for i in balls:
        flag = True
        for j in balls:
            if i == j:
                continue
            if j[0] < i[0] < j[0] + j[2] and j[1] < i[1] < j[1] + j[3] and i[3] < j[3]:
                flag = False
                break
        if flag:
            res.append(i)
    # print(res)
    return res


def work(input_q, output_q):
    ball_cascade = 'data/cascade.xml'
    cascade = cv.CascadeClassifier()
    cascade.load(ball_cascade)
    model = models.load_model('binary_small.h5')
    model.compile(loss="binary_crossentropy", optimizer='adam', metrics=['accuracy'])
    last_x = 160
    last_y = 240
    last_r = 0
    speed_l = 29
    speed_r = 29
    last_ang = 0

    while True:
        frame = input_q.get()
        balls = cascade.detectMultiScale(frame, scaleFactor=2)
        balls = predict(balls, frame, model)
        balls = check(balls)
        speed_r, speed_l, last_x, last_y, last_ang, frame = Set_speed(speed_r, speed_l, last_x, last_y,
                                                                               last_ang, balls, frame)
        output_q.put(frame)



class Stream:
    def __init__(self):
        self.cap = cv.VideoCapture(0)
        self.ok, self.frame = self.cap.read()

        self.stopped = False

    def start(self):
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        while True:
            if self.stopped:
                return
            self.ok, self.frame = self.cap.read()

    def read(self):
        self.frame = cv.resize(self.frame, (320, 240))
        return self.frame

    def stop(self):
        self.stopped = True


if __name__ == '__main__':

    host = ''
    port = 3333
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv.bind((host, port))
    print('ready')
    serv.listen(1)
    clien, addr = serv.accept()



    capture = Stream().start()
    input_q = Queue(maxsize=8)
    output_q = Queue(maxsize=8)

    pool = Pool(4, work, (input_q, output_q))
    try:
        while True:
            frame = capture.read()
            input_q.put(frame)

            fr = output_q.get()
            fr = fr.flatten()
            data = fr.tostring()
            clien.send(data)

            if cv.waitKey(10) == 27:
                break
    except:
        pool.terminate()
        capture.stop()
        cv.destroyAllWindows()
