from context import DongleHandler
from DongleHandler import *
import logging
import random

# This is basic test on Ultra Thin Wafer by Samsung Electronics.
if __name__ == "__main__":

    # for logging
    logging.basicConfig(level=logging.DEBUG)

    # simple, pre-defined routine for test
    # simple_routine = parse_json_task_routine('resource\\task_routine\\sample_routine.json')
    # TODO: change the directory's path
    # device = parse_json_device('resource\\device\\Ultra Thin Wafer.json')
    # sample_task_list = parse_task_list('resource\\sample_commands.json')
    # task_routine = TaskRoutine(device, 0, sample_task_list, 1)
    # task_routine.start_routine()

    # parse device file
    device = parse_json_device('resource\\device\\Ultra Thin Wafer.json')
    # generate task list
    generate_task_list_json("resource\\random_task_lists.json", 3)
    # parse generated task list
    task_list = parse_task_list("resource\\random_task_lists.json")
    # main routine
    task_routine = TaskRoutine(device, 0, task_list, 2)