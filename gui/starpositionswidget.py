# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'starpositionswidget.ui'
#
# Created: Wed Apr 11 14:53:42 2018
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

class Ui_StarPositionWidget(object):
    def setupUi(self, StarPositionWidget):
        StarPositionWidget.setObjectName(_fromUtf8("StarPositionWidget"))
        StarPositionWidget.resize(700, 600)
        self.verticalLayout = QtGui.QVBoxLayout(StarPositionWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget = QtGui.QTabWidget(StarPositionWidget)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.tab_2)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setMargin(10)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_7 = QtGui.QLabel(self.tab_2)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_2.addWidget(self.label_7, 0, 0, 1, 1)
        self.phase_spinbox = QtGui.QDoubleSpinBox(self.tab_2)
        self.phase_spinbox.setEnabled(True)
        self.phase_spinbox.setMinimumSize(QtCore.QSize(70, 0))
        self.phase_spinbox.setDecimals(4)
        self.phase_spinbox.setMinimum(0.0)
        self.phase_spinbox.setMaximum(1.0)
        self.phase_spinbox.setSingleStep(0.01)
        self.phase_spinbox.setProperty("value", 0.25)
        self.phase_spinbox.setObjectName(_fromUtf8("phase_spinbox"))
        self.gridLayout_2.addWidget(self.phase_spinbox, 1, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 1, 2, 1, 1)
        self.plot_btn = QtGui.QPushButton(self.tab_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plot_btn.sizePolicy().hasHeightForWidth())
        self.plot_btn.setSizePolicy(sizePolicy)
        self.plot_btn.setObjectName(_fromUtf8("plot_btn"))
        self.gridLayout_2.addWidget(self.plot_btn, 0, 3, 2, 1)
        self.roche_chk = QtGui.QCheckBox(self.tab_2)
        self.roche_chk.setObjectName(_fromUtf8("roche_chk"))
        self.gridLayout_2.addWidget(self.roche_chk, 1, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_2)
        self.line_6 = QtGui.QFrame(self.tab_2)
        self.line_6.setFrameShape(QtGui.QFrame.HLine)
        self.line_6.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_6.setObjectName(_fromUtf8("line_6"))
        self.verticalLayout_2.addWidget(self.line_6)
        self.plot_widget = QtGui.QWidget(self.tab_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plot_widget.sizePolicy().hasHeightForWidth())
        self.plot_widget.setSizePolicy(sizePolicy)
        self.plot_widget.setObjectName(_fromUtf8("plot_widget"))
        self.verticalLayout_2.addWidget(self.plot_widget)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.tab)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setMargin(10)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.message_label = QtGui.QLabel(self.tab)
        self.message_label.setMinimumSize(QtCore.QSize(150, 0))
        self.message_label.setMaximumSize(QtCore.QSize(150, 16777215))
        self.message_label.setObjectName(_fromUtf8("message_label"))
        self.horizontalLayout.addWidget(self.message_label)
        self.progressBar = QtGui.QProgressBar(self.tab)
        self.progressBar.setEnabled(True)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.horizontalLayout.addWidget(self.progressBar)
        self.gridLayout_3.addLayout(self.horizontalLayout, 3, 3, 1, 4)
        self.line = QtGui.QFrame(self.tab)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout_3.addWidget(self.line, 0, 2, 1, 1)
        self.start_btn = QtGui.QPushButton(self.tab)
        self.start_btn.setMinimumSize(QtCore.QSize(35, 35))
        self.start_btn.setMaximumSize(QtCore.QSize(35, 35))
        self.start_btn.setText(_fromUtf8(""))
        self.start_btn.setObjectName(_fromUtf8("start_btn"))
        self.gridLayout_3.addWidget(self.start_btn, 2, 3, 1, 1)
        self.backtostart_btn = QtGui.QPushButton(self.tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.backtostart_btn.sizePolicy().hasHeightForWidth())
        self.backtostart_btn.setSizePolicy(sizePolicy)
        self.backtostart_btn.setMinimumSize(QtCore.QSize(35, 35))
        self.backtostart_btn.setMaximumSize(QtCore.QSize(35, 35))
        self.backtostart_btn.setText(_fromUtf8(""))
        self.backtostart_btn.setObjectName(_fromUtf8("backtostart_btn"))
        self.gridLayout_3.addWidget(self.backtostart_btn, 2, 4, 1, 1)
        self.skip_btn = QtGui.QPushButton(self.tab)
        self.skip_btn.setMinimumSize(QtCore.QSize(35, 35))
        self.skip_btn.setMaximumSize(QtCore.QSize(35, 35))
        self.skip_btn.setText(_fromUtf8(""))
        self.skip_btn.setObjectName(_fromUtf8("skip_btn"))
        self.gridLayout_3.addWidget(self.skip_btn, 2, 5, 1, 1)
        self.render_widget = QtGui.QWidget(self.tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.render_widget.sizePolicy().hasHeightForWidth())
        self.render_widget.setSizePolicy(sizePolicy)
        self.render_widget.setObjectName(_fromUtf8("render_widget"))
        self.gridLayout_3.addWidget(self.render_widget, 0, 3, 1, 4)
        self.horizontalSlider = QtGui.QSlider(self.tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.horizontalSlider.sizePolicy().hasHeightForWidth())
        self.horizontalSlider.setSizePolicy(sizePolicy)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName(_fromUtf8("horizontalSlider"))
        self.gridLayout_3.addWidget(self.horizontalSlider, 2, 6, 1, 1)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.max_spinbox = QtGui.QDoubleSpinBox(self.tab)
        self.max_spinbox.setDecimals(1)
        self.max_spinbox.setMinimum(-100.0)
        self.max_spinbox.setMaximum(100.0)
        self.max_spinbox.setSingleStep(0.5)
        self.max_spinbox.setProperty("value", 1.5)
        self.max_spinbox.setObjectName(_fromUtf8("max_spinbox"))
        self.gridLayout.addWidget(self.max_spinbox, 5, 1, 1, 1)
        self.line_3 = QtGui.QFrame(self.tab)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.gridLayout.addWidget(self.line_3, 1, 0, 1, 2)
        self.line_4 = QtGui.QFrame(self.tab)
        self.line_4.setFrameShape(QtGui.QFrame.HLine)
        self.line_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_4.setObjectName(_fromUtf8("line_4"))
        self.gridLayout.addWidget(self.line_4, 3, 0, 1, 2)
        self.dpi_combobox = QtGui.QComboBox(self.tab)
        self.dpi_combobox.setObjectName(_fromUtf8("dpi_combobox"))
        self.dpi_combobox.addItem(_fromUtf8(""))
        self.dpi_combobox.addItem(_fromUtf8(""))
        self.dpi_combobox.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.dpi_combobox, 6, 1, 1, 1)
        self.label_8 = QtGui.QLabel(self.tab)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout.addWidget(self.label_8, 6, 0, 1, 1)
        self.render_phaseSpinbox = QtGui.QDoubleSpinBox(self.tab)
        self.render_phaseSpinbox.setEnabled(False)
        self.render_phaseSpinbox.setDecimals(2)
        self.render_phaseSpinbox.setMinimum(0.0)
        self.render_phaseSpinbox.setMaximum(1.0)
        self.render_phaseSpinbox.setSingleStep(0.01)
        self.render_phaseSpinbox.setProperty("value", 0.25)
        self.render_phaseSpinbox.setObjectName(_fromUtf8("render_phaseSpinbox"))
        self.gridLayout.addWidget(self.render_phaseSpinbox, 2, 1, 1, 1)
        self.label_4 = QtGui.QLabel(self.tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)
        self.label_5 = QtGui.QLabel(self.tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 5, 0, 1, 1)
        self.render_btn = QtGui.QPushButton(self.tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.render_btn.sizePolicy().hasHeightForWidth())
        self.render_btn.setSizePolicy(sizePolicy)
        self.render_btn.setMaximumSize(QtCore.QSize(16777215, 100))
        self.render_btn.setObjectName(_fromUtf8("render_btn"))
        self.gridLayout.addWidget(self.render_btn, 0, 0, 1, 2)
        self.single_chk = QtGui.QCheckBox(self.tab)
        self.single_chk.setObjectName(_fromUtf8("single_chk"))
        self.gridLayout.addWidget(self.single_chk, 2, 0, 1, 1)
        self.min_spinbox = QtGui.QDoubleSpinBox(self.tab)
        self.min_spinbox.setDecimals(1)
        self.min_spinbox.setMinimum(-100.0)
        self.min_spinbox.setMaximum(100.0)
        self.min_spinbox.setSingleStep(0.5)
        self.min_spinbox.setProperty("value", -1.5)
        self.min_spinbox.setObjectName(_fromUtf8("min_spinbox"))
        self.gridLayout.addWidget(self.min_spinbox, 4, 1, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout, 0, 1, 1, 1)
        self.line_2 = QtGui.QFrame(self.tab)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout_3.addWidget(self.line_2, 1, 3, 1, 4)
        self.saveall_btn = QtGui.QPushButton(self.tab)
        self.saveall_btn.setObjectName(_fromUtf8("saveall_btn"))
        self.gridLayout_3.addWidget(self.saveall_btn, 3, 1, 1, 1)
        self.saveframe_btn = QtGui.QPushButton(self.tab)
        self.saveframe_btn.setObjectName(_fromUtf8("saveframe_btn"))
        self.gridLayout_3.addWidget(self.saveframe_btn, 2, 1, 1, 1)
        self.horizontalLayout_2.addLayout(self.gridLayout_3)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidget)

        self.retranslateUi(StarPositionWidget)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(StarPositionWidget)

    def retranslateUi(self, StarPositionWidget):
        StarPositionWidget.setWindowTitle(_translate("StarPositionWidget", "Star Positions", None))
        self.label_7.setText(_translate("StarPositionWidget", "Phase", None))
        self.plot_btn.setText(_translate("StarPositionWidget", "Plot", None))
        self.roche_chk.setText(_translate("StarPositionWidget", "Critical Roche Potentials", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("StarPositionWidget", "Single Plot", None))
        self.message_label.setText(_translate("StarPositionWidget", "Ready", None))
        self.dpi_combobox.setItemText(0, _translate("StarPositionWidget", "64dpi", None))
        self.dpi_combobox.setItemText(1, _translate("StarPositionWidget", "128dpi", None))
        self.dpi_combobox.setItemText(2, _translate("StarPositionWidget", "256dpi", None))
        self.label_8.setText(_translate("StarPositionWidget", "Resolution", None))
        self.label_4.setText(_translate("StarPositionWidget", "Axis Min", None))
        self.label_5.setText(_translate("StarPositionWidget", "Axis Max", None))
        self.render_btn.setText(_translate("StarPositionWidget", "Render", None))
        self.single_chk.setText(_translate("StarPositionWidget", "Single", None))
        self.saveall_btn.setText(_translate("StarPositionWidget", "Save All", None))
        self.saveframe_btn.setText(_translate("StarPositionWidget", "Save Frame", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("StarPositionWidget", "Animation", None))

