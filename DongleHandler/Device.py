# Defines each device with its characteristics.
class Device:
    def __init__(self, name, uuid, addr, ep):
        self.name = name
        self.uuid = uuid
        self.addr = addr
        self.ep   = ep

    @classmethod
    def make_instance(cls, device_file):
        pass