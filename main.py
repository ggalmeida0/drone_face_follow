from face_detection import FaceDetector
import cv2
from djitellopy import Tello
from states import DroneState
from pid import follow_face
from sys import argv
import traceback
from yoloface.utils import IMG_HEIGHT, IMG_WIDTH


#Observations: 
# Maybe try to run the video capturing in a another thread for better speedup

def main():
        drone = Tello()
        drone.connect()
        drone.streamon()
        detector = FaceDetector()
        if len(argv) == 2 and argv[1] == "-v":
                just_video(drone,detector)
        else:
                flight(drone,detector)
        drone.streamoff()
        
def just_video(drone,detector):
        while True:
                frame = drone.get_frame_read().frame
                frame = cv2.resize(frame,(IMG_WIDTH,IMG_HEIGHT))
                faces = detector.yolo_detect(frame)
                cv2.imshow("Video",frame)
                if len(faces) > 0:
                        print(faces[0][2] * faces[0][3])
                if cv2.waitKey(1) == 32:
                        break


def flight(drone,detector):
        drone.get_frame_read() #Start getting frames before takeoff
        drone.takeoff()
        state = DroneState.FIND_FACE
        try:
                while True:
                        frame = drone.get_frame_read().frame
                        frame = cv2.resize(frame,(IMG_WIDTH,IMG_HEIGHT))
                        faces = detector.yolo_detect(frame)
                        if state == DroneState.FIND_FACE:
                                if len(faces) > 0: state = DroneState.FOLLOW
                                else: drone.rotate_clockwise(30)
                        elif state == DroneState.FOLLOW:
                                if faces:
                                        owner_box = faces[0] # Here we can recognize the owner in the future
                                        follow_face(drone,owner_box)
                                else:
                                        state = DroneState.FIND_FACE
        except Exception as e:
                print(f"Threw Exception: {e}")
                print("Full Traceback:\n",traceback.print_exc())
                drone.land()
if __name__ == "__main__":
    main()