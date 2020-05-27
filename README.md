# Dongle handler
**nRF52840 dongle handler with BLE, Zigbee command functions**

The dongle handler is a python program that sends and receives BLE/Zigbee messages to some appropriate devices.

It supports both batch mode and interactive mode.

# Build
So far, there is no need to build the program. You just need prerequistic libraries.
``` shell
pip3 install zb-cli-wrapper
pip3 install blatann
```

# Execution
## Batch Mode
To execute the program in batch mode, you need **command.json** file and a set of **./config/<CONNECTION_TYPE>/<COMMAND>.json** files.

The **command.json** file consists like this kind of form:
``` json
{
    "Device": "Ultra Thin Wafer",
    "uuid": "asdf-qwer-zxcv",
    "address": "0xe48f",
    "ep": "8",
    "command_list": [
        {
            "command": "./config/Zigbee/config_zigbee_onoff_on",
            "iteration": 1
        },
        {
            "command": "./config/Zigbee/config_zigbee_onoff_off",
            "iteration": 1
        }
    ]
}
```
It contains the target device's information, and a sequence of command list.

The **config.json** file consists like this kind of form:
``` json
{
    "connection": "Zigbee",
    "command": "LVL_CTRL_MV_TO_LVL_CMD",
    "payloads": [
        {
            "value": "0x05",
            "type": "TYPES.UINT8"
        },
        {
            "value": "0x00",
            "type": "TYPES.UINT16"
        }
    ],
    "duration": "2"
}
```
Each config.json files specifies the type of connection they are willing to connect, a specific command to send, and payloads if necessary.

통신을 하려는 device의 정보(이름과 uuid)와 통신하는 방식을 정의한 후, 원하는 service와 해당 service의 characteristic 중 하나에 대해서 대해서 상세하게 서술한다.

해당 characteristic의 type이 read인지, write인지, notify인지에 따라서 value를 보낼 것인지 받을 것인지가 달라진다.

## Interactive Mode
현재의 프로그램은 다음 명령어를 가지고 있다.
 * on
 * off
 * low
 * mid
 * high
 * quit

직접 쳐보면서 이게 무슨 명령어인지 파악해보자 :)

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
 * Updating BLE & Zigbee configuration files.
 * Unifying BLE CLI and Zigbee CLI.
 * Implementing the return fetching part.
 * Completing the light-color change part.
 * Implementing the GUI for this python program.
 * Implementing logger