import cv2
from yoloface.utils import *

class FaceDetector:
    def yolo_detect(self,img,cfg="./yoloface/cfg/yolov3-face.cfg",weights="yoloface/model-weights/yolov3-wider_16000.weights"):
        net = cv2.dnn.readNetFromDarknet(cfg, weights)
        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
        blob = cv2.dnn.blobFromImage(img, 1 / 255, (IMG_WIDTH, IMG_HEIGHT),
                                     [0, 0, 0], 1, crop=False)
        net.setInput(blob)
        outs = net.forward(get_outputs_names(net))
        faces = post_process(img, outs, CONF_THRESHOLD, NMS_THRESHOLD)
        return faces