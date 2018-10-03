# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'syntheticcurvewidget.ui'
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

class Ui_SyntheticCurveWidget(object):
    def setupUi(self, SyntheticCurveWidget):
        SyntheticCurveWidget.setObjectName(_fromUtf8("SyntheticCurveWidget"))
        SyntheticCurveWidget.resize(1000, 600)
        self.verticalLayout = QtGui.QVBoxLayout(SyntheticCurveWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.loaded_treewidget = QtGui.QTreeWidget(SyntheticCurveWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loaded_treewidget.sizePolicy().hasHeightForWidth())
        self.loaded_treewidget.setSizePolicy(sizePolicy)
        self.loaded_treewidget.setMaximumSize(QtCore.QSize(16777215, 260))
        self.loaded_treewidget.setAlternatingRowColors(True)
        self.loaded_treewidget.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.loaded_treewidget.setObjectName(_fromUtf8("loaded_treewidget"))
        self.loaded_treewidget.header().setDefaultSectionSize(53)
        self.loaded_treewidget.header().setMinimumSectionSize(30)
        self.loaded_treewidget.header().setStretchLastSection(True)
        self.gridLayout_2.addWidget(self.loaded_treewidget, 0, 0, 1, 1)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.alias_chk = QtGui.QCheckBox(SyntheticCurveWidget)
        self.alias_chk.setObjectName(_fromUtf8("alias_chk"))
        self.gridLayout.addWidget(self.alias_chk, 7, 0, 1, 2)
        self.pop_btn = QtGui.QPushButton(SyntheticCurveWidget)
        self.pop_btn.setEnabled(True)
        self.pop_btn.setObjectName(_fromUtf8("pop_btn"))
        self.gridLayout.addWidget(self.pop_btn, 1, 0, 1, 2)
        self.time_combobox = QtGui.QComboBox(SyntheticCurveWidget)
        self.time_combobox.setObjectName(_fromUtf8("time_combobox"))
        self.time_combobox.addItem(_fromUtf8(""))
        self.time_combobox.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.time_combobox, 4, 0, 1, 2)
        self.line_2 = QtGui.QFrame(SyntheticCurveWidget)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout.addWidget(self.line_2, 3, 0, 1, 2)
        self.export_btn = QtGui.QPushButton(SyntheticCurveWidget)
        self.export_btn.setEnabled(True)
        self.export_btn.setObjectName(_fromUtf8("export_btn"))
        self.gridLayout.addWidget(self.export_btn, 2, 0, 1, 2)
        self.plotobs_chk = QtGui.QCheckBox(SyntheticCurveWidget)
        self.plotobs_chk.setChecked(True)
        self.plotobs_chk.setObjectName(_fromUtf8("plotobs_chk"))
        self.gridLayout.addWidget(self.plotobs_chk, 5, 0, 1, 2)
        self.plot_btn = QtGui.QPushButton(SyntheticCurveWidget)
        self.plot_btn.setObjectName(_fromUtf8("plot_btn"))
        self.gridLayout.addWidget(self.plot_btn, 0, 0, 1, 2)
        self.enablegrid_chk = QtGui.QCheckBox(SyntheticCurveWidget)
        self.enablegrid_chk.setObjectName(_fromUtf8("enablegrid_chk"))
        self.gridLayout.addWidget(self.enablegrid_chk, 8, 0, 1, 2)
        self.plotmodel_chk = QtGui.QCheckBox(SyntheticCurveWidget)
        self.plotmodel_chk.setChecked(True)
        self.plotmodel_chk.setObjectName(_fromUtf8("plotmodel_chk"))
        self.gridLayout.addWidget(self.plotmodel_chk, 6, 0, 1, 2)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 1, 1, 1)
        self.plot_widget = QtGui.QWidget(SyntheticCurveWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plot_widget.sizePolicy().hasHeightForWidth())
        self.plot_widget.setSizePolicy(sizePolicy)
        self.plot_widget.setMinimumSize(QtCore.QSize(500, 300))
        self.plot_widget.setObjectName(_fromUtf8("plot_widget"))
        self.gridLayout_2.addWidget(self.plot_widget, 1, 0, 1, 2)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.plot_btn.raise_()
        self.pop_btn.raise_()
        self.export_btn.raise_()
        self.time_combobox.raise_()
        self.plotobs_chk.raise_()
        self.plotmodel_chk.raise_()
        self.enablegrid_chk.raise_()
        self.alias_chk.raise_()

        self.retranslateUi(SyntheticCurveWidget)
        QtCore.QMetaObject.connectSlotsByName(SyntheticCurveWidget)

    def retranslateUi(self, SyntheticCurveWidget):
        SyntheticCurveWidget.setWindowTitle(_translate("SyntheticCurveWidget", "Plot Synthetic Curves", None))
        self.loaded_treewidget.headerItem().setText(0, _translate("SyntheticCurveWidget", "File Name", None))
        self.loaded_treewidget.headerItem().setText(1, _translate("SyntheticCurveWidget", "Type", None))
        self.loaded_treewidget.headerItem().setText(2, _translate("SyntheticCurveWidget", "Band", None))
        self.loaded_treewidget.headerItem().setText(3, _translate("SyntheticCurveWidget", "L1", None))
        self.loaded_treewidget.headerItem().setText(4, _translate("SyntheticCurveWidget", "L2", None))
        self.loaded_treewidget.headerItem().setText(5, _translate("SyntheticCurveWidget", "L3", None))
        self.loaded_treewidget.headerItem().setText(6, _translate("SyntheticCurveWidget", "X1", None))
        self.loaded_treewidget.headerItem().setText(7, _translate("SyntheticCurveWidget", "X2", None))
        self.loaded_treewidget.headerItem().setText(8, _translate("SyntheticCurveWidget", "Y1", None))
        self.loaded_treewidget.headerItem().setText(9, _translate("SyntheticCurveWidget", "Y2", None))
        self.loaded_treewidget.headerItem().setText(10, _translate("SyntheticCurveWidget", "Opacity", None))
        self.loaded_treewidget.headerItem().setText(11, _translate("SyntheticCurveWidget", "Extinction", None))
        self.loaded_treewidget.headerItem().setText(12, _translate("SyntheticCurveWidget", "Calibration", None))
        self.loaded_treewidget.headerItem().setText(13, _translate("SyntheticCurveWidget", "Factor", None))
        self.loaded_treewidget.headerItem().setText(14, _translate("SyntheticCurveWidget", "Zero", None))
        self.alias_chk.setToolTip(_translate("SyntheticCurveWidget", "Alias with phase start and phase end. Does nothing if working with HJD.", None))
        self.alias_chk.setText(_translate("SyntheticCurveWidget", "Alias with Phase", None))
        self.pop_btn.setToolTip(_translate("SyntheticCurveWidget", "Pop plot window", None))
        self.pop_btn.setText(_translate("SyntheticCurveWidget", "Pop", None))
        self.time_combobox.setToolTip(_translate("SyntheticCurveWidget", "Select x axis unit", None))
        self.time_combobox.setItemText(0, _translate("SyntheticCurveWidget", "Phase", None))
        self.time_combobox.setItemText(1, _translate("SyntheticCurveWidget", "HJD", None))
        self.export_btn.setText(_translate("SyntheticCurveWidget", "Export", None))
        self.plotobs_chk.setToolTip(_translate("SyntheticCurveWidget", "Include observation in plot", None))
        self.plotobs_chk.setText(_translate("SyntheticCurveWidget", "Observation", None))
        self.plot_btn.setToolTip(_translate("SyntheticCurveWidget", "Plot selected item", None))
        self.plot_btn.setText(_translate("SyntheticCurveWidget", "Plot", None))
        self.enablegrid_chk.setText(_translate("SyntheticCurveWidget", "Enable Grid", None))
        self.plotmodel_chk.setToolTip(_translate("SyntheticCurveWidget", "Compute and plot synthetic curve", None))
        self.plotmodel_chk.setText(_translate("SyntheticCurveWidget", "Model", None))

