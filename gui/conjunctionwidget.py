# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'conjunctionwidget.ui'
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

class Ui_conjunctionwidget(object):
    def setupUi(self, conjunctionwidget):
        conjunctionwidget.setObjectName(_fromUtf8("conjunctionwidget"))
        conjunctionwidget.resize(400, 700)
        conjunctionwidget.setMinimumSize(QtCore.QSize(300, 500))
        conjunctionwidget.setMaximumSize(QtCore.QSize(600, 1000))
        self.verticalLayout_2 = QtGui.QVBoxLayout(conjunctionwidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.export_btn = QtGui.QPushButton(conjunctionwidget)
        self.export_btn.setObjectName(_fromUtf8("export_btn"))
        self.gridLayout.addWidget(self.export_btn, 0, 2, 1, 1)
        self.line = QtGui.QFrame(conjunctionwidget)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 1, 0, 1, 4)
        self.compute_btn = QtGui.QPushButton(conjunctionwidget)
        self.compute_btn.setObjectName(_fromUtf8("compute_btn"))
        self.gridLayout.addWidget(self.compute_btn, 0, 3, 1, 1)
        self.data_treewidget = QtGui.QTreeWidget(conjunctionwidget)
        self.data_treewidget.setObjectName(_fromUtf8("data_treewidget"))
        self.gridLayout.addWidget(self.data_treewidget, 4, 0, 1, 4)
        self.line_2 = QtGui.QFrame(conjunctionwidget)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout.addWidget(self.line_2, 3, 0, 1, 4)
        self.label = QtGui.QLabel(conjunctionwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.kstep_spinbox = QtGui.QSpinBox(conjunctionwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.kstep_spinbox.sizePolicy().hasHeightForWidth())
        self.kstep_spinbox.setSizePolicy(sizePolicy)
        self.kstep_spinbox.setMinimum(1)
        self.kstep_spinbox.setMaximum(99999)
        self.kstep_spinbox.setObjectName(_fromUtf8("kstep_spinbox"))
        self.gridLayout.addWidget(self.kstep_spinbox, 0, 1, 1, 1)
        self.ut_groupbox = QtGui.QGroupBox(conjunctionwidget)
        self.ut_groupbox.setEnabled(True)
        self.ut_groupbox.setFlat(False)
        self.ut_groupbox.setCheckable(True)
        self.ut_groupbox.setChecked(False)
        self.ut_groupbox.setObjectName(_fromUtf8("ut_groupbox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.ut_groupbox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.dt_chk = QtGui.QCheckBox(self.ut_groupbox)
        self.dt_chk.setObjectName(_fromUtf8("dt_chk"))
        self.verticalLayout.addWidget(self.dt_chk)
        self.line_3 = QtGui.QFrame(self.ut_groupbox)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.verticalLayout.addWidget(self.line_3)
        self.radec_container = QtGui.QWidget(self.ut_groupbox)
        self.radec_container.setEnabled(False)
        self.radec_container.setObjectName(_fromUtf8("radec_container"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.radec_container)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.dec_d_spinbox_2 = QtGui.QSpinBox(self.radec_container)
        self.dec_d_spinbox_2.setMinimum(-90)
        self.dec_d_spinbox_2.setMaximum(90)
        self.dec_d_spinbox_2.setObjectName(_fromUtf8("dec_d_spinbox_2"))
        self.gridLayout_3.addWidget(self.dec_d_spinbox_2, 3, 1, 1, 1)
        self.label_10 = QtGui.QLabel(self.radec_container)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout_3.addWidget(self.label_10, 0, 3, 1, 1)
        self.label_11 = QtGui.QLabel(self.radec_container)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout_3.addWidget(self.label_11, 2, 1, 1, 1)
        self.label_12 = QtGui.QLabel(self.radec_container)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.gridLayout_3.addWidget(self.label_12, 0, 1, 1, 1)
        self.ra_m_spinbox_2 = QtGui.QSpinBox(self.radec_container)
        self.ra_m_spinbox_2.setMaximum(59)
        self.ra_m_spinbox_2.setObjectName(_fromUtf8("ra_m_spinbox_2"))
        self.gridLayout_3.addWidget(self.ra_m_spinbox_2, 1, 2, 1, 1)
        self.ra_s_spinbox_2 = QtGui.QSpinBox(self.radec_container)
        self.ra_s_spinbox_2.setMaximum(59)
        self.ra_s_spinbox_2.setObjectName(_fromUtf8("ra_s_spinbox_2"))
        self.gridLayout_3.addWidget(self.ra_s_spinbox_2, 1, 3, 1, 1)
        self.ra_h_spinbox_2 = QtGui.QSpinBox(self.radec_container)
        self.ra_h_spinbox_2.setMaximum(23)
        self.ra_h_spinbox_2.setObjectName(_fromUtf8("ra_h_spinbox_2"))
        self.gridLayout_3.addWidget(self.ra_h_spinbox_2, 1, 1, 1, 1)
        self.label_13 = QtGui.QLabel(self.radec_container)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.gridLayout_3.addWidget(self.label_13, 2, 2, 1, 1)
        self.dec_m_spinbox_2 = QtGui.QSpinBox(self.radec_container)
        self.dec_m_spinbox_2.setMaximum(59)
        self.dec_m_spinbox_2.setObjectName(_fromUtf8("dec_m_spinbox_2"))
        self.gridLayout_3.addWidget(self.dec_m_spinbox_2, 3, 2, 1, 1)
        self.label_14 = QtGui.QLabel(self.radec_container)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.gridLayout_3.addWidget(self.label_14, 0, 2, 1, 1)
        self.dec_s_spinbox_2 = QtGui.QSpinBox(self.radec_container)
        self.dec_s_spinbox_2.setMaximum(59)
        self.dec_s_spinbox_2.setObjectName(_fromUtf8("dec_s_spinbox_2"))
        self.gridLayout_3.addWidget(self.dec_s_spinbox_2, 3, 3, 1, 1)
        self.label_15 = QtGui.QLabel(self.radec_container)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.gridLayout_3.addWidget(self.label_15, 2, 3, 1, 1)
        self.label_16 = QtGui.QLabel(self.radec_container)
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.gridLayout_3.addWidget(self.label_16, 1, 0, 1, 1)
        self.label_17 = QtGui.QLabel(self.radec_container)
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.gridLayout_3.addWidget(self.label_17, 3, 0, 1, 1)
        self.horizontalLayout_2.addLayout(self.gridLayout_3)
        self.verticalLayout.addWidget(self.radec_container)
        self.gridLayout.addWidget(self.ut_groupbox, 2, 0, 1, 4)
        self.verticalLayout_2.addLayout(self.gridLayout)

        self.retranslateUi(conjunctionwidget)
        QtCore.QMetaObject.connectSlotsByName(conjunctionwidget)

    def retranslateUi(self, conjunctionwidget):
        conjunctionwidget.setWindowTitle(_translate("conjunctionwidget", "Compute Conjunction Times", None))
        self.export_btn.setText(_translate("conjunctionwidget", "Export", None))
        self.compute_btn.setText(_translate("conjunctionwidget", "Compute", None))
        self.data_treewidget.headerItem().setText(0, _translate("conjunctionwidget", "HJD", None))
        self.data_treewidget.headerItem().setText(1, _translate("conjunctionwidget", "Min Type", None))
        self.data_treewidget.headerItem().setText(2, _translate("conjunctionwidget", "UT", None))
        self.label.setToolTip(_translate("conjunctionwidget", "Space conjunction times by a whole orbit cycles per minima [KTSTEP]", None))
        self.label.setText(_translate("conjunctionwidget", "Cycle Step", None))
        self.ut_groupbox.setTitle(_translate("conjunctionwidget", "Compute UTC", None))
        self.dt_chk.setText(_translate("conjunctionwidget", "Include dT", None))
        self.label_10.setText(_translate("conjunctionwidget", "Second", None))
        self.label_11.setText(_translate("conjunctionwidget", "°", None))
        self.label_12.setText(_translate("conjunctionwidget", "Hour", None))
        self.label_13.setText(_translate("conjunctionwidget", "\'", None))
        self.label_14.setText(_translate("conjunctionwidget", "Minute", None))
        self.label_15.setText(_translate("conjunctionwidget", "\"", None))
        self.label_16.setText(_translate("conjunctionwidget", "Right Ascension", None))
        self.label_17.setText(_translate("conjunctionwidget", "Declination", None))

