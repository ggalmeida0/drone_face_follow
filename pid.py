import numpy as np
from yoloface.utils import IMG_WIDTH
from simple_pid import PID

TARGET_AREA = (30000,40000)

def follow_face(drone,box):
    pid = PID(.4,0,.1)
    x, _, width, height = box
    current_area = width * height
    target_x = IMG_WIDTH // 2
    error = target_x - x
    if current_area < TARGET_AREA[0]: fb = 20
    elif current_area > TARGET_AREA[1]: fb = -20
    else: fb = 0
    speed = pid(error)
    speed = int(np.clip(speed,-100,100))
    print("current area: ",current_area)
    drone.send_rc_control(0,fb,0,speed)
    
    return error