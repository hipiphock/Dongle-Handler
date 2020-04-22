# bluetooth low energy scan
import json
import random
# from bluetooth.ble import DiscoveryService
import serial
from zb_cli_wrapper.zb_cli_dev import ZbCliDevice
from zb_cli_wrapper.src.utils.cmd_wrappers.zigbee.constants import *

# CURRENT WAFER'S ENDPOINT IS 8
    
class Attr:
    def __init__(self, _eui64, _cluster, _attr_id, _type, _value, _ep, _profile):
        self.eui64 = _eui64
        self.ep = _ep
        self.cluster = _cluster
        self.id = _attr_id
        self.type = _type
        self.value = _value
        self.profile = _profile
        
def make_attr(command_str, address, payloads):
    command_map = { "ON_OFF_OFF_CMD":ON_OFF_OFF_CMD, 
                    "ON_OFF_ON_CMD":ON_OFF_ON_CMD,
                    "LVL_CTRL_MV_TO_LVL_CMD":LVL_CTRL_MV_TO_LVL_CMD,
                    "COLOR_CTRL_MV_TO_HUE_CMD":COLOR_CTRL_MV_TO_HUE_CMD,
                    "COLOR_CTRL_MV_TO_SAT_CMD":COLOR_CTRL_MV_TO_SAT_CMD,
                    "COLOR_CTRL_MV_TO_HUE_SAT_CMD":COLOR_CTRL_MV_TO_HUE_SAT_CMD
    }
    command_int = command_map[command_str]
    cluster = 0
    attr_id = 0
    data_type = TYPES.BOOL
    if command_str.find("ON_OFF") != -1:
        cluster = ON_OFF_CLUSTER
        attr_id = ON_OFF_ONOFF_ATTR
    elif command_str.find("LVL_CTRL") != -1:
        cluster = LVL_CTRL_CLUSTER
        attr_id = LVL_CTRL_CURR_LVL_ATTR
        data_type = TYPES.UINT16
    elif command_str.find("COLOR_CTRL") != -1:
        cluster = COLOR_CTRL_CLUSTER
        if command_str.find("TO_HUE_CMD") != -1:
            attr_id = COLOR_CTRL_CURR_HUE_ATTR
        elif command_str.find("TO_SAT_CMD") != -1:
            attr_id = COLOR_CTRL_CURR_SAT_ATTR
        data_type = TYPES.UINT16
    if payloads == []:
        return Attr(address, cluster, attr_id, data_type, command_int, 8, 0x0104)
    else:
        return Attr(address, cluster, attr_id, data_type, payloads, 8, 0x0104)
        

def load_command():
    with open('command.json') as commandfile:
        content = json.load(commandfile)
        command = content['command']
        iteration = content['iteration']
        for i in range(iteration):
            do_individual_job(command)

def do_individual_job(config):
    with open(config+".json") as configfile:
        data = json.load(configfile)
        device_name = data['Device']
        print("Device name: {}".format(device_name))
        connection_type = data['connection']
        print("Connection type: {}".format(connection_type))
        if connection_type == "Zigbee":
            device_addr = data['address']
            print("Device address: {}".format(device_addr))
            cluster = data['cluster']
            print("cluster: {}".format(cluster))
            command = data['command']
            print("Command: {}".format(command))
            description = data['description']
            print("description: {}".format(description))
            payloads = []
            if config.split("/")[-1].find("onoff") == -1:
                payloads = data['payloads']
                print("Payloads: {}".format(payloads))
            attribute = make_attr(command, device_addr, payloads)
            zigbee_write(attribute)
            
        else:
            device_uuid = data['uuid']
            print("Device uuid: {}".format(device_uuid))
            service = data['service']
            service_uuid = service['uuid']
            print("Service uuid: {}".format(service_uuid))
            service_char = service['characteristics']
            char_uuid = service_char['uuid']
            print("Characteristic uuid: {}".format(char_uuid))
            char_type = service_char['type']
            print("Characteristic type: {}".format(char_type))

def zigbee_write(attribute):
    try:
        cli_instance = ZbCliDevice('','','COM13')
        cli_instance.bdb.channel = [24]
        cli_instance.bdb.role = 'zr'
        cli_instance.bdb.start()
    except serial.serialutil.SerialException:
        print("FAILED")
        cli_instance.close_cli()
        return None
    # cli_instance.bdb.start()
    addr = int(attribute.eui64, 16)
    # cli_instance.zcl.readattr(eui64=addr, attr=attribute, ep=attribute.ep, profile=attribute.profile)
    cli_instance.zcl.writeattr(eui64=addr, attr= attribute, ep=attribute.ep, profile=attribute.profile)
    # if attribute.payload == []:
    #     cli_instance.zcl.generic(eui64= addr, ep = attribute.ep, profile=attribute.profile, cluster=attribute.cluster, cmd_id=attribute.cmd_id)
    # else:
    #     cli_instance.zcl.generic(eui64= addr, ep = attribute.ep, profile=attribute.profile, cluster=attribute.cluster, cmd_id=attribute.cmd_id, payload=attribute.payload)
        
        

load_command()
# service = DiscoveryService()
# devices = service.discover(2)

# for address, name in devices.items():
#     print("name: {}, address: {}".format(name, address))