import cv2
import os
from yoloface.utils import *

#Need to create automated testing for model evaluation

class FaceDetector:
    def __init__(self):
        self.model = cv2.CascadeClassifier("tello_env/lib/python3.9/site-packages/cv2/data/haarcascade_frontalface_default.xml")
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
        
if __name__ == "__main__":
    DATA_DIR = "face_data"
    detector = FaceDetector()
    test_detector(DATA_DIR,detector.hcd_detect)

