# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'starpositionswidget.ui'
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

class Ui_StarPositionWidget(object):
    def setupUi(self, StarPositionWidget):
        StarPositionWidget.setObjectName(_fromUtf8("StarPositionWidget"))
        StarPositionWidget.resize(600, 600)
        self.verticalLayout = QtGui.QVBoxLayout(StarPositionWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.render_btn = QtGui.QPushButton(StarPositionWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.render_btn.sizePolicy().hasHeightForWidth())
        self.render_btn.setSizePolicy(sizePolicy)
        self.render_btn.setObjectName(_fromUtf8("render_btn"))
        self.gridLayout.addWidget(self.render_btn, 0, 8, 2, 1)
        self.line_9 = QtGui.QFrame(StarPositionWidget)
        self.line_9.setFrameShape(QtGui.QFrame.VLine)
        self.line_9.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_9.setObjectName(_fromUtf8("line_9"))
        self.gridLayout.addWidget(self.line_9, 1, 5, 1, 1)
        self.label_4 = QtGui.QLabel(StarPositionWidget)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 0, 3, 1, 1)
        self.single_chk = QtGui.QCheckBox(StarPositionWidget)
        self.single_chk.setObjectName(_fromUtf8("single_chk"))
        self.gridLayout.addWidget(self.single_chk, 1, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.line_4 = QtGui.QFrame(StarPositionWidget)
        self.line_4.setFrameShape(QtGui.QFrame.VLine)
        self.line_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_4.setObjectName(_fromUtf8("line_4"))
        self.gridLayout.addWidget(self.line_4, 0, 2, 2, 1)
        self.line_5 = QtGui.QFrame(StarPositionWidget)
        self.line_5.setFrameShape(QtGui.QFrame.VLine)
        self.line_5.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_5.setObjectName(_fromUtf8("line_5"))
        self.gridLayout.addWidget(self.line_5, 0, 7, 2, 1)
        self.max_spinbox = QtGui.QDoubleSpinBox(StarPositionWidget)
        self.max_spinbox.setDecimals(1)
        self.max_spinbox.setMinimum(-100.0)
        self.max_spinbox.setMaximum(100.0)
        self.max_spinbox.setSingleStep(0.5)
        self.max_spinbox.setProperty("value", 1.0)
        self.max_spinbox.setObjectName(_fromUtf8("max_spinbox"))
        self.gridLayout.addWidget(self.max_spinbox, 1, 4, 1, 1)
        self.setlimits_btn = QtGui.QPushButton(StarPositionWidget)
        self.setlimits_btn.setObjectName(_fromUtf8("setlimits_btn"))
        self.gridLayout.addWidget(self.setlimits_btn, 1, 6, 1, 1)
        self.min_spinbox = QtGui.QDoubleSpinBox(StarPositionWidget)
        self.min_spinbox.setDecimals(1)
        self.min_spinbox.setMinimum(-100.0)
        self.min_spinbox.setMaximum(100.0)
        self.min_spinbox.setSingleStep(0.5)
        self.min_spinbox.setProperty("value", -1.0)
        self.min_spinbox.setObjectName(_fromUtf8("min_spinbox"))
        self.gridLayout.addWidget(self.min_spinbox, 1, 3, 1, 1)
        self.label_5 = QtGui.QLabel(StarPositionWidget)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 0, 4, 1, 1)
        self.phase_spinbox = QtGui.QDoubleSpinBox(StarPositionWidget)
        self.phase_spinbox.setEnabled(False)
        self.phase_spinbox.setDecimals(2)
        self.phase_spinbox.setMinimum(0.0)
        self.phase_spinbox.setMaximum(1.0)
        self.phase_spinbox.setSingleStep(0.01)
        self.phase_spinbox.setProperty("value", 0.25)
        self.phase_spinbox.setObjectName(_fromUtf8("phase_spinbox"))
        self.gridLayout.addWidget(self.phase_spinbox, 1, 1, 1, 1)
        self.label_6 = QtGui.QLabel(StarPositionWidget)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.line = QtGui.QFrame(StarPositionWidget)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.plot_widget = QtGui.QWidget(StarPositionWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plot_widget.sizePolicy().hasHeightForWidth())
        self.plot_widget.setSizePolicy(sizePolicy)
        self.plot_widget.setMinimumSize(QtCore.QSize(200, 200))
        self.plot_widget.setObjectName(_fromUtf8("plot_widget"))
        self.verticalLayout.addWidget(self.plot_widget)
        self.line_2 = QtGui.QFrame(StarPositionWidget)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.verticalLayout.addWidget(self.line_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.backtostart_btn = QtGui.QPushButton(StarPositionWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.backtostart_btn.sizePolicy().hasHeightForWidth())
        self.backtostart_btn.setSizePolicy(sizePolicy)
        self.backtostart_btn.setMinimumSize(QtCore.QSize(35, 35))
        self.backtostart_btn.setMaximumSize(QtCore.QSize(35, 35))
        self.backtostart_btn.setText(_fromUtf8(""))
        self.backtostart_btn.setObjectName(_fromUtf8("backtostart_btn"))
        self.horizontalLayout.addWidget(self.backtostart_btn)
        self.start_btn = QtGui.QPushButton(StarPositionWidget)
        self.start_btn.setMinimumSize(QtCore.QSize(35, 35))
        self.start_btn.setMaximumSize(QtCore.QSize(35, 35))
        self.start_btn.setText(_fromUtf8(""))
        self.start_btn.setObjectName(_fromUtf8("start_btn"))
        self.horizontalLayout.addWidget(self.start_btn)
        self.skip_btn = QtGui.QPushButton(StarPositionWidget)
        self.skip_btn.setMinimumSize(QtCore.QSize(35, 35))
        self.skip_btn.setMaximumSize(QtCore.QSize(35, 35))
        self.skip_btn.setText(_fromUtf8(""))
        self.skip_btn.setObjectName(_fromUtf8("skip_btn"))
        self.horizontalLayout.addWidget(self.skip_btn)
        self.line_8 = QtGui.QFrame(StarPositionWidget)
        self.line_8.setFrameShape(QtGui.QFrame.VLine)
        self.line_8.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_8.setObjectName(_fromUtf8("line_8"))
        self.horizontalLayout.addWidget(self.line_8)
        self.horizontalSlider = QtGui.QSlider(StarPositionWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.horizontalSlider.sizePolicy().hasHeightForWidth())
        self.horizontalSlider.setSizePolicy(sizePolicy)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName(_fromUtf8("horizontalSlider"))
        self.horizontalLayout.addWidget(self.horizontalSlider)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line_3 = QtGui.QFrame(StarPositionWidget)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.verticalLayout.addWidget(self.line_3)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.message_label = QtGui.QLabel(StarPositionWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.message_label.sizePolicy().hasHeightForWidth())
        self.message_label.setSizePolicy(sizePolicy)
        self.message_label.setObjectName(_fromUtf8("message_label"))
        self.horizontalLayout_2.addWidget(self.message_label)
        self.line_7 = QtGui.QFrame(StarPositionWidget)
        self.line_7.setFrameShape(QtGui.QFrame.VLine)
        self.line_7.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_7.setObjectName(_fromUtf8("line_7"))
        self.horizontalLayout_2.addWidget(self.line_7)
        self.saveframe_btn = QtGui.QPushButton(StarPositionWidget)
        self.saveframe_btn.setObjectName(_fromUtf8("saveframe_btn"))
        self.horizontalLayout_2.addWidget(self.saveframe_btn)
        self.saveall_btn = QtGui.QPushButton(StarPositionWidget)
        self.saveall_btn.setObjectName(_fromUtf8("saveall_btn"))
        self.horizontalLayout_2.addWidget(self.saveall_btn)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(StarPositionWidget)
        QtCore.QMetaObject.connectSlotsByName(StarPositionWidget)

    def retranslateUi(self, StarPositionWidget):
        StarPositionWidget.setWindowTitle(_translate("StarPositionWidget", "Star Positions", None))
        self.render_btn.setText(_translate("StarPositionWidget", "Render", None))
        self.label_4.setText(_translate("StarPositionWidget", "Axis Min", None))
        self.single_chk.setText(_translate("StarPositionWidget", "Single", None))
        self.setlimits_btn.setText(_translate("StarPositionWidget", "Set", None))
        self.label_5.setText(_translate("StarPositionWidget", "Axis Max", None))
        self.label_6.setText(_translate("StarPositionWidget", "Phase", None))
        self.message_label.setText(_translate("StarPositionWidget", "Ready", None))
        self.saveframe_btn.setText(_translate("StarPositionWidget", "Save Frame", None))
        self.saveall_btn.setText(_translate("StarPositionWidget", "Save All", None))
