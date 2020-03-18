# bluetooth low energy scan
import json
# from bluetooth.ble import DiscoveryService

def load_command():
    with open('command.json') as commandfile:
        content = json.load(commandfile)
        command = content['command']
        iteration = content['iteration']
        value_range = content['range']
        for i in range(iteration):
            do_individual_job(i, value_range)

def do_individual_job(config, value_range):
    with open(config) as configfile:
        data = json.load(configfile)
        device_name = data['Device']
        print("Device name: {}".format(device_name))
        device_uuid = data['uuid']
        print("Device uuid: {}".format(device_uuid))
        connection_type = data['connection']
        print("Connection type: {}".format(connection_type))
        service = data['service']
        service_uuid = service['uuid']
        print("Service uuid: {}".format(service_uuid))
        service_char = service['characteristics']
        char_uuid = service_char['uuid']
        print("Characteristic uuid: {}".format(char_uuid))
        char_type = service_char['type']
        print("Characteristic type: {}".format(char_type))
        print("Value: {}".format(get_value(value_range[0], value_range[1])))

def get_value(start, end):
    return random.randrange(start, end)

load_command()
# service = DiscoveryService()
# devices = service.discover(2)

# for address, name in devices.items():
#     print("name: {}, address: {}".format(name, address))