#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
# from pyocd.target.pack import pack_target ManagedPacks
from PyQt5.QtWidgets import QApplication, QComboBox, QDialog, QVBoxLayout, QTableWidgetItem, QFileDialog, QMessageBox, QAbstractItemView
from PyQt5.QtCore import pyqtSignal, QThread, Qt
from PyQt5.QtGui import QIcon

from pack_manager_ui import *
from threading import Thread
import cmsis_pack_manager
import requests
import time
import sys
from appdirs import user_data_dir
from os.path import join, dirname, exists
from json import load
from pyocd.target.pack.pack_target import ManagedPacks

class Download_pack(QThread):
    signal = pyqtSignal(str)
    def __init__(self,url, path):
        # super().__init__()
        super(Download_pack, self).__init__()
        self.url = url
        self.path = path
    
    def __del__(self):
        self.wait()
    
    def run(self):
        self.downloader(self.url,self.path)

    def set_url(self,url):
        self.url = url
    
    def set_path(self,path):
        self.path = path


    def downloader(self, url, path):
        start = time.time()
        size = 0
        response = requests.get(url, stream=True)
        # print(response)
        chunk_size = 1024
        content_size = int(response.headers['content-length'])
        print(content_size)

        if response.status_code == 200:
            msg = "file's size is:{0:.2f}".format(
                content_size / chunk_size / 1024)
            print("msg is:%s" % msg)
            # self.ui.log.append(msg)
            self.signal.emit(msg)
            self.sleep(1)
            with open(path, "wb") as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    size += len(data)
                    # print('\r' + '下载进度：%s%.2f%%' % (">" * int(size * 50 /content_size), float(size / content_size * 100)), end="")
                    msg = '\r' + '下载进度：{}{:.2f}%%'.format(">" * int(size * 50 / content_size), float(size / content_size * 100))
                    print("msg is:%s" % msg)
                    # self.ui.log.append(msg)
                    self.signal.emit(msg)
                    self.sleep(5)
        end = time.time()
        print(end - start)



class Pack_Manager(object):

    def __init__(self):
        app = QApplication(sys.argv)
        self.window = QDialog()
        self.download_thread = Download_pack("http://www.keil.com/pack/Keil.LPC1700_DFP.2.6.0.pack", sys.path[0]+"/2.6.0.pack")
        self.download_thread.signal.connect(self.download_process)
        # www.keil.com/pack/Keil.LPC1700_DFP.2.6.0.pack
        self.ui = Ui_PackManager()
        self.ui.setupUi(self.window)
        print ("sys.path[0]=%s" % sys.path[0])
        self.ui.pushButton.clicked.connect(self.download_pack)
        self.installed_pack=[]
        packs = ManagedPacks.get_installed_packs()
        for pack in packs:
            self.installed_pack.append(pack.get_pack_name().split('\\')[1])
        # print(packs[0].get_pack_name())
        self.ui.device_list.currentIndexChanged.connect(self.device_change)
        self.ui.vendor_list.currentIndexChanged.connect(self.vendor_change)
        self.ui.device_fileter.textChanged.connect(self.device_filter)

        self.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tableWidget.clicked.connect(self.item_clicked)
        self.show_all_packs_in_table()
        self.window.show()
        app.exec_()
    
    def item_clicked(self):
        print("item clicked")
        print(self.ui.tableWidget.selectedItems()[0].text())
        self.get_pack_url(self.ui.tableWidget.selectedItems()[2].text(),self.ui.tableWidget.selectedItems()[3].text())


    def download_pack(self):
        print("down loading")
        self.download_thread.start()


    def download_process(self,msg):
        print("downloading...")

        self.ui.log.append(msg)

    def vendor_change(self):
        # print(self.ui.vendor_list.currentText())
        self.show_select_vendor_pack(self.ui.vendor_list.currentText())

    def device_change(self):
        # print(self.ui.device_list.currentText())
        self.show_select_device_pack(self.ui.device_list.currentText())
    
    def device_filter(self):
        filter = self.ui.device_fileter.text()
        self.ui.tableWidget.clear()
        i=0
        for index in self.all_index:
            if len(index['name']) > len(filter) and filter.lower() == index['name'][0:len(filter)].lower():
                item = QTableWidgetItem(index["name"])
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget.setItem(i, 0, item)

                item = QTableWidgetItem(index["vendor"].split(':')[0])
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget.setItem(i, 1, item)

                item = QTableWidgetItem(index["from_pack"]["pack"])
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget.setItem(i, 2, item)

                item = QTableWidgetItem(index["from_pack"]["version"])
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget.setItem(i, 3, item)

                # self.ui.vendor_list.addItem(vendor)
                if index["from_pack"]["pack"] in self.installed_pack:
                    # print("%s installed" % index["from_pack"]["pack"])
                    item = QTableWidgetItem(QIcon("./img/circle-check-3x.png"),"")
                else:
                    item = QTableWidgetItem(QIcon("./img/circle-x-3x.png"),"")

                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget.setItem(i, 4, item)


                self.ui.device_list.addItem(index["name"])
                i = i+1


    def get_pack_url(self,pack,version):
        json_path = user_data_dir('cmsis-pack-manager')
        index_path = join(json_path, "index.json")
        with open(index_path) as i:
            index = load(i)
            for pack_index in index:
                if pack == index[pack_index]["from_pack"]['pack']  and  version == index[pack_index]["from_pack"]['version']:
                    print(index[pack_index]["from_pack"]['url'] + index[pack_index]["from_pack"]['vendor'] + '.' +  index[pack_index]["from_pack"]['pack'] + '.' + index[pack_index]["from_pack"]['version'] + ".pack")
                # print("\r\n\r\n")
    def show_all_packs_in_table(self):
        json_path = user_data_dir('cmsis-pack-manager')
        index_path = join(json_path, "index.json")

        self.all_index = []
        self.all_devices = []
        self.all_vendor = []
        self.all_vendor.append("*")

        self.all_devices.append("*")
        # aliases_path = join(json_path, "aliases.json")
        self.ui.tableWidget.setColumnCount(5)
        self.ui.tableWidget.setHorizontalHeaderLabels(["Device", "Manufacturter",  "pack", "version", "status"])
        with open(index_path) as i:
            index = load(i)
            print(len(index))
            self.ui.tableWidget.setRowCount(len(index))
            i=0
            for pack_index in index:

                self.all_index.append(index[pack_index])

                item = QTableWidgetItem(pack_index)
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget.setItem(i, 0, item)

                item = QTableWidgetItem(index[pack_index]["vendor"].split(':')[0])
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget.setItem(i, 1, item)

                item = QTableWidgetItem(index[pack_index]["from_pack"]["pack"])
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget.setItem(i, 2, item)

                item = QTableWidgetItem(index[pack_index]["from_pack"]["version"])
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget.setItem(i, 3, item)


                # self.ui.vendor_list.addItem(vendor)
                if index[pack_index]["from_pack"]["pack"] in self.installed_pack:
                    # print("%s installed" % index["from_pack"]["pack"])
                    item = QTableWidgetItem(QIcon("./img/circle-check-3x.png"),"")
                else:
                    item = QTableWidgetItem(QIcon("./img/circle-x-3x.png"),"")

                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget.setItem(i, 4, item)


                if index[pack_index]["vendor"].split(':')[0] in self.all_vendor:
                    pass
                else:
                    self.all_vendor.append(
                        index[pack_index]["vendor"].split(':')[0])
                
                if pack_index in self.all_devices:
                    pass
                else:
                    self.all_devices.append(pack_index)
                i = i+1

        for pack in self.all_vendor:
            self.ui.vendor_list.addItem(pack)
        
        for device in self.all_devices:
            self.ui.device_list.addItem(device)

    def show_select_vendor_pack(self,vendor):

        i = 0
        # self.ui.vendor_list.clear()
        self.ui.device_list.clear()
        self.ui.tableWidget.clear()
        for index in self.all_index:
            if vendor != "*":
                if index["vendor"].split(':')[0] == vendor:
                    # print(vendor)
                    item = QTableWidgetItem(index["name"])
                    item.setTextAlignment(Qt.AlignCenter)
                    self.ui.tableWidget.setItem(i, 0, item)

                    item = QTableWidgetItem(index["vendor"].split(':')[0])
                    item.setTextAlignment(Qt.AlignCenter)
                    self.ui.tableWidget.setItem(i, 1, item)

                    item = QTableWidgetItem(index["from_pack"]["pack"])
                    item.setTextAlignment(Qt.AlignCenter)
                    self.ui.tableWidget.setItem(i, 2, item)

                    item = QTableWidgetItem(index["from_pack"]["version"])
                    item.setTextAlignment(Qt.AlignCenter)
                    self.ui.tableWidget.setItem(i, 3, item)

                    # self.ui.vendor_list.addItem(vendor)

                    self.ui.device_list.addItem(index["name"])


                    # self.ui.vendor_list.addItem(vendor)
                    if index["from_pack"]["pack"] in self.installed_pack:
                        # print("%s installed" % index["from_pack"]["pack"])
                        item = QTableWidgetItem(QIcon("./img/circle-check-3x.png"),"")
                    else:
                        item = QTableWidgetItem(QIcon("./img/circle-x-3x.png"),"")

                    item.setTextAlignment(Qt.AlignCenter)
                    self.ui.tableWidget.setItem(i, 4, item)


                    i = i+1
            else:
                item = QTableWidgetItem(index["name"])
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget.setItem(i, 0, item)

                item = QTableWidgetItem(index["vendor"].split(':')[0])
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget.setItem(i, 1, item)

                item = QTableWidgetItem(index["from_pack"]["pack"])
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget.setItem(i, 2, item)

                item = QTableWidgetItem(index["from_pack"]["version"])
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget.setItem(i, 3, item)

                self.ui.device_list.addItem(index["name"])

                # self.ui.vendor_list.addItem(vendor)
                if index["from_pack"]["pack"] in self.installed_pack:
                    # print("%s installed" % index["from_pack"]["pack"])
                    item = QTableWidgetItem(QIcon("./img/circle-check-3x.png"),"")
                else:
                    item = QTableWidgetItem(QIcon("./img/circle-x-3x.png"),"")

                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget.setItem(i, 4, item)
                i = i+1
    def show_select_device_pack(self,device):
        i = 0
        # self.ui.vendor_list.clear()
        # self.ui.device_list.clear()
        self.ui.tableWidget.clear()
        for index in self.all_index:
            if index["name"] == device:
                item = QTableWidgetItem(index["name"])
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget.setItem(i, 0, item)

                item = QTableWidgetItem(index["vendor"].split(':')[0])
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget.setItem(i, 1, item)

                item = QTableWidgetItem(index["from_pack"]["pack"])
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget.setItem(i, 2, item)

                item = QTableWidgetItem(index["from_pack"]["version"])
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget.setItem(i, 3, item)

                # self.ui.vendor_list.addItem(vendor)
                # self.ui.vendor_list.addItem(vendor)
                if index["from_pack"]["pack"] in self.installed_pack:
                    # print("%s installed" % index["from_pack"]["pack"])
                    item = QTableWidgetItem(QIcon("./img/circle-check-3x.png"),"")
                else:
                    item = QTableWidgetItem(QIcon("./img/circle-x-3x.png"),"")

                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget.setItem(i, 4, item)
                # self.ui.device_list.addItem(index["name"])
                i = i+1

if __name__ == '__main__':
    Pack_Manager()
