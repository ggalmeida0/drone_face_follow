from face_detection import FaceDetector
import cv2
from time import sleep
from djitellopy import Tello


#Observations: 
# Maybe try to run the video capturing in a another thread for better speedup

def main():
        # drone = Tello()
        # drone.connect()
        # drone.streamon()
        # detector = FaceDetector()
        # drone.get_frame_read()
        # drone.takeoff()
        # try:
        #         while True:
        #                 frame = drone.get_frame_read().frame
        #                 frame = cv2.resize(frame,(360,240))
        #                 faces = detector.detectFaces(frame)
        #                 drone.rotate_clockwise(30)
        #                 if len(faces) > 0:
        #                         cv2.rectangle(frame,faces[0],25)
        #                         cv2.imshow("Video Streaming",frame)
        #                         drone.land()
        #                         drone.streamoff()
        #                         break
        # except:
        #         drone.land()
        while True:
                cam = cv2.VideoCapture(0)
                readFrame, frame = cam.read()
                detector = FaceDetector()
                if readFrame:
                        faces = detector.yolo_detect(frame)
                        cv2.imshow("Video Streaming",frame)
                
                if cv2.waitKey(1) == 27:
                        break

if __name__ == "__main__":
    main()