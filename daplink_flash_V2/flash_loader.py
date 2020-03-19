#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
from pyocd.core.helpers import ConnectHelper
from pyocd.target.builtin import BUILTIN_TARGETS
# from pyocd.target.pack import pack_target ManagedPacks
from pyocd.target.pack.pack_target import ManagedPacks
from PyQt5.QtWidgets import QApplication, QComboBox, QWidget, QVBoxLayout, QTableWidgetItem, QFileDialog, QMessageBox
from flash_loaer_ui import *
import pyocd.core
from pyocd.core.memory_map import MemoryType
import cmsis_pack_manager
from pyocd.target.pack.cmsis_pack import (CmsisPack, MalformedCmsisPackError)
from pyocd.flash.file_programmer import FileProgrammer


class Flash_Loader(object):

    def __init__(self):
        app = QApplication(sys.argv)
        self.window = QWidget()

        self.ui = Ui_Form()
        self.ui.setupUi(self.window)
        self.cache = cmsis_pack_manager.Cache(True, True)
        managedpack = ManagedPacks()
        self.packs = ManagedPacks().get_installed_packs()
        vendors =[]
        current_packs=[]
        self.current_targets=[]

        # show all vendor in ui
        # for pack in self.packs:
        #     if pack.vendor in vendors:
        #         pass
        #     else:
        #         vendors.append(pack.vendor)

        for pack in self.packs:
            pack_path = os.path.join(self.cache.data_path, pack.get_pack_name())
            pack_temp = CmsisPack(pack_path)
            if len(pack_temp.devices) > 0:
                target_vendor = pack_temp.devices[0].vendor
            else:
                continue

            if target_vendor in vendors:
                pass
            else:
                vendors.append(target_vendor)

        for vendor in vendors:
            self.ui.vendor_list.addItem(vendor)

        # show the first vendor's all device in ui in vendor list 
        # for pack in self.packs:
        #     # print("%s| *%s|" %(pack.vendor,ui.vendor_list.currentText()))
        #     if pack.vendor == self.ui.vendor_list.currentText():
        #         current_packs.append(pack)
        #         # print("fix")
        for pack in self.packs:
            pack_path = os.path.join(self.cache.data_path, pack.get_pack_name())
            pack_temp = CmsisPack(pack_path)
            if len(pack_temp.devices) > 0:
                target_vendor = pack_temp.devices[0].vendor
            else:
                continue
            if target_vendor == self.ui.vendor_list.currentText():
                current_packs.append(pack)

        # print(ui.vendor_list.currentText())            
        for current_pack in current_packs:
            # print(type(current_pack))
            pack_path = os.path.join(self.cache.data_path, current_pack.get_pack_name())
            # print(pack_path)
            pack = CmsisPack(pack_path)
            for device in pack.devices:
                self.current_targets.append(device)
        # print(current_targets)    
        for target in self.current_targets:
            self.ui.device_list.addItem(target.part_number)

        probes = ConnectHelper.get_all_connected_probes(blocking=False)
        for probe in probes:
            self.ui.daplink_list.addItem(probe.description)
        if len(probes) > 0:
            self.probe = probes[0]
            print(self.probe)
        else:
            self.probe = None
        

        self.ui.vendor_list.currentTextChanged.connect(self.vendor_change)
        self.ui.device_list.currentIndexChanged.connect(self.device_change)

        self.ui.erase.clicked.connect(self.erase_device)
        self.ui.flash.clicked.connect(self.flash_device)
        self.ui.update_dap.clicked.connect(self.update_daplink)
        self.ui.connect.clicked.connect(self.open_session)
        self.ui.selsec_firmware.clicked.connect(self.select_file)
        self.ui.daplink_list.currentIndexChanged.connect(self.daplink_change)
        self.ui.erase.setDisabled(True)
        self.ui.flash.setDisabled(True)
        self.device_change()
        self.window.show()
        app.exec_()

    def get_targets_in_vendor(self,vendor):
        select_vendor_packs=[]
        self.current_targets.clear()

        # print("get targets in vendor:%s" % vendor)
        for pack in self.packs:
            pack_path = os.path.join(self.cache.data_path, pack.get_pack_name())
            pack_temp = CmsisPack(pack_path)
            if len(pack_temp.devices) > 0:
                target_vendor = pack_temp.devices[0].vendor
            else:
                continue
            if target_vendor == vendor:
                select_vendor_packs.append(pack)
        # print(select_vendor_packs)
        for current_pack in select_vendor_packs:
            # print(type(current_pack))
            pack_path = os.path.join(self.cache.data_path, current_pack.get_pack_name())
            # print(pack_path)
            pack = CmsisPack(pack_path)
            for device in pack.devices:
                self.current_targets.append(device)
        # print(current_targets)
        self.ui.device_list.clear()
        for target in self.current_targets:
            self.ui.device_list.addItem(target.part_number)


    def daplink_change(self):
        # print("daplink change")
        probes = ConnectHelper.get_all_connected_probes(blocking=False)

        for probe in probes:
            if probe.description == self.ui.daplink_list.currentText():
                self.probe = probe
            else:
                self.probe = None
    def open_session(self):
        # print("open session")
        if self.probe is None:
            QMessageBox.information(self.window, "ERROR", "No probe",  QMessageBox.Ok)
            return

        if self.ui.device_list.currentText() is "":
            QMessageBox.information(self.window, "ERROR", "select mcu first",  QMessageBox.Ok)
            return

        self.session = ConnectHelper.session_with_chosen_probe(
            target_override=self.ui.device_list.currentText(),unique_id=self.probe.unique_id)
        self.session.open()

        # print(self.probe.unique_id)
        board = self.session.board
        # print("Board's name:%s" % board.name)
        # print("Board's description:%s" % board.description)
        # print("Board's target_type:%s" % board.target_type)
        # print("Board's unique_id:%s" % board.unique_id)
        # print("Board's test_binary:%s" % board.test_binary)
        # print("Unique ID: %s" % board.unique_id)
        

        memory_map = board.target.get_memory_map()
        ram_region = memory_map.get_default_region_of_type(MemoryType.RAM)
        rom_region = memory_map.get_boot_memory()

        self.addr_bin = rom_region.start
        self.ui.erase.setEnabled(True)
        self.ui.flash.setEnabled(True)

# 如果厂商变了，就把mcu列表改为相应厂商的mcu
    def vendor_change(self):
        self.get_targets_in_vendor(self.ui.vendor_list.currentText())

        
    def device_change(self):
        # print("device change")
        print("In device change slot current device is:%s" %self.ui.device_list.currentText())
        for device in self.current_targets:
            if device.part_number == self.ui.device_list.currentText():
                self.active_device = device
        # print(self.active_device.memory_map)
        device_msg = self.ui.vendor_list.currentText() + "  " + self.active_device.part_number + ":  "
        for region in self.active_device.memory_map.regions:
            le = region.length/1024
            no = str(le).split('.')[0] + "K"
            if region.type == MemoryType.FLASH:
                device_msg = device_msg + "    flash"  + ":" + no + "  "
            elif region.type == MemoryType.RAM:
                device_msg = device_msg + "    ram"  + ":  " + no + "  "
        self.ui.log.clear()
        self.ui.log.append(device_msg)

    def flash_device(self):
        print("flash device")
        if os.path.exists(self.ui.filepath.text()):
            self.ui.log.append("Start flashing")
            FileProgrammer(self.session, progress=self.progress_monitor).program(self.ui.filepath.text(), base_address=self.addr_bin)
            self.ui.log.append("Finish flashing")
        else:
            QMessageBox.critical(self.window,"ERROR","Firmware is not exist",QMessageBox.Yes)
            # QMessageBox.critical
    def progress_monitor(self, amount):
        print("progress")
        print(amount)
        self.ui.progressBar.setValue(amount * 100)

    def erase_device(self):
        print("erase flash")

    def update_daplink(self):
        self.ui.daplink_list.clear()
        probes = ConnectHelper.get_all_connected_probes(blocking=False)

        for probe in probes:
            self.ui.daplink_list.addItem(probe.description)
        if len(probes) > 0:
            self.probe = probes[0]
        else:
            self.probe = None
    
    def select_file(self):
        filepath, filetype = QFileDialog.getOpenFileName(
            self.window, "open fireware", "./", "hex(*.hex);;bin(*.bin);;")
        # print(fname)
        self.ui.filepath.setText(filepath)



if __name__ == '__main__':
    # probes = ConnectHelper.get_all_connected_probes()
    Flash_Loader()
    # app = QApplication(sys.argv)
    # window = QWidget()

    # ui = Ui_Form()
    # ui.setupUi(window)
    # cache = cmsis_pack_manager.Cache(True, True)
    # managedpack = ManagedPacks()
    # packs = ManagedPacks().get_installed_packs()
    # vendors =[]
    # current_packs=[]
    # current_targets=[]

    # for pack in packs:
    #     # print(pack.vendor)
    #     if pack.vendor in vendors:
    #         pass
    #     else:
    #         vendors.append(pack.vendor)
    # for vendor in vendors:
    #     ui.vendor_list.addItem(vendor)

    # for pack in packs:
    #     # print("%s| *%s|" %(pack.vendor,ui.vendor_list.currentText()))
    #     if pack.vendor == ui.vendor_list.currentText():
    #         current_packs.append(pack)
    #         print("fix")
    # # print(ui.vendor_list.currentText())            
    # for current_pack in current_packs:
    #     # print(type(current_pack))
    #     pack_path = os.path.join(cache.data_path, current_pack.get_pack_name())
    #     print(pack_path)
    #     pack = CmsisPack(pack_path)
    #     current_targets.append(pack.devices)
    # print(current_targets)    
    # for targets in current_targets:
    #     # ui.device_list.addItem(target.)    
    #     for target in targets:
    #         ui.device_list.addItem(target.part_number)
    # window.show()
    # app.exec_()
