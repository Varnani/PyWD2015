# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'historywidget.ui'
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

class Ui_HistoryWidget(object):
    def setupUi(self, HistoryWidget):
        HistoryWidget.setObjectName(_fromUtf8("HistoryWidget"))
        HistoryWidget.resize(800, 600)
        self.verticalLayout = QtGui.QVBoxLayout(HistoryWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.plot_widget = QtGui.QWidget(HistoryWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plot_widget.sizePolicy().hasHeightForWidth())
        self.plot_widget.setSizePolicy(sizePolicy)
        self.plot_widget.setMinimumSize(QtCore.QSize(200, 300))
        self.plot_widget.setObjectName(_fromUtf8("plot_widget"))
        self.gridLayout.addWidget(self.plot_widget, 4, 0, 1, 4)
        self.plot_btn = QtGui.QPushButton(HistoryWidget)
        self.plot_btn.setObjectName(_fromUtf8("plot_btn"))
        self.gridLayout.addWidget(self.plot_btn, 0, 0, 1, 1)
        self.auto_chk = QtGui.QCheckBox(HistoryWidget)
        self.auto_chk.setObjectName(_fromUtf8("auto_chk"))
        self.gridLayout.addWidget(self.auto_chk, 0, 3, 1, 1)
        self.history_treewidget = QtGui.QTreeWidget(HistoryWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.history_treewidget.sizePolicy().hasHeightForWidth())
        self.history_treewidget.setSizePolicy(sizePolicy)
        self.history_treewidget.setMaximumSize(QtCore.QSize(16777215, 225))
        self.history_treewidget.setObjectName(_fromUtf8("history_treewidget"))
        self.gridLayout.addWidget(self.history_treewidget, 2, 0, 1, 4)
        self.clear_btn = QtGui.QPushButton(HistoryWidget)
        self.clear_btn.setObjectName(_fromUtf8("clear_btn"))
        self.gridLayout.addWidget(self.clear_btn, 0, 2, 1, 1)
        self.line = QtGui.QFrame(HistoryWidget)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 1, 0, 1, 4)
        self.export_btn = QtGui.QPushButton(HistoryWidget)
        self.export_btn.setObjectName(_fromUtf8("export_btn"))
        self.gridLayout.addWidget(self.export_btn, 0, 1, 1, 1)
        self.line_2 = QtGui.QFrame(HistoryWidget)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout.addWidget(self.line_2, 3, 0, 1, 4)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(HistoryWidget)
        QtCore.QMetaObject.connectSlotsByName(HistoryWidget)

    def retranslateUi(self, HistoryWidget):
        HistoryWidget.setWindowTitle(_translate("HistoryWidget", "Solution History", None))
        self.plot_btn.setText(_translate("HistoryWidget", "Plot", None))
        self.auto_chk.setToolTip(_translate("HistoryWidget", "Automatically plot selected parameter when DC program finishes its calculation", None))
        self.auto_chk.setText(_translate("HistoryWidget", "Auto", None))
        self.history_treewidget.headerItem().setText(0, _translate("HistoryWidget", "Parameter Name", None))
        self.clear_btn.setText(_translate("HistoryWidget", "Clear", None))
        self.export_btn.setText(_translate("HistoryWidget", "Export", None))

