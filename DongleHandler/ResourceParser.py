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
        uuid    = content['uuid']
        eui64   = content['eui64']
        ep      = content['ep']
        return Device(name, uuid, eui64, ep)

# parsing task routine file
def parse_json_task_routine(file_name):
    with open(file_name) as task_routine_file:
        content = json.load(task_routine_file)
        task_list   = content['task_list']
        iteration   = content['iteration']
        return task_list, iteration

# parsing command file
def parse_json_command(file_name):
    with open(file_name) as command_file:
        content = json.load(command_file)
        cluster    = content['cluster']
        command    = content['command']
        payloads   = content['payloads']
        duration   = content['duration']
        return Task(cluster, command, payloads, duration)