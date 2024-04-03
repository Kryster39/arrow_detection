from GUI.GUI import autoTeachingBoard
import onnxruntime

#pyinstaller: pyinstaller -w -p C:\Users\user\anaconda3\envs\Pyinstaller -F .\autoTeaching.py

session = onnxruntime.InferenceSession("detection_model/best.onnx")
#model = ArrowDetectionModel()
#model.load_weights("detection_model/model/best")

t = autoTeachingBoard(session)