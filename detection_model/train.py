from model import ArrowDetectionModel
from dataloader import DataLoader

import os
import sys
import cv2
import numpy as np

if len(sys.argv) <= 4:
    print("[train.py] example: python train.py _dataset_path _batch_size _epoches _save_model _load_model")

model = ArrowDetectionModel()
if len(sys.argv) > 5:
    model.load_weights(sys.argv[5])

DL = DataLoader(dataset_path=sys.argv[1])
class_weight={0:0.2, 1:1.7, 2:0.7, 3:0.7, 4:1.7, 5:1., 6:1.}

print(model.summary())
epoches = int(sys.argv[3])
for i in range(epoches):
    print("Epoch {}/{}".format(i+1, epoches))
    history = model.fit(DL.get_train_data(batch_size=int(sys.argv[2])))#, class_weight=class_weight)
    #print(history.history['loss'])

if len(sys.argv) > 4:
    model.save_weights(sys.argv[4])
