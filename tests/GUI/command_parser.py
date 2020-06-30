import json
from collections import OrderedDict
import re


def read_command_from_json(file_name):
    with open(file_name) as json_file:
        json_data = json.load(json_file)
        print(json_data["task_list"])


def make_command(list):
    print(list)
    file_data = OrderedDict()
    file_data["device"] = "DongleHandler\\..\\resource\\device\\Ultra Thin Wafer.json"
    file_data["connection"] = 0
    commands = []
    for item in list:
        data = re.split(", ", item)
        command = data[0]
        if command == "connect":
            print("connect")
        elif command == "on/off":
            value = data[1]
            iteration = int(data[2])
            print(type(value))
            if value == "0x1": # on
                for i in range(iteration):
                    commands.append( "DongleHandler\\..\\resource\\command\\Zigbee\\on.json")
            else:# off
                for i in range(iteration):
                    commands.append( "DongleHandler\\..\\resource\\command\\Zigbee\\off.json")
        elif command == "color":
            value = data[1]
            iteration = int(data[2])
            print(data[1])
        elif command == "level":
            value = data[1]
            iteration = int(data[2])
            print(data[1])
        elif command == "disconnect":
            print("disconnect")
    file_data["task_list"] = commands
    file_data["iteration"] = 0
    # print(json.dumps(file_data, ensure_ascii=False, indent="\t"))
    with open('command.json', 'w', encoding='utf-8') as make_file:
        json.dump(file_data, make_file, ensure_ascii=False, indent="\t")