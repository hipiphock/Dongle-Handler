# main controller of Dongle Handler
import time
from datetime import datetime
import json
import logging

from DongleHandler import *
# Zigbee
from zb_cli_wrapper.zb_cli_dev import ZbCliDevice
from zb_cli_wrapper.src.utils.zigbee_classes.clusters.attribute import Attribute
# BLE
from blatann import BleDevice


# added for clear path
# TODO: need to clean path problem
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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
        if self.connection_type == ZIGBEE_CONNECTION:
            # Before connecting the device with the dongle,
            # the dongle must join the hub's network.
            # TODO: implement automated port selector
            with open('resource\\dongle_status.json', "r") as dongle_file:
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
                # TODO: change the directory's path
                with open('resource\\dongle_status.json', "w") as dongle_file:
                    dongle_config['status'] = 1
                    json.dump(dongle_config, dongle_file)
                    dongle_file.close()
                print("The dongle has started commissioning.")
                print("Please search for the dongle via SmartThings App within 5 seconds.")
                time.sleep(5.0)

            zblogger = ZigbeeLogger()
            zblogger.log_init()

            # 1. Start connection with the device.
            # The connection of the device is ruled by SmartThings hub.

            # do the task_list
            for i in range(self.iteration):
                for task in self.task_list:
                    if task.task_kind == COMMAND_TASK:
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
                        # TODO: change code like
                        # 1. create READ_ATTR task with respect to Cmd task
                        # 2. append READ_ATTR task to task_list
                        attr_id, attr_type = get_attr_element(task.cluster, task.command)
                        param_attr = Attribute(task.cluster, attr_id, attr_type)
                        returned_attr = cli_instance.zcl.readattr(self.device.addr, param_attr, ep=ULTRA_THIN_WAFER_ENDPOINT)
                        zblogger.get_command_log(task)
                    elif task.task_kind == READ_ATTRIBUTE_TASK:
                        param_attr = Attribute(task.cluster, task.attr_id, task.attr_type)
                        returned_attr = cli_instance.zcl.readattr(self.device.addr, param_attr, ep=ULTRA_THIN_WAFER_ENDPOINT)
                        zblogger.get_read_attr_log(task, returned_attr.value)
                    elif task.task_kind == WRITE_ATTRIBUTE_TASK:
                        param_attr = Attribute(task.cluster, task.attr_id, task.attr_type)
                        cli_instance.zcl.writeattr(self.device.addr, param_attr, ep=ULTRA_THIN_WAFER_ENDPOINT)
                        returned_attr = cli_instance.zcl.readattr(self.device.addr, param_attr, ep=ULTRA_THIN_WAFER_ENDPOINT)
                        zblogger.get_read_attr_log(task, returned_attr.value)
                    

            # # each task routine ends with disconnection
            zblogger.close_logfile()
            cli_instance.close_cli()
        
        # Case: BLE connection
        elif self.connection_type == BLE_CONNECTION:
            # first, create a BLE object
            port = "COM3" # for example, TODO: create port selector
            ble_device = BleDevice(port)
            ble_device.open()




def get_attr_element(cluster, command):
    attr_id = 0
    attr_type = 0
    if cluster == 0x0006:
        attr_id = ON_OFF_ONOFF_ATTR
        attr_type = TYPES.BOOL
    elif cluster == 0x0008:
        attr_id = LVL_CTRL_CURR_LVL_ATTR
        attr_type = TYPES.UINT8
    elif cluster == 0x0300:
        attr_id = COLOR_CTRL_COLOR_TEMP_MIRED_ATTR
        attr_type = TYPES.UINT16
    return attr_id, attr_type

# Zigbee Logger
mylogger = logging.getLogger("ZB")
mylogger.setLevel(logging.INFO)

# TODO: need to remake logger for attribute tasks
class ZigbeeLogger:
    def log_init(self):
        timestring = time.strftime("%Y.%m.%d.%H.%M.%S", time.gmtime())
        log_name = "logs\\" + timestring + ".log"
        file_handler = logging.FileHandler(log_name)
        mylogger.addHandler(file_handler)
        mylogger.info("PROGRAM START")
        # mylogger.info("Time\t\tCLuster\t\tCommand\t\tpayload\t\tinterval\t\treturn value")

    def get_command_log(self, task):
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        cluster = task.cluster
        command = task.command
        payloads = task.payloads
        cluster_string = ""
        command_string = ""
        if cluster == ON_OFF_CLUSTER:
            cluster_string = "ON_OFF"
            if command == ON_OFF_OFF_CMD:
                command_string = "OFF"
            elif command == ON_OFF_ON_CMD:
                command_string = "ON"
            elif command == ON_OFF_TOGGLE_CMD:
                command_string = "TOGGLE"
            else:
                command_string = "UNKNOWN_COMMAND"
        elif cluster == LVL_CTRL_CLUSTER:
            cluster_string = "LVL_CTRL"
            if command == LVL_CTRL_MV_TO_LVL_CMD:
                command_string = "MV_TO_LVL"
            elif command == LVL_CTRL_MOVE_CMD:
                command_string = "MOVE"
            elif command == LVL_CTRL_STEP_CMD:
                command_string = "STEP"
            elif command == LVL_CTRL_STOP_CMD:
                command_string = "STOP"
            elif command == LVL_CTRL_MV_TO_LVL_ONOFF_CMD:
                command_string = "MV_TO_LVL_ONOFF"
            elif command == LVL_CTRL_MOVE_ONOFF_CMD:
                command_string = "MOVE_ONOFF"
            elif command == LVL_CTRL_STEP_ONOFF_CMD:
                command_string = "STEP_ONOFF"
            else:
                command_string = "UNKNOWN_COMMAND"
        elif cluster == COLOR_CTRL_CLUSTER:
            cluster_string = "COLOR_CTRL"
            if command == COLOR_CTRL_MV_TO_COLOR_CMD:
                command_string = "MV_TO_COLOR"
            elif command == COLOR_CTRL_MOVE_COLOR_CMD:
                command_string = "MOVE_COLOR"
            elif command == COLOR_CTRL_STEP_COLOR_CMD:
                command_string = "STEP_COLOR"
            elif command == COLOR_CTRL_MV_TO_COLOR_TEMP_CMD:
                command_string = "MV_TO_COLOR_TEMP"
            elif command == COLOR_CTRL_STOP_MOVE_STEP_CMD:
                command_string = "STOP_MOVE_STEP"
            elif command == COLOR_CTRL_MV_COLOR_TEMP_CMD:
                command_string = "MV_COLOR_TEMP"
            elif command == COLOR_CTRL_STEP_COLOR_TEMP_CMD:
                command_string = "STEP_COLOR_TEMP"
            else:
                command_string = "UNKNOWN_COMMAND"
        else:
            cluster_string = "UNKNOWN CLUSTER"
            command_string = "UNKNOWN COMMAND"
        mylogger.info("{};{};{};{};{};{}".format(
            timestamp, "COMMAND_TASK", cluster_string, command_string, payloads, task.duration))

    def get_read_attr_log(self, task, ret_val):
        timestamp = datetime.utcnow().strftime("%H:%M:%S.%f")[:-3]
        cluster = task.cluster
        attr_id = task.attr_id
        cluster_string = ""
        attr_string = ""
        if cluster == ON_OFF_CLUSTER:
            cluster_string = "ON_OFF_CLUSTER"
            attr_string = ON_OFF_ONOFF_ATTR
        elif cluster == LVL_CTRL_CLUSTER:
            cluster_string = "LVL_CTRL_CLUSTER"
            if attr_id == LVL_CTRL_CURR_LVL_ATTR:
                attr_string = "CURR_LVL"
            elif attr_id == LVL_CTRL_REMAIN_TIME_ATTR:
                attr_string = "REMAIN_TIME"
            elif attr_id == LVL_CTRL_ONOFF_TRANS_TIME_ATTR:
                attr_string = "ONOFF_TRANS_TIME"
            elif attr_id == LVL_CTRL_ON_LEVEL_ATTR:
                attr_string = "ON_LEVEL"
        elif cluster == COLOR_CTRL_CLUSTER:
            cluster_string = "COLOR_CTRL_CLUSTER"
            if attr_id == COLOR_CTRL_CURR_HUE_ATTR:
                attr_string = "CURR_HUE"
            elif attr_id == COLOR_CTRL_CURR_SAT_ATTR:
                attr_string = "CURR_SAT"
            elif attr_id == COLOR_CTRL_REMAINING_TIME_ATTR:
                attr_string = "REMAINING_TIME"
            elif attr_id == COLOR_CTRL_CURR_X_ATTR:
                attr_string = "CURR_X"
            elif attr_id == COLOR_CTRL_CURR_Y_ATTR:
                attr_string = "CURR_Y"
            elif attr_id == COLOR_CTRL_COLOR_TEMP_MIRED_ATTR:
                attr_string = "COLOR_TEMP_MIRED"
            elif attr_id == COLOR_CTRL_COLOR_MODE_ATTR:
                attr_string = "COLOR_MODE"
            elif attr_id == COLOR_CTRL_ENHANCED_COLOR_MODE_ATTR:
                attr_string = "ENHANCED_COLOR_MODE"
            elif attr_id == COLOR_CTRL_COLOR_CAPABILITY_ATTR:
                attr_string = "COLOR_CAPABILITY"
            elif attr_id == COLOR_CTRL_COLOR_TEMP_MIN_MIRED_ATTR:
                attr_string = "COLOR_TEMP_MIN_MIRED"
            elif attr_id == COLOR_CTRL_COLOR_TEMP_MAX_MIRED_ATTR:
                attr_string = "COLOR_TEMP_MAX_MIRED"
        mylogger.info("{};{};{};{};{};{}".format(
                timestamp, "READ_ATTRIBUTE_TASK", cluster_string, attr_string, task.duration, ret_val))
    
    def get_write_attr_log(self, task):
        timestamp = datetime.utcnow().strftime("%H:%M:%S.%f")[:-3]
        cluster = task.cluster
        attr_id = task.attr_id
        cluster_string = ""
        attr_string = ""
        if cluster == ON_OFF_CLUSTER:
            attr_string = ON_OFF_ONOFF_ATTR
        elif cluster == LVL_CTRL_CLUSTER:
            if attr_id == LVL_CTRL_CURR_LVL_ATTR:
                attr_string = "CURR_LVL"
            elif attr_id == LVL_CTRL_REMAIN_TIME_ATTR:
                attr_string = "REMAIN_TIME"
            elif attr_id == LVL_CTRL_ONOFF_TRANS_TIME_ATTR:
                attr_string = "ONOFF_TRANS_TIME"
            elif attr_id == LVL_CTRL_ON_LEVEL_ATTR:
                attr_string = "ON_LEVEL"
        elif cluster == COLOR_CTRL_CLUSTER:
            if attr_id == COLOR_CTRL_CURR_HUE_ATTR:
                attr_string = "CURR_HUE"
            elif attr_id == COLOR_CTRL_CURR_SAT_ATTR:
                attr_string = "CURR_SAT"
            elif attr_id == COLOR_CTRL_REMAINING_TIME_ATTR:
                attr_string = "REMAINING_TIME"
            elif attr_id == COLOR_CTRL_CURR_X_ATTR:
                attr_string = "CURR_X"
            elif attr_id == COLOR_CTRL_CURR_Y_ATTR:
                attr_string = "CURR_Y"
            elif attr_id == COLOR_CTRL_COLOR_TEMP_MIRED_ATTR:
                attr_string = "COLOR_TEMP_MIRED"
            elif attr_id == COLOR_CTRL_COLOR_MODE_ATTR:
                attr_string = "COLOR_MODE"
            elif attr_id == COLOR_CTRL_ENHANCED_COLOR_MODE_ATTR:
                attr_string = "ENHANCED_COLOR_MODE"
            elif attr_id == COLOR_CTRL_COLOR_CAPABILITY_ATTR:
                attr_string = "COLOR_CAPABILITY"
            elif attr_id == COLOR_CTRL_COLOR_TEMP_MIN_MIRED_ATTR:
                attr_string = "COLOR_TEMP_MIN_MIRED"
            elif attr_id == COLOR_CTRL_COLOR_TEMP_MAX_MIRED_ATTR:
                attr_string = "COLOR_TEMP_MAX_MIRED"
        mylogger.info("{};{};{};{};{}".format(
                timestamp, "WRITE_ATTRIBUTE_TASK", cluster_string, attr_string, task.duration))
    
    def close_logfile(self):
        for handler in mylogger.handlers:
            handler.close()