# new resource parser
import random
import json
from DongleHandler import *

# generate json task list file
# TODO: generate 
def generate_task_list_json(file_name, num_tasks):
    tasks = {}
    tasks['tasks'] = []
    for i in range(num_tasks):
        # select cluster, command, and attribute(optional)
        task_kind   =   int(input("Task Kind: "))
        cluster     =   int(input("Cluster: "))
        if task_kind == COMMAND_TASK:
            command =   int(input("Command: "))
            cmd_task = Cmd.generate_random_cmd(cluster, command, 0.51)
            cmd_str = cmd_task.task_to_string()
            tasks['tasks'].append(cmd_str)
            # TODO: automatically add read attribute task for logging and certifying command
            # get attribute id, type
            attr_list = cmd_task.get_dependent_attr_list()
            for attr in attr_list:
                read_attr = ReadAttr(cluster, attr, 0.51)
                read_attr_str = read_attr.task_to_string()
                tasks['tasks'].append(read_attr_str)

        elif task_kind == READ_ATTRIBUTE_TASK:
            attr_id =   int(input("Attribute: "))
            read_attr = ReadAttr(cluster, attr_id, 0.51)
            read_attr_str = read_attr.task_to_string()
            tasks['tasks'].append(read_attr_str)

        elif task_kind == WRITE_ATTRIBUTE_TASK:
            attr_id = int(input("Attribute: "))
            write_attr = WriteAttr(cluster, attr_id, 0.51)
            write_attr_str = write_attr.task_to_string()
            tasks['tasks'].append(read_attr_str)
    with open(file_name, 'w') as outfile:
        json.dump(tasks, outfile)

# parsing device file
def parse_json_device(file_name):
    with open(file_name) as device_file:
        content = json.load(device_file)
        name    = content['name']
        uuid    = int(content['uuid'], 16)
        eui64   = int(content['eui64'], 16)
        ep      = content['ep']
        return Device(name, uuid, eui64, ep)

# parse task lists
def parse_task_list(file_name):
    task_list = []
    with open(file_name) as task_file:
        content = json.load(task_file)
        json_task_list = content['tasks']
        for task in json_task_list:
            parsed_task = json.loads(task)
            task_kind = parsed_task['task_kind']
            cluster = parsed_task['cluster']
            duration = parsed_task['duration']
            if task_kind == COMMAND_TASK:
                command = parsed_task['command']
                payloads = parsed_task['payloads']
                cmd_task = Cmd(cluster, command, payloads, duration)
                task_list.append(cmd_task)
            elif task_kind == READ_ATTRIBUTE_TASK:
                attr_id = parsed_task['attr_id']
                read_attr_task = ReadAttr(cluster, attr_id, duration)
                task_list.append(read_attr_task)
            elif task_kind == WRITE_ATTRIBUTE_TASK:
                attr_id = parsed_task['attr_id']
                write_attr_task = WriteAttr(cluster, attr_id, duration)
                task_list.append(write_attr_task)
            # else:
            #     payloads   = [(_payloads[0][0], int(_payloads[0][1], 16)), (_payloads[1][0], int(_payloads[1][1], 16))]
            #     if payloads[1][0] != 0:
            #         duration = payloads[1][0]*0.1
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