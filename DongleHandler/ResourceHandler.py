123# new resource parser
import random
import json
from DongleHandler import *

# generate json task list file
# TODO: generate 
def generate_task_list_json(file_name, num_tasks):
    commands = {}
    commands['commands'] = []
    for i in range(num_tasks):
        # select cluster, command, and attribute(optional)
        # attribute is selected only on read/write attribute command
        task_kind = int(input("Task Kind: "))
        cluster = int(input("Cluster: "))
        # command
        if task_kind == COMMAND_TASK:
            command = int(input("Command: "))
            cmd_task = Cmd.generate_random_cmd(cluster, command, 0.51)
            cmd_str = cmd_task.task_to_string()
            commands['commands'].append(cmd_str)
            # TODO: automatically add read attribute task for logging and certifying command
            # get attribute id, type
            attr_list = cmd_task.get_changed_attr_list()
            for attr in attr_list:
                read_attr = ReadAttr(cluster, attr.id, attr.type, 0.51)
                read_attr_str = ReadAttr.task_to_string()
                commands['commands'].append(read_attr_str)
        elif task_kind == READ_ATTRIBUTE_TASK:
            attr_id = int(input("Attribute: "))
            read_attr = ReadAttr(cluster, attr_id, 0.51)
            read_attr_str = ReadAttr.task_to_string()
            commands['commands'].append(read_attr_str)
        elif task_kind == WRITE_ATTRIBUTE_TASK:
            attr_id = input()
            write_attr = WriteAttr(cluster, attr_id, 0.51)
            write_attr_str = WriteAttr.task_to_string()
            commands['commands'].append(read_attr_str)
    with open(file_name, 'w') as outfile:
        json.dump(commands, outfile)

# parsing device file
def parse_json_device(file_name):
    with open(file_name) as device_file:
        content = json.load(device_file)
        name    = content['name']
        uuid    = int(content['uuid'], 16)
        eui64   = int(content['eui64'], 16)
        ep      = content['ep']
        return Device(name, uuid, eui64, ep)

def parse_task_list(file_name):
    task_list = []
    duration = 0.5
    with open(file_name) as command_file:
        content = json.load(command_file)
        command_list = content['commands']
        for command_str in command_list:
            parsed_command = json.loads(command_str)
            cluster = int(parsed_command['cluster'], 16)
            command = int(parsed_command['command'], 16)
            _payloads = parsed_command['payloads']
            if _payloads == "None":
                payloads = None
            else:
                payloads   = [(_payloads[0][0], int(_payloads[0][1], 16)), (_payloads[1][0], int(_payloads[1][1], 16))]
                if payloads[1][0] != 0:
                    duration = payloads[1][0]*0.1
            attr_id = int(parsed_command['attr_id'], 16)
            attr_type = int(parsed_command['attr_type'], 16)
            task = Task(cluster, command, payloads, attr_id, attr_type, duration)
            task_list.append(task)
    return task_list


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