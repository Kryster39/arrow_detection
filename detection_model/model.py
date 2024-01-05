import tensorflow as tf
import tensorflow.keras as keras
from tensorflow.keras.layers import Input, Conv2D, Conv2DTranspose, Concatenate, MaxPooling2D, Dropout, LeakyReLU, Softmax, BatchNormalization, Reshape
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import CategoricalCrossentropy, SparseCategoricalCrossentropy

import os
import sys
import shutil

os.environ['TF_XLA_FLAGS'] = '--tf_xla_enable_xla_devices'
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
if tf.test.gpu_device_name():
    print('GPU found')
else:
    print("No GPU found")

def Block_ccp(_input, filters=8, kernel_size=5):
    conv2d_1 = Conv2D(filters, kernel_size=kernel_size, padding='same')(_input)
    lrelu_1 = LeakyReLU()(conv2d_1)
    BaN_1 = BatchNormalization()(lrelu_1)

    conv2d_2 = Conv2D(filters, kernel_size=1, padding='same')(BaN_1) #relu
    lrelu_2 = LeakyReLU()(conv2d_2)
    BaN_2 = BatchNormalization()(lrelu_2)
    
    feature = Dropout(0.2)(BaN_2)
    pooling = MaxPooling2D()(BaN_2) #feature
    return feature, pooling

def Block_ccp_u(_input, conv_feature, filters=8, kernel_size=5):
    conv2d_u1 = Conv2DTranspose(filters, kernel_size=kernel_size, strides=2, padding='same')(_input)
    lrelu_1 = LeakyReLU()(conv2d_u1)
    BaN_1 = BatchNormalization()(lrelu_1)
    cat = Concatenate()([BaN_1, conv_feature])

    conv2d_u2 = Conv2DTranspose(filters, kernel_size=1, padding='same')(cat) #kernel_size
    lrelu_2 = LeakyReLU()(conv2d_u2)
    BaN_2 = BatchNormalization()(lrelu_2)
    return BaN_2

def ArrowDetectionModel():
    _input = Input(shape=(192, 704, 1))
    f1, block_1 = Block_ccp(_input, filters=8, kernel_size=5)
    f2, block_2 = Block_ccp(block_1, filters=16, kernel_size=5)
    f3, block_3 = Block_ccp(block_2, filters=32, kernel_size=3)
    f4, block_4 = Block_ccp(block_3, filters=64, kernel_size=3)

    bottleneck_1 = Conv2D(128, kernel_size=1, padding='same')(block_4)
    lrelu_1 = LeakyReLU()(bottleneck_1)
    bottleneck_2 = Conv2D(64, kernel_size=1, padding='same')(lrelu_1)
    lrelu_2 = LeakyReLU()(bottleneck_2)

    block_u1 = Block_ccp_u(lrelu_2, f4, filters=64, kernel_size=3)
    block_u2 = Block_ccp_u(block_u1, f3, filters=32, kernel_size=3)
    block_u3 = Block_ccp_u(block_u2, f2, filters=16, kernel_size=5)
    block_u4 = Block_ccp_u(block_u3, f1, filters=8, kernel_size=5)

    smx = Conv2D(filters=7, kernel_size=1, padding='same', activation='softmax')(block_u4)
    #smx = Softmax()(sig)
    output = Reshape((192*704, 7))(smx)

    model = Model(inputs=_input, outputs=output)
    
    model.compile(
        optimizer=Adam(learning_rate=0.005), #default 0.001
        loss=SparseCategoricalCrossentropy())
    return model
