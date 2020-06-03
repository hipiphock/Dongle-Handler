# Task is an element for each task routine
import random
from DongleHandler.Constants import *

class Task:
    def __init__(self, cluster, command, payloads, duration):
        self.cluster = cluster
        self.command = command
        self.payloads = payloads
        self.duration = duration

    @classmethod
    def generate_regular_random_task(cls, cluster, command, duration):
        if cluster == ON_OFF_CLUSTER:
            command = random.randint(0x00, 0x01)
            payloads = None
            randval2 = 0.5
        elif cluster == LVL_CTRL_CLUSTER:
            command = LVL_CTRL_MV_TO_LVL_ONOFF_CMD
            randval1 = random.randint(0x00, 0xfe)
            # randval2 = random.randint(0x0000, 0xffff)
            randval2 = 0
            payloads = [(randval1, TYPES.UINT8), (randval2, TYPES.UINT16)]
        elif cluster == COLOR_CTRL_CLUSTER:
            command = COLOR_CTRL_MV_TO_TEMPERATURE_CMD
            randval1 = random.randint(0x00, 0xfe)
            # randval2 = random.randint(0x0001, 0xfeff)
            randval2 = 0
            payloads = [(randval1, TYPES.UINT16), (randval2, TYPES.UINT16)]
        return cls(cluster, command, payloads, duration)

    @classmethod
    def generate_irregular_random_task(cls, cluster, command, duration):
        if cluster == ON_OFF_CLUSTER:
            command = random.randint(0x00, 0x01)
            payloads = None
        elif cluster == LVL_CTRL_CLUSTER:
            command = LVL_CTRL_MV_TO_LVL_ONOFF_CMD
            randval1 = random.randint(0x00, 0xfe) + 0xff
            # randval2 = random.randint(0x0000, 0xffff) + 0xffff
            randval2 = 0
            payloads = [(randval1, TYPES.UINT8), (randval2, TYPES.UINT16)]
        elif cluster == COLOR_CTRL_CLUSTER:
            command = COLOR_CTRL_MV_TO_TEMPERATURE_CMD
            randval1 = random.randint(0x0000, 0xfeff) + 0xff00
            # randval2 = random.randint(0x0001, 0xffff) + 0xffff
            randval2 = 0
            payloads = [(randval1, TYPES.UINT16), (randval2, TYPES.UINT16)]
        return cls(cluster, command, payloads, duration)