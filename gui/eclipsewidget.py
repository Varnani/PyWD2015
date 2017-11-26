# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eclipsewidget.ui'
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

class Ui_EclipseWidget(object):
    def setupUi(self, EclipseWidget):
        EclipseWidget.setObjectName(_fromUtf8("EclipseWidget"))
        EclipseWidget.resize(330, 590)
        EclipseWidget.setMinimumSize(QtCore.QSize(330, 590))
        EclipseWidget.setMaximumSize(QtCore.QSize(330, 590))
        self.label_53 = QtGui.QLabel(EclipseWidget)
        self.label_53.setGeometry(QtCore.QRect(10, 0, 711, 31))
        self.label_53.setObjectName(_fromUtf8("label_53"))
        self.line_12 = QtGui.QFrame(EclipseWidget)
        self.line_12.setGeometry(QtCore.QRect(10, 20, 711, 21))
        self.line_12.setFrameShape(QtGui.QFrame.HLine)
        self.line_12.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_12.setObjectName(_fromUtf8("line_12"))
        self.iftime_chk = QtGui.QCheckBox(EclipseWidget)
        self.iftime_chk.setGeometry(QtCore.QRect(10, 30, 231, 41))
        self.iftime_chk.setObjectName(_fromUtf8("iftime_chk"))
        self.load_btn = QtGui.QPushButton(EclipseWidget)
        self.load_btn.setGeometry(QtCore.QRect(10, 470, 311, 50))
        self.load_btn.setObjectName(_fromUtf8("load_btn"))
        self.datawidget = QtGui.QTreeWidget(EclipseWidget)
        self.datawidget.setGeometry(QtCore.QRect(10, 110, 311, 351))
        self.datawidget.setObjectName(_fromUtf8("datawidget"))
        self.clear_btn = QtGui.QPushButton(EclipseWidget)
        self.clear_btn.setGeometry(QtCore.QRect(10, 530, 311, 50))
        self.clear_btn.setObjectName(_fromUtf8("clear_btn"))
        self.label = QtGui.QLabel(EclipseWidget)
        self.label.setGeometry(QtCore.QRect(10, 60, 141, 31))
        self.label.setObjectName(_fromUtf8("label"))
        self.filepath_label = QtGui.QLabel(EclipseWidget)
        self.filepath_label.setGeometry(QtCore.QRect(10, 80, 311, 31))
        self.filepath_label.setObjectName(_fromUtf8("filepath_label"))

        self.retranslateUi(EclipseWidget)
        QtCore.QMetaObject.connectSlotsByName(EclipseWidget)

    def retranslateUi(self, EclipseWidget):
        EclipseWidget.setWindowTitle(_translate("EclipseWidget", "Eclipse Timings", None))
        self.label_53.setText(_translate("EclipseWidget", "Load eclipse timings from a file", None))
        self.iftime_chk.setText(_translate("EclipseWidget", "IFTIME - Write eclipse timings", None))
        self.load_btn.setText(_translate("EclipseWidget", "Load", None))
        self.datawidget.headerItem().setText(0, _translate("EclipseWidget", "Time", None))
        self.datawidget.headerItem().setText(1, _translate("EclipseWidget", "Eclipse Type", None))
        self.datawidget.headerItem().setText(2, _translate("EclipseWidget", "Weight", None))
        self.clear_btn.setText(_translate("EclipseWidget", "Clear", None))
        self.label.setText(_translate("EclipseWidget", "Data preview of file:", None))
        self.filepath_label.setText(_translate("EclipseWidget", "None", None))

