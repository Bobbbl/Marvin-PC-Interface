# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'marvin-tester.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(181, 163)
        self.horizontalLayoutWidget = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 120, 160, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_2 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.plainTextEdit_4 = QtWidgets.QPlainTextEdit(self.horizontalLayoutWidget)
        self.plainTextEdit_4.setObjectName("plainTextEdit_4")
        self.horizontalLayout.addWidget(self.plainTextEdit_4)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 70, 160, 31))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.plainTextEdit_3 = QtWidgets.QPlainTextEdit(self.horizontalLayoutWidget_2)
        self.plainTextEdit_3.setObjectName("plainTextEdit_3")
        self.horizontalLayout_2.addWidget(self.plainTextEdit_3)
        self.gridLayoutWidget = QtWidgets.QWidget(Form)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 160, 51))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.plainTextEdit_2 = QtWidgets.QPlainTextEdit(self.gridLayoutWidget)
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")
        self.gridLayout.addWidget(self.plainTextEdit_2, 1, 1, 1, 1)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.gridLayoutWidget)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.gridLayout.addWidget(self.plainTextEdit, 1, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Marvin Tester"))
        self.pushButton_2.setText(_translate("Form", "Polierpumpe"))
        self.pushButton.setText(_translate("Form", "Spindel"))
        self.label_2.setText(_translate("Form", "Y"))
        self.label.setText(_translate("Form", "X"))

