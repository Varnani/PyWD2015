# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ocwidget.ui'
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

class Ui_OCWidget(object):
    def setupUi(self, OCWidget):
        OCWidget.setObjectName(_fromUtf8("OCWidget"))
        OCWidget.resize(800, 500)
        OCWidget.setMinimumSize(QtCore.QSize(750, 350))
        self.horizontalLayout = QtGui.QHBoxLayout(OCWidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.plot_widget = QtGui.QWidget(OCWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plot_widget.sizePolicy().hasHeightForWidth())
        self.plot_widget.setSizePolicy(sizePolicy)
        self.plot_widget.setMinimumSize(QtCore.QSize(400, 300))
        self.plot_widget.setObjectName(_fromUtf8("plot_widget"))
        self.gridLayout.addWidget(self.plot_widget, 0, 3, 5, 1)
        self.line_3 = QtGui.QFrame(OCWidget)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.gridLayout.addWidget(self.line_3, 1, 0, 1, 2)
        self.dpdt_chk = QtGui.QCheckBox(OCWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dpdt_chk.sizePolicy().hasHeightForWidth())
        self.dpdt_chk.setSizePolicy(sizePolicy)
        self.dpdt_chk.setObjectName(_fromUtf8("dpdt_chk"))
        self.gridLayout.addWidget(self.dpdt_chk, 2, 1, 1, 1)
        self.linear_chk = QtGui.QCheckBox(OCWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.linear_chk.sizePolicy().hasHeightForWidth())
        self.linear_chk.setSizePolicy(sizePolicy)
        self.linear_chk.setObjectName(_fromUtf8("linear_chk"))
        self.gridLayout.addWidget(self.linear_chk, 2, 0, 1, 1)
        self.line = QtGui.QFrame(OCWidget)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 3, 0, 1, 2)
        self.data_treewidget = QtGui.QTreeWidget(OCWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.data_treewidget.sizePolicy().hasHeightForWidth())
        self.data_treewidget.setSizePolicy(sizePolicy)
        self.data_treewidget.setObjectName(_fromUtf8("data_treewidget"))
        self.gridLayout.addWidget(self.data_treewidget, 4, 0, 1, 2)
        self.compute_btn = QtGui.QPushButton(OCWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.compute_btn.sizePolicy().hasHeightForWidth())
        self.compute_btn.setSizePolicy(sizePolicy)
        self.compute_btn.setObjectName(_fromUtf8("compute_btn"))
        self.gridLayout.addWidget(self.compute_btn, 0, 0, 1, 1)
        self.export_btn = QtGui.QPushButton(OCWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.export_btn.sizePolicy().hasHeightForWidth())
        self.export_btn.setSizePolicy(sizePolicy)
        self.export_btn.setObjectName(_fromUtf8("export_btn"))
        self.gridLayout.addWidget(self.export_btn, 0, 1, 1, 1)
        self.line_2 = QtGui.QFrame(OCWidget)
        self.line_2.setFrameShape(QtGui.QFrame.VLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout.addWidget(self.line_2, 0, 2, 5, 1)
        self.horizontalLayout.addLayout(self.gridLayout)

        self.retranslateUi(OCWidget)
        QtCore.QMetaObject.connectSlotsByName(OCWidget)

    def retranslateUi(self, OCWidget):
        OCWidget.setWindowTitle(_translate("OCWidget", "Compute O - C", None))
        self.dpdt_chk.setText(_translate("OCWidget", "Residuals with dP/dt", None))
        self.linear_chk.setText(_translate("OCWidget", "Linear Residuals", None))
        self.data_treewidget.headerItem().setText(0, _translate("OCWidget", "Cycle", None))
        self.data_treewidget.headerItem().setText(1, _translate("OCWidget", "Linear", None))
        self.data_treewidget.headerItem().setText(2, _translate("OCWidget", "with dP/dt", None))
        self.compute_btn.setText(_translate("OCWidget", "Compute", None))
        self.export_btn.setText(_translate("OCWidget", "Export", None))

