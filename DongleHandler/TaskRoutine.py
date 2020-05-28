# main controller of Dongle Handler
from DongleHandler import *
from zb_cli_wrapper.zb_cli_dev import ZbCliDevice
import time

# Work Routine for
class TaskRoutine:
    def __init__(self, device, connection_type, task_list, iteration):
        self.device = device
        self.connection_type = connection_type
        self.task_list = task_list
        self.iteration = iteration
    
    def start_routine(self):
        # each task routine starts with connection
        # TODO: implement automated port selector
        cli_instance = ZbCliDevice('', '', 'COM13')
        # cli_instance.bdb.channel = [24]
        # cli_instance.bdb.role = 'zr'
        # cli_instance.bdb.start()
        # TODO: implement automated method that does not
        # require SmartThings' permission.

        # do the task_list
        for task in self.task_list:
            if task.payloads == None:
                cli_instance.zcl.generic(
                    eui64=self.device.addr,
                    ep=self.device.ep,
                    profile=DEFAULT_ZIGBEE_PROFILE_ID,
                    cluster=task.cluster,
                    cmd_id=task.command)
            else:
                cli_instance.zcl.generic(
                    eui64=self.device.addr,
                    ep=self.device.ep,
                    profile=DEFAULT_ZIGBEE_PROFILE_ID,
                    cluster=task.cluster,
                    cmd_id=task.command,
                    payload=task.payloads)
            time.sleep(0.5)

        # each task routine ends with disconnection
        