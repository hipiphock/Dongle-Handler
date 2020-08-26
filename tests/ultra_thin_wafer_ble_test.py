from context import DongleHandler
from DongleHandler import *
import logging

# This is basic test on Ultra Thin Wafer by Samsung Electronics.
if __name__ == "__main__":

    # for logging
    logging.basicConfig(level=logging.DEBUG)

    # Device Initialization
    ultra_thin_wafer = Device("Ultra Thin Wafer", 0x8e89bed6, 0xFFFE88571D018E53, 8)

    # move commands 
    task_list = []
    task_list.append(1)
    task_list.append(1)
    task_list.append(1)

    simple_routine = TaskRoutine(ultra_thin_wafer, BLE_CONNECTION, task_list, 1)
    simple_routine.start_routine()