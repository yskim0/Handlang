# Imports for Deep Learning
from keras.layers import Conv2D, Dense, Dropout, Flatten
from keras.models import Sequential
from keras.preprocessing.image import ImageDataGenerator
from keras.layers.normalization import BatchNormalization
# ensure consistency across runs
from numpy.random import seed
seed(1)
import tensorflow as tf
tf.random.set_seed(2)


# Imports to view data
#import cv2
from glob import glob
#from matplotlib import pyplot as plt
from numpy import floor
import random
'''
def plot_three_samples(letter):
    print("Samples images for letter " + letter)
    base_path = './input/asl_alphabet_train/asl_alphabet_train/'
    # kaggle 데이터셋 위 경로로 저장해서 진행
    img_path = base_path + letter + '/**'
    path_contents = glob(img_path)
    
    plt.figure(figsize=(16,16))
    imgs = random.sample(path_contents, 3)
    plt.subplot(131)
    plt.imshow(cv2.imread(imgs[0]))
    plt.subplot(132)
    plt.imshow(cv2.imread(imgs[1]))
    plt.subplot(133)
    plt.imshow(cv2.imread(imgs[2]))
    return
'''
#plot_three_samples('0')

data_dir = "Sign-Language-Digits-Dataset/Dataset"
# kaggle 데이터셋 위 경로로 저장해서 진행
target_size = (64, 64)
target_dims = (64, 64, 3) # add channel for RGB
n_classes = 10 #########
val_frac = 0.1
batch_size = 64

data_augmentor = ImageDataGenerator(samplewise_center=True, 
                                    samplewise_std_normalization=True, 
                                    validation_split=val_frac)

train_generator = data_augmentor.flow_from_directory(data_dir, target_size=target_size, batch_size=batch_size, shuffle=True, subset="training")
val_generator = data_augmentor.flow_from_directory(data_dir, target_size=target_size, batch_size=batch_size, subset="validation")

handlang_model = Sequential()
handlang_model.add(Conv2D(64, kernel_size=4, strides=1, activation='relu', input_shape=target_dims))
handlang_model.add(Conv2D(64, kernel_size=4, strides=2, activation='relu'))
handlang_model.add(Dropout(0.5))
handlang_model.add(Conv2D(128, kernel_size=4, strides=1, activation='relu'))
handlang_model.add(Conv2D(128, kernel_size=4, strides=2, activation='relu'))
handlang_model.add(Dropout(0.5))
handlang_model.add(Conv2D(256, kernel_size=4, strides=1, activation='relu'))
handlang_model.add(Conv2D(256, kernel_size=4, strides=2, activation='relu'))
#handlang_model.add(BatchNormalization()) #######################################
handlang_model.add(Flatten())
handlang_model.add(Dropout(0.5))
handlang_model.add(Dense(1024, activation='relu')) ############################
handlang_model.add(Dense(512, activation='relu'))
#handlang_model.add(Dropout(0.5)) ###############################
handlang_model.add(Dense(n_classes, activation='softmax'))

handlang_model.summary()

handlang_model.compile(optimizer='adamax', loss='categorical_crossentropy', metrics=["accuracy"])

from keras.callbacks import ModelCheckpoint
handlang_model.fit_generator(train_generator, epochs=10, validation_data=val_generator,
                            callbacks=[ModelCheckpoint(filepath='models/su_dense.h5', save_best_only=True, verbose=1)])

# 덮어씌워지는 거라서 epoch 별로 저장하려면 이름 변경