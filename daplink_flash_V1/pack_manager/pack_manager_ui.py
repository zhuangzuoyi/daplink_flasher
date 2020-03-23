# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pack_manager_ui.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PackManager(object):
    def setupUi(self, PackManager):
        PackManager.setObjectName("PackManager")
        PackManager.resize(850, 700)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(PackManager)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(PackManager)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.vendor_list = QtWidgets.QComboBox(PackManager)
        self.vendor_list.setObjectName("vendor_list")
        self.horizontalLayout.addWidget(self.vendor_list)
        self.label_2 = QtWidgets.QLabel(PackManager)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.device_list = QtWidgets.QComboBox(PackManager)
        self.device_list.setObjectName("device_list")
        self.horizontalLayout.addWidget(self.device_list)
        self.device_fileter = QtWidgets.QLineEdit(PackManager)
        self.device_fileter.setObjectName("device_fileter")
        self.horizontalLayout.addWidget(self.device_fileter)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton = QtWidgets.QPushButton(PackManager)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(PackManager)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(PackManager)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_2.addWidget(self.pushButton_3)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.tableWidget = QtWidgets.QTableWidget(PackManager)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget)
        self.log = QtWidgets.QTextBrowser(PackManager)
        self.log.setObjectName("log")
        self.verticalLayout.addWidget(self.log)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(PackManager)
        QtCore.QMetaObject.connectSlotsByName(PackManager)

    def retranslateUi(self, PackManager):
        _translate = QtCore.QCoreApplication.translate
        PackManager.setWindowTitle(_translate("PackManager", "Dialog"))
        self.label.setText(_translate("PackManager", "Vendor"))
        self.label_2.setText(_translate("PackManager", "Device"))
        self.pushButton.setText(_translate("PackManager", "PushButton"))
        self.pushButton_2.setText(_translate("PackManager", "PushButton"))
        self.pushButton_3.setText(_translate("PackManager", "PushButton"))
