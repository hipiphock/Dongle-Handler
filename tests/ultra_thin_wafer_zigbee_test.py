import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from DongleHandler import *
import logging

# This is basic test on Ultra Thin Wafer by Samsung Electronics.
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)    # for logging

    # Device Initialization
    ultra_thin_wafer = Device("Ultra Thin Wafer", 0x8e89bed6, 0xFFFE88571D018E53, 8)

    # Making Task & TaskRoutine
    off_task    = Task(ON_OFF_CLUSTER, ON_OFF_OFF_CMD, None)
    on_task     = Task(ON_OFF_CLUSTER, ON_OFF_ON_CMD, None)

    low_task    = Task(LVL_CTRL_CLUSTER, LVL_CTRL_MV_TO_LVL_ONOFF_CMD, [(0x02, TYPES.UINT8), (0x05, TYPES.UINT16)])
    mid_task    = Task(LVL_CTRL_CLUSTER, LVL_CTRL_MV_TO_LVL_ONOFF_CMD, [(0x50, TYPES.UINT8), (0x05, TYPES.UINT16)])
    high_task   = Task(LVL_CTRL_CLUSTER, LVL_CTRL_MV_TO_LVL_ONOFF_CMD, [(0xFD, TYPES.UINT8), (0x05, TYPES.UINT16)])

    task_list = []
    task_list.append(off_task)
    task_list.append(on_task)
    task_list.append(high_task)
    task_list.append(mid_task)
    task_list.append(low_task)

    simple_routine = TaskRoutine(ultra_thin_wafer, ZIGBEE_CONNECTION, task_list, 3)

    # start routine
    simple_routine.start_routine()