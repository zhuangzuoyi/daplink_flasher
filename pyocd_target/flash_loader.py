#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
from pyocd.core.helpers import ConnectHelper
from pyocd.target.builtin import BUILTIN_TARGETS
# from pyocd.target.pack import pack_target ManagedPacks
from pyocd.target.pack.pack_target import ManagedPacks
from PyQt5.QtWidgets import QApplication, QComboBox, QWidget, QVBoxLayout, QTableWidgetItem, QFileDialog, QMessageBox
from daplink_flash_ui import *
import pyocd.core
from pyocd.core.memory_map import MemoryType
# import cmsis_pack_manager
from pyocd.target.pack.cmsis_pack import (CmsisPack, MalformedCmsisPackError)
from pyocd.flash.file_programmer import FileProgrammer
import logging
from pyocd.target import TARGET

class Flash_Loader(object):

    def __init__(self):
        app = QApplication(sys.argv)
        self.window = QWidget()

        self.ui = Ui_Form()
        self.ui.setupUi(self.window)
        self.session = None


        probes = ConnectHelper.get_all_connected_probes(blocking=False)
        for probe in probes:
            self.ui.daplink_list.addItem(probe.description)
        if len(probes) > 0:
            self.probe = probes[0]
            # print(self.probe)
        else:
            self.probe = None
        

        # logger = logging.getLogger(__name__)
        # logger.setLevel(level=logging.DEBUG)

        # StreamHandler
        # stream_handler = logging.StreamHandler(self.ui.log.append)
        # stream_handler.setLevel(level=logging.DEBUG)
        # logger.addHandler(stream_handler)

        self.ui.flash.clicked.connect(self.flash_device_run)
        self.ui.update_dap.clicked.connect(self.update_daplink)
        self.ui.connect.clicked.connect(self.open_session)
        self.ui.selsec_firmware.clicked.connect(self.select_file)
        self.ui.daplink_list.currentIndexChanged.connect(self.daplink_change)

        self.ui.flash.setDisabled(True)
        self.ui.progressBar.setValue(0)
        self.window.show()
        app.exec_()


    def daplink_change(self):
        probes = ConnectHelper.get_all_connected_probes(blocking=False)

        for probe in probes:
            if probe.description == self.ui.daplink_list.currentText():
                self.probe = probe
            else:
                self.probe = None
    def open_session(self):
        if self.session is not None and  self.session.is_open:
            self.session.close()

        if self.probe is None:
            QMessageBox.information(self.window, "ERROR", "No probe",  QMessageBox.Ok)
            return

        target_device = "stm32f103c8"

        if target_device  not in TARGET:
            QMessageBox.information(self.window, "ERROR", "MCU not supported",  QMessageBox.Ok)
            return

        self.session = ConnectHelper.session_with_chosen_probe(
            target_override=target_device,unique_id=self.probe.unique_id)
        self.session.open()

        # print(self.probe.unique_id)
        board = self.session.board
        self.target = board.target

        memory_map = board.target.get_memory_map()
        ram_region = memory_map.get_default_region_of_type(MemoryType.RAM)
        rom_region = memory_map.get_boot_memory()

        self.addr_bin = rom_region.start
        self.ui.flash.setEnabled(True)

    def flash_device(self):
        print("flash device")
        if os.path.exists(self.ui.filepath.text()):
            self.ui.log.append("Start flashing")
            FileProgrammer(self.session, progress=self.progress_monitor).program(self.ui.filepath.text(), base_address=self.addr_bin)
            self.ui.log.append("Finish flashing")
        else:
            QMessageBox.critical(self.window,"ERROR","Firmware is not exist",QMessageBox.Yes)


    def flash_device_run(self):

        if os.path.exists(self.ui.filepath.text()):
            self.ui.log.append("Start flashing")
            FileProgrammer(self.session, progress=self.progress_monitor).program(
                self.ui.filepath.text(), base_address=self.addr_bin)
            self.ui.log.append("Finish flashing")
            self.target.reset()
        else:
            QMessageBox.critical(self.window,"ERROR","Firmware is not exist",QMessageBox.Yes)
        


    def progress_monitor(self, amount):
        print("progress")
        print(amount)
        self.ui.progressBar.setValue(amount * 100)



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
    Flash_Loader()

