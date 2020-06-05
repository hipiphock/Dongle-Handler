# Dongle handler
**nRF52840 dongle handler with BLE, Zigbee command functions**

The dongle handler is a python program that can send & receive BLE/Zigbee messages to devices that supports BLE/Zigbee connection.

# Build

# Design
The programmed dongle basically sends ZigBee/BLE commands to particular IoT device.

The program consists of three parts:
 * Device
 * Task
 * Task Routine

The Task Routine is the core structure of this project.

The program can do three things:
 * It can register & remove devices.
 * It can make & delete command tasks.
 * It can make task routines based on pre-defined devices & tasks.

The three of those properties are registerd via json files in /resource directory.

## Device
The device property consists of:
 * name
 * uuid (this is needed for BLE connection)
 * address (this is the eui64 address for ZigBee commission)
 * endpoint (another element for ZigBee commission)

The device's **name** represents the target device's name.

The device's **uuid** is needed for sending/receiving BLE services and characteristics.

The device's **address** and **endpoint** are for ZigBee commissioning.

## Task
Each task represents ZigBee/BLE task to send to target device.


## Making task routine
This is **the core** of this project. The Task Routine sends commands to the target device specified by **Device**, and receives the message from the target device. Then, it confirms whether the transmission was successfun and the device was OK or not.

# Example
This is the example for the device.
``` json
{
    "name"  :   "Ultra Thin Wafer",
    "uuid"  :   "0x8e89bed6",
    "eui64" :   "0xFFFE88571D018E53",
    "ep"    :   8
}
```

This is the example for a single ZigBee task.
``` json
{
    "cluster":      "0x0300",
    "command":      "0x0a",
    "payloads":     [[333, "0x21"], [0, "0x21"]],
    "duration":     0.5
}
```

And finally, this is the example for one task routine.
``` json
{
    "device"    :   "DongleHandler\\..\\resource\\device\\Ultra Thin Wafer.json",
    "connection":   0,
    "task_list" :   [
        "DongleHandler\\..\\resource\\command\\Zigbee\\off.json",
        "DongleHandler\\..\\resource\\command\\Zigbee\\on.json",
        "DongleHandler\\..\\resource\\command\\Zigbee\\level_100.json",
        "DongleHandler\\..\\resource\\command\\Zigbee\\level_50.json",
        "DongleHandler\\..\\resource\\command\\Zigbee\\level_10.json",
        "DongleHandler\\..\\resource\\command\\Zigbee\\color_dl.json",
        "DongleHandler\\..\\resource\\command\\Zigbee\\color_sw.json"
    ],
    "iteration" :   3
}
```

# Prerequisites
Check your device whether the device supports the dongle or not.
This project aims to nRF 52840 Dongle.

Not that if you confirmed that the program supports your device, make sure to program your dongle with **zigbee-cli-wrapper** by Nordic Semiconductors.

You can easily program your dongle with this [instruction](https://infocenter.nordicsemi.com/index.jsp?topic=%2Fsdk_tz_v4.0.0%2Fzigbee_cli_wrapper.html).

After installing the wrapper to your dongle,

``` shell
pip3 install zb-cli-wrapper
```

# Hardware Requirements
This program is made for nRF52840 dongle from Nordic Semiconductor.
Not only you need this dongle for execution, but also you must write the following hex file to your dongle.
When setthing the serial connection with dongle and PC:
 * 115200 bit/s,
 * 8-bit-long word,
 * no parity,
 * 1-bit stop.

would be required to be set.

# Future Goals & TODO lists
 * Unifying BLE CLI and Zigbee CLI.
 * Implementing the GUI for this python program.
