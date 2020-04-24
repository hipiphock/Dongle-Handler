import json
import random
import serial
from zb_cli_wrapper.zb_cli_dev import ZbCliDevice
from zb_cli_wrapper.src.utils.cmd_wrappers.zigbee.constants import *

ZIGBEE_STARTED = False
device_addr = 0xe48f
ep = 8 
device_uuid = "asdf-qwer-zxcv"
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

    # does the individual process of Zigbee command
    # or BLE service
    def do_individual_job(self, config):
        print(config.command)
        if config.connection == 'Zigbee':
            global ZIGBEE_STARTED
            global cli_instance
            if ZIGBEE_STARTED == False:
                try:
                    cli_instance = ZbCliDevice('','','COM13')
                    cli_instance.bdb.channel = [24]
                    cli_instance.bdb.role = 'zr'
                    cli_instance.bdb.start()
                    ZIGBEE_STARTED = True
                except serial.serialutil.SerialException:
                    cli_instance.close_cli()
                    return None
            attribute = make_attr(config.command,
                    self.addr, 
                    self.ep, 
                    config.payloads)
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

# inner class representing config.json files
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
        
def make_attr(command_str, address, ep, payloads):
    command_map = { "ON_OFF_OFF_CMD":ON_OFF_OFF_CMD, 
                    "ON_OFF_ON_CMD":ON_OFF_ON_CMD,
                    "LVL_CTRL_MV_TO_LVL_CMD":LVL_CTRL_MV_TO_LVL_CMD,
                    "COLOR_CTRL_MV_TO_HUE_CMD":COLOR_CTRL_MV_TO_HUE_CMD,
                    "COLOR_CTRL_MV_TO_SAT_CMD":COLOR_CTRL_MV_TO_SAT_CMD,
                    "COLOR_CTRL_MV_TO_HUE_SAT_CMD":COLOR_CTRL_MV_TO_HUE_SAT_CMD}
    command_int = command_map[command_str]
    cluster = 0
    # attr_id = 0
    if command_str.find("ON_OFF") != -1:
        cluster = ON_OFF_CLUSTER
        # attr_id = ON_OFF_ONOFF_ATTR
    elif command_str.find("LVL_CTRL") != -1:
        cluster = LVL_CTRL_CLUSTER
        # attr_id = LVL_CTRL_CURR_LVL_ATTR
    elif command_str.find("COLOR_CTRL") != -1:
        cluster = COLOR_CTRL_CLUSTER
        # if command_str.find("TO_HUE_CMD") != -1:
        #     attr_id = COLOR_CTRL_CURR_HUE_ATTR
        # elif command_str.find("TO_SAT_CMD") != -1:
        #     attr_id = COLOR_CTRL_CURR_SAT_ATTR
    addr = int(address, 16)
    return ZigbeeAttr(addr, ep, cluster, command_int, payloads)

# parses command
def load_command():
    with open('command.json') as commandfile:
        content = json.load(commandfile)
        device_name = content['Device']
        print("Device name: {}".format(device_name))
        device_uuid = content['uuid']
        print("Device uuid: {}".format(device_uuid))
        global device_addr
        device_addr = content['address']
        print("Device address: {}".format(device_addr))
        global ep
        ep = content['ep']
        print("ep: {}".format(ep))
        command_list = content['command_list']
        for command_set in command_list:
            do_each_command(command_set)

def do_each_command(command):
    config_file = command['command'] + ".json"
    iteration = command['iteration']
    for i in range(iteration):
        do_individual_job(config_file)  

def do_individual_job(config):
    with open(config) as configfile:
        data = json.load(configfile)
        connection_type = data['connection']
        print("\nConnection type: {}".format(connection_type))
        if connection_type == "Zigbee":
            command = data['command']
            print("Command: {}".format(command))
            payloads = []
            if config.split("/")[-1].find("onoff") == -1:
                payloads = data['payloads']
                print("Payloads: {}".format(payloads))
            attribute = make_attr(command, device_addr, ep, format_payload(payloads))
            zigbee_write(attribute)
        else:
            service = data['service']
            service_uuid = service['uuid']
            print("Service uuid: {}".format(service_uuid))
            service_char = service['characteristics']
            char_uuid = service_char['uuid']
            print("Characteristic uuid: {}".format(char_uuid))
            char_type = service_char['type']
            print("Characteristic type: {}".format(char_type))

def format_payload(payload):
    if payload == "None":
        return
    types_map = {"TYPES.BOOL": TYPES.BOOL,
        "TYPES.UINT8": TYPES.UINT8,
        "TYPES.UINT16": TYPES.UINT16, 
        "TYPES.UINT32": TYPES.UINT32,
        "TYPES.UINT64": TYPES.UINT64,
        "TYPES.SINT8": TYPES.SINT8,
        "TYPES.SINT16": TYPES.SINT16,
        "TYPES.SINT64": TYPES.SINT64, 
        "TYPES.ENUM8": TYPES.ENUM8,
        "TYPES.MAP8": TYPES.MAP8, 
        "TYPES.EUI64": TYPES.EUI64,
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

def zigbee_write(attribute):
    global ZIGBEE_STARTED
    if ZIGBEE_STARTED == False:
        try:
            global cli_instance
            cli_instance = ZbCliDevice('','','COM13')
            cli_instance.bdb.channel = [24]
            cli_instance.bdb.role = 'zr'
        except serial.serialutil.SerialException:
            cli_instance.close_cli()
            return None
        cli_instance.bdb.start()
        ZIGBEE_STARTED = True

    if attribute.payload == []:
        cli_instance.zcl.generic(eui64= attribute.eui64, ep = attribute.ep, profile=DEFAULT_ZIGBEE_PROFILE_ID, cluster=attribute.cluster, cmd_id=attribute.cmd_id)
        # x = cli_instance.zcl.raw(eui64= addr, ep = attribute.ep, cluster = attribute.cluster, payload_hex=attribute.payload)
        # print(x)
    else:
        cli_instance.zcl.generic(eui64= attribute.eui64, ep = attribute.ep, profile=DEFAULT_ZIGBEE_PROFILE_ID, cluster=attribute.cluster, cmd_id=attribute.cmd_id, payload=attribute.payload)

if __name__ == "__main__":
    # find_dongle_port()
    commander = CommandSet.make_instance('command.json')
    commander.start_routine()
    # load_command()