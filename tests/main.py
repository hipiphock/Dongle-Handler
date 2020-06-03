from context import DongleHandler
from DongleHandler import *
import logging

# This is basic test on Ultra Thin Wafer by Samsung Electronics.
if __name__ == "__main__":

    # for logging
    logging.basicConfig(level=logging.DEBUG)

    # Device Initialization
    ultra_thin_wafer = parse_json_device('DongleHandler\\..\\resource\\device\\Ultra Thin Wafer.json')

    # Making Task & TaskRoutine
    off_task    = parse_json_command('DongleHandler\\..\\resource\\command\\off.json')
    on_task     = parse_json_command('DongleHandler\\..\\resource\\command\\on.json')

    low_task    = parse_json_command('DongleHandler\\..\\resource\\command\\level_10.json')
    mid_task    = parse_json_command('DongleHandler\\..\\resource\\command\\level_50.json')
    high_task   = parse_json_command('DongleHandler\\..\\resource\\command\\level_100.json')

    simple_routine = parse_json_task_routine('DongleHandler\\..\\resource\\command\\level_100.json')

    # start routine
    simple_routine.start_routine()