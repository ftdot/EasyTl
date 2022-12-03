# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'I:\Projects\Python\EasyTl\easytl-gui\ui\instanceSettingsWidget.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_instanceSettingsWidget(object):
    def setupUi(self, instanceSettingsWidget):
        instanceSettingsWidget.setObjectName("instanceSettingsWidget")
        instanceSettingsWidget.resize(650, 332)
        instanceSettingsWidget.setMinimumSize(QtCore.QSize(650, 332))
        instanceSettingsWidget.setMaximumSize(QtCore.QSize(650, 332))
        instanceSettingsWidget.setStyleSheet("")
        self.groupBox_2 = QtWidgets.QGroupBox(instanceSettingsWidget)
        self.groupBox_2.setGeometry(QtCore.QRect(190, 40, 211, 171))
        self.groupBox_2.setObjectName("groupBox_2")
        self.apiIdEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.apiIdEdit.setGeometry(QtCore.QRect(10, 50, 191, 20))
        self.apiIdEdit.setObjectName("apiIdEdit")
        self.apiHashEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.apiHashEdit.setGeometry(QtCore.QRect(10, 90, 191, 20))
        self.apiHashEdit.setObjectName("apiHashEdit")
        self.ownerIdEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.ownerIdEdit.setGeometry(QtCore.QRect(10, 130, 191, 20))
        self.ownerIdEdit.setClearButtonEnabled(False)
        self.ownerIdEdit.setObjectName("ownerIdEdit")
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setGeometry(QtCore.QRect(30, 34, 51, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setGeometry(QtCore.QRect(30, 74, 71, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setGeometry(QtCore.QRect(30, 114, 91, 16))
        self.label_3.setObjectName("label_3")
        self.runInstanceButton = QtWidgets.QPushButton(instanceSettingsWidget)
        self.runInstanceButton.setEnabled(True)
        self.runInstanceButton.setGeometry(QtCore.QRect(430, 230, 191, 31))
        self.runInstanceButton.setDefault(False)
        self.runInstanceButton.setFlat(False)
        self.runInstanceButton.setObjectName("runInstanceButton")
        self.groupBox = QtWidgets.QGroupBox(instanceSettingsWidget)
        self.groupBox.setGeometry(QtCore.QRect(420, 40, 211, 171))
        self.groupBox.setObjectName("groupBox")
        self.loggingLevelCB = QtWidgets.QComboBox(self.groupBox)
        self.loggingLevelCB.setGeometry(QtCore.QRect(10, 90, 191, 22))
        self.loggingLevelCB.setCurrentText("INFO")
        self.loggingLevelCB.setObjectName("loggingLevelCB")
        self.loggingLevelCB.addItem("")
        self.loggingLevelCB.setItemText(0, "INFO")
        self.loggingLevelCB.addItem("")
        self.loggingLevelCB.setItemText(1, "DEBUG")
        self.consoleLoggingLevelCB = QtWidgets.QComboBox(self.groupBox)
        self.consoleLoggingLevelCB.setGeometry(QtCore.QRect(10, 130, 191, 22))
        self.consoleLoggingLevelCB.setCurrentText("As logging level")
        self.consoleLoggingLevelCB.setObjectName("consoleLoggingLevelCB")
        self.consoleLoggingLevelCB.addItem("")
        self.consoleLoggingLevelCB.addItem("")
        self.consoleLoggingLevelCB.setItemText(1, "INFO")
        self.consoleLoggingLevelCB.addItem("")
        self.consoleLoggingLevelCB.setItemText(2, "DEBUG")
        self.enablePLAutoUpdateChB = QtWidgets.QCheckBox(self.groupBox)
        self.enablePLAutoUpdateChB.setGeometry(QtCore.QRect(10, 50, 191, 20))
        self.enablePLAutoUpdateChB.setObjectName("enablePLAutoUpdateChB")
        self.removeInstanceButton = QtWidgets.QPushButton(instanceSettingsWidget)
        self.removeInstanceButton.setGeometry(QtCore.QRect(200, 280, 191, 31))
        self.removeInstanceButton.setObjectName("removeInstanceButton")
        self.instancesList = QtWidgets.QListWidget(instanceSettingsWidget)
        self.instancesList.setEnabled(True)
        self.instancesList.setGeometry(QtCore.QRect(0, 0, 171, 331))
        self.instancesList.setMovement(QtWidgets.QListView.Static)
        self.instancesList.setLayoutMode(QtWidgets.QListView.SinglePass)
        self.instancesList.setViewMode(QtWidgets.QListView.ListMode)
        self.instancesList.setObjectName("instancesList")
        self.newInstanceButton = QtWidgets.QPushButton(instanceSettingsWidget)
        self.newInstanceButton.setGeometry(QtCore.QRect(200, 230, 191, 31))
        self.newInstanceButton.setObjectName("newInstanceButton")
        self.instanceName = QtWidgets.QLabel(instanceSettingsWidget)
        self.instanceName.setGeometry(QtCore.QRect(190, 10, 441, 21))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(-1)
        self.instanceName.setFont(font)
        self.instanceName.setStyleSheet("font-size: 16px;")
        self.instanceName.setObjectName("instanceName")
        self.saveSettingsButton = QtWidgets.QPushButton(instanceSettingsWidget)
        self.saveSettingsButton.setGeometry(QtCore.QRect(430, 280, 191, 31))
        self.saveSettingsButton.setObjectName("saveSettingsButton")

        self.retranslateUi(instanceSettingsWidget)
        QtCore.QMetaObject.connectSlotsByName(instanceSettingsWidget)

    def retranslateUi(self, instanceSettingsWidget):
        _translate = QtCore.QCoreApplication.translate
        instanceSettingsWidget.setWindowTitle(_translate("instanceSettingsWidget", "Form"))
        self.groupBox_2.setTitle(_translate("instanceSettingsWidget", "Settings"))
        self.apiIdEdit.setPlaceholderText(_translate("instanceSettingsWidget", "API ID"))
        self.apiHashEdit.setPlaceholderText(_translate("instanceSettingsWidget", "API HASH"))
        self.ownerIdEdit.setPlaceholderText(_translate("instanceSettingsWidget", "Your ID"))
        self.label.setText(_translate("instanceSettingsWidget", "API ID:"))
        self.label_2.setText(_translate("instanceSettingsWidget", "API HASH:"))
        self.label_3.setText(_translate("instanceSettingsWidget", "Your ID:"))
        self.runInstanceButton.setText(_translate("instanceSettingsWidget", "Run"))
        self.groupBox.setTitle(_translate("instanceSettingsWidget", "Advanced settings"))
        self.consoleLoggingLevelCB.setItemText(0, _translate("instanceSettingsWidget", "As logging level"))
        self.enablePLAutoUpdateChB.setText(_translate("instanceSettingsWidget", "Enable plugins Auto-Update"))
        self.removeInstanceButton.setText(_translate("instanceSettingsWidget", "Remove Instance"))
        self.newInstanceButton.setText(_translate("instanceSettingsWidget", "New instance"))
        self.instanceName.setText(_translate("instanceSettingsWidget", "No instance"))
        self.saveSettingsButton.setText(_translate("instanceSettingsWidget", "Save settings"))
