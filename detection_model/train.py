from model import ArrowDetectionModel
from dataloader import DataLoader

import os
import sys
import cv2

if len(sys.argv) <= 4:
    print("[train.py] example: python train.py _dataset_path _batch_size _epoches _save_model _load_model")

model = ArrowDetectionModel()
if len(sys.argv) > 5:
    model.load_weights(sys.argv[5])

DL = DataLoader(dataset_path=sys.argv[1])

g = DL.get_train_data()

epoches = int(sys.argv[3])
for i in range(epoches):
    print("Epoch {}/{}".format(i+1, epoches))
    history = model.fit(DL.get_train_data(batch_size=int(sys.argv[2])))
    #print(history.history['loss'])

if len(sys.argv) > 4:
    model.save_weights(sys.argv[4])
