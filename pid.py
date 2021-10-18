import numpy as np
from yoloface.utils import IMG_WIDTH
from simple_pid import PID
import csv
from datetime import datetime
from time import time

TARGET_AREA = 30000
ERROR_THRESH = 50
TARGET_X = IMG_WIDTH // 2

class PidController:
    def __init__(self,enable_data_collection=False):
        if enable_data_collection:
            self.collect_data = True
            filename = f"pid_data/{datetime.now().isoformat()}.csv"
            self.fp = open(filename,"w")
            self.csv_writer = csv.writer(self.fp)
            self.start_time = time()
            self.csv_writer.writerow(["Time","Centering Input","Distance Input","Centering Output","Distance Output"])
        else:
            self.collect_data = False

    def _write(self,errors,outputs):
        timestamp = time() - self.start_time
        self.csv_writer.writerow([timestamp] + outputs + errors)
    
    def stop(self):
        if self.collect_data: self.fp.close()

    def follow_face(self,drone,box):
        centering_pid, distance_pid = PID(.1,.4,0), PID(-0.0004506432452641935,0.454142558841697,0)
        x, _, width, height = box
        current_area = width * height
        centering_error, distance_error = TARGET_X - x , current_area - TARGET_AREA
        centering_speed, distancing_speed = centering_pid(centering_error), distance_pid(distance_error)
        centering_speed, distancing_speed = int(np.clip(centering_speed,-100,100)), int(np.clip(distancing_speed,-100,100))
        if self.collect_data: self._write([centering_error,distance_error],[centering_speed,distancing_speed])
        drone.send_rc_control(0,distancing_speed,0,centering_speed)

