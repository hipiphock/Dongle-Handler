# # MADE FOR TEST
# import serial
# import ZigbeeCommand
# import BLECommand
# from zb_cli_wrapper.zb_cli_dev import ZbCliDevice

# # main routine for zigbee connection
# def main():
#     # first, try to connect with dongle
#     try:
#         cli_instance = ZbCliDevice('', '','COM13')    # COM port can be changed in accordance with your environment
#         cli_instance.bdb.channel = 15
#         cli_instance.bdb.role = 'zr'
#     except serial.serialutil.SerialException:
#         print('Can not create CLI device')
#         cli_instance.close_cli()
#         return None

#     print("Created CLI device, trying to connect ...")

#     cli_instance.bdb.start()

# if __name__ == "__main__":
#     main()