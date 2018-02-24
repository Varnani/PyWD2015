# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'loadobservationwidget.ui'
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

class Ui_ObservationWidget(object):
    def setupUi(self, ObservationWidget):
        ObservationWidget.setObjectName(_fromUtf8("ObservationWidget"))
        ObservationWidget.resize(800, 245)
        ObservationWidget.setMinimumSize(QtCore.QSize(800, 245))
        ObservationWidget.setMaximumSize(QtCore.QSize(800, 245))
        self.curve_treewidget = QtGui.QTreeWidget(ObservationWidget)
        self.curve_treewidget.setGeometry(QtCore.QRect(170, 50, 621, 185))
        self.curve_treewidget.setFrameShape(QtGui.QFrame.StyledPanel)
        self.curve_treewidget.setIndentation(10)
        self.curve_treewidget.setExpandsOnDoubleClick(True)
        self.curve_treewidget.setObjectName(_fromUtf8("curve_treewidget"))
        self.curve_treewidget.header().setDefaultSectionSize(170)
        self.curve_treewidget.header().setMinimumSectionSize(200)
        self.curve_treewidget.header().setStretchLastSection(True)
        self.add_btn = QtGui.QPushButton(ObservationWidget)
        self.add_btn.setGeometry(QtCore.QRect(10, 50, 131, 36))
        self.add_btn.setObjectName(_fromUtf8("add_btn"))
        self.line = QtGui.QFrame(ObservationWidget)
        self.line.setGeometry(QtCore.QRect(10, 20, 861, 20))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.label = QtGui.QLabel(ObservationWidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 261, 21))
        self.label.setObjectName(_fromUtf8("label"))
        self.remove_btn = QtGui.QPushButton(ObservationWidget)
        self.remove_btn.setGeometry(QtCore.QRect(10, 150, 131, 36))
        self.remove_btn.setObjectName(_fromUtf8("remove_btn"))
        self.edit_btn = QtGui.QPushButton(ObservationWidget)
        self.edit_btn.setGeometry(QtCore.QRect(10, 100, 131, 36))
        self.edit_btn.setObjectName(_fromUtf8("edit_btn"))
        self.plot_btn = QtGui.QPushButton(ObservationWidget)
        self.plot_btn.setGeometry(QtCore.QRect(10, 200, 131, 36))
        self.plot_btn.setObjectName(_fromUtf8("plot_btn"))
        self.line_2 = QtGui.QFrame(ObservationWidget)
        self.line_2.setGeometry(QtCore.QRect(139, 52, 31, 181))
        self.line_2.setFrameShape(QtGui.QFrame.VLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))

        self.retranslateUi(ObservationWidget)
        QtCore.QMetaObject.connectSlotsByName(ObservationWidget)

    def retranslateUi(self, ObservationWidget):
        ObservationWidget.setWindowTitle(_translate("ObservationWidget", "Load Observations", None))
        self.curve_treewidget.headerItem().setText(0, _translate("ObservationWidget", "Filename", None))
        self.curve_treewidget.headerItem().setText(1, _translate("ObservationWidget", "Type", None))
        self.curve_treewidget.headerItem().setText(2, _translate("ObservationWidget", "Band", None))
        self.add_btn.setText(_translate("ObservationWidget", "Add", None))
        self.label.setText(_translate("ObservationWidget", "Load or edit observations from files:", None))
        self.remove_btn.setText(_translate("ObservationWidget", "Remove", None))
        self.edit_btn.setText(_translate("ObservationWidget", "Edit", None))
        self.plot_btn.setText(_translate("ObservationWidget", "Plot", None))

