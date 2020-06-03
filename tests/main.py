from context import DongleHandler
from DongleHandler import *
import logging
import random

# This is basic test on Ultra Thin Wafer by Samsung Electronics.
if __name__ == "__main__":

    # for logging
    logging.basicConfig(level=logging.DEBUG)

    # simple, pre-defined routine for test
    # simple_routine = parse_json_task_routine('DongleHandler\\..\\resource\\task_routine\\sample_routine.json')
    # simple_routine.start_routine()

    # generate regular random samples
    print("Random Regular")
    regular_random_task_list = []
    for i in range(10):
        task = Task.generate_regular_random_task(ON_OFF_CLUSTER, ON_OFF_OFF_CMD)
        regular_random_task_list.append(task)
    for i in range(10):
        task = Task.generate_regular_random_task(LVL_CTRL_CLUSTER, LVL_CTRL_MV_TO_LVL_ONOFF_CMD)
        regular_random_task_list.append(task)
    for i in range(10):
        task = Task.generate_regular_random_task(COLOR_CTRL_CLUSTER, COLOR_CTRL_MV_TO_TEMPERATURE_CMD)
        regular_random_task_list.append(task)
    device = parse_json_device('DongleHandler\\..\\resource\\device\\Ultra Thin Wafer.json')
    regular_task_routine = TaskRoutine(device, 0, regular_random_task_list, 1)
    regular_task_routine.start_routine()

    # generate irregular random samples
    print("Random Irregular")
    irregular_random_task_list = []
    for i in range(10):
        task = Task.generate_irregular_random_task(ON_OFF_CLUSTER, ON_OFF_OFF_CMD)
        irregular_random_task_list.append(task)
    for i in range(10):
        task = Task.generate_irregular_random_task(LVL_CTRL_CLUSTER, LVL_CTRL_MV_TO_LVL_ONOFF_CMD)
        irregular_random_task_list.append(task)
    for i in range(10):
        task = Task.generate_irregular_random_task(COLOR_CTRL_CLUSTER, COLOR_CTRL_MV_TO_TEMPERATURE_CMD)
        irregular_random_task_list.append(task)
    irregular_task_routine = TaskRoutine(device, 0, irregular_random_task_list, 1)
    irregular_task_routine.start_routine()