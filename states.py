from enum import Enum, auto

class DroneState(Enum):
    FIND_FACE = auto()
    FOLLOW = auto()
