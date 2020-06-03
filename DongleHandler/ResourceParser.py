import json

def make_json_device(file_name, device_name, device_uuid, device_eui64, device_ep):
    data = {}
    data['name']        = device_name
    data['uuid']        = device_uuid
    data['eui64']       = device_eui64
    data['ep']          = device_ep
    with open(file_name, 'w') as outfile:
        json.dump(data, outfile)

def make_json_task_routine(file_name, task_list):
    pass

# def make_json_command(file_name, device_name, device_uuid, device_addr, device_ep, cmd_list):
#     data = {}
#     data['Device']      = device_name
#     data['uuid']        = device_uuid
#     data['address']     = device_addr
#     data['ep']          = device_ep
#     data['command_list']= []
#     for cmd in cmd_list:
#         data['command_list'].append(cmd)
#     with open(file_name, 'w') as outfile:
#         json.dump(data, outfile)

def make_json_command(file_name, cluster, command, payloads, duration):
    data = {}
    data['cluster']         = cluster
    data['command']         = command
    data['payloads']        = payloads
    data['duration']        = duration
    with open(file_name, 'w') as outfile:
        json.dump(data, outfile)