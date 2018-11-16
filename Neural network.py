
from tensorflow.python.keras.preprocessing.image import ImageDataGenerator
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Conv2D, MaxPooling2D
from tensorflow.python.keras.layers import Activation, Dropout, Flatten, Dense


train = '/home/boris-zverkov/dataset/train/'
valid = '/home/boris-zverkov/dataset/validation/'
test = '/home/boris-zverkov/dataset/test/'
batch_size = 16
nb_train = 1326
nb_valid = 285
nb_test = 286

datagen = ImageDataGenerator(rescale=1./255)
train_generator = datagen.flow_from_directory(
    train,
    target_size=(150, 150),
    batch_size=batch_size,
    class_mode='binary')
validation_generator = datagen.flow_from_directory(
    valid,
    target_size=(150, 150),
    batch_size=batch_size,
    class_mode='binary')
test_generator = datagen.flow_from_directory(
    test,
    target_size=(150, 150),
    batch_size=batch_size,
    class_mode='binary')


model = Sequential()
model.add(Conv2D(32, (3,3), input_shape=(150, 150, 3), activation='relu'))
model.add(Conv2D(32, (3,3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
# model.add(Dropout(0.2))

model.add(Conv2D(32, (3,3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
# model.add(Dropout(0.2))

model.add(Conv2D(32, (3,3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
# model.add(Dropout(0.2))

model.add(Flatten())
model.add(Dense(500, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(1, activation='sigmoid'))

model.compile(loss='binary_crossentropy',
             optimizer='adam',
             metrics=['accuracy'])


model.fit_generator(train_generator,
                   steps_per_epoch=nb_train // batch_size,
                   epochs=30,
                   validation_data=validation_generator,
                   validation_steps=nb_valid // batch_size)

scores = model.evaluate_generator(test_generator, nb_test // batch_size)
print("Аккуратность на тестовых данных: %.2f%%" % (scores[1]*100))

