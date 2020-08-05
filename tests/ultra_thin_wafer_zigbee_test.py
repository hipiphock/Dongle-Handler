from context import DongleHandler
from DongleHandler import *
import logging

# This is basic test on Ultra Thin Wafer by Samsung Electronics.
if __name__ == "__main__":

    # for logging
    logging.basicConfig(level=logging.DEBUG)

    # Device Initialization
    ultra_thin_wafer = Device("Ultra Thin Wafer", 0x8e89bed6, 0xFFFE88571D018E53, 8)

    # commands
    move_to_color_cmd = Cmd(COLOR_CTRL_CLUSTER, COLOR_CTRL_MV_TO_COLOR_CMD, [(0x31E9, TYPES.UINT16), (0x31E9, TYPES.UINT16), (0x0000, TYPES.UINT16)], 0)
    move_color_cmd = Cmd(COLOR_CTRL_CLUSTER, COLOR_CTRL_MOVE_COLOR_CMD, [(0X0001, TYPES.SINT16), (0X0001, TYPES.SINT16)], 1.01)
    read_color_x_attr = ReadAttr(COLOR_CTRL_CLUSTER, COLOR_CTRL_CURR_X_ATTR, 1.01)
    
    
    move_color_temp_cmd = Cmd(COLOR_CTRL_CLUSTER, COLOR_CTRL_MV_COLOR_TEMP_CMD, [(0x01, TYPES.MAP8), (0x0001, TYPES.UINT16), (0x00c8, TYPES.UINT16), (0x0172, TYPES.UINT16)], 1.01)
    # 00:stop 01:up 02:reserved 03:down
    # 0x00a5 이후론 바로 바뀜
    # 0x0001의 경우 시간이 대충 2분 45초 정도
    move_to_color_temp_cmd = Cmd(COLOR_CTRL_CLUSTER, COLOR_CTRL_MV_TO_COLOR_TEMP_CMD, [(0x00c8, TYPES.UINT16), (0x0000, TYPES.UINT16)], 0.51)

    # read attrs
    read_color_temp_attr = ReadAttr(COLOR_CTRL_CLUSTER, COLOR_CTRL_COLOR_TEMP_MIRED_ATTR, 1.01)

    # move commands 
    task_list = []
    task_list.append(move_to_color_cmd)
    task_list.append(move_color_cmd)
    

    simple_routine = TaskRoutine(ultra_thin_wafer, ZIGBEE_CONNECTION, task_list, 1)

    # start routine
    simple_routine.start_routine()