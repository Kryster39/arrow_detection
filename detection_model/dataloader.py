from glob import glob
from random import randint

import os
import sys
import numpy as np
import cv2

#[0:200, 0:680] -> [60:120, 60:600]
def crop_and_resize(img, crop=[60,120, 60,600]):
    h, w = img.shape[0], img.shape[1]
    img = img[crop[0]:crop[1], crop[2]:crop[3]]
    
    img = cv2.resize( img, (w, h))
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
        train_data = glob(os.path.join(dataset_path, 'train', 'label_*.png'))
        test_data = glob(os.path.join(dataset_path, 'test', 'label_*.png'))

        self.train_data = []
        for tnd in train_data:
            image = cv2.imread(os.path.join(os.path.dirname(tnd), os.path.basename(tnd)[6:]), cv2.IMREAD_COLOR)[:,:,::-1]
            label = cv2.imread(tnd, cv2.IMREAD_GRAYSCALE)
            self.train_data.append((image, label))

    def get_train_data(self, batch_size=4):
        for batch in range(0, len(self.train_data), batch_size):
            images = []
            labels = []
            for image, label in self.train_data[batch:batch+batch_size]:
                #crop and resize
                crop = [randint(0,60), randint(120,200), randint(0,60), randint(600,680)]
                image = crop_and_resize(image, crop=crop)
                label = crop_and_resize(label, crop=crop)

                #blur and noise
                arg = ( randint(0,10), randint(-10,10), randint(0,100) )
                image = blur_and_noise(image, blur=arg[0], noise_level=arg[1:])

                #image[:,:,0][label==0] = 0
                #image[:,:,1][label==0] = 0
                #image[:,:,2][label==0] = 0
                cv2.imshow('My Image', image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

                images.append(image)
                labels.append(label)
            yield (images, labels)