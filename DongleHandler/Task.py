# Task is an element for each task routine
# TODO: add readattr command
import random
from DongleHandler.Constants import *

# There are two types of tasks:
# 1. Task that just sends commnad
# 2. Task that reads attribute from the device
# 3. Task that writes attribute to the device
class Task:
    def __init__(self, task_kind, cluster, duration):
        self.task_kind  = task_kind     # 0=commmand, 1=read_attr, 2=write_attr
        self.cluster    = cluster
        self.duration   = duration
    
    def task_to_string(self):
        pass

def duration_control(payload):
    duration = max(0.1*payload[1][1] + 0.01, 0.51)
    return duration

class Cmd(Task):
    def __init__(self, cluster, command, payloads, duration):
        super().__init__(cluster, COMMAND_TASK, duration)
        self.command    = command
        self.payloads   = payloads
    # additional method for payload generation needed

    @classmethod
    def generate_random_cmd(cls, cluster, command, duration):
        payloads = None
        if cluster == SCENE_CLUSTER:
            if command == SCENE_ADD_SCENE_CMD:
                group_id = 0
                scene_id = 0
                trans_time = 0
                scene_name = "str"
                var = {1, 2, 3} # ZCL Spec p137
                payloads = [(group_id, TYPES.UINT16), (scene_id, TYPES.UINT8), (trans_time, TYPES.UINT16), (scene_name, TYPES.STRING), ()]
            
            elif command == SCENE_VEIW_SCENE_CMD or command == SCENE_REMOVE_SCENE_CMD:
                group_id = 0
                scene_id = 0
                payloads = [(group_id, TYPES.UINT16), (scene_id, TYPES.UINT8)]

        elif cluster == ON_OFF_CLUSTER:
            payloads = None

        elif cluster == LVL_CTRL_CLUSTER:
            if command == LVL_CTRL_MV_TO_LVL_CMD or command == LVL_CTRL_MV_TO_LVL_ONOFF_CMD:
                level = random.randint(0x00, 0xfe)
                trans_time = random.randint(0x0000, 0x0014)
                payloads = [(level, TYPES.UINT8), (trans_time, TYPES.UINT16)]

            elif command == LVL_CTRL_MOVE_CMD:
                mv_mode = 8
                rate = 8
                payloads = [(mv_mode, TYPES.ENUM8), (rate, TYPES.UINT8)]

            elif command == LVL_CTRL_STEP_CMD or command == LVL_CTRL_STEP_ONOFF_CMD:
                step_mode = 0
                step_size = 0
                trans_time = random.randint(0x0000, 0x0014)
                payloads = [(step_mode, TYPES.ENUM8), (step_size, TYPES.UINT8), (trans_time, TYPES.UINT16)]
            
            elif command == LVL_CTRL_STOP_CMD or command == LVL_CTRL_STOP_ONOFF_CMD:
                payloads = None

        elif cluster == COLOR_CTRL_CLUSTER:
            if command == COLOR_CTRL_MV_TO_COLOR_CMD:
                randval1 = random.randint(0x0000, 0xfeff)
                randval2 = random.randint(0x0000, 0xfeff)
                randval3 = random.randint(0x0000, 0xfeff)
                payloads = [(randval1, TYPES.UINT16), (randval2, TYPES.UINT16), (randval3, TYPES.UINT16)]
            
            elif command == COLOR_CTRL_MOVE_COLOR_CMD:
                randval1 = random.randint(0x0000, 0xfeff)
                randval2 = random.randint(0x0000, 0xfeff)
                payloads = [(randval1, TYPES.UINT16), (randval2, TYPES.UINT16)]

            elif command == COLOR_CTRL_STEP_COLOR_CMD:
                randval1 = random.randint(0x0000, 0xfeff)
                randval2 = random.randint(0x0000, 0xfeff)
                randval3 = random.randint(0x0000, 0xfeff)
                payloads = [(randval1, TYPES.UINT16), (randval2, TYPES.UINT16), (randval3, TYPES.UINT16)]

            elif command == COLOR_CTRL_MV_TO_COLOR_TEMP_CMD:
                randval1 = random.randint(0x0000, 0xfeff)
                randval2 = random.randint(0x0000, 0xfeff)
                payloads = [(randval1, TYPES.UINT16), (randval2, TYPES.UINT16)]
            
            elif command == COLOR_CTRL_STOP_MOVE_STEP_CMD:
                payloads = None

            elif command == COLOR_CTRL_MV_COLOR_TEMP_CMD:
                randval1 = 0
                randval2 = random.randint(0x0000, 0xfeff)
                randval3 = random.randint(0x0000, 0xfeff)
                randval4 = random.randint(0x0000, 0xfeff)
                payloads = [(randval1, TYPES.MAP8), (randval2, TYPES.UINT16), (randval3, TYPES.UINT16), (randval4, TYPES.UINT16)]
            
            elif command == CLOLR_CTRL_STEP_COLOR_TEMP_CMD:
                payloads = None
        
        return Cmd(cluster, command, payloads, duration)

    def get_changed_attr_list(self):
        attr_list = []
        if self.cluster == ON_OFF_CLUSTER:
            pass
        elif self.cluster == LVL_CTRL_CLUSTER:
            pass
        elif self.cluster == COLOR_CTRL_CLUSTER:
            pass
        return attr_list
    
    def task_to_string(self):
        super().task_to_string()
        ret_str =   '{\"task_kind\": \"'+ str(self.task_kind)\
            +   '", \"command\": \"'    + str(self.command)\
            +   '", \"payloads\": \"'   + str(self.payloads)\
            +   '", \"duration\": \"'   + str(self.duration)\
            +   '}'
        return ret_str

class ReadAttr(Task):
    def __init__(self, cluster, attr_id, duration):
        super().__init__(READ_ATTRIBUTE_TASK, cluster, duration)
        self.attr_id = attr_id
        # automated procedure to get 
        attr_type = 0
        if cluster == SCENE_CLUSTER:
            if attr_id == SCENE_SCENE_COUNT_ATTR:
                attr_type = TYPES.UINT8
            elif attr_id == SCENE_CURRENT_SCENE_ATTR:
                attr_type = TYPES.UINT8
            elif attr_id == SCENE_CURRENT_GROUP_ATTR:
                attr_type = TYPES.UINT16
            elif attr_id == SCENE_SCENE_VALID_ATTR:
                attr_type = TYPES.BOOL
            elif attr_id == SCENE_NAME_SUPPORT_ATTR:
                attr_type = TYPES.MAP8

        elif cluster == ON_OFF_CLUSTER:
            attr_type = TYPES.BOOL
        
        elif cluster == LVL_CTRL_CLUSTER:
            if attr_id == LVL_CTRL_CURR_LVL_ATTR:
                attr_type = TYPES.UINT8
            elif attr_id == LVL_CTRL_REMAIN_TIME_ATTR:
                attr_type = TYPES.UINT16
            elif attr_id == LVL_CTRL_ONOFF_TRANS_TIME_ATTR:
                attr_type = TYPES.UINT16
            elif attr_id == LVL_CTRL_ON_LEVEL_ATTR:
                attr_type = TYPES.UINT8
        
        elif cluster == COLOR_CTRL_CLUSTER:
            if attr_id == COLOR_CTRL_CURR_HUE_ATTR:
                attr_type = TYPES.UINT8
            elif attr_id == COLOR_CTRL_CURR_SAT_ATTR:
                attr_type = TYPES.UINT8
            elif attr_id == COLOR_CTRL_REMAINING_TIME_ATTR:
                attr_type = TYPES.UINT16
            elif attr_id == COLOR_CTRL_CURR_X_ATTR:
                attr_type = TYPES.UINT16
            elif attr_id == COLOR_CTRL_CURR_Y_ATTR:
                attr_type = TYPES.UINT16
            elif attr_id == COLOR_CTRL_COLOR_TEMP_MIRED_ATTR:
                attr_type = TYPES.UINT16
            elif attr_id == COLOR_CTRL_COLOR_MODE_ATTR:
                attr_type = TYPES.ENUM8
            elif attr_id == COLOR_CTRL_ENHANCED_COLOR_MODE_ATTR:
                attr_type = TYPES.ENUM8
            elif attr_id == COLOR_CTRL_COLOR_CAPABILITY_ATTR:
                attr_type = TYPES.MAP16
            elif attr_id == COLOR_CTRL_COLOR_TEMP_MIN_MIRED_ATTR:
                attr_type = TYPES.UINT16
            elif attr_id == COLOR_CTRL_COLOR_TEMP_MAX_MIRED_ATTR:
                attr_type = TYPES.UINT16

        self.attr_type  = attr_type

    def task_to_string(self):
        super().task_to_string()
        ret_str =   '{\"task_kind\": \"'+ self.task_kind\
            +   '", \"attr_id\": \"'    + self.attr_id\
            +   '", \"attr_type\": \"'  + self.attr_type\
            +   '", \"duration\": \"'   + self.duration\
            +   '}'
        return ret_str


class WriteAttr(Task):
    def __init__(self, cluster, attr_id, duration):
        super().__init__(WRITE_ATTRIBUTE_TASK, cluster, duration)
        self.attr_id    = attr_id
        self.attr_type  = attr_type

        def task_to_string(self):
            super().task_to_string()
            ret_str =   '{\"task_kind\": \"'+ self.task_kind\
                +   '", \"attr_id\": \"'    + self.attr_id\
                +   '", \"attr_type\": \"'  + self.attr_type\
                +   '", \"duration\": \"'   + self.duration\
                +   '}'
            return ret_str