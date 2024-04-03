#import tensorflow as tf
#from model import ArrowDetectionModel
import tf2onnx

#model = ArrowDetectionModel()
#model.load_weights('model/best')

#model = tf.saved_model.load("/model/best")


onnx_model, _ = tf2onnx.convert.from_saved_model("/model/trypbfile", opset=15)

with open("converted_model.onnx", "wb") as f:
    f.write(onnx_model.SerializeToString())
