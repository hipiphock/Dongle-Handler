# Task is an element for each taskRoutine to have for

class Task:
    def __init__(self, cluster, command, payloads, duration):
        self.cluster = cluster
        self.command = command
        self.payloads = payloads
        self.duration = duration

    @classmethod
    def make_instance(cls, configfile):
        pass