# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interfaces/pywd/editlightcurvedialog.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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

class Ui_EditLightCurveDialog(object):
    def setupUi(self, EditLightCurveDialog):
        EditLightCurveDialog.setObjectName(_fromUtf8("EditLightCurveDialog"))
        EditLightCurveDialog.resize(330, 560)
        EditLightCurveDialog.setMinimumSize(QtCore.QSize(330, 560))
        EditLightCurveDialog.setMaximumSize(QtCore.QSize(330, 560))
        self.accept_btn = QtGui.QPushButton(EditLightCurveDialog)
        self.accept_btn.setGeometry(QtCore.QRect(10, 510, 151, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.accept_btn.setFont(font)
        self.accept_btn.setObjectName(_fromUtf8("accept_btn"))
        self.datawidget = QtGui.QTreeWidget(EditLightCurveDialog)
        self.datawidget.setGeometry(QtCore.QRect(10, 190, 311, 311))
        self.datawidget.setObjectName(_fromUtf8("datawidget"))
        self.label = QtGui.QLabel(EditLightCurveDialog)
        self.label.setGeometry(QtCore.QRect(10, 138, 111, 20))
        self.label.setObjectName(_fromUtf8("label"))
        self.filepath_label = QtGui.QLabel(EditLightCurveDialog)
        self.filepath_label.setGeometry(QtCore.QRect(10, 160, 311, 20))
        self.filepath_label.setObjectName(_fromUtf8("filepath_label"))
        self.discard_btn = QtGui.QPushButton(EditLightCurveDialog)
        self.discard_btn.setGeometry(QtCore.QRect(170, 510, 151, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.discard_btn.setFont(font)
        self.discard_btn.setObjectName(_fromUtf8("discard_btn"))
        self.band_box = QtGui.QSpinBox(EditLightCurveDialog)
        self.band_box.setGeometry(QtCore.QRect(50, 10, 31, 22))
        self.band_box.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.band_box.setMinimum(1)
        self.band_box.setMaximum(94)
        self.band_box.setProperty("value", 7)
        self.band_box.setObjectName(_fromUtf8("band_box"))
        self.label_2 = QtGui.QLabel(EditLightCurveDialog)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 41, 21))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.l1_ipt = QtGui.QLineEdit(EditLightCurveDialog)
        self.l1_ipt.setGeometry(QtCore.QRect(190, 10, 51, 20))
        self.l1_ipt.setObjectName(_fromUtf8("l1_ipt"))
        self.label_3 = QtGui.QLabel(EditLightCurveDialog)
        self.label_3.setGeometry(QtCore.QRect(170, 10, 16, 21))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(EditLightCurveDialog)
        self.label_4.setGeometry(QtCore.QRect(250, 10, 16, 21))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.l2_ipt = QtGui.QLineEdit(EditLightCurveDialog)
        self.l2_ipt.setGeometry(QtCore.QRect(270, 10, 51, 20))
        self.l2_ipt.setObjectName(_fromUtf8("l2_ipt"))
        self.x2_ipt = QtGui.QLineEdit(EditLightCurveDialog)
        self.x2_ipt.setGeometry(QtCore.QRect(110, 40, 51, 20))
        self.x2_ipt.setObjectName(_fromUtf8("x2_ipt"))
        self.label_5 = QtGui.QLabel(EditLightCurveDialog)
        self.label_5.setGeometry(QtCore.QRect(10, 40, 16, 21))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.x1_ipt = QtGui.QLineEdit(EditLightCurveDialog)
        self.x1_ipt.setGeometry(QtCore.QRect(30, 40, 51, 20))
        self.x1_ipt.setObjectName(_fromUtf8("x1_ipt"))
        self.label_6 = QtGui.QLabel(EditLightCurveDialog)
        self.label_6.setGeometry(QtCore.QRect(90, 40, 16, 21))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.label_7 = QtGui.QLabel(EditLightCurveDialog)
        self.label_7.setGeometry(QtCore.QRect(170, 40, 16, 21))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.y2_ipt = QtGui.QLineEdit(EditLightCurveDialog)
        self.y2_ipt.setGeometry(QtCore.QRect(270, 40, 51, 20))
        self.y2_ipt.setObjectName(_fromUtf8("y2_ipt"))
        self.label_8 = QtGui.QLabel(EditLightCurveDialog)
        self.label_8.setGeometry(QtCore.QRect(250, 40, 16, 21))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.y1_ipt = QtGui.QLineEdit(EditLightCurveDialog)
        self.y1_ipt.setGeometry(QtCore.QRect(190, 40, 51, 20))
        self.y1_ipt.setObjectName(_fromUtf8("y1_ipt"))
        self.label_9 = QtGui.QLabel(EditLightCurveDialog)
        self.label_9.setGeometry(QtCore.QRect(10, 110, 31, 21))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.opsf_ipt = QtGui.QLineEdit(EditLightCurveDialog)
        self.opsf_ipt.setGeometry(QtCore.QRect(145, 110, 51, 20))
        self.opsf_ipt.setObjectName(_fromUtf8("opsf_ipt"))
        self.label_10 = QtGui.QLabel(EditLightCurveDialog)
        self.label_10.setGeometry(QtCore.QRect(110, 110, 31, 21))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.el3a_ipt = QtGui.QLineEdit(EditLightCurveDialog)
        self.el3a_ipt.setGeometry(QtCore.QRect(40, 110, 51, 20))
        self.el3a_ipt.setObjectName(_fromUtf8("el3a_ipt"))
        self.label_11 = QtGui.QLabel(EditLightCurveDialog)
        self.label_11.setGeometry(QtCore.QRect(230, 110, 41, 21))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.sigma_ipt = QtGui.QLineEdit(EditLightCurveDialog)
        self.sigma_ipt.setGeometry(QtCore.QRect(270, 110, 51, 20))
        self.sigma_ipt.setObjectName(_fromUtf8("sigma_ipt"))
        self.e3_ipt = QtGui.QLineEdit(EditLightCurveDialog)
        self.e3_ipt.setGeometry(QtCore.QRect(190, 70, 51, 20))
        self.e3_ipt.setObjectName(_fromUtf8("e3_ipt"))
        self.label_12 = QtGui.QLabel(EditLightCurveDialog)
        self.label_12.setGeometry(QtCore.QRect(10, 70, 16, 21))
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.label_13 = QtGui.QLabel(EditLightCurveDialog)
        self.label_13.setGeometry(QtCore.QRect(250, 70, 16, 21))
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.label_14 = QtGui.QLabel(EditLightCurveDialog)
        self.label_14.setGeometry(QtCore.QRect(170, 70, 16, 21))
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.e2_ipt = QtGui.QLineEdit(EditLightCurveDialog)
        self.e2_ipt.setGeometry(QtCore.QRect(110, 70, 51, 20))
        self.e2_ipt.setObjectName(_fromUtf8("e2_ipt"))
        self.e4_ipt = QtGui.QLineEdit(EditLightCurveDialog)
        self.e4_ipt.setGeometry(QtCore.QRect(270, 70, 51, 20))
        self.e4_ipt.setObjectName(_fromUtf8("e4_ipt"))
        self.label_15 = QtGui.QLabel(EditLightCurveDialog)
        self.label_15.setGeometry(QtCore.QRect(90, 70, 16, 21))
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.e1_ipt = QtGui.QLineEdit(EditLightCurveDialog)
        self.e1_ipt.setGeometry(QtCore.QRect(30, 70, 51, 20))
        self.e1_ipt.setObjectName(_fromUtf8("e1_ipt"))
        self.line = QtGui.QFrame(EditLightCurveDialog)
        self.line.setGeometry(QtCore.QRect(10, 90, 311, 21))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.ksd_box = QtGui.QSpinBox(EditLightCurveDialog)
        self.ksd_box.setGeometry(QtCore.QRect(120, 10, 41, 22))
        self.ksd_box.setButtonSymbols(QtGui.QAbstractSpinBox.UpDownArrows)
        self.ksd_box.setMinimum(1)
        self.ksd_box.setMaximum(3)
        self.ksd_box.setProperty("value", 1)
        self.ksd_box.setObjectName(_fromUtf8("ksd_box"))
        self.label_16 = QtGui.QLabel(EditLightCurveDialog)
        self.label_16.setGeometry(QtCore.QRect(90, 10, 41, 21))
        self.label_16.setObjectName(_fromUtf8("label_16"))

        self.retranslateUi(EditLightCurveDialog)
        QtCore.QMetaObject.connectSlotsByName(EditLightCurveDialog)

    def retranslateUi(self, EditLightCurveDialog):
        EditLightCurveDialog.setWindowTitle(_translate("EditLightCurveDialog", "Edit Light Curve", None))
        self.accept_btn.setText(_translate("EditLightCurveDialog", "Accept", None))
        self.datawidget.headerItem().setText(0, _translate("EditLightCurveDialog", "Time/Phase", None))
        self.datawidget.headerItem().setText(1, _translate("EditLightCurveDialog", "Observation", None))
        self.datawidget.headerItem().setText(2, _translate("EditLightCurveDialog", "Weight", None))
        self.label.setText(_translate("EditLightCurveDialog", "Data Preview of file:", None))
        self.filepath_label.setText(_translate("EditLightCurveDialog", "FILEPATH//////////////////////////////////", None))
        self.discard_btn.setText(_translate("EditLightCurveDialog", "Discard", None))
        self.label_2.setToolTip(_translate("EditLightCurveDialog", "Band identification number. Check [Bandpass List] table for all available bands and their respective #\'s", None))
        self.label_2.setText(_translate("EditLightCurveDialog", "Band #", None))
        self.l1_ipt.setText(_translate("EditLightCurveDialog", "0", None))
        self.label_3.setToolTip(_translate("EditLightCurveDialog", "Bandpass luminosity for star 1 [HLA]", None))
        self.label_3.setText(_translate("EditLightCurveDialog", "L1", None))
        self.label_4.setToolTip(_translate("EditLightCurveDialog", "Bandpass luminosity for star 2 [CLA]", None))
        self.label_4.setText(_translate("EditLightCurveDialog", "L2", None))
        self.l2_ipt.setText(_translate("EditLightCurveDialog", "0", None))
        self.x2_ipt.setText(_translate("EditLightCurveDialog", "0", None))
        self.label_5.setToolTip(_translate("EditLightCurveDialog", "Wavelength-specific limb darkening coefficient in linear term, for star 1 [X1A] ", None))
        self.label_5.setText(_translate("EditLightCurveDialog", "X1", None))
        self.x1_ipt.setText(_translate("EditLightCurveDialog", "0", None))
        self.label_6.setToolTip(_translate("EditLightCurveDialog", "Wavelength-specific limb darkening coefficient in linear term, for star 2 [X2A] ", None))
        self.label_6.setText(_translate("EditLightCurveDialog", "X2", None))
        self.label_7.setToolTip(_translate("EditLightCurveDialog", "Bandpass-specific limb darkening coefficient in non-linear term, for star 1 [Y1A] ", None))
        self.label_7.setText(_translate("EditLightCurveDialog", "Y1", None))
        self.y2_ipt.setText(_translate("EditLightCurveDialog", "0", None))
        self.label_8.setToolTip(_translate("EditLightCurveDialog", "Bandpass-specific limb darkening coefficient in non-linear term, for star 2 [Y2A] ", None))
        self.label_8.setText(_translate("EditLightCurveDialog", "Y2", None))
        self.y1_ipt.setText(_translate("EditLightCurveDialog", "0", None))
        self.label_9.setToolTip(_translate("EditLightCurveDialog", "Third light", None))
        self.label_9.setText(_translate("EditLightCurveDialog", "EL3A", None))
        self.opsf_ipt.setText(_translate("EditLightCurveDialog", "0", None))
        self.label_10.setToolTip(_translate("EditLightCurveDialog", "Opacity, attenuation of star light by circumstellar matter", None))
        self.label_10.setText(_translate("EditLightCurveDialog", "OPSF", None))
        self.el3a_ipt.setText(_translate("EditLightCurveDialog", "0", None))
        self.label_11.setToolTip(_translate("EditLightCurveDialog", "Estimated standard deviation of observed light", None))
        self.label_11.setText(_translate("EditLightCurveDialog", "SIGMA", None))
        self.sigma_ipt.setText(_translate("EditLightCurveDialog", "0", None))
        self.e3_ipt.setText(_translate("EditLightCurveDialog", "0", None))
        self.label_12.setToolTip(_translate("EditLightCurveDialog", "Phase 1", None))
        self.label_12.setText(_translate("EditLightCurveDialog", "E1", None))
        self.label_13.setToolTip(_translate("EditLightCurveDialog", "Phase 4", None))
        self.label_13.setText(_translate("EditLightCurveDialog", "E4", None))
        self.label_14.setToolTip(_translate("EditLightCurveDialog", "Phase 3", None))
        self.label_14.setText(_translate("EditLightCurveDialog", "E3", None))
        self.e2_ipt.setText(_translate("EditLightCurveDialog", "0", None))
        self.e4_ipt.setText(_translate("EditLightCurveDialog", "0", None))
        self.label_15.setToolTip(_translate("EditLightCurveDialog", "Phase 2", None))
        self.label_15.setText(_translate("EditLightCurveDialog", "E2", None))
        self.e1_ipt.setText(_translate("EditLightCurveDialog", "0", None))
        self.label_16.setToolTip(_translate("EditLightCurveDialog", "Set standard deviation apply method. Check \"?\" for extended explanation.", None))
        self.label_16.setWhatsThis(_translate("EditLightCurveDialog", "<html><head/><body><p>An integer array that is 0, 1, or 2 for each input sub-dataset (velocity, light, or eclipse timings). </p><p>The KSDs tell DC whether to apply the input standard deviations (σ’s) to compute curvedependent weights (KSD=0), </p><p>to apply DC’s internally computed σ’s for the weights (KSD=1),</p><p>or to apply σ’s based on one or two restricted phase ranges for the weights (KSD=2).</p><p><span style=\" font-weight:600;\">If unsure, set to 1.</span></p></body></html>", None))
        self.label_16.setText(_translate("EditLightCurveDialog", "KSD", None))
