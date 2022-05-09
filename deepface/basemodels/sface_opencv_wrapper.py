import os

import cv2 as cv
import gdown

from deepface.commons import functions

_url = "https://github.com/opencv/opencv_zoo/raw/master/models/face_recognition_sface/face_recognition_sface_2021dec.onnx"


class _Layer:
    input_shape = (None, 112, 122, 3)


class SFace:
    def __init__(self, model_path, backend_id=0, target_id=0):
        self._modelPath = model_path
        self._backendId = backend_id
        self._targetId = target_id
        self._model = cv.FaceRecognizerSF.create(
            model=self._modelPath,
            config="",
            backend_id=self._backendId,
            target_id=self._targetId)

        self.layers = [_Layer()]

    def _preprocess(self, image, bbox):
        if bbox is None:
            return image
        else:
            return self._model.alignCrop(image, bbox)

    def predict(self, image, bbox=None, **kwargs):
        # Preprocess
        # print(image.max())
        # input_blob = self._preprocess(image, bbox)

        # Forward
        features = self._model.feature(image[0])
        return features


def load_model(*args, **kwargs):
    home = functions.get_deepface_home()

    file_name = home + '/.deepface/weights/face_recognition_sface_2021dec.onnx'
    if not os.path.isfile(file_name):
        print("sface weights will be downloaded...")

        output = file_name
        gdown.download(_url, output, quiet=False)

    model = SFace(file_name, 0, 0)
    return model
