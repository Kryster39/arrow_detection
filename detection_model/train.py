from model import ArrowDetectionModel
from PIL import Image
from glob import glob

import os
import sys
import numpy as np
import cv2

def zoom_at(img, zoom=1):
    # Translate to zoomed coordinates
    shape = [ zoom * i for i in img.shape ]
    h, w = shape[0], shape[1]

    cx, cy = w/2, h/2
    
    img = cv2.resize( img, (0, 0), fx=zoom, fy=zoom)
    img = img[ int(round(cy - h/zoom * .5)) : int(round(cy + h/zoom * .5)),
               int(round(cx - w/zoom * .5)) : int(round(cx + w/zoom * .5))]
    
    return img

datas = glob(os.path.join(sys.argv[1], 'train', 'label_*.png'))
for data in datas[:1]:
    image = cv2.imread(os.path.join(os.path.dirname(data), os.path.basename(data)[6:]), cv2.IMREAD_COLOR)[:,:,::-1]
    label = cv2.imread(data, cv2.IMREAD_GRAYSCALE)

    cv2.imshow('My Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    #zoom in
    image = zoom_at(image, zoom=1.2)
    label = zoom_at(label, zoom=1.2)

    #
    #image[:,:,0][label==0] = 0
    #image[:,:,1][label==0] = 0
    #image[:,:,2][label==0] = 0
    #cv2.imshow('My Image', image)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()



#model = ArrowDetectionModel()
#print(model.summary())