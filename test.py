# test
import sys
import json
import random
import serial
from zb_cli_wrapper.zb_cli_dev import ZbCliDevice
from zb_cli_wrapper.src.utils.cmd_wrappers.zigbee.constants import *

cli_instance = ZbCliDevice('','','COM13')
# cli_instance.bdb.channel = [24]
# cli_instance.bdb.role = 'zr'
# cli_instance.bdb.start()

# eui64 = int('f4ce362658dc0ce5', 16)
# eui64 = int('0xf4ce362658dc0ce5', 16)
eui64 = int('0x73b4', 16)
cli_instance.zcl.generic(eui64, 8, ON_OFF_CLUSTER, DEFAULT_ZIGBEE_PROFILE_ID, ON_OFF_OFF_CMD)
# cli_instance.zcl.generic(eui64, 8, ON_OFF_CLUSTER, DEFAULT_ZIGBEE_PROFILE_ID, ON_OFF_ON_CMD)