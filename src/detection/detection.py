from keras.preprocessing import image
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
import os
import numpy as np

def find(img):
    for i in file:
        if i.startswith(img):
            return i

number_imgs = 8000
Y = np.empty(shape=(number_imgs, 3))
print(Y)
X = np.empty(shape=(number_imgs, 150, 150, 3))
train = 'dataset2'
file = open('dataset2.dat', 'r')
num = 0
for img in file:
    s = img.strip().split(' ')
    print(s[0])
    h = np.array([float(s[1]), float(s[2]), float(s[3])])
    Y[num] = h
    path = os.path.join(train, s[0])
    im = image.load_img(path, target_size=(150, 150))
    img = image.img_to_array(im)
    img = np.expand_dims(img, axis=0)
    X[num] = img
    if num == number_imgs - 1:
        break
    num += 1
file.close()
X = X.astype('float32')
X /= 255.0

n = int(len(Y) * 0.85)
X_train, X_test = X[:n], X[n:]
Y_train, Y_test = Y[:n], Y[n:]
num = 0
# ls = [[40, 50, 300], [50, 60, 300], [32, 32, 200], [40, 40, 300]]
# for i in ls:
model = Sequential()
model.add(Conv2D(40, (5, 5), input_shape=(150, 150, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.2))

model.add(Conv2D(50, (3,3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.2))

# model.add(Conv2D(i[2], (3,3), activation='relu'))
# model.add(MaxPooling2D(pool_size=(2,2)))
# model.add(Dropout(0.2))

model.add(Flatten())
model.add(Dense(200, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(3, activation='sigmoid'))

model.compile(loss='mean_absolute_percentage_error',
             optimizer='adam',
             metrics=['accuracy'])

model.fit(X_train, Y_train, validation_split=0.15, nb_epoch=10, batch_size=100)

scores = model.evaluate(X_test, Y_test)
print("Test: %.2f%%" % (scores[1]*100))

model_json = model.to_json()
json_file = open("model_det.json", "w")
json_file.write(model_json)
json_file.close()

model.save_weights("model_det.h5")
# num += 1

