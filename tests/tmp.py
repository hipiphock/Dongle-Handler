from context import DongleHandler
from DongleHandler import *

if __name__ == "__main__":
# Test for reading OnOffStranion nag
    with open('DongleHandler\\..\\resource\\dongle_status.json', "r") as dongle_file:
        dongle_config = json.load(dongle_file)
        port = dongle_config['port']
        status = dongle_config['status']
        dongle_file.close()
    time.sleep(3)
    cli_instance = ZbCliDevice('', '', port)
    if status == 0:
        cli_instance.bdb.channel = [24]
        cli_instance.bdb.role = 'zr'
        cli_instance.bdb.start()
        with open('DongleHandler\\..\\resource\\dongle_status.json', "w") as dongle_file:
            dongle_config['status'] = 1
            json.dump(dongle_config, dongle_file)
            dongle_file.close()
        print("The dongle has started commissioning.")
        print("Please search for the dongle via SmartThings App within 5 seconds.")
        time.sleep(5.0)
    device = parse_json_device('DongleHandler\\..\\resource\\device\\Ultra Thin Wafer.json')
    attr_cluster = LVL_CTRL_CLUSTER
    attr_id = LVL_CTRL_ONOFF_TRANS_TIME_ATTR
    attr_type = TYPES.UINT16
    attr = Attribute(attr_cluster, attr_id, attr_type)
    ret_attr = cli_instance.zcl.readattr(device.addr, attr, ep=ULTRA_THIN_WAFER_ENDPOINT)
    print(ret_attr)