# main controller of Dongle Handler
import time
import json
import logging

from DongleHandler import *
from zb_cli_wrapper.zb_cli_dev import ZbCliDevice
from zb_cli_wrapper.src.utils.zigbee_classes.clusters.attribute import Attribute


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
        with open('DongleHandler\\..\\resource\\dongle_status.json', "r") as dongle_file:
            dongle_config = json.load(dongle_file)
            port = dongle_config['port']
            status = dongle_config['status']
            dongle_file.close()
        time.sleep(3)
        cli_instance = ZbCliDevice('', '', port)
        if status == 0:
            cli_instance.bdb.channel = [24]
            cli_instance.bdb.role = 'zr'
            cli_instance.bdb.start()
            with open('DongleHandler\\..\\resource\\dongle_status.json', "w") as dongle_file:
                dongle_config['status'] = 1
                json.dump(dongle_config, dongle_file)
                dongle_file.close()
            print("The dongle has started commissioning.")
            print("Please search for the dongle via SmartThings App within 5 seconds.")
            time.sleep(5.0)

        mylogger = logging.getLogger("ZB")
        mylogger.setLevel(logging.INFO)
        timestring = time.strftime("%Y.%m.%d.%H.%M.%S", time.gmtime())
        log_name = "DongleHandler\\..\\logs\\" + timestring + ".log"
        file_handler = logging.FileHandler(log_name)
        mylogger.addHandler(file_handler)
        mylogger.info("PROGRAM START")

        # 1. Start connection with the device.
        # The connection of the device is ruled by SmartThings hub.
        # Therefore, the only job the dongle needs to do is 

        # do the task_list
        for i in range(self.iteration):
            for task in self.task_list:
                timestamp = time.strftime("Time: %Y/%m/%d %H:%m:%S", time.localtime())
                mylogger.info("{}: From cluster {} executing {} with payload {}".format(timestamp, task.cluster, task.command, task.payloads))
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
                time.sleep(task.duration)
                attr_id, attr_type = get_attr_element(task.cluster, task.command)
                attr = Attribute(task.cluster, attr_id, attr_type)
                returned_attr = cli_instance.zcl.readattr(self.device.addr, attr, ep=ULTRA_THIN_WAFER_ENDPOINT)
                mylogger.info("returned value: {}".format(returned_attr.value))

        # # each task routine ends with disconnection
        cli_instance.close_cli()
        # port = serial.Serial("COM13", 115200)
        # port.close()
        # port.open()
        # port.write(str.encode('reset'))
        # port.reset_input_buffer()
        # port.reset_output_buffer()
        # port.close()
        # # Problem:

def get_attr_element(cluster, command):
    attr_id = 0
    attr_type = 0
    if cluster == 6:
        attr_id = ON_OFF_ONOFF_ATTR
        attr_type = TYPES.BOOL
    elif cluster == 8:
        attr_id = LVL_CTRL_CURR_LVL_ATTR
        attr_type = TYPES.UINT8
    elif cluster == 0x0300:
        attr_id = COLOR_CTRL_TEMP_MIRED_ATTR
        attr_type = TYPES.UINT16
    return attr_id, attr_type