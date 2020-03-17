# BLE handler
IoT 장치에게 BLE 통신을 할 때, 정해진 command를 내리는 프로그램

주어진 json 파일을 이용하여서 명령을 내린다.

``` shell
$ python3 command.py command.json
```

이때, command.json은 다음과 같은 형식을 가진다.

``` json
{
    "command":[
        "config1.json", 
        "config2.json", 
        "config3.json", 
        "config4.json", 
        "config5.json", 
        "config6.json", 
        "config7.json", 
        "config8.json", 
        "config9.json", 
        "config10.json"
    ]
}
```

json 안에 들어가는 config.json의 경우 다음과 같은 형식을 가진다.

``` json
{
    "Device":"Ultra Thin Wafer",
    "uuid": "qwer-asdf-zxcv",
    "connection":"BLE",
    "service":{
        "uuid": "4cc49cc9-bde6-4b43-8c51-93785dd7873e",
        "characteristics":{
            "uuid":"qwer-asdf-zxcv",
            "type":"write",
            "value":"0x0001"
        }
    }
}
```

통신을 하려는 device의 정보(이름과 uuid)와 통신하는 방식을 정의한 후, 원하는 service와 해당 service의 characteristic 중 하나에 대해서 대해서 상세하게 서술한다.

해당 characteristic의 type이 read인지, write인지, notify인지에 따라서 value를 보낼 것인지 받을 것인지가 달라진다.

# Todo:
Pybluez와 같은 library를 사용해서 command set을 쓴다.