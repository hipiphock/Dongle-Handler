import enum

# maps cluster value into 
# which function does it is concerned with
class Service:
    OnOff = 0x0006
    Level = 0x0008
    Color = 0x0300

# Each config should be one Zigbee command,
# since each Zigbee command is a transaction
class ZigbeeCommand:
    def __init__(self, uuid, service, characteristic, value):
        self.uuid = uuid
        self.service = Service(service)
        self.characteristic = characteristic
        self.value = value
    