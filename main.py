import sys
import json
import random
import serial
from zb_cli_wrapper.zb_cli_dev import ZbCliDevice
from zb_cli_wrapper.src.utils.cmd_wrappers.zigbee.constants import *

ZIGBEE_STARTED = False
cli_instance = None

# finds the port that dongle is inserted
def find_dongle_port():
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        # find the appropriate port based on the name of the dongle
        # TODO: Implement automated port selector
        pass

# representing command.json file,
# CommandSet defines:
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
            addr    = content['address']
            ep      = content['ep']
            cmds    = content['command_list']
            cmdlist = []
            for cmd in cmds:
                configfile  = cmd['command'] + ".json"
                iteration   = cmd['iteration']
                config = Config.make_instance(configfile)
                cmdlist.append({'config':config, 'iteration':iteration})
        return cls(name, uuid, addr, ep, cmdlist)

    # main procedure of command.json
    def start_routine(self):
        for command in self.cmdlist:
            config      = command['config']
            iteration   = command['iteration']
            for i in range(iteration):
                self.do_individual_job(config)
            # global cli_instance
            # cli_instance.close_cli()
            print("command routine finished")

    # does the individual process of Zigbee command
    # or BLE service
    def do_individual_job(self, config):
        if config.connection == 'Zigbee':
            global ZIGBEE_STARTED
            global cli_instance
            if ZIGBEE_STARTED == False:
                try:
                    print("Starting Zigbee Connection...")
                    cli_instance = ZbCliDevice('','','COM13')
                    cli_instance.bdb.channel = [24]
                    cli_instance.bdb.role = 'zr'
                    cli_instance.bdb.start()
                    ZIGBEE_STARTED = True
                except serial.serialutil.SerialException:
                    cli_instance.close_cli()
                    return None
            attribute = make_attr(self.addr, self.ep,
                    config.command, config.payloads)
            print("address: {}".format(attribute.eui64))
            print("endpoint: {}".format(attribute.ep))
            print("cluster: {}".format(attribute.cluster))
            print("cmd: {}".format(attribute.cmd_id))
            print("payloads: {}".format(attribute.payload))
            if attribute.payload == []:
                cli_instance.zcl.generic(
                        eui64= attribute.eui64, 
                        ep = attribute.ep,
                        profile=DEFAULT_ZIGBEE_PROFILE_ID,
                        cluster=attribute.cluster, 
                        cmd_id=attribute.cmd_id)                
            else:
                cli_instance.zcl.generic(
                        eui64= attribute.eui64, 
                        ep = attribute.ep, 
                        profile=DEFAULT_ZIGBEE_PROFILE_ID, 
                        cluster=attribute.cluster, 
                        cmd_id=attribute.cmd_id, 
                        payload=attribute.payload)

# class representing config.json files
# each config file's should be made by this inner class
class Config:
    def __init__(self, connection, command, payloads=None):
        self.connection = connection
        self.command = command
        self.payloads = payloads
    
    @classmethod
    def make_instance(cls, configfile):
        with open(configfile) as config_file:
            content = json.load(config_file)
            connection  = content['connection']
            command     = content['command']
            payload     = content['payloads']
            payloads    = format_payload(payload)
            # additional job required for payloads:
            # - the generic function gets payloads as lists of tuples
        return cls(connection, command, payloads)
        
# defines Zigbee Attribute
class ZigbeeAttr:
    def __init__(self, _eui64, _ep, _cluster, _cmd_id, _payload):
        self.eui64 = _eui64
        self.ep = _ep
        self.cluster = _cluster
        self.cmd_id = _cmd_id
        self.payload = _payload
        
def make_attr(address, ep, command, payloads):
    command_map = { "ON_OFF_OFF_CMD":   ON_OFF_OFF_CMD, 
                    "ON_OFF_ON_CMD":    ON_OFF_ON_CMD,
                    "LVL_CTRL_MV_TO_LVL_CMD":   LVL_CTRL_MV_TO_LVL_CMD,
                    "COLOR_CTRL_MV_TO_HUE_CMD":     COLOR_CTRL_MV_TO_HUE_CMD,
                    "COLOR_CTRL_MV_TO_SAT_CMD":     COLOR_CTRL_MV_TO_SAT_CMD,
                    "COLOR_CTRL_MV_TO_HUE_SAT_CMD": COLOR_CTRL_MV_TO_HUE_SAT_CMD}
    command_int = command_map[command]
    cluster = 0
    if command.find("ON_OFF") != -1:
        cluster = ON_OFF_CLUSTER
    elif command.find("LVL_CTRL") != -1:
        cluster = LVL_CTRL_CLUSTER
    elif command.find("COLOR_CTRL") != -1:
        cluster = COLOR_CTRL_CLUSTER
    addr = int(address, 16)
    return ZigbeeAttr(addr, ep, cluster, command_int, payloads)

def format_payload(payload):
    if payload == "None":
        return
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

# main routine
if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("You must select either interactive mode or batch mode.")
        print("Usage: python3 main.py <-I or -B> <if -B: filename>")
    else:
        if sys.argv[1] == '-I':
            print("Interactive Mode:")
            cli_instance = ZbCliDevice('','','COM13')
            # cli_instance.bdb.channel = [24]
            # cli_instance.bdb.role = 'zr'
            # cli_instance.bdb.start()
            # rough coding: turning light on and off
            eui64 = int('88571DFFFE0E5416', 16)
            while True:
                print("Enter input:")
                usr_cmd = input()
                if usr_cmd == 'off':
                    print("turning off the light")
                    cli_instance.zcl.generic(eui64, 8, ON_OFF_CLUSTER, DEFAULT_ZIGBEE_PROFILE_ID, ON_OFF_OFF_CMD)
                elif usr_cmd == 'on':
                    print("turning on the light")
                    cli_instance.zcl.generic(eui64, 8, ON_OFF_CLUSTER, DEFAULT_ZIGBEE_PROFILE_ID, ON_OFF_ON_CMD)
                elif usr_cmd == 'exit' or usr_cmd == 'quit' or usr_cmd == 'q':
                    # exit
                    print("exit")
                    cli_instance.close_cli()
                    exit()

        elif sys.argv[1] == '-B':
            print("Batch Mode:")
            commander_file = sys.argv[2]
            commander = CommandSet.make_instance(commander_file)
            commander.start_routine()
        else:
            print("You must select either interactive mode or batch mode.")
    # find_dongle_port()
    # commander = CommandSet.make_instance(commander_file)
    # commander.start_routine()
    # ser = serial.Serial('COM13')
    # ser.write(b'reset')
    # ser.close()