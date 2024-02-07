import onnxruntime
import numpy as np
import cv2

onnx_model_path = "best.onnx"
session = onnxruntime.InferenceSession(onnx_model_path)

image = cv2.imread(r'D:\github\arrow_detection\detection_model\dataset\test\78.png')
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

input_data = np.array(gray_image, np.float32)[np.newaxis,:,:,np.newaxis]

output = session.run(None, {"input_1": input_data})[0]

print("output shape: ", output.shape)

output = np.reshape(output, (192, 704, 7))
output = np.array(np.argmax(output, axis=-1)*40,np.uint8)
cv2.imshow('Grayscale Image', output)
cv2.waitKey(0)
cv2.destroyAllWindows()

