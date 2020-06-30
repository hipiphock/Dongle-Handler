import random
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import QStandardItem
from PyQt5 import QtCore
from command_parser import *

from ..context import DongleHandler
from DongleHandler import *

#UI파일 연결 - UI파일은 Python 코드 파일과 같은 디렉토리에 위치
form_class = uic.loadUiType("resource\\mainwindow_tab.ui")[0]

command_model = QStandardItemModel()
process_model = QStandardItemModel()
result_model = QStandardItemModel()

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        #menu bar
        self.action_import_device.triggered.connect(self.import_device)
        self.action_import_command.triggered.connect(self.import_command)
        self.action_export_device.triggered.connect(self.export_device)
        self.action_export_command.triggered.connect(self.export_command)

        #main window
        self.btn_more.clicked.connect(self.click_more)
        self.btn_start.clicked.connect(self.click_start)

        self.btn_up.clicked.connect(self.click_item_up)
        self.btn_down.clicked.connect(self.click_item_down)
        self.btn_up.hide()
        self.btn_down.hide()
        self.listView_command.setDragDropMode(QAbstractItemView.InternalMove)
        self.listView_command.setDefaultDropAction(QtCore.Qt.CopyAction)
        self.listView_command.setSpacing(5)

        #single command tab
        self.cbo_input_onoff.currentIndexChanged.connect(self.select_onoff_input_style)
        self.cbo_input_color.currentIndexChanged.connect(self.select_color_input_style)
        self.cbo_input_level.currentIndexChanged.connect(self.select_level_input_style)
        self.btn_insert.clicked.connect(self.click_insert)

        #routine tab
        self.cbo_input_onoff_routine.currentIndexChanged.connect(self.select_onoff_routine_input_style)
        self.cbo_input_color_routine.currentIndexChanged.connect(self.select_color_routine_input_style)
        self.cbo_input_level_routine.currentIndexChanged.connect(self.select_level_routine_input_style)
        self.btn_insert_routine.clicked.connect(self.click_insert_routine)

    def click_item_up(self):
        item = self.listView_command.selectedIndexes()
        if item: #item != []
            row = item[0].row()
            column = item[0].column()
            print(item, "up", row, column)
            # command_model.beginMoveColumns(self, item[0].first(),item[0].last(), command_model.itemFromIndex(self, row-1),column)

    def click_item_down(self):
        item = self.listView_command.selectedIndexes()
        if item: #item != []
            row = item[0].row()
            print(item, "down", row)

    def import_command(self):
        print("import command")
        file_name = QFileDialog.getOpenFileName(self, 'Open file', './')
        if file_name[0]:
            read_command_from_json(file_name[0])

    def import_device(self):
        print("import device")
        file_name = QFileDialog.getOpenFileName(self, 'Open file', './')
        if file_name[0]:
            with open(file_name[0]) as json_file:
                json_data = json.load(json_file)
                self.lineEdit_device_name.setText(json_data["name"])
                self.lineEdit_device_uuid.setText(json_data["uuid"])
                self.lineEdit_device_addr.setText(json_data["eui64"])
                self.lineEdit_device_ep.setText(json_data["ep"])

    def export_device(self):
        print("export device")
        name = self.lineEdit_device_name.text()
        uuid = self.lineEdit_device_uuid.text()
        addr = self.lineEdit_device_addr.text()
        ep = self.lineEdit_device_ep.text()
        if name != "" and uuid != "" and addr != "" and ep != "":
            device_data = OrderedDict()
            device_data["name"] = name
            device_data["uuid"] = uuid
            device_data["eui64"] = addr
            device_data["ep"] = ep
            with open('device.json', 'w', encoding='utf-8') as make_file:
                json.dump(device_data, make_file, ensure_ascii=False, indent="\t")
        else:
            print("device info not exist")
            QMessageBox.about(self, "fail making json", "장치 정보가 입력되지 않았습니다.")

    def export_command(self):
        print("\nexport command")
        count = command_model.rowCount()
        if count != 0:
            list = []
            for index in range(command_model.rowCount()):
                item = command_model.item(index).text()
                list.append(item)
            make_command(list)
        else:
            print("command not exist")
            QMessageBox.about(self, "fail making json", "커맨드가 입력되지 않았습니다.")

    def add_command(self, command_string):
        command_model.appendRow(QStandardItem(command_string))
        self.listView_command.setModel(command_model)

    def select_onoff_input_style(self):
        index = self.cbo_input_onoff.currentIndex()
        if index == 0:
            self.rdo_on.show()
            self.rdo_off.show()
            self.rdo_toggle.show()
        elif index == 1:
            self.rdo_on.hide()
            self.rdo_off.hide()
            self.rdo_toggle.hide()
        elif index == 2:
            self.rdo_on.hide()
            self.rdo_off.hide()
            self.rdo_toggle.hide()
        else:
            self.rdo_on.hide()
            self.rdo_off.hide()
            self.rdo_toggle.hide()

    def select_onoff_routine_input_style(self):
        index = self.cbo_input_onoff_routine.currentIndex()
        if index == 0:
            self.rdo_on_routine.show()
            self.rdo_off_routine.show()
            self.rdo_toggle_routine.show()
        elif index == 1:
            self.rdo_on_routine.hide()
            self.rdo_off_routine.hide()
            self.rdo_toggle_routine.hide()
        elif index == 2:
            self.rdo_on_routine.hide()
            self.rdo_off_routine.hide()
            self.rdo_toggle_routine.hide()
        else:
            self.rdo_on_routine.hide()
            self.rdo_off_routine.hide()
            self.rdo_toggle_routine.hide()

    def select_color_input_style(self):
        index = self.cbo_input_color.currentIndex()
        if index == 0:
            self.lineEdit_color.show()
        elif index == 1:
            self.lineEdit_color.hide()
        elif index == 2:
            self.lineEdit_color.hide()
        else:
            self.lineEdit_color.hide()

    def select_color_routine_input_style(self):
        index = self.cbo_input_color_routine.currentIndex()
        if index == 0:
            self.lineEdit_color_routine.show()
        elif index == 1:
            self.lineEdit_color_routine.hide()
        elif index == 2:
            self.lineEdit_color_routine.hide()
        else:
            self.lineEdit_color_routine.hide()

    def select_level_input_style(self):
        index = self.cbo_input_level.currentIndex()
        if index == 0:
            self.lineEdit_level.show()
        elif index == 1:
            self.lineEdit_level.hide()
        elif index == 2:
            self.lineEdit_level.hide()
        else:
            self.lineEdit_level.hide()

    def select_level_routine_input_style(self):
        index = self.cbo_input_level_routine.currentIndex()
        if index == 0:
            self.lineEdit_level_routine.show()
        elif index == 1:
            self.lineEdit_level_routine.hide()
        elif index == 2:
            self.lineEdit_level_routine.hide()
        else:
            self.lineEdit_level_routine.hide()

    def click_insert(self):
        print("btn_insert Clicked")
        module_type = self.cbo_module.currentIndex()
        if module_type == 0: #Zigbee HA
            command_type = self.tab_single.currentIndex()
            if command_type == 0:  # connect
                item = "connect"
                self.add_command(item)
            elif command_type == 1:  # on/off
                onoff_input_type = self.cbo_input_onoff.currentIndex()
                onoff_count = self.spinBox_onoff.value()
                if onoff_input_type == 0:  # self input
                    if self.rdo_on.isChecked():
                        item = "on/off, "+hex(0x01)+", " + str(onoff_count)
                        self.add_command(item)
                    elif self.rdo_off.isChecked():
                        item = "on/off, "+hex(0x00)+", " + str(onoff_count)
                        self.add_command(item)
                    elif self.rdo_toggle.isChecked():
                        item = "on/off, toggle, 빠질 예정 "+ str(onoff_count)
                        # self.add_command(item)
                    else:
                        print("insert nothing")
                elif onoff_input_type == 1:  # regular random
                    temp = random.randint(0x00, 0x01)
                    item = "on/off, " + hex(temp) + ", " + str(onoff_count)
                    self.add_command(item)
                elif onoff_input_type == 2:  # irregular random
                    temp = random.randint(0x00, 0x01)
                    item = "on/off, " + hex(temp) + ", " + str(onoff_count)
                    self.add_command(item)
                else:  # random
                    temp = random.randint(0x00, 0x01)
                    item = "on/off, " + hex(temp) + ", " + str(onoff_count)
                    self.add_command(item)
            elif command_type == 2:  # color
                color_input_type = self.cbo_input_color.currentIndex()
                color_count = self.spinBox_color.value()
                if color_input_type == 0:  # self input
                    temp = self.lineEdit_color.text()
                    if "0x" in temp:
                        item = "color, " + temp + ", " + str(color_count)
                        self.add_command(item)
                    elif temp.isdigit:
                        temp = int(temp)
                        item = "color, " + hex(temp) + ", " + str(color_count)
                        self.add_command(item)
                    print(temp)
                elif color_input_type == 1:  # regular random
                    temp = random.randint(200, 370)
                    item = "color, " + hex(temp) + ", " + str(color_count)
                    self.add_command(item)
                elif color_input_type == 2:  # irregular random
                    temp = random.randint(0x0000, 0xfeff) + 0xff00
                    item = "color, " + hex(temp) + ", " + str(color_count)
                    self.add_command(item)
                else:
                    temp = random.randint(200, 370) if random.randint(0, 1) == 0 else random.randint(0x0000,
                                                                                                     0xfeff) + 0xff00
                    item = "color, " + hex(temp) + ", " + str(color_count)
                    self.add_command(item)
            elif command_type == 3:  # level
                level_input_type = self.cbo_input_color.currentIndex()
                level_count = self.spinBox_level.value()
                if level_input_type == 0:  # self input
                    temp = self.lineEdit_level.text()
                    if "0x" in temp:
                        item = "level, " + temp + ", " + str(level_count)
                        self.add_command(item)
                    elif temp.isdigit:
                        temp = int(temp)
                        item = "level, " + hex(temp) + ", " + str(level_count)
                        self.add_command(item)
                elif level_input_type == 1:  # regular random
                    temp = random.randint(0x00, 0xfe)
                    item = "level, " + hex(temp) + ", " + str(level_count)
                    self.add_command(item)
                elif level_input_type == 2:  # irregular random
                    temp = random.randint(0x00, 0xfe) + 0xff
                    item = "level, " + hex(temp) + ", " + str(level_count)
                    self.add_command(item)
                else:
                    temp = random.randint(0x00, 0xfe) if random.randint(0, 1) == 0 else random.randint(0x00,
                                                                                                       0xfe) + 0xff
                    item = "level, " + hex(temp) + ", " + str(level_count)
                    self.add_command(item)
            else:  # disconnect
                item = "disconnect"
                self.add_command(item)
        # elif type == 1: #Zigbee 3.0
        # elif type == 2: #BLE
        # else: #UART

    def click_insert_routine(self):
        print("btn_insert_routine Clicked")
        module_type = self.cbo_module.currentIndex()
        if module_type == 0: #Zigbee HA
            order = self.cbo_routine.currentIndex()
            item_connect = "connect"
            item_disconnect = "disconnect"
            item_onoff = ""
            item_color = ""
            item_level = ""

            onoff_input_type = self.cbo_input_onoff_routine.currentIndex()
            onoff_routine_count = self.spinBox_onoff_routine.value()
            if onoff_routine_count != 0:
                if onoff_input_type == 0:  # self input
                    if self.rdo_on_routine.isChecked():
                        item_onoff = "on/off, " + hex(0x01) + ", " + str(onoff_routine_count)
                    elif self.rdo_off_routine.isChecked():
                        item_onoff = "on/off, " + hex(0x00) + ", " + str(onoff_routine_count)
                    elif self.rdo_toggle_routine.isChecked():
                        item_onoff = "on/off, toggle, 빠질 예정 " + str(onoff_routine_count)
                    else:
                        print("insert nothing")
                elif onoff_input_type == 1:  # regular random
                    temp = random.randint(0x00, 0x01)
                    item_onoff = "on/off, " + hex(temp) + ", " + str(onoff_routine_count)
                elif onoff_input_type == 2:  # irregular random
                    temp = random.randint(0x00, 0x01)
                    item_onoff = "on/off, " + hex(temp) + ", " + str(onoff_routine_count)
                else:  # random
                    temp = random.randint(0x00, 0x01)
                    item_onoff = "on/off, " + hex(temp) + ", " + str(onoff_routine_count)
            else:
                print("no onoff")


            color_input_type = self.cbo_input_color_routine.currentIndex()
            color_routine_count = self.spinBox_color_routine.value()
            if color_routine_count != 0:
                if color_input_type == 0:  # self input
                    temp = self.lineEdit_color_routine.text()
                    if "0x" in temp:
                        item_color = "color, " + temp + ", " + str(color_routine_count)
                    elif temp.isdigit:
                        temp = int(temp)
                        item_color = "color, " + hex(temp) + ", " + str(color_routine_count)
                elif color_input_type == 1:  # regular random
                    temp = random.randint(200, 370)
                    item_color = "color, " + hex(temp) + ", " + str(color_routine_count)
                elif color_input_type == 2:  # irregular random
                    temp = random.randint(0x0000, 0xfeff) + 0xff00
                    item_color = "color, " + hex(temp) + ", " + str(color_routine_count)
                else:
                    temp = random.randint(200, 370) if random.randint(0, 1) == 0 else random.randint(0x0000,
                                                                                                     0xfeff) + 0xff00
                    item_color = "color, " + hex(temp) + ", " + str(color_routine_count)
            else:
                print("no color")

            level_input_type = self.cbo_input_color_routine.currentIndex()
            level_routine_count = self.spinBox_level_routine.value()
            if level_routine_count != 0:
                if level_input_type == 0:  # self input
                    temp = self.lineEdit_level_routine.text()
                    if "0x" in temp:
                        item_level = "level, " + temp + ", " + str(level_routine_count)
                    elif temp.isdigit:
                        temp = int(temp)
                        item_level = "level, " + hex(temp) + ", " + str(level_routine_count)
                elif level_input_type == 1:  # regular random
                    temp = random.randint(0x00, 0xfe)
                    item_level = "level, " + hex(temp) + ", " + str(level_routine_count)
                elif level_input_type == 2:  # irregular random
                    temp = random.randint(0x00, 0xfe) + 0xff
                    item_level = "level, " + hex(temp) + ", " + str(level_routine_count)
                else:
                    temp = random.randint(0x00, 0xfe) if random.randint(0, 1) == 0 else random.randint(0x00,
                                                                                                       0xfe) + 0xff
                    item_level = "level, " + hex(temp) + ", " + str(level_routine_count)
            else:
                print("no level")

            print(item_color, item_level)
            for i in range(self.spinBox_routine.value()):
                self.add_command(item_connect)
                if order == 0:  # connect-onoff-color-level-disconnect
                    if item_onoff != "":
                        self.add_command(item_onoff)
                    if item_color != "":
                        self.add_command(item_color)
                    if item_level != "":
                        self.add_command(item_level)
                elif order == 1:  # connect-onoff-level-color-disconnect
                    if item_onoff != "":
                        self.add_command(item_onoff)
                    if item_level != "":
                        self.add_command(item_level)
                    if item_color != "":
                        self.add_command(item_color)
                elif order == 2:  # connect-color-onoff-level-disconnect
                    if item_color != "":
                        self.add_command(item_color)
                    if item_onoff != "":
                        self.add_command(item_onoff)
                    if item_level != "":
                        self.add_command(item_level)
                elif order == 3:  # connect-level-onoff-color-disconnect
                    if item_level != "":
                        self.add_command(item_level)
                    if item_onoff != "":
                        self.add_command(item_onoff)
                    if item_color != "":
                        self.add_command(item_color)
                elif order == 4:  # connect-color-level-onoff-disconnect
                    if item_color != "":
                        self.add_command(item_color)
                    if item_level != "":
                        self.add_command(item_level)
                    if item_onoff != "":
                        self.add_command(item_onoff)
                else:  # connect-level-color-onoff-disconnect
                    if item_level != "":
                        self.add_command(item_level)
                    if item_color != "":
                        self.add_command(item_color)
                    if item_onoff != "":
                        self.add_command(item_onoff)
                self.add_command(item_disconnect)

        # elif module_type == 1: #Zigbee 3.0
        # elif module_type == 2: #BLE
        # else: #UART

    def click_more(self):
        print("btn_more Clicked")

    def click_start(self):
        print("btn_start Clicked")


if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass()

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
