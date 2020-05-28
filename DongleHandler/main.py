import sys
import json
import random
import serial
import logging
import time
from Constants import *
from zb_cli_wrapper.zb_cli_dev import ZbCliDevice
from zb_cli_wrapper.src.utils.zigbee_classes.clusters.attribute import Attribute

ZIGBEE_STARTED = False
cli_instance = None

# finds the port that dongle is inserted
def find_dongle_port():
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        # find the appropriate port based on the name of the dongle
        # TODO: Implement automated port selector
        pass

# representing command.json file, CommandSet defines:
# - Device's information
# - Sequences of commands and its number of iterations
class CommandSet:
    def __init__(self, name, uuid, addr, ep, cmdlist):
        self.name = name
        self.uuid = uuid
        self.addr = addr
        self.ep = ep
        self.cmdlist = cmdlist
    # in this program, instance of CommandSet should be generated via
    # this classmethod.
    @classmethod
    def make_instance(cls, cmdfile):
        with open(cmdfile) as commandfile:
            content = json.load(commandfile)
            name    = content['Device']
            uuid    = content['uuid']
            _addr   = content['address']
            addr    = int(_addr, 16)
            _ep     = content['ep']
            ep      = int(_ep, 16)
            cmds    = content['command_list']
            cmdlist = []
            for cmd in cmds:
                # TODO: make command array inside each command block
                configs     = cmd['command']
                iteration   = cmd['iteration']
                configlist  = []
                for config in configs:
                    configlist.append(Config.make_instance(config))
                cmdlist.append({'config':configlist, 'iteration':iteration})
        return cls(name, uuid, addr, ep, cmdlist)

    # main procedure of command.json
    def start_routine(self):
        for command in self.cmdlist:
            configlist  = command['config']
            iteration   = command['iteration']
            for i in range(iteration):
                print("{}th iteration:".format(i+1))
                for config in configlist:
                    self.do_individual_job(config)
            print("command routine finished")

    # does the individual process of Zigbee command or BLE service
    def do_individual_job(self, config):
        if config.connection == 'Zigbee':
            global ZIGBEE_STARTED
            global cli_instance
            if ZIGBEE_STARTED == False:
                try:
                    print("Starting Zigbee Connection...")
                    cli_instance = ZbCliDevice('','','COM13')
                    # cli_instance.bdb.channel = [24]
                    # cli_instance.bdb.role = 'zr'
                    # cli_instance.bdb.start()
                    ZIGBEE_STARTED = True
                except serial.serialutil.SerialException:
                    cli_instance.close_cli()
                    return None
            timestamp = time.strftime("Time: %Y/%m/%d %H:%m:%S", time.localtime())
            mylogger.info("{}: Executing {} with payload {}".format(
                timestamp, config.cmdname, config.payloads))
            # case: command without payload
            # example: on & off
            if config.payloads == None:
                cli_instance.zcl.generic(eui64= self.addr, ep = self.ep,
                        profile=DEFAULT_ZIGBEE_PROFILE_ID,
                        cluster=config.cluster, cmd_id=config.command)
            # case: command that needs payload
            # example: level control & color control
            else:
                cli_instance.zcl.generic(eui64= self.addr, ep = self.ep,
                        profile=DEFAULT_ZIGBEE_PROFILE_ID, 
                        cluster=config.cluster, cmd_id=config.command, payload=config.payloads)
            time.sleep(float(config.duration))
            # when reading attribute, you need to set which attribute to read.
            attr_id, attr_type = get_attr_element(config.command)
            attr = Attribute(config.cluster, attr_id, attr_type)
            returned_attr = cli_instance.zcl.readattr(self.addr, attr,
                                ep=ULTRA_THIN_WAFER_ENDPOINT)
            mylogger.info("returned value: {}".format(returned_attr.value))
        elif config.connection == 'BLE':
            pass
        else:
            print("UNSUPPORTED TYPE OF CONNECTION.")
            exit(1)

def get_attr_element(command):
    attr_id = 0
    attr_type = 0
    if command == ON_OFF_OFF_CMD or command == ON_OFF_ON_CMD:
        attr_id = ON_OFF_ONOFF_ATTR
        attr_type = TYPES.BOOL
    elif command == LVL_CTRL_MV_TO_LVL_CMD or command == LVL_CTRL_MV_TO_LVL_ONOFF_CMD:
        attr_id = LVL_CTRL_CURR_LVL_ATTR
        attr_type = TYPES.UINT8
    return attr_id, attr_type

# class representing config.json files
# each config file's should be made by this inner class
class Config:
    def __init__(self, connection, cluster, command, cmdname, payloads=None, duration=0):
        self.connection = connection
        self.cluster = cluster
        self.command = command
        self.cmdname = cmdname          # necessary for logging
        self.payloads = payloads
        self.duration = duration
    
    @classmethod
    def make_instance(cls, configfile):
        with open(configfile) as config_file:
            content = json.load(config_file)
            connection  = content['connection']
            cmdname     = content['command']
            payload     = content['payloads']
            duration    = content['duration']
            cluster     = get_cluster(cmdname)
            command     = format_command(cmdname)
            payloads    = format_payload(payload)
        return cls(connection, cluster, command, cmdname, payloads, duration)

def get_cluster(command):
    cluster = 0
    if command.find("ON_OFF") != -1:
        cluster = ON_OFF_CLUSTER
    elif command.find("LVL_CTRL") != -1:
        cluster = LVL_CTRL_CLUSTER
    elif command.find("COLOR_CTRL") != -1:
        cluster = COLOR_CTRL_CLUSTER
    return cluster

def format_command(command):
    command_map = { "ON_OFF_OFF_CMD":   ON_OFF_OFF_CMD, 
                    "ON_OFF_ON_CMD":    ON_OFF_ON_CMD,
                    "ON_OFF_TOGGLE_CMD":        ON_OFF_TOGGLE_CMD,
                    "LVL_CTRL_MV_TO_LVL_CMD":   LVL_CTRL_MV_TO_LVL_CMD,
                    "COLOR_CTRL_MV_TO_HUE_CMD":     COLOR_CTRL_MV_TO_HUE_CMD,
                    "COLOR_CTRL_MV_TO_SAT_CMD":     COLOR_CTRL_MV_TO_SAT_CMD,
                    "COLOR_CTRL_MV_TO_HUE_SAT_CMD": COLOR_CTRL_MV_TO_HUE_SAT_CMD }
    cmdid = command_map[command]
    return cmdid

# TODO: generating random variable
def format_payload(payload):
    if payload == "None":
        return None
    types_map = {
        "TYPES.BOOL":   TYPES.BOOL,
        "TYPES.UINT8":  TYPES.UINT8,
        "TYPES.UINT16": TYPES.UINT16, 
        "TYPES.UINT32": TYPES.UINT32,
        "TYPES.UINT64": TYPES.UINT64,
        "TYPES.SINT8":  TYPES.SINT8,
        "TYPES.SINT16": TYPES.SINT16,
        "TYPES.SINT64": TYPES.SINT64, 
        "TYPES.ENUM8":  TYPES.ENUM8,
        "TYPES.MAP8":   TYPES.MAP8, 
        "TYPES.EUI64":  TYPES.EUI64,
        "TYPES.STRING": TYPES.STRING }
    result = []
    for item in payload:
        value_type = types_map[item['type']]
        if value_type is not TYPES.STRING:
            value = int(item['value'], 16)
        else:
            value = item['value']
        result.append((value, value_type))
    return result

def initialization():
    global cli_instance
    cli_instance.bdb.channel = [24]
    cli_instance.bdb.role = 'zr'
    cli_instance.bdb.start()

# main routine
if __name__ == "__main__":
    # LOGGING CONFIGURATION
    mylogger = logging.getLogger("ZB")
    mylogger.setLevel(logging.INFO)
    file_handler = logging.FileHandler("mylog.log")
    mylogger.addHandler(file_handler)
    mylogger.info("PROGRAM START")

    # logging.basicConfig(level=logging.DEBUG)    # for logging
    
    if len(sys.argv) == 1:
        print("You must select either interactive mode or batch mode.")
        print("Usage: python3 main.py <-I or -B> <if -B: filename>")
    else:
        # interactive mode
        if sys.argv[1] == '-I':
            print("INTERACTIVE MODE")
            cli_instance = ZbCliDevice('','','COM13')
            # cli_instance.bdb.channel = [24]
            # cli_instance.bdb.role = 'zr'
            # cli_instance.bdb.start()
            # rough coding: turning light on and off
            eui64 = int('FFFE88571D018E53', 16)
            on_off_attr    = Attribute(ON_OFF_CLUSTER, ON_OFF_ONOFF_ATTR,
                                    TYPES.BOOL)
            level_attr  = Attribute(LVL_CTRL_CLUSTER, LVL_CTRL_CURR_LVL_ATTR,
                                    TYPES.UINT8)
            while True:
                print("Enter input:")
                usr_cmd = input()
                # off command
                if usr_cmd == 'off':
                    print("turning off the light")
                    cli_instance.zcl.generic(eui64, 8, ON_OFF_CLUSTER, 
                            DEFAULT_ZIGBEE_PROFILE_ID, ON_OFF_OFF_CMD)
                    cli_instance.zcl.readattr(eui64, on_off_attr, ep=ULTRA_THIN_WAFER_ENDPOINT)
                # on command
                elif usr_cmd == 'on':
                    print("turning on the light")
                    cli_instance.zcl.generic(eui64, 8, ON_OFF_CLUSTER, 
                            DEFAULT_ZIGBEE_PROFILE_ID, ON_OFF_ON_CMD)
                    cli_instance.zcl.readattr(eui64, on_off_attr, ep=ULTRA_THIN_WAFER_ENDPOINT)
                # set light level into 'low'
                elif usr_cmd == 'low':
                    low_payload = [(2, TYPES.UINT8), (0, TYPES.UINT16)]
                    print("setting light into low level")
                    cli_instance.zcl.generic(eui64, 8, LVL_CTRL_CLUSTER,
                            DEFAULT_ZIGBEE_PROFILE_ID, 
                            LVL_CTRL_MV_TO_LVL_ONOFF_CMD, payload=low_payload)
                    time.sleep(1)
                    cli_instance.zcl.readattr(eui64, level_attr, ep=ULTRA_THIN_WAFER_ENDPOINT)
                # set light level into 'mid'
                elif usr_cmd == 'mid':
                    mid_payload = [(80, TYPES.UINT8), (0, TYPES.UINT16)]
                    print("setting light into mid level")
                    cli_instance.zcl.generic(eui64, 8, LVL_CTRL_CLUSTER, 
                            DEFAULT_ZIGBEE_PROFILE_ID,
                            LVL_CTRL_MV_TO_LVL_ONOFF_CMD, payload=mid_payload)
                    time.sleep(1)
                    cli_instance.zcl.readattr(eui64, level_attr, ep=ULTRA_THIN_WAFER_ENDPOINT)
                # set light level into 'high'
                elif usr_cmd == 'high':
                    high_payload = [(254, TYPES.UINT8), (0, TYPES.UINT16)]
                    print("setting light into high level")
                    cli_instance.zcl.generic(eui64, 8, LVL_CTRL_CLUSTER, 
                            DEFAULT_ZIGBEE_PROFILE_ID, 
                            LVL_CTRL_MV_TO_LVL_ONOFF_CMD, payload=high_payload)
                    time.sleep(1)
                    cli_instance.zcl.readattr(eui64, level_attr, ep=ULTRA_THIN_WAFER_ENDPOINT)
                # custom level controller
                elif usr_cmd == 'level':
                    lvl_input = input()
                    custom_val = int(lvl_input)
                    custom_payload = [(custom_val, TYPES.UINT8), (0, TYPES.UINT16)]
                    print("setting light into high level")
                    cli_instance.zcl.generic(eui64, 8, LVL_CTRL_CLUSTER, 
                            DEFAULT_ZIGBEE_PROFILE_ID, 
                            LVL_CTRL_MV_TO_LVL_ONOFF_CMD, payload=custom_payload)
                    cli_instance.zcl.readattr(eui64, level_attr, ep=ULTRA_THIN_WAFER_ENDPOINT)
                # get status
                elif usr_cmd == 'read':
                    onoff_result = cli_instance.zcl.readattr(eui64, on_off_attr, ep=ULTRA_THIN_WAFER_ENDPOINT)
                    level_result = cli_instance.zcl.readattr(eui64, level_attr, ep=ULTRA_THIN_WAFER_ENDPOINT)
                    print(level_result)
                # terminate the program
                elif usr_cmd == 'exit' or usr_cmd == 'quit' or usr_cmd == 'q':
                    print("exit")
                    cli_instance.close_cli()
                    exit()
        # batch mode
        elif sys.argv[1] == '-B':
            print("BATCH MODE")
            commander_file = sys.argv[2]
            commander = CommandSet.make_instance(commander_file)
            commander.start_routine()
        else:
            print("You must select either interactive mode or batch mode.")
            print("Usage: python3 main.py <-I or -B> <if -B: filename>")