from zb_cli_wrapper.zb_cli_dev import ZbCliDevice
from zb_cli_wrapper.src.utils.zigbee_classes.clusters.attribute import Attribute

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from DongleHandler import *

# This is basic test on Ultra Thin Wafer by Samsung
if __name__ == "__main__":

    # Device Initialization
    ultra_thin_wafer = Device("Ultra Thin Wafer", 0x8e89bed6, 0xFFFE88571D018E53, 8)

    # Making Task & TaskRoutine
    off_task    = Task(0x0006, 0x00, None)
    on_task     = Task(0x0006, 0x01, None)
    low_task    = Task(0x0008, 0x04, [(0x02, 0x20), (0x05, 0x21)])
    mid_task    = Task(0x0008, 0x04, [(0x50, 0x20), (0x05, 0x21)])
    high_task   = Task(0x0008, 0x04, [(0xFD, 0x20), (0x05, 0x21)])

    task_list = []
    task_list.append(off_task)
    task_list.append(on_task)
    task_list.append(low_task)
    task_list.append(mid_task)
    task_list.append(high_task)

    simple_routine = TaskRoutine(ultra_thin_wafer, ZIGBEE_CONNECTION, task_list, 3)

    # start routine
    simple_routine.start_routine()