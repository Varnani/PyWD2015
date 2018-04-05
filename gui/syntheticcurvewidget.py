# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'syntheticcurvewidget.ui'
#
# Created: Thu Apr  5 14:11:18 2018
#      by: PyQt4 UI code generator 4.11.2
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
        SyntheticCurveWidget.resize(910, 700)
        self.verticalLayout_2 = QtGui.QVBoxLayout(SyntheticCurveWidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(SyntheticCurveWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 8, 0, 1, 1)
        self.phase_spinbox = QtGui.QDoubleSpinBox(SyntheticCurveWidget)
        self.phase_spinbox.setEnabled(True)
        self.phase_spinbox.setDecimals(2)
        self.phase_spinbox.setMaximum(1.0)
        self.phase_spinbox.setSingleStep(0.1)
        self.phase_spinbox.setProperty("value", 0.25)
        self.phase_spinbox.setObjectName(_fromUtf8("phase_spinbox"))
        self.gridLayout.addWidget(self.phase_spinbox, 8, 1, 1, 1)
        self.drawstars_chk = QtGui.QCheckBox(SyntheticCurveWidget)
        self.drawstars_chk.setObjectName(_fromUtf8("drawstars_chk"))
        self.gridLayout.addWidget(self.drawstars_chk, 7, 0, 1, 2)
        self.plotmodel_chk = QtGui.QCheckBox(SyntheticCurveWidget)
        self.plotmodel_chk.setChecked(True)
        self.plotmodel_chk.setObjectName(_fromUtf8("plotmodel_chk"))
        self.gridLayout.addWidget(self.plotmodel_chk, 5, 0, 1, 2)
        self.plotobs_chk = QtGui.QCheckBox(SyntheticCurveWidget)
        self.plotobs_chk.setChecked(True)
        self.plotobs_chk.setObjectName(_fromUtf8("plotobs_chk"))
        self.gridLayout.addWidget(self.plotobs_chk, 4, 0, 1, 2)
        self.time_combobox = QtGui.QComboBox(SyntheticCurveWidget)
        self.time_combobox.setObjectName(_fromUtf8("time_combobox"))
        self.time_combobox.addItem(_fromUtf8(""))
        self.time_combobox.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.time_combobox, 3, 0, 1, 2)
        self.pop_btn = QtGui.QPushButton(SyntheticCurveWidget)
        self.pop_btn.setObjectName(_fromUtf8("pop_btn"))
        self.gridLayout.addWidget(self.pop_btn, 1, 0, 1, 2)
        self.plot_btn = QtGui.QPushButton(SyntheticCurveWidget)
        self.plot_btn.setObjectName(_fromUtf8("plot_btn"))
        self.gridLayout.addWidget(self.plot_btn, 0, 0, 1, 2)
        self.line_2 = QtGui.QFrame(SyntheticCurveWidget)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout.addWidget(self.line_2, 2, 0, 1, 2)
        self.line_3 = QtGui.QFrame(SyntheticCurveWidget)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.gridLayout.addWidget(self.line_3, 6, 0, 1, 2)
        self.roche_chk = QtGui.QCheckBox(SyntheticCurveWidget)
        self.roche_chk.setEnabled(True)
        self.roche_chk.setObjectName(_fromUtf8("roche_chk"))
        self.gridLayout.addWidget(self.roche_chk, 9, 0, 1, 2)
        self.fillout_label = QtGui.QLabel(SyntheticCurveWidget)
        self.fillout_label.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fillout_label.sizePolicy().hasHeightForWidth())
        self.fillout_label.setSizePolicy(sizePolicy)
        self.fillout_label.setAlignment(QtCore.Qt.AlignCenter)
        self.fillout_label.setObjectName(_fromUtf8("fillout_label"))
        self.gridLayout.addWidget(self.fillout_label, 11, 0, 1, 2)
        self.line_4 = QtGui.QFrame(SyntheticCurveWidget)
        self.line_4.setFrameShape(QtGui.QFrame.HLine)
        self.line_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_4.setObjectName(_fromUtf8("line_4"))
        self.gridLayout.addWidget(self.line_4, 10, 0, 1, 2)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 2, 1, 1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.loaded_treewidget = QtGui.QTreeWidget(SyntheticCurveWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loaded_treewidget.sizePolicy().hasHeightForWidth())
        self.loaded_treewidget.setSizePolicy(sizePolicy)
        self.loaded_treewidget.setMinimumSize(QtCore.QSize(0, 120))
        self.loaded_treewidget.setMaximumSize(QtCore.QSize(16777215, 275))
        self.loaded_treewidget.setAlternatingRowColors(True)
        self.loaded_treewidget.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.loaded_treewidget.setObjectName(_fromUtf8("loaded_treewidget"))
        self.loaded_treewidget.header().setDefaultSectionSize(53)
        self.loaded_treewidget.header().setMinimumSectionSize(30)
        self.loaded_treewidget.header().setStretchLastSection(True)
        self.verticalLayout.addWidget(self.loaded_treewidget)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.line_5 = QtGui.QFrame(SyntheticCurveWidget)
        self.line_5.setFrameShape(QtGui.QFrame.VLine)
        self.line_5.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_5.setObjectName(_fromUtf8("line_5"))
        self.gridLayout_2.addWidget(self.line_5, 0, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_2)
        self.line = QtGui.QFrame(SyntheticCurveWidget)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout_2.addWidget(self.line)
        self.plot_widget = QtGui.QWidget(SyntheticCurveWidget)
        self.plot_widget.setMinimumSize(QtCore.QSize(500, 300))
        self.plot_widget.setObjectName(_fromUtf8("plot_widget"))
        self.verticalLayout_2.addWidget(self.plot_widget)

        self.retranslateUi(SyntheticCurveWidget)
        QtCore.QMetaObject.connectSlotsByName(SyntheticCurveWidget)

    def retranslateUi(self, SyntheticCurveWidget):
        SyntheticCurveWidget.setWindowTitle(_translate("SyntheticCurveWidget", "Plot Synthetic Curves", None))
        self.label.setToolTip(_translate("SyntheticCurveWidget", "Phase of star positions", None))
        self.label.setText(_translate("SyntheticCurveWidget", "Phase", None))
        self.drawstars_chk.setToolTip(_translate("SyntheticCurveWidget", "Draw star positions in a subplot", None))
        self.drawstars_chk.setText(_translate("SyntheticCurveWidget", "Star Positions", None))
        self.plotmodel_chk.setToolTip(_translate("SyntheticCurveWidget", "Compute and plot synthetic curve", None))
        self.plotmodel_chk.setText(_translate("SyntheticCurveWidget", "Model", None))
        self.plotobs_chk.setToolTip(_translate("SyntheticCurveWidget", "Include observation in plot", None))
        self.plotobs_chk.setText(_translate("SyntheticCurveWidget", "Observation", None))
        self.time_combobox.setToolTip(_translate("SyntheticCurveWidget", "Select x axis unit", None))
        self.time_combobox.setItemText(0, _translate("SyntheticCurveWidget", "Phase", None))
        self.time_combobox.setItemText(1, _translate("SyntheticCurveWidget", "HJD", None))
        self.pop_btn.setToolTip(_translate("SyntheticCurveWidget", "Pop plot window", None))
        self.pop_btn.setText(_translate("SyntheticCurveWidget", "Pop", None))
        self.plot_btn.setToolTip(_translate("SyntheticCurveWidget", "Plot selected item", None))
        self.plot_btn.setText(_translate("SyntheticCurveWidget", "Plot", None))
        self.roche_chk.setToolTip(_translate("SyntheticCurveWidget", "Draw Roche equipotential surfaces onto star positions. This option is only valid when Phase = 0.25", None))
        self.roche_chk.setText(_translate("SyntheticCurveWidget", "Roche Pot.\'s", None))
        self.fillout_label.setToolTip(_translate("SyntheticCurveWidget", "Compute fillout factor as defined in BinaryMaker software;\n"
"Bradstreet, D. H. 1993, IAU Commission on Close Binary Stars, 21, 151\n"
"Bradstreet, D. H. and Steelman, D. P. 2002, Bulletin of the American Astronomical Society, 34, 75.02  ", None))
        self.fillout_label.setText(_translate("SyntheticCurveWidget", "Fillout = N/A", None))
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

