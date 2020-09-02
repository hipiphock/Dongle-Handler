### BLE controller ###
# TODO:
# 1. The dongle should search for near device.
# 2. The dongle should establish connection with IoT device.
# 3. The dongle should send/receive services & characteristics.

import sys
import time
import logging
from queue import Queue, Empty

from pc_ble_driver_py import config
config.__conn_ic_id__ = "NRF52"
from pc_ble_driver_py.observers import *
from pc_ble_driver_py.ble_driver import(
    BLEDriver,
    BLEAdvData,
    BLEEvtID,
    BLEEnableParams,
    BLEGapTimeoutSrc,
    BLEUUID,
    BLEGapScanParams,
    BLEConfigCommon,
    BLEConfig,
    BLEConfigConnGatt,
)
from pc_ble_driver_py.ble_adapter import BLEAdapter

DEFAULT_MTU = 250
CFG_TAG     = 1

class BLEhandler(BLEDriverObserver, BLEAdapterObserver):
    def __init__(self, adapter):
        super(BLEhandler, self).__init__()
        self.adapter = adapter
        self.conn_q = Queue()
        self.adapter.observer_register(self)
        self.adapter.driver.observer_register(self)
        self.adapter.default_mtu = DEFAULT_MTU

    def open(self):
        self.adapter.driver.open()
        gatt_cfg = BLEConfigConnGatt()
        gatt_cfg.att_mtu = self.adapter.default_mtu
        gatt_cfg.tag = CFG_TAG
        self.adapter.driver.ble_cfg_set(BLEConfig.conn_gatt, gatt_cfg)

        self.adapter.driver.ble_enable()
    
    def close(self):
        self.adapter.driver.close()

    def connect_and_discover(self):
        scan_duration = 10
        params = BLEGapScanParams(interval_ms=200, window_ms=150, timeout_s=scan_duration)

        self.adapter.driver.ble_gap_scan_start(scan_params=params)

        try:
            new_conn = self.conn_q.get(timeout=scan_duration)
            self.adapter.service_discovery(new_conn)
            self.adapter.enable_notification(
                new_conn, BLEUUID(BLEUUID.Standard.battery_level)
            )
            return new_conn
        except Empty:
            print("Nothing found.")
            return None


if __name__ == "__main__":
    serial_port = "COM7"
    driver = BLEDriver(
        serial_port=serial_port,
        auto_flash=False,
        baud_rate=1000000,
        log_severity_level="info"
    )
    adapter = BLEAdapter(driver)
    ble_handler = BLEhandler(adapter)

    ble_handler.open()
    conn = ble_handler.connect_and_discover()
    print(conn)

    if conn is not None:
        time.sleep(10)

    ble_handler.close()