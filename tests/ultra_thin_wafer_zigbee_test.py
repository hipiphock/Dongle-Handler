from context import DongleHandler
from DongleHandler import *
import logging

# This is basic test on Ultra Thin Wafer by Samsung Electronics.
if __name__ == "__main__":

    # for logging
    logging.basicConfig(level=logging.DEBUG)

    # Device Initialization
    ultra_thin_wafer = Device("Ultra Thin Wafer", 0x8e89bed6, 0xFFFE88571D018E53, 8)

    # Making Task & TaskRoutine
    # off_task    = Task(ON_OFF_CLUSTER, ON_OFF_OFF_CMD, None, 0.5)
    on_task     = Task(ON_OFF_CLUSTER, ON_OFF_ON_CMD, None, 0.5)

    low_task    = Task(LVL_CTRL_CLUSTER, LVL_CTRL_MV_TO_LVL_ONOFF_CMD, [(0x02, TYPES.UINT8), (6, TYPES.UINT16)], 0.61)
    # mid_task    = Task(LVL_CTRL_CLUSTER, LVL_CTRL_MV_TO_LVL_ONOFF_CMD, [(0x50, TYPES.UINT8), (6, TYPES.UINT16)], 0.61)
    high_task   = Task(LVL_CTRL_CLUSTER, LVL_CTRL_MV_TO_LVL_ONOFF_CMD, [(0xFD, TYPES.UINT8), (6, TYPES.UINT16)], 0.61)

    # sw_light_task = Task(COLOR_CTRL_CLUSTER, COLOR_CTRL_MV_TO_TEMPERATURE_CMD, [(370, TYPES.UINT16), (5, TYPES.UINT16)], 0.5)
    # dl_light_task = Task(COLOR_CTRL_CLUSTER, COLOR_CTRL_MV_TO_TEMPERATURE_CMD, [(200, TYPES.UINT16), (5, TYPES.UINT16)], 0.5)

    task_list = []
    # task_list.append(off_task)
    task_list.append(on_task)
    task_list.append(high_task)
    # task_list.append(mid_task)
    task_list.append(low_task)
    task_list.append(high_task)
    # task_list.append(mid_task)
    task_list.append(low_task)
    task_list.append(high_task)
    # task_list.append(mid_task)
    task_list.append(low_task)
    # task_list.append(sw_light_task)
    # task_list.append(dl_light_task)
    # task_list.append(sw_light_task)
    # task_list.append(dl_light_task)

    simple_routine = TaskRoutine(ultra_thin_wafer, ZIGBEE_CONNECTION, task_list, 2)

    # start routine
    simple_routine.start_routine()