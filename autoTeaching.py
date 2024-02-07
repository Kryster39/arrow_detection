from detection_model.model import ArrowDetectionModel
from GUI.GUI import autoTeachingBoard

model = ArrowDetectionModel()
model.load_weights("detection_model/model/best")

t = autoTeachingBoard(model)

#pyinstaller '_pywrap_tensorflow_internal'