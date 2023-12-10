import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
from glob import glob

#r:up, k:left, g:right
class_map = {0:'nan', 1:'up', 2:'right', 3:'keyK', 4:'keyJ', 5:'left', 6:'down'}
class_trns = {0:0, 1:1, 2:4, 3:6, 4:5, 5:3, 6:2}
color_map = {0:'r', 1:'g', 2:'b', 3:'y', 4:'k', 5:'o'}

images = glob(os.path.join(sys.argv[1], "*.png"))
for image in images:
    img = np.array(Image.open(image))
    shape = img.shape[:-1]
    lbl = np.zeros(img.shape[:-1])
    
    f = open(image[:-3]+"txt", 'r')
    lines = f.readlines()
    for l, line in enumerate(lines):
        line = line[:-1].split(' ')
        label_class = int(line[0])+1
        label_range = [ float(i) for i in line[1:] ]
        label_range = [ 
            int((label_range[0]-label_range[2]/2)*shape[1]), 
            int((label_range[0]+label_range[2]/2)*shape[1]), 
            int((label_range[1]-label_range[3]/2)*shape[0]), 
            int((label_range[1]+label_range[3]/2)*shape[0]) ]
        lbl[label_range[2]:label_range[3], label_range[0]:label_range[1]] = class_trns[label_class]#*40

    #save_image = Image.fromarray(img[700:900, 630:1300])
    #save_image.save(os.path.join(sys.argv[2], os.path.basename(image)))
    #save_image = Image.fromarray(lbl[700:900, 630:1300].astype(np.uint8))
    #save_image.save(os.path.join(sys.argv[2], 'label_'+os.path.basename(image)))
    '''
    fig, ax = plt.subplots()
    plt.imshow(img)

    f = open(image[:-3]+"txt", 'r')
    lines = f.readlines()
    for l, line in enumerate(lines):
        line = line[:-1].split(' ')

        rect = ( (float(line[1])-float(line[3])/2)*shape[0], (float(line[2])-float(line[4])/2)*shape[1], 
            float(line[3])*shape[0], float(line[4])*shape[1] )
        rectangle = patches.Rectangle(
            (rect[0],rect[1]), rect[2], rect[3], 
            linewidth=1, edgecolor=color_map[int(line[0])],
            facecolor='none', rotation_point='center')
        ax.add_patch(rectangle)

        #630 700 1300 900
    rectangle = patches.Rectangle(
            (630, 700), 670, 200, 
            linewidth=1, edgecolor='k',
            facecolor='none', rotation_point='center')
    ax.add_patch(rectangle)
    print(lines)
    print(shape)
    print((float(line[1])*shape[0], float(line[2])*shape[1], 
            float(line[3])*shape[0], float(line[4])*shape[1]))
    plt.show()
    plt.close()
    '''
