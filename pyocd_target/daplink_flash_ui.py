# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'flash_loader_ui.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(300, 469)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.daplink_list = QtWidgets.QComboBox(Form)
        self.daplink_list.setObjectName("daplink_list")
        self.horizontalLayout_7.addWidget(self.daplink_list)
        self.update_dap = QtWidgets.QPushButton(Form)
        self.update_dap.setObjectName("update_dap")
        self.horizontalLayout_7.addWidget(self.update_dap)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.filepath = QtWidgets.QLineEdit(Form)
        self.filepath.setObjectName("filepath")
        self.horizontalLayout_5.addWidget(self.filepath)
        self.selsec_firmware = QtWidgets.QPushButton(Form)
        self.selsec_firmware.setObjectName("selsec_firmware")
        self.horizontalLayout_5.addWidget(self.selsec_firmware)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.connect = QtWidgets.QPushButton(Form)
        self.connect.setObjectName("connect")
        self.horizontalLayout_6.addWidget(self.connect)
        self.flash = QtWidgets.QPushButton(Form)
        self.flash.setObjectName("flash")
        self.horizontalLayout_6.addWidget(self.flash)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.verticalLayout.addLayout(self.horizontalLayout_8)
        self.progressBar = QtWidgets.QProgressBar(Form)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        self.log = QtWidgets.QTextBrowser(Form)
        self.log.setObjectName("log")
        self.verticalLayout.addWidget(self.log)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "DapLink flash"))
        self.update_dap.setText(_translate("Form", "更新设备"))
        self.selsec_firmware.setText(_translate("Form", "打开固件"))
        self.connect.setText(_translate("Form", "connect"))
        self.flash.setText(_translate("Form", "flash"))
