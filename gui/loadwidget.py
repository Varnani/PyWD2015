# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'loadwidget.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_LoadWidget(object):
    def setupUi(self, LoadWidget):
        LoadWidget.setObjectName(_fromUtf8("LoadWidget"))
        LoadWidget.resize(650, 215)
        LoadWidget.setMinimumSize(QtCore.QSize(650, 215))
        LoadWidget.setMaximumSize(QtCore.QSize(650, 215))
        self.label_2 = QtGui.QLabel(LoadWidget)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 201, 21))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.line = QtGui.QFrame(LoadWidget)
        self.line.setGeometry(QtCore.QRect(10, 26, 631, 20))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.label = QtGui.QLabel(LoadWidget)
        self.label.setGeometry(QtCore.QRect(60, 70, 41, 21))
        self.label.setObjectName(_fromUtf8("label"))
        self.vc1_fileline = QtGui.QLineEdit(LoadWidget)
        self.vc1_fileline.setGeometry(QtCore.QRect(130, 70, 381, 20))
        self.vc1_fileline.setReadOnly(True)
        self.vc1_fileline.setObjectName(_fromUtf8("vc1_fileline"))
        self.vc1load_btn = QtGui.QPushButton(LoadWidget)
        self.vc1load_btn.setGeometry(QtCore.QRect(580, 69, 61, 21))
        self.vc1load_btn.setObjectName(_fromUtf8("vc1load_btn"))
        self.vc2_fileline = QtGui.QLineEdit(LoadWidget)
        self.vc2_fileline.setGeometry(QtCore.QRect(130, 110, 381, 20))
        self.vc2_fileline.setReadOnly(True)
        self.vc2_fileline.setObjectName(_fromUtf8("vc2_fileline"))
        self.vc2load_btn = QtGui.QPushButton(LoadWidget)
        self.vc2load_btn.setGeometry(QtCore.QRect(580, 109, 61, 21))
        self.vc2load_btn.setObjectName(_fromUtf8("vc2load_btn"))
        self.label_6 = QtGui.QLabel(LoadWidget)
        self.label_6.setGeometry(QtCore.QRect(60, 110, 41, 21))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.nlc_label = QtGui.QLabel(LoadWidget)
        self.nlc_label.setGeometry(QtCore.QRect(500, 180, 141, 21))
        self.nlc_label.setObjectName(_fromUtf8("nlc_label"))
        self.line_2 = QtGui.QFrame(LoadWidget)
        self.line_2.setGeometry(QtCore.QRect(130, 145, 381, 20))
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.lcadd_btn = QtGui.QPushButton(LoadWidget)
        self.lcadd_btn.setGeometry(QtCore.QRect(20, 180, 115, 25))
        self.lcadd_btn.setObjectName(_fromUtf8("lcadd_btn"))
        self.vc1edit_btn = QtGui.QPushButton(LoadWidget)
        self.vc1edit_btn.setGeometry(QtCore.QRect(520, 70, 51, 21))
        self.vc1edit_btn.setObjectName(_fromUtf8("vc1edit_btn"))
        self.vc2edit_btn = QtGui.QPushButton(LoadWidget)
        self.vc2edit_btn.setGeometry(QtCore.QRect(520, 110, 51, 21))
        self.vc2edit_btn.setObjectName(_fromUtf8("vc2edit_btn"))
        self.label_3 = QtGui.QLabel(LoadWidget)
        self.label_3.setGeometry(QtCore.QRect(30, 45, 101, 21))
        self.label_3.setObjectName(_fromUtf8("label_3"))

        self.retranslateUi(LoadWidget)
        QtCore.QMetaObject.connectSlotsByName(LoadWidget)

    def retranslateUi(self, LoadWidget):
        LoadWidget.setWindowTitle(_translate("LoadWidget", "Load Observations", None))
        self.label_2.setText(_translate("LoadWidget", "Load observations from files:", None))
        self.label.setText(_translate("LoadWidget", "Star 1", None))
        self.vc1_fileline.setText(_translate("LoadWidget", "Load a file...", None))
        self.vc1load_btn.setText(_translate("LoadWidget", "Load", None))
        self.vc2_fileline.setText(_translate("LoadWidget", "Load a file...", None))
        self.vc2load_btn.setText(_translate("LoadWidget", "Load", None))
        self.label_6.setText(_translate("LoadWidget", "Star 2", None))
        self.nlc_label.setText(_translate("LoadWidget", "Light curve count: 0", None))
        self.lcadd_btn.setText(_translate("LoadWidget", "Add Light Curve", None))
        self.vc1edit_btn.setText(_translate("LoadWidget", "Edit", None))
        self.vc2edit_btn.setText(_translate("LoadWidget", "Edit", None))
        self.label_3.setText(_translate("LoadWidget", "Velocity Curves", None))

