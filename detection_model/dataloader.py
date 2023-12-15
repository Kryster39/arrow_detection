from glob import glob
from random import randint, shuffle

import os
import sys
import numpy as np
import cv2

#[0:200, 0:680] -> [60:120, 60:600]
def crop_and_resize(img, crop=[60,120, 60,600], label=False):
    h, w = img.shape[0], img.shape[1]
    img = img[crop[0]:crop[1], crop[2]:crop[3]]
    
    if not label:
        img = cv2.resize( img, (w, h))
    else:
        img = cv2.resize( img, (w, h), interpolation=cv2.INTER_NEAREST)
    return img

def blur_and_noise(img, blur=5, noise_level=(0, 50)):
    img = cv2.blur(img, (blur, blur))

    mean, std = noise_level
    noise = np.zeros(img.shape, np.uint8)
    cv2.randn(noise, mean, std)
    img = cv2.add(img, noise)
    return img

class DataLoader():
    def __init__(self, dataset_path):
        self.train_file = glob(os.path.join(dataset_path, 'train', 'label_*.png'))
        self.test_file = glob(os.path.join(dataset_path, 'test', 'label_*.png'))

        self.train_data = []
        self.test_data = []

    def get_train_data(self, batch_size=4):
        if not self.train_data:
            for tnd in self.train_file:
                image = cv2.imread(os.path.join(os.path.dirname(tnd), os.path.basename(tnd)[6:]), cv2.IMREAD_GRAYSCALE)
                label = cv2.imread(tnd, cv2.IMREAD_GRAYSCALE)
                self.train_data.append((image, label))

        shuffle(self.train_data)
        for batch in range(0, len(self.train_data), batch_size):
            images = []
            labels = []
            for image, label in self.train_data[batch:batch+batch_size]:
                #crop and resize
                crop = [randint(0,60), randint(120,192), randint(0,60), randint(600,704)]
                image = crop_and_resize(image, crop=crop)
                label = crop_and_resize(label, crop=crop, label=True)

                #blur and noise
                arg = ( randint(1,10), randint(-10,10), randint(0,40) )
                image = blur_and_noise(image, blur=arg[0], noise_level=arg[1:])

                #one hot
                one_hot_label = np.zeros((label.shape[0], label.shape[1], 7))
                for i in range(7):
                    one_hot_label[:,:,i][label==i] = 1
                label = one_hot_label

                kernel = np.ones((3,3))
                label = cv2.dilate(label, kernel=kernel)
                #image[:,:,0][label==0] = 0
                #image[:,:,1][label==0] = 0
                #image[:,:,2][label==0] = 0
                #cv2.imshow('My Image', image)
                #cv2.waitKey(0)
                #cv2.destroyAllWindows()

                images.append(image)
                labels.append(label)
                #outputs.append((image, label))
            #print(len(outputs), len(outputs[0]), outputs[0][1].shape)
            yield (np.array(images), np.array(labels))

    def get_test_data(self, num=-1):
        if not self.test_data:
            for tsd in self.test_file:
                image = cv2.imread(os.path.join(os.path.dirname(tsd), os.path.basename(tsd)[6:]), cv2.IMREAD_GRAYSCALE)
                label = cv2.imread(tsd, cv2.IMREAD_GRAYSCALE)
                self.test_data.append((image, label))

        if num==-1:
            num = len(self.test_data)

        images = []
        labels = []
        for image, label in self.test_data[:num]:

            #one hot
            one_hot_label = np.zeros((label.shape[0], label.shape[1], 7))
            for i in range(7):
                one_hot_label[:,:,i][label==i] = 1
            label = one_hot_label
            
            kernel = np.ones((3,3))
            label = cv2.dilate(label, kernel=kernel)

            images.append(image)
            labels.append(label)
            #outputs.append((image, label))
        #print(len(outputs), len(outputs[0]), outputs[0][1].shape)
        return (np.array(images), np.array(labels))