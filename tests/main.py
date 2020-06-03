from context import DongleHandler
from DongleHandler import *
import logging

# This is basic test on Ultra Thin Wafer by Samsung Electronics.
if __name__ == "__main__":

    # for logging
    logging.basicConfig(level=logging.DEBUG)

    simple_routine = parse_json_task_routine('DongleHandler\\..\\resource\\task_routine\\sample_routine.json')

    # start routine
    simple_routine.start_routine()