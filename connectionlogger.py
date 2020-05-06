# BLE & Zigbee log generator
import logging
import json

# Output file format is json, with sequence of command and results
# Each array index has:
# - index number(command sequence)
# - command that has been sent
# - value returned from the Wafer

class ConnectionLogger:
    def __init__(self, idx, command, retval):
        self.idx = idx
        self.command = command
        self.retval = retval
    
    def write_log(self):
        data = {}
        data.append({
            'iteration': self.idx,
            'command': self.command,
            'result': self.retval
        })
        with open("log.json", "w+") as outputfile:
            json.dump(data, outputfile)
    
    