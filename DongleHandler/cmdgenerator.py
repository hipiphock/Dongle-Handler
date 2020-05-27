import json

# cmd_list:
# [
#   [[cmd1, cmd2, cmd3], iter1],
#   [[cmd1, cmd2, cmd3], iter2],
#   [[cmd1, cmd2, cmd3], iter3],
# ]
def make_json_command(file_name, device_name, device_uuid, device_addr, device_ep, cmd_list):
    data = {}
    data['Device']      = device_name
    data['uuid']        = device_uuid
    data['address']     = device_addr
    data['ep']          = device_ep
    data['command_list']= []
    for cmd in cmd_list:
        data['command_list'].append(cmd)
    with open(file_name, 'w') as outfile:
        json.dump(data, outfile)

def make_json_config(file_name, connection, command, payloads, duration):
    data = {}
    data['connection']      = connection
    data['command']         = command
    data['payloads']        = payloads
    data['duration']        = duration
    with open(file_name, 'w') as outfile:
        json.dump(data, outfile)