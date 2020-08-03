### BLE controller ###
# TODO:
# 1. The dongle should search for near device.
# 2. The dongle should establish connection with IoT device.
# 3. The dongle should send/receive services & characteristics.

from blatann import BleDevice
import threading

def detector(port):
    ble_device = BleDevice(port)
    ble_device.open()
    