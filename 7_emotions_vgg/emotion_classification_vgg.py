from __future__ import print_function

import os

from tensorflow.python.keras.preprocessing.image import ImageDataGenerator
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense, Dropout, Activation, Flatten, BatchNormalization
from tensorflow.python.keras.layers import Conv2D, MaxPooling2D
from tensorflow.python.keras.callbacks import TensorBoard

from tensorflow.python.keras.optimizers import Adam
from tensorflow.python.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau


num_classes = 7
img_rows, img_cols = 48, 48
batch_size = 32

dir_path = os.getcwd()

train_data_dir = dir_path + '/datasets/training'
validation_data_dir = dir_path + '/datasets/validation'

print(train_data_dir)

train_data_generator = ImageDataGenerator(rescale=1. / 255,
                                          rotation_range=30,
                                          shear_range=0.3,
                                          zoom_range=0.3,
                                          width_shift_range=0.4,
                                          height_shift_range=0.4,
                                          horizontal_flip=True,
                                          fill_mode='nearest')

validation_data_generator = ImageDataGenerator(rescale=1. / 255)

train_generator = train_data_generator.flow_from_directory(train_data_dir,
                                                           color_mode='grayscale',
                                                           target_size=(img_rows, img_cols),
                                                           batch_size=batch_size,
                                                           class_mode='categorical',
                                                           shuffle=True)

validation_generator = validation_data_generator.flow_from_directory(validation_data_dir,
                                                                     color_mode='grayscale',
                                                                     target_size=(img_rows, img_cols),
                                                                     batch_size=batch_size,
                                                                     class_mode='categorical',
                                                                     shuffle=True)

model = Sequential()

# Feature Learning Layer 0
model.add(Conv2D(32, (3, 3), padding='same', kernel_initializer='he_normal', input_shape=(img_rows, img_cols, 1)))
model.add(Activation('elu'))
model.add(BatchNormalization())
model.add(Conv2D(32, (3, 3), padding='same', kernel_initializer='he_normal', input_shape=(img_rows, img_cols, 1)))
model.add(Activation('elu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.2))

# Feature Learning Layer 1
model.add(Conv2D(64, (3, 3), padding='same', kernel_initializer='he_normal'))
model.add(Activation('elu'))
model.add(BatchNormalization())
model.add(Conv2D(64, (3, 3), padding='same', kernel_initializer='he_normal'))
model.add(Activation('elu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.2))

# Feature Learning Layer 3
model.add(Conv2D(128, (3, 3), padding='same', kernel_initializer='he_normal'))
model.add(Activation('elu'))
model.add(BatchNormalization())
model.add(Conv2D(128, (3, 3), padding='same', kernel_initializer='he_normal'))
model.add(Activation('elu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.2))

# Feature Learning Layer 4
model.add(Conv2D(256, (3, 3), padding='same', kernel_initializer='he_normal'))
model.add(Activation('elu'))
model.add(BatchNormalization())
model.add(Conv2D(256, (3, 3), padding='same', kernel_initializer='he_normal'))
model.add(Activation('elu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.2))

# Feature Learning Layer 4
model.add(Flatten())
model.add(Dense(64, kernel_initializer='he_normal'))
model.add(Activation('elu'))
model.add(BatchNormalization())
model.add(Dropout(0.5))

# Feature Learning Layer 5
model.add(Dense(64, kernel_initializer='he_normal'))
model.add(Activation('elu'))
model.add(BatchNormalization())
model.add(Dropout(0.5))

# Feature Learning Layer 6
model.add(Dense(num_classes, kernel_initializer='he_normal'))
model.add(Activation('softmax'))

print(model.summary())

#
# Creating Models
#

checkpoint = ModelCheckpoint('emotion_classification_vgg_7_emotions.h5',
                             monitor='val_loss',
                             mode='min',
                             save_best_only=True,
                             verbose=1)

early_stop = EarlyStopping(monitor='val_loss',
                           min_delta=0,
                           patience=3,
                           verbose=1,
                           restore_best_weights=True)

reduce_lr = ReduceLROnPlateau(monitor='val_loss',
                              factor=0.2,
                              patience=3,
                              verbose=1,
                              min_delta=0.0001)

tensor_board = TensorBoard(log_dir='./graph')

callbacks = [early_stop, checkpoint, reduce_lr, tensor_board]

model.compile(loss='categorical_crossentropy',
              optimizer=Adam(lr=0.001),
              metrics=['accuracy'])

nb_train_samples = 28789
nb_validation_samples = 3589
epochs = 25

history = model.fit_generator(train_generator,
                              steps_per_epoch=nb_train_samples // batch_size,
                              epochs=epochs,
                              callbacks=callbacks,
                              validation_data=validation_generator,
                              validation_steps=nb_validation_samples // batch_size)

model_json = model.to_json()

with open("emotion_classification_vgg_7_emotions.json", "w") as json_file:
    json_file.write(model_json)