# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'view.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1080, 720)
        self.splitter = QtWidgets.QSplitter(Form)
        self.splitter.setEnabled(True)
        self.splitter.setGeometry(QtCore.QRect(90, 630, 911, 51))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setHandleWidth(30)
        self.splitter.setObjectName("splitter")
        self.btn_open = QtWidgets.QPushButton(self.splitter)
        self.btn_open.setObjectName("btn_open")
        self.btn_save = QtWidgets.QPushButton(self.splitter)
        self.btn_save.setObjectName("btn_save")
        self.btn_stop = QtWidgets.QPushButton(self.splitter)
        self.btn_stop.setObjectName("btn_stop")
        self.btn_quit = QtWidgets.QPushButton(self.splitter)
        self.btn_quit.setObjectName("btn_quit")
        self.splitter_2 = QtWidgets.QSplitter(Form)
        self.splitter_2.setGeometry(QtCore.QRect(100, 150, 891, 361))
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.label_1 = QtWidgets.QLabel(self.splitter_2)
        self.label_1.setText("")
        self.label_1.setObjectName("label_1")
        self.label_2 = QtWidgets.QLabel(self.splitter_2)
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.btn_open.setText(_translate("Form", "Start"))
        self.btn_save.setText(_translate("Form", "Save"))
        self.btn_stop.setText(_translate("Form", "Stop"))
        self.btn_quit.setText(_translate("Form", "Quit"))


