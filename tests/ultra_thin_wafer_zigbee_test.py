from DongleHandler import *
from zb_cli_wrapper.zb_cli_dev import ZbCliDevice
from zb_cli_wrapper.src.utils.zigbee_classes.clusters.attribute import Attribute

# This is basic test on Ultra Thin Wafer by Samsung
if __name__ == "__main__":

    # Device Initialization
    ultra_thin_wafer = Device("Ultra Thin Wafer", 0x8e89bed6, 0xFFFE88571D018E53, 8)

    # Making Task & TaskRoutine
    low_task    = Task(0x0008, 0x04, [(0x02, 0x20), (0x00, 0x21)])
    mid_task    = Task(0x0008, 0x04, [(0x50, 0x20), (0x00, 0x21)])
    high_task   = Task(0x0008, 0x04, [(0xFD, 0x20), (0x00, 0x21)])

    task_list = []
    task_list.append(low_task)
    task_list.append(mid_task)
    task_list.append(high_task)

    simple_routine = TaskRoutine(ultra_thin_wafer, ZIGBEE_CONNECTION, task_list, 3)

    # start routine
    simple_routine.start_routine()