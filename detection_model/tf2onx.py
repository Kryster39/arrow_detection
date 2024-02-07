#import tensorflow as tf
#from model import ArrowDetectionModel
import tf2onnx

#model = ArrowDetectionModel()
#model.load_weights('model/best')

#model = tf.saved_model.load("/model/best")


onnx_model, _ = tf2onnx.convert.from_saved_model("/model/trypbfile", opset=15)

with open("converted_model.onnx", "wb") as f:
    f.write(onnx_model.SerializeToString())

#tf.saved_model.save(model, 'trypbfile')
'''
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    sess.run(tf.local_variables_initializer())

    frozen_graph = tf.graph_util.convert_variables_to_constants(
        sess, tf.get_default_graph().as_graph_def(), [''])

    tf.io.write_graph(frozen_graph, "../pb/", "frozen_model.pb", as_text=False)
'''