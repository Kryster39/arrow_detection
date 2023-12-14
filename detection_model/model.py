import tensorflow as tf
import tensorflow.keras as keras
from tensorflow.keras.layers import Input, Conv2D, Conv2DTranspose, Concatenate, MaxPooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import CategoricalCrossentropy

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
    feature = Conv2D(filters, kernel_size=1, padding='same', activation='relu')(conv2d_1)
    pooling = MaxPooling2D()(feature)
    return feature, pooling

def Block_ccp_u(_input, conv_feature, filters=8, kernel_size=5):
    conv2d_u1 = Conv2DTranspose(filters, kernel_size=kernel_size, strides=2, padding='same', activation='relu')(_input)
    cat = Concatenate()([conv2d_u1, conv_feature])
    conv2d_u2 = Conv2DTranspose(filters, kernel_size=kernel_size, padding='same', activation='relu')(cat)
    return conv2d_u2

def ArrowDetectionModel():
    _input = Input(shape=(192, 704, 1))
    f1, block_1 = Block_ccp(_input, filters=8, kernel_size=3)
    f2, block_2 = Block_ccp(block_1, filters=16, kernel_size=3)
    f3, block_3 = Block_ccp(block_2, filters=32, kernel_size=3)
    f4, block_4 = Block_ccp(block_3, filters=64, kernel_size=3)
    f5, block_5 = Block_ccp(block_4, filters=128, kernel_size=3)
    f6, block_6 = Block_ccp(block_5, filters=256, kernel_size=3)

    bottleneck_1 = Conv2D(512, kernel_size=1, padding='same', activation='relu')(block_6)
    bottleneck_2 = Conv2D(256, kernel_size=1, padding='same', activation='relu')(bottleneck_1)

    block_u1 = Block_ccp_u(bottleneck_2, f6, filters=256, kernel_size=3)
    block_u2 = Block_ccp_u(block_u1, f5, filters=128, kernel_size=3)
    block_u3 = Block_ccp_u(block_u2, f4, filters=64, kernel_size=3)
    block_u4 = Block_ccp_u(block_u3, f3, filters=32, kernel_size=3)
    block_u5 = Block_ccp_u(block_u4, f2, filters=16, kernel_size=3)
    block_u6 = Block_ccp_u(block_u5, f1, filters=8, kernel_size=3)

    output = Conv2D(filters=7, kernel_size=1, padding='same', activation='softmax')(block_u6)

    model = Model(inputs=_input, outputs=output)
    
    model.compile(
        optimizer=Adam(),
        loss=CategoricalCrossentropy())
    return model
