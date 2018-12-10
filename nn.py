from keras.preprocessing import image
from keras import models
from keras.layers import Input, Dense, Conv2D, MaxPooling2D, Flatten, Dropout
from keras.models import Model, Sequential
from keras.layers.merge import concatenate
from timeit import default_timer as timer
import cv2 as cv

import os
import numpy as np

def find(img):
    for i in file:
        if i.startswith(img):
            return i

number_imgs = 1687
Y = np.empty(shape=(number_imgs, 4))
X = np.empty(shape=(number_imgs, 320, 240, 3))
train = '/home/boris-zverkov/im_car2'
file = open('/home/boris-zverkov/new_nn2.dat', 'r')
num = 0
for img in file:
    s = img.strip().split(' ')
    h = np.array([int(s[1]), float(s[2]), float(s[3]), float(s[4])])
    print(h)
    Y[num] = h
    path = os.path.join(train, s[0])
    im = image.load_img(path, target_size=(320, 240))
    img = image.img_to_array(im)
    img = np.expand_dims(img, axis=0)
    X[num] = img
    if num == number_imgs - 1:
        break
    num += 1
file.close()
print(Y)
X = X.astype('float32')
X /= 255.0

np.save('data_new_nn', X)
np.save('res_new_nn', Y)
print('saved')

# json_file = open("finding.json", "r")
# js_model = json_file.read()
# json_file.close()
#
# model = models.model_from_json(js_model)
# model.load_weights("finding.h5")

# inp = Input(shape=(320, 240, 3))
#
# conv1 = Conv2D(5, (7,7), strides=(2, 2), padding='valid', activation='relu')(inp)
# pool1 = MaxPooling2D(pool_size=(3,3), strides=3)(conv1)
# conv2 = Conv2D(10, (5,5), strides=(2,2), padding='valid', activation='relu')(pool1)
# pool2 = MaxPooling2D(pool_size=(2,2), strides=(2,2))(conv2)
# fl = Flatten()(pool2)
# dense = Dense(150, activation='relu')(fl)
#
# ball = Dense(1, activation='relu')(dense)
# coord = Dense(2, activation='tanh')(dense)
# r = Dense(1, activation='sigmoid')(dense)
# out = concatenate([ball, coord, r])
# model = Model(inputs=inp, outputs=out)
#
# model.compile(loss='mean_squared_error',
#              optimizer='adam',
#              metrics=['accuracy'])
#
#
# model.fit(X, Y, validation_split=0.15, epochs=3)


model = Sequential()
model.add(Conv2D(30, (5, 5), input_shape=(320, 240, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.2))

model.add(Conv2D(30, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.2))
model.add(Conv2D(30, (3,3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.2))

model.add(Flatten())
model.add(Dense(150, activation='relu'))
model.add(Dense(4, activation='tanh'))

model.compile(loss='mean_squared_error',
             optimizer='adam',
             metrics=['accuracy'])


model.fit(X, Y, validation_split=0.15, epochs=20)

#
# model = Sequential()
# model.add(Conv2D(1, (7,7), input_shape=(320, 240, 3), strides=(2, 2), padding='valid', activation='relu'))
# model.add(MaxPooling2D(pool_size=(3,3), strides=3))
# model.add(Conv2D(4, (5,5), strides=(2,2), padding='valid', activation='relu'))
# model.add(MaxPooling2D(pool_size=(2,2), strides=(2,2)))
# model.add(Flatten())
# model.add(Dense(128, activation='relu'))
#
# model.add(Dense(4, activation='relu'))
#
# model.compile(loss='mean_absolute_percentage_error',
#              optimizer='adam',
#              metrics=['accuracy'])
#
# model.fit(X, Y, validation_split=0.15, epochs=5)



model_json = model.to_json()
json_file = open("finding_old_struct_squared1.json", "w")
json_file.write(model_json)
json_file.close()

model.save_weights("finding_old_struct_squared1.h5")
# model = Sequential()
# model.add(Conv2D(1, (7,7), input_shape=(320, 240, 3), strides=(2, 2), padding='valid', activation='relu'))
# model.add(MaxPooling2D(pool_size=(3,3), strides=3))
# model.add(Conv2D(4, (5,5), strides=(2,2), padding='valid', activation='relu'))
# model.add(MaxPooling2D(pool_size=(2,2), strides=(2,2)))
# model.add(Flatten())
# model.add(Dense(128, activation='relu'))
# #
# ball = Dense(1, activation='relu')
# coord = Dense(2, activation='tanh')
# r = Dense(1, activation='sigmoid')
# merge = concatenate([ball, coord, r])
# model.add(merge)
#
# model.add(Dense(4, activation='relu'))
#
# model.compile(loss='mean_absolute_percentage_error',
#              optimizer='adam',
#              metrics=['accuracy'])
# model.fit(X, Y, nb_epoch=1)
# print(model.predict(frame))
#
# model_json = model.to_json()
# json_file = open("finding.json", "w")
# json_file.write(model_json)
# json_file.close()
#
# model.save_weights("finding.h5")
#
#
#
