#from model import ArrowDetectionModel
from dataloader import DataLoader
from PIL import Image
#from glob import glob
#from random import randint

import os
import sys
import numpy as np
import cv2
'''
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

datas = glob(os.path.join(sys.argv[1], 'train', 'label_*.png'))
images = []
labels = []
for data in datas[:1]:
    image = cv2.imread(os.path.join(os.path.dirname(data), os.path.basename(data)[6:]), cv2.IMREAD_COLOR)[:,:,::-1]
    label = cv2.imread(data, cv2.IMREAD_GRAYSCALE)

    cv2.imshow('My Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    #crop and resize
    crop = [randint(0,60), randint(120,200), randint(0,60), randint(600,680)]
    image = crop_and_resize(image, crop=crop)
    label = crop_and_resize(label, crop=crop)

    cv2.imshow('My Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    #blur and noise
    arg = ( randint(0,10), randint(-10,10), randint(0,100) )
    print(arg)
    image = blur_and_noise(image, blur=arg[0], noise_level=arg[1:])

    cv2.imshow('My Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    image[:,:,0][label==0] = 0
    image[:,:,1][label==0] = 0
    image[:,:,2][label==0] = 0
    cv2.imshow('My Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    images.append(image)
    labels.append(label)
'''
DL = DataLoader(dataset_path='dataset')
g = DL.get_train_data(batch_size=4)
xy = next(g)
print(len(xy[0]), xy[0][1].shape)
xy = next(g)
print(len(xy[0]), xy[0][1].shape)
'''
const xs = tf.data.generator(data);
const ys = tf.data.generator(labels);
# We zip the data and labels together, shuffle and batch 32 samples at a time.
const ds = tf.data.zip({xs, ys}).shuffle(100 /* bufferSize */).batch(32);

# Train the model for 5 epochs.
model.fitDataset(ds, {epochs: 5}).then(info => {
    console.log('Accuracy', info.history.acc);
});
'''
#model = ArrowDetectionModel()
#print(model.summary())