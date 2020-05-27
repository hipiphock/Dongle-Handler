from Device import *
from zb_cli_wrapper.zb_cli_dev import ZbCliDevice

# Work Routine for
class TaskRoutine:
    def __init__(self, device, connection_type, task_list):
        self.device = device
        self.connection_type = connection_type
        self.task_list = task_list
    
    def start_routine():
        # each task routine starts with connection
        cli_instance = ZbCliDevice('','','COM13')
        cli_instance.bdb.channel = [24]
        cli_instance.bdb.role = 'zr'
        cli_instance.bdb.start()
        # TODO: implement automated method that does not
        # require SmartThings' permission.

        # do the task_list
        

        # each task routine ends with disconnection
        