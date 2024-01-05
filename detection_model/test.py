from model import ArrowDetectionModel
from dataloader import DataLoader

import os
import sys
import numpy as np
import cv2

if len(sys.argv) <= 3:
    print("[test.py] example: python test.py _dataset_path _output_path _load_model _number_of_tests")

model = ArrowDetectionModel()
if len(sys.argv) > 3:
    model.load_weights(sys.argv[3])

DL = DataLoader(dataset_path=sys.argv[1])
images, labels = [], []
if len(sys.argv) > 4:
    images, labels = DL.get_test_data(num=int(sys.argv[4])) 
else:
    images, labels = DL.get_test_data()

predicts = model.predict(images)

for i, (predict, label) in enumerate(zip(predicts, labels)):
    pred = np.reshape(predict, (192, 704, 7))
    pred = np.argmax(pred, axis=-1)
    pred = pred.astype(np.uint8)*40

    #lbl = np.argmax(label, axis=-1)
    lbl = label.astype(np.uint8)*40

    file_name = DL.test_file[i]
    cv2.imwrite(os.path.join(sys.argv[2], "pred_"+os.path.basename(file_name)[6:]),
                pred)
    cv2.imwrite(os.path.join(sys.argv[2], os.path.basename(file_name)),
                    lbl)