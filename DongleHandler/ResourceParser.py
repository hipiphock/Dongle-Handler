import json
from DongleHandler import *

# generating device file
def make_json_device(file_name, device_name, device_uuid, device_eui64, device_ep):
    data = {}
    data['name']        = device_name
    data['uuid']        = device_uuid
    data['eui64']       = device_eui64
    data['ep']          = device_ep
    with open(file_name, 'w') as outfile:
        json.dump(data, outfile)

# generating command file
def make_json_command(file_name, cluster, command, payloads, duration):
    data = {}
    data['cluster']         = cluster
    data['command']         = command
    data['payloads']        = payloads
    data['duration']        = duration
    with open(file_name, 'w') as outfile:
        json.dump(data, outfile)

# parsing device file
def parse_json_device(file_name):
    with open(file_name) as device_file:
        content = json.load(device_file)
        name    = content['name']
        uuid    = int(content['uuid'], 16)
        eui64   = int(content['eui64'], 16)
        ep      = content['ep']
        return Device(name, uuid, eui64, ep)

# parsing task routine file
def parse_json_task_routine(file_name):
    with open(file_name) as task_routine_file:
        content = json.load(task_routine_file)
        _device     = content['device']
        connection  = content['connection']
        _task_list  = content['task_list']
        iteration   = content['iteration']
        device = parse_json_device(_device)
        task_list = []
        for _task in _task_list:
            task = parse_json_command(_task)
            task_list.append(task)
        return TaskRoutine(device, connection, task_list, iteration)

# parsing command file
# TODO: deal with payloads
def parse_json_command(file_name):
    duration = 0.5
    with open(file_name) as command_file:
        content = json.load(command_file)
        cluster    = int(content['cluster'], 16)
        command    = int(content['command'], 16)
        _payloads  = content['payloads']
        if _payloads == "None":
            payloads = None
        else:
            payloads   = [(_payloads[0][0], int(_payloads[0][1], 16)), (_payloads[1][0], int(_payloads[1][1], 16))]
            if payloads[1][0] != 0:
                duration = payloads[1][0]*0.1
    return Task(cluster, command, payloads, duration)