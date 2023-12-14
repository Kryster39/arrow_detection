from model import ArrowDetectionModel
from dataloader import DataLoader

import os
import sys

if len(sys.argv) <= 4:
    print("[train.py] example: python train.py _dataset_path _batch_size _epoches _save_model _load_model")

model = ArrowDetectionModel()
if len(sys.argv) > 5:
    model.load_weights(sys.argv[5])

DL = DataLoader(dataset_path=sys.argv[1])

epoches = int(sys.argv[3])
for i in range(epoches):
    print("Epoch {}/{}".format(i+1, epoches))
    history = model.fit(DL.get_train_data(batch_size=int(sys.argv[2])))
    #print(history.history['loss'])

if len(sys.argv) > 4:
    model.save_weights(sys.argv[4])

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