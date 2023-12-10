import tensorflow as tf
import tensorflow.keras as keras
from tensorflow.keras.layers import Input, Conv2D, Conv2DTranspose, Concatenate, MaxPooling2D
from tensorflow.keras.models import Model

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
    conv2d_1 = Conv2D(filters, kernel_size=kernel_size, padding='same', activation='relu')(_input)
    feature = Conv2D(filters, kernel_size=kernel_size, padding='same', activation='relu')(conv2d_1)
    pooling = MaxPooling2D()(feature)
    return feature, pooling

def Block_ccp_u(_input, conv_feature, filters=8, kernel_size=5):
    conv2d_u1 = Conv2DTranspose(filters, kernel_size=kernel_size, strides=2, padding='same', activation='relu')(_input)
    cat = Concatenate()([conv2d_u1, conv_feature])
    conv2d_u2 = Conv2DTranspose(filters, kernel_size=kernel_size, padding='same', activation='relu')(cat)
    return conv2d_u2

def ArrowDetectionModel():
    _input = Input(shape=(680, 200, 3))
    f1, block_1 = Block_ccp(_input, filters=8, kernel_size=5)
    f2, block_2 = Block_ccp(block_1, filters=16, kernel_size=5)
    f3, block_3 = Block_ccp(block_2, filters=32, kernel_size=3)

    block_u1 = Block_ccp_u(block_3, f3, filters=32, kernel_size=3)
    block_u2 = Block_ccp_u(block_u1, f2, filters=16, kernel_size=5)
    block_u3 = Block_ccp_u(block_u2, f1, filters=8, kernel_size=5)

    output = Conv2D(filters=6, kernel_size=3, padding='same', activation='softmax')(block_u3)

    model = Model(inputs=_input, outputs=output)
    return model
