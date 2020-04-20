import enum

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

    # Controls the brightness of the light
    class LevelControl:
        def __init__(self, commandid, payloads):
            super().__init__()
            self.commandid = commandid
    
    # Controls the temperature
    class ColorControl:
        def __init__(self, commandid, payloads):
            super().__init__()
            self.commandid = commandid


# Each config should be one Zigbee command,
# since each Zigbee command is a transaction
class ZigbeeCommand:
    def __init__(self, address, cluster, command, payloads):
        self.address = address
        self.cluster = Cluster(cluster)
        self.command = command
        self.payloads = payloads
    