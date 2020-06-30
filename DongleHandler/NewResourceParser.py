# new resource parser
import json
from DongleHandler import *

def parse_commands(file_name):
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
            attribute = 0
            task = Task(cluster, command, attribute, payloads, duration)
            task_list.append(task)
    return task_list