import enum
from zb_cli_wrapper.zb_cli_dev import ZbCliDevice

# maps cluster value into 
# which function does it is concerned with
class Cluster:
    def __init__(self, clusterid):
        # OnOff = 0x0006
        # Level = 0x0008
        # Color = 0x0300
        self.clusterid = clusterid
    
    # On & Off Cluster
    class OnOff:
        def __init__(self, commandid):
            super().__init__()
            self.commandid = commandid
            # 0x00  = Off
            # 0x01  = On

    # Controls the brightness of the light
    class LevelControl:
        def __init__(self, commandid, payloads):
            super().__init__()
            self.commandid = commandid
            self.payloads = payloads
            # 0x00  = Move to level
            # 0x01  = Move
            # 0x02  = Step
            # 0x03  = Stop
            # 0x04  = Move to Level (with On/Off)
            # 0x05  = Move (with On/Off)
            # 0x06  = Step (with On/Off)
            # 0x07  = Stop (with On/Off)
    
    # Controls the temperature
    class ColorControl:
        def __init__(self, commandid, payloads):
            super().__init__()
            self.commandid = commandid
            self.payloads = payloads


# Each config should be one Zigbee command,
# since each Zigbee command is a transaction
class ZigbeeCommand:
    def __init__(self, address, cluster, command, payloads):
        self.address = address
        self.cluster = Cluster(cluster)
        self.command = command
        self.payloads = payloads