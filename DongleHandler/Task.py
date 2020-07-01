# Task is an element for each task routine
# TODO: add readattr command
import random
from DongleHandler.Constants import *

# There are two types of tasks:
# 1. Task that just sends commnad
# 2. Task that reads attribute from the device
# 3. Task that writes attribute to the device
class Task:
    def __init__(self, cluster, command, payloads, attr_id, attr_type, duration):
        self.cluster    = cluster
        self.command    = command
        self.payloads   = payloads
        self.attr_id    = attr_id
        self.attr_type  = attr_type
        self.duration   = duration

    # OnOffTransitionTime is very important
    @classmethod
    def generate_regular_random_task(cls, cluster, command):
        if cluster == ON_OFF_CLUSTER:
            command = random.randint(0x00, 0x01)
            payloads = None
            duration = 0.5
        elif cluster == LVL_CTRL_CLUSTER:
            command = LVL_CTRL_MV_TO_LVL_ONOFF_CMD
            randval1 = random.randint(0x00, 0xfe)
            # randval2 = random.randint(0x0000, 0xffff)
            randval2 = random.randint(0x0000, 0x000A)
            # randval2 = 0
            payloads = [(randval1, TYPES.UINT8), (randval2, TYPES.UINT16)]
            duration = randval2*0.1 + 0.01
            # duration = 0.5
        elif cluster == COLOR_CTRL_CLUSTER:
            command = COLOR_CTRL_MV_TO_COLOR_TEMP_CMD
            randval1 = random.randint(200, 370)
            # randval2 = random.randint(0x0001, 0xfeff)
            randval2 = 0
            payloads = [(randval1, TYPES.UINT16), (randval2, TYPES.UINT16)]
            # duration = randval2*0.1
            duration = 0.5
        return cls(cluster, command, payloads, duration)
    
    def task_to_string(self):
        ret_str =   '{\"cluster\": \"'  + cluster\
            +   '", \"command\": \"'    + command\
            +   '", \"payloads\": \"'   + payloads\
            +   '", \"attr_id\": \"'    + attr_id\
            +   '", \"attr_type\": \"'  + attr_type\
            +   '", \"duration\": \"'   + duration\
            +   '}'
        return ret_str

def duration_control(payload):
    duration = max(0.1*payload[1][1] + 0.01, 0.51)
    return duration