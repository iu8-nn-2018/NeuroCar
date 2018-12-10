import numpy as np
import cv2
from timeit import default_timer as timer
import time
from keras.preprocessing import image
from keras.utils import np_utils
from tensorflow.keras import models
from keras import models as ms
import os


json_file = open("finding_old_struct_squared1.json", "r")
js_model = json_file.read()
json_file.close()

model = models.model_from_json(js_model)
model.load_weights("finding_old_struct_squared1.h5")
# model = models.load_model('file')

model.compile(loss="mean_squared_error", optimizer='adam', metrics=['accuracy'])
print('compiled')

cap = cv2.VideoCapture(0)
while True:
    ok, fr = cap.read()
    if not ok:
        break
    im = cv2.resize(fr, (240, 320))
    im = im.astype('float32')
    im /= 255.0
    im = np.expand_dims(im, axis=0)
    res = model.predict(im)
    # print(res)
    x = int(float(res[0][1]) * 320) + 320
    y = int(float(res[0][2]) * 240) + 240
    r = max(0, int(float(res[0][3]) * 320))
    print(x, y, r)
    cv2.circle(fr, (x,y), r, (255, 0, 0), 2)
    cv2.imshow('f', fr)
    if cv2.waitKey(10) == 27:
        break
cap.release()
p = '/home/boris-zverkov/im_car2'
for i in os.listdir(p):
    fr = cv2.imread(os.path.join(p, i))
    print(fr)
    im = cv2.resize(fr, (240, 320))
    im = im.astype('float32')
    im /= 255.0
    im = np.expand_dims(im, axis=0)
    res = model.predict(im)
    print(res)
    x = int(float(res[0][1]) * 320) + 320
    y = int(float(res[0][2]) * 240) + 240
    r = max(0, int(float(res[0][3]) * 320))
    cv2.circle(fr, (x,y), r, (255, 0, 0), 2)
    cv2.imshow('f', fr)
    while True:
        if cv2.waitKey(10) == 27:
            break
