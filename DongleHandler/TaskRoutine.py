# main controller of Dongle Handler
from DongleHandler import *
from zb_cli_wrapper.zb_cli_dev import ZbCliDevice
import time
import serial

# Work Routine for
class TaskRoutine:
    def __init__(self, device, connection_type, task_list, iteration):
        self.device = device
        self.connection_type = connection_type
        self.task_list = task_list
        self.iteration = iteration
    
    # start_routine() consists of three steps:
    # 1. Starting connection with the device(the device joins the network).
    # 2. Sending/Receiving with the dongle and the device.
    # 3. Disbanding the device from Zigbee 
    def start_routine(self):
        
        # Before connecting the device with the dongle,
        # the dongle must join the hub's network.
        # TODO: implement automated port selector
        cli_instance = ZbCliDevice('', '', 'COM13')
        cli_instance.bdb.channel = [24]
        cli_instance.bdb.role = 'zr'
        cli_instance.bdb.start()
        print("The dongle has started commissioning.")
        print("Please search for the dongle via SmartThings App within 5 seconds.")
        time.sleep(5.0)

        # 1. Start connection with the device.
        # The connection of the device is ruled by SmartThings hub.
        # Therefore, the only job the dongle needs to do is 

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
        cli_instance.close_cli()
        port = serial.Serial("COM13", 115200)
        port.write(str.encode('reset'))
        port.writechar(' ')
        port.reset_input_buffer()
        port.reset_output_buffer()
        port.close()
        # Problem: 