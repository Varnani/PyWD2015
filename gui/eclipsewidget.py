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
        EclipseWidget.resize(330, 640)
        EclipseWidget.setMinimumSize(QtCore.QSize(330, 640))
        EclipseWidget.setMaximumSize(QtCore.QSize(330, 640))
        self.label_53 = QtGui.QLabel(EclipseWidget)
        self.label_53.setGeometry(QtCore.QRect(10, 0, 711, 31))
        self.label_53.setObjectName(_fromUtf8("label_53"))
        self.line_12 = QtGui.QFrame(EclipseWidget)
        self.line_12.setGeometry(QtCore.QRect(10, 20, 311, 21))
        self.line_12.setFrameShape(QtGui.QFrame.HLine)
        self.line_12.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_12.setObjectName(_fromUtf8("line_12"))
        self.iftime_chk = QtGui.QCheckBox(EclipseWidget)
        self.iftime_chk.setGeometry(QtCore.QRect(10, 40, 231, 21))
        self.iftime_chk.setObjectName(_fromUtf8("iftime_chk"))
        self.load_btn = QtGui.QPushButton(EclipseWidget)
        self.load_btn.setGeometry(QtCore.QRect(10, 520, 311, 50))
        self.load_btn.setObjectName(_fromUtf8("load_btn"))
        self.datawidget = QtGui.QTreeWidget(EclipseWidget)
        self.datawidget.setGeometry(QtCore.QRect(10, 160, 311, 351))
        self.datawidget.setObjectName(_fromUtf8("datawidget"))
        self.clear_btn = QtGui.QPushButton(EclipseWidget)
        self.clear_btn.setGeometry(QtCore.QRect(10, 580, 311, 50))
        self.clear_btn.setObjectName(_fromUtf8("clear_btn"))
        self.label = QtGui.QLabel(EclipseWidget)
        self.label.setGeometry(QtCore.QRect(10, 110, 141, 21))
        self.label.setObjectName(_fromUtf8("label"))
        self.filepath_label = QtGui.QLabel(EclipseWidget)
        self.filepath_label.setGeometry(QtCore.QRect(10, 130, 311, 31))
        self.filepath_label.setObjectName(_fromUtf8("filepath_label"))
        self.ksd_box = QtGui.QSpinBox(EclipseWidget)
        self.ksd_box.setGeometry(QtCore.QRect(40, 69, 51, 22))
        self.ksd_box.setButtonSymbols(QtGui.QAbstractSpinBox.UpDownArrows)
        self.ksd_box.setMinimum(1)
        self.ksd_box.setMaximum(3)
        self.ksd_box.setProperty("value", 1)
        self.ksd_box.setObjectName(_fromUtf8("ksd_box"))
        self.label_16 = QtGui.QLabel(EclipseWidget)
        self.label_16.setGeometry(QtCore.QRect(10, 70, 41, 20))
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.label_11 = QtGui.QLabel(EclipseWidget)
        self.label_11.setGeometry(QtCore.QRect(190, 70, 51, 20))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.sigma_ipt = QtGui.QLineEdit(EclipseWidget)
        self.sigma_ipt.setGeometry(QtCore.QRect(250, 70, 71, 21))
        self.sigma_ipt.setObjectName(_fromUtf8("sigma_ipt"))
        self.line_13 = QtGui.QFrame(EclipseWidget)
        self.line_13.setGeometry(QtCore.QRect(10, 90, 311, 21))
        self.line_13.setFrameShape(QtGui.QFrame.HLine)
        self.line_13.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_13.setObjectName(_fromUtf8("line_13"))

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
        self.label_16.setToolTip(_translate("EclipseWidget", "Set standard deviation apply method. [?]", None))
        self.label_16.setWhatsThis(_translate("EclipseWidget", "<html><head/><body><p>An integer array that is 0, 1, or 2 for each input sub-dataset (velocity, light, or eclipse timings). </p><p>The KSDs tell DC whether to apply the input standard deviations (σ’s) to compute curvedependent weights (KSD=0), </p><p>to apply DC’s internally computed σ’s for the weights (KSD=1),</p><p>or to apply σ’s based on one or two restricted phase ranges for the weights (KSD=2).</p><p><span style=\" font-weight:600;\">If unsure, set to 1.</span></p></body></html>", None))
        self.label_16.setText(_translate("EclipseWidget", "KSD", None))
        self.label_11.setToolTip(_translate("EclipseWidget", "Estimated standard deviation of observed light", None))
        self.label_11.setText(_translate("EclipseWidget", "SIGMA", None))
        self.sigma_ipt.setText(_translate("EclipseWidget", "0", None))

