# bluetooth low energy scan
import json
# from bluetooth.ble import DiscoveryService

def load_command():
    with open('command.json') as commandfile:
        content = json.load(commandfile)
        commandlist = content['command']
        for i in commandlist:
            do_individual_job(i)

def do_individual_job(config):
    with open(config) as configfile:
        data = json.load(configfile)
        # print(data)
        device_name = data['Device']
        # print(device_name)
        device_uuid = data['uuid']
        # print(device_uuid)
        connection_type = data['connection']
        # print(connection_type)
        service = data['service']
        # print(service)
        service_uuid = service['uuid']
        # print(service_uuid)
        service_char = service['characteristics']
        # print(service_char)
        char_uuid = service_char['uuid']
        # print(char_uuid)
        char_type = service_char['type']
        # print(char_type)
        char_value = service_char['value']
        # print(char_value)

load_command()
# service = DiscoveryService()
# devices = service.discover(2)

# for address, name in devices.items():
#     print("name: {}, address: {}".format(name, address))