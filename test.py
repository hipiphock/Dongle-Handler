# bluetooth low energy scan
import json
from bluetooth.ble import DiscoveryService

def load_command():
    commandfile = open("command.json", "r")
    content = commandfile.read()
    commandlist = content['command']
    for i in range(commandlist):
        do_individual_job(i)

def do_individual_job(config):
    with open(config) as configfile:
        data = json.load(configfile)
        device_name = data['Device']
        device_uuid = data['uuid']
        connection_type = data['connection']
        service = data['service']
        service_uuid = service['uuid']
        service_char = service['characteristics']
        char_uuid = service_char['uuid']
        char_type = service_char['type']
        char_value = service_char['value']


service = DiscoveryService()
devices = service.discover(2)

for address, name in devices.items():
    print("name: {}, address: {}".format(name, address))