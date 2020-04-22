# MADE FOR TEST
import serial
import ZigbeeCommand
import BLECommand
from zb_cli_wrapper.zb_cli_dev import ZbCliDevice
from zb_cli_wrapper.src.utils.cmd_wrappers.zigbee.constants import *
from zb_cli_wrapper.src.utils.zigbee_classes.clusters.attribute import Attribute

# main routine for zigbee connection
def main():

    eui64 = 9824354097448244246

    # first, try to connect with dongle
    # try:
    cli_instance = ZbCliDevice('', '','COM13')    # COM port can be changed in accordance with your environment
    #     cli_instance.bdb.channel = 24
    #     cli_instance.bdb.role = 'zr'
    # except serial.serialutil.SerialException:
    #     print('Can not create CLI device')
    #     cli_instance.close_cli()
    #     return None

    # print("Created CLI device, trying to connect ...")
    # cli_instance.bdb.start()
    # print(cli_instance.wait_until_connected())

    # attribute = Attribute(ON_OFF_CLUSTER, 0, TYPES.BOOL, ON_OFF_OFF_CMD)
    # cli_instance.zcl.generic(eui64, 8, ON_OFF_CLUSTER, DEFAULT_ZIGBEE_PROFILE_ID, ON_OFF_OFF_CMD)
    # cli_instance.zcl.generic(eui64, 8, ON_OFF_CLUSTER, DEFAULT_ZIGBEE_PROFILE_ID, ON_OFF_ON_CMD)
    cli_instance.zcl.raw(eui64, 8, ON_OFF_CLUSTER, '0x00')


if __name__ == "__main__":
    main()