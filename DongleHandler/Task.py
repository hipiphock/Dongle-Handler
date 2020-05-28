# Task is an element for each taskRoutine to have for

class Task:
    def __init__(self, cluster, command, payloads):
        self.cluster = cluster
        self.command = command
        self.payloads = payloads

    @classmethod
    def make_instance(cls, configfile):
        pass

    # def do_one_task(self, cli_instance):
    #     if self.payloads == None:
    #         cli_instance.zcl.generic()