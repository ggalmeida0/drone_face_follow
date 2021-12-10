from face_detection import FaceDetector
import cv2
from djitellopy import Tello
from states import DroneState
from pid import PidController
from sys import argv
import traceback
from yoloface.utils import IMG_HEIGHT, IMG_WIDTH

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
        print("Current Battery: ",drone.get_battery(),"%")
        drone.get_frame_read() #Start getting frames before takeoff
        drone.takeoff()
        state = DroneState.LEVEL_HEIGHT
        controller = PidController(enable_data_collection=True)
        TARGET_HEIGHT = 130
        try:
                while True:
                        frame = drone.get_frame_read().frame
                        frame = cv2.resize(frame,(IMG_WIDTH,IMG_HEIGHT))
                        faces = detector.yolo_detect(frame)
                        if state == DroneState.LEVEL_HEIGHT:
                                current_height = drone.get_height()
                                print("Current Height: ",current_height)
                                if current_height > TARGET_HEIGHT: drone.send_rc_control(0,0,-10,0)
                                elif current_height < TARGET_HEIGHT: drone.send_rc_control(0,0,10,0)
                                else: state = DroneState.FIND_FACE

                        if state == DroneState.FIND_FACE:
                                if len(faces) > 0: state = DroneState.FOLLOW
                                else: drone.rotate_clockwise(30)
                        elif state == DroneState.FOLLOW:
                                if faces:
                                        owner_box = faces[0] # Here we can recognize the owner in the future
                                        controller.follow_face(drone,owner_box)
                                else:
                                        state = DroneState.FIND_FACE
                        if drone.get_height() != TARGET_HEIGHT: state = DroneState.LEVEL_HEIGHT
        except Exception as e:
                print(f"Threw Exception: {e}")
                print("Full Traceback:\n",traceback.print_exc())
                drone.land()
                controller.stop()
if __name__ == "__main__":
    main()