# Task is an element for each task routine
# TODO: add readattr command
import random
from DongleHandler.Constants import *

# There are two types of tasks:
# 1. Task that just sends commnad
# 2. Task that reads attribute from the device
# 3. Task that writes attribute to the device
class Task:
    def __init__(self, cluster, command, attribute, payloads, duration):
        self.cluster    = cluster
        self.command    = command
        self.attribute  = attribute
        self.payloads   = payloads
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
            command = COLOR_CTRL_MV_TO_TEMPERATURE_CMD
            randval1 = random.randint(200, 370)
            # randval2 = random.randint(0x0001, 0xfeff)
            randval2 = 0
            payloads = [(randval1, TYPES.UINT16), (randval2, TYPES.UINT16)]
            # duration = randval2*0.1
            duration = 0.5
        return cls(cluster, command, payloads, duration)

    @classmethod
    def generate_irregular_random_task(cls, cluster, command):
        if cluster == ON_OFF_CLUSTER:
            command = random.randint(0x00, 0x01)
            payloads = None
            duration = 0.5
        elif cluster == LVL_CTRL_CLUSTER:
            command = LVL_CTRL_MV_TO_LVL_ONOFF_CMD
            randval1 = random.randint(0x00, 0xfe) + 0xff
            # randval2 = random.randint(0x0000, 0xffff) + 0xffff
            randval2 = 0
            payloads = [(randval1, TYPES.UINT8), (randval2, TYPES.UINT16)]
            # duration = randval2*0.1
            duration = 0.5
        elif cluster == COLOR_CTRL_CLUSTER:
            command = COLOR_CTRL_MV_TO_TEMPERATURE_CMD
            randval1 = random.randint(0x0000, 0xfeff) + 0xff00
            # randval2 = random.randint(0x0001, 0xffff) + 0xffff
            randval2 = 0
            payloads = [(randval1, TYPES.UINT16), (randval2, TYPES.UINT16)]
            # duration = randval2*0.1
            duration = 0.5
        return cls(cluster, command, payloads, duration)