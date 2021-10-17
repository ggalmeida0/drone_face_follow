import numpy as np
from yoloface.utils import IMG_WIDTH
from simple_pid import PID

TARGET_AREA = 35000
ERROR_THRESH = 50
TARGET_X = IMG_WIDTH // 2

def follow_face(drone,box):
    centering_pid, distance_pid = PID(.1,.4,0), PID(.001,.4,0)
    x, _, width, height = box
    current_area = width * height
    centering_error, distance_error = TARGET_X - x , current_area - TARGET_AREA
    print("Current Distance Error: ",distance_error)
    print("Current Centering Error: ",centering_error)
    centering_speed, distancing_speed = centering_pid(centering_error), distance_pid(distance_error)
    centering_speed, distancing_speed = int(np.clip(centering_speed,-100,100)), int(np.clip(distancing_speed,-100,100))
    print("current area: ",current_area)
    drone.send_rc_control(0,distancing_speed,0,centering_speed)