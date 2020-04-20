import enum

# maps cluster value into 
# which function does it is concerned with
class Cluster(enum.Enum):
    OnOff = 0x0006
    Level = 0x0008
    Color = 0x0300

# Each config should be one Zigbee command,
# since each Zigbee command is a transaction
class ZigbeeCommand:
    def __init__(self, address, cluster, command, payloads):
        self.address = address
        self.cluster = Cluster(cluster)
        self.command = command
        self.payloads = payloads
    