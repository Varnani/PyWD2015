# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'spotconfigurewidget.ui'
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

class Ui_SpotConfigureWidget(object):
    def setupUi(self, SpotConfigureWidget):
        SpotConfigureWidget.setObjectName(_fromUtf8("SpotConfigureWidget"))
        SpotConfigureWidget.resize(920, 200)
        SpotConfigureWidget.setMinimumSize(QtCore.QSize(920, 200))
        SpotConfigureWidget.setMaximumSize(QtCore.QSize(920, 200))
        self.label = QtGui.QLabel(SpotConfigureWidget)
        self.label.setGeometry(QtCore.QRect(386, 103, 151, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.line = QtGui.QFrame(SpotConfigureWidget)
        self.line.setGeometry(QtCore.QRect(60, 102, 321, 20))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.label_70 = QtGui.QLabel(SpotConfigureWidget)
        self.label_70.setGeometry(QtCore.QRect(120, 120, 51, 16))
        self.label_70.setObjectName(_fromUtf8("label_70"))
        self.label_76 = QtGui.QLabel(SpotConfigureWidget)
        self.label_76.setGeometry(QtCore.QRect(330, 120, 51, 16))
        self.label_76.setObjectName(_fromUtf8("label_76"))
        self.label_74 = QtGui.QLabel(SpotConfigureWidget)
        self.label_74.setGeometry(QtCore.QRect(190, 120, 51, 16))
        self.label_74.setObjectName(_fromUtf8("label_74"))
        self.label_75 = QtGui.QLabel(SpotConfigureWidget)
        self.label_75.setGeometry(QtCore.QRect(260, 120, 51, 16))
        self.label_75.setObjectName(_fromUtf8("label_75"))
        self.label_71 = QtGui.QLabel(SpotConfigureWidget)
        self.label_71.setGeometry(QtCore.QRect(62, 120, 16, 16))
        self.label_71.setObjectName(_fromUtf8("label_71"))
        self.line_2 = QtGui.QFrame(SpotConfigureWidget)
        self.line_2.setGeometry(QtCore.QRect(540, 102, 321, 20))
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.line_3 = QtGui.QFrame(SpotConfigureWidget)
        self.line_3.setGeometry(QtCore.QRect(441, 130, 41, 61))
        self.line_3.setFrameShape(QtGui.QFrame.VLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.spotconfigsave_btn = QtGui.QPushButton(SpotConfigureWidget)
        self.spotconfigsave_btn.setGeometry(QtCore.QRect(730, 40, 101, 25))
        self.spotconfigsave_btn.setObjectName(_fromUtf8("spotconfigsave_btn"))
        self.spotconfigload_btn = QtGui.QPushButton(SpotConfigureWidget)
        self.spotconfigload_btn.setGeometry(QtCore.QRect(730, 70, 101, 25))
        self.spotconfigload_btn.setObjectName(_fromUtf8("spotconfigload_btn"))
        self.label_2 = QtGui.QLabel(SpotConfigureWidget)
        self.label_2.setGeometry(QtCore.QRect(10, 100, 41, 21))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(SpotConfigureWidget)
        self.label_3.setGeometry(QtCore.QRect(870, 100, 41, 21))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(SpotConfigureWidget)
        self.label_4.setGeometry(QtCore.QRect(10, 120, 16, 21))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_72 = QtGui.QLabel(SpotConfigureWidget)
        self.label_72.setGeometry(QtCore.QRect(93, 120, 16, 16))
        self.label_72.setObjectName(_fromUtf8("label_72"))
        self.label_77 = QtGui.QLabel(SpotConfigureWidget)
        self.label_77.setGeometry(QtCore.QRect(790, 120, 51, 16))
        self.label_77.setObjectName(_fromUtf8("label_77"))
        self.label_78 = QtGui.QLabel(SpotConfigureWidget)
        self.label_78.setGeometry(QtCore.QRect(650, 120, 51, 16))
        self.label_78.setObjectName(_fromUtf8("label_78"))
        self.label_73 = QtGui.QLabel(SpotConfigureWidget)
        self.label_73.setGeometry(QtCore.QRect(522, 120, 16, 16))
        self.label_73.setObjectName(_fromUtf8("label_73"))
        self.label_8 = QtGui.QLabel(SpotConfigureWidget)
        self.label_8.setGeometry(QtCore.QRect(470, 120, 16, 21))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.label_79 = QtGui.QLabel(SpotConfigureWidget)
        self.label_79.setGeometry(QtCore.QRect(720, 120, 51, 16))
        self.label_79.setObjectName(_fromUtf8("label_79"))
        self.label_80 = QtGui.QLabel(SpotConfigureWidget)
        self.label_80.setGeometry(QtCore.QRect(553, 120, 16, 16))
        self.label_80.setObjectName(_fromUtf8("label_80"))
        self.label_81 = QtGui.QLabel(SpotConfigureWidget)
        self.label_81.setGeometry(QtCore.QRect(580, 120, 51, 16))
        self.label_81.setObjectName(_fromUtf8("label_81"))
        self.addspot2_btn = QtGui.QPushButton(SpotConfigureWidget)
        self.addspot2_btn.setGeometry(QtCore.QRect(469, 160, 442, 25))
        self.addspot2_btn.setObjectName(_fromUtf8("addspot2_btn"))
        self.addspot1_btn = QtGui.QPushButton(SpotConfigureWidget)
        self.addspot1_btn.setGeometry(QtCore.QRect(10, 160, 442, 25))
        self.addspot1_btn.setMinimumSize(QtCore.QSize(0, 0))
        self.addspot1_btn.setObjectName(_fromUtf8("addspot1_btn"))
        self.ifsmv1_chk = QtGui.QCheckBox(SpotConfigureWidget)
        self.ifsmv1_chk.setGeometry(QtCore.QRect(240, 40, 150, 20))
        self.ifsmv1_chk.setObjectName(_fromUtf8("ifsmv1_chk"))
        self.fspot1_ipt = QtGui.QDoubleSpinBox(SpotConfigureWidget)
        self.fspot1_ipt.setGeometry(QtCore.QRect(160, 40, 70, 25))
        self.fspot1_ipt.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.fspot1_ipt.setDecimals(4)
        self.fspot1_ipt.setMaximum(99.0)
        self.fspot1_ipt.setSingleStep(1.0)
        self.fspot1_ipt.setProperty("value", 1.0)
        self.fspot1_ipt.setObjectName(_fromUtf8("fspot1_ipt"))
        self.label_5 = QtGui.QLabel(SpotConfigureWidget)
        self.label_5.setGeometry(QtCore.QRect(20, 40, 131, 25))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.ifsmv2_chk = QtGui.QCheckBox(SpotConfigureWidget)
        self.ifsmv2_chk.setGeometry(QtCore.QRect(240, 75, 150, 20))
        self.ifsmv2_chk.setObjectName(_fromUtf8("ifsmv2_chk"))
        self.label_6 = QtGui.QLabel(SpotConfigureWidget)
        self.label_6.setGeometry(QtCore.QRect(20, 70, 131, 25))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.fspot2_ipt = QtGui.QDoubleSpinBox(SpotConfigureWidget)
        self.fspot2_ipt.setGeometry(QtCore.QRect(160, 70, 70, 25))
        self.fspot2_ipt.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.fspot2_ipt.setDecimals(4)
        self.fspot2_ipt.setMaximum(99.0)
        self.fspot2_ipt.setSingleStep(1.0)
        self.fspot2_ipt.setProperty("value", 1.0)
        self.fspot2_ipt.setObjectName(_fromUtf8("fspot2_ipt"))
        self.nomax_combobox = QtGui.QComboBox(SpotConfigureWidget)
        self.nomax_combobox.setGeometry(QtCore.QRect(508, 70, 121, 25))
        self.nomax_combobox.setObjectName(_fromUtf8("nomax_combobox"))
        self.nomax_combobox.addItem(_fromUtf8(""))
        self.nomax_combobox.addItem(_fromUtf8(""))
        self.label_7 = QtGui.QLabel(SpotConfigureWidget)
        self.label_7.setGeometry(QtCore.QRect(510, 40, 111, 20))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.kspot_chk = QtGui.QCheckBox(SpotConfigureWidget)
        self.kspot_chk.setGeometry(QtCore.QRect(400, 75, 91, 20))
        self.kspot_chk.setObjectName(_fromUtf8("kspot_chk"))
        self.kspev_chk = QtGui.QCheckBox(SpotConfigureWidget)
        self.kspev_chk.setGeometry(QtCore.QRect(400, 40, 80, 20))
        self.kspev_chk.setObjectName(_fromUtf8("kspev_chk"))
        self.whatsthis_btn = QtGui.QPushButton(SpotConfigureWidget)
        self.whatsthis_btn.setGeometry(QtCore.QRect(850, 40, 55, 55))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.whatsthis_btn.setFont(font)
        self.whatsthis_btn.setObjectName(_fromUtf8("whatsthis_btn"))
        self.label_9 = QtGui.QLabel(SpotConfigureWidget)
        self.label_9.setGeometry(QtCore.QRect(120, 135, 71, 20))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.label_10 = QtGui.QLabel(SpotConfigureWidget)
        self.label_10.setGeometry(QtCore.QRect(190, 135, 71, 20))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.label_11 = QtGui.QLabel(SpotConfigureWidget)
        self.label_11.setGeometry(QtCore.QRect(260, 135, 71, 20))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.label_12 = QtGui.QLabel(SpotConfigureWidget)
        self.label_12.setGeometry(QtCore.QRect(330, 135, 71, 20))
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.label_13 = QtGui.QLabel(SpotConfigureWidget)
        self.label_13.setGeometry(QtCore.QRect(580, 135, 71, 20))
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.label_14 = QtGui.QLabel(SpotConfigureWidget)
        self.label_14.setGeometry(QtCore.QRect(790, 135, 71, 20))
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.label_15 = QtGui.QLabel(SpotConfigureWidget)
        self.label_15.setGeometry(QtCore.QRect(650, 135, 71, 20))
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.label_16 = QtGui.QLabel(SpotConfigureWidget)
        self.label_16.setGeometry(QtCore.QRect(720, 135, 71, 20))
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.line_5 = QtGui.QFrame(SpotConfigureWidget)
        self.line_5.setGeometry(QtCore.QRect(10, 15, 901, 20))
        self.line_5.setFrameShape(QtGui.QFrame.HLine)
        self.line_5.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_5.setObjectName(_fromUtf8("line_5"))
        self.label_17 = QtGui.QLabel(SpotConfigureWidget)
        self.label_17.setGeometry(QtCore.QRect(20, 5, 191, 20))
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.line_4 = QtGui.QFrame(SpotConfigureWidget)
        self.line_4.setGeometry(QtCore.QRect(655, 35, 61, 71))
        self.line_4.setFrameShape(QtGui.QFrame.VLine)
        self.line_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_4.setObjectName(_fromUtf8("line_4"))

        self.retranslateUi(SpotConfigureWidget)
        QtCore.QMetaObject.connectSlotsByName(SpotConfigureWidget)

    def retranslateUi(self, SpotConfigureWidget):
        SpotConfigureWidget.setWindowTitle(_translate("SpotConfigureWidget", "Configure Spots", None))
        self.label.setText(_translate("SpotConfigureWidget", "Add or Remove Spots", None))
        self.label_70.setToolTip(_translate("SpotConfigureWidget", "Spot latitude", None))
        self.label_70.setText(_translate("SpotConfigureWidget", "LAT", None))
        self.label_76.setToolTip(_translate("SpotConfigureWidget", "Ratio of local spot temperature to local temperature without the spot", None))
        self.label_76.setText(_translate("SpotConfigureWidget", "TEMSP", None))
        self.label_74.setToolTip(_translate("SpotConfigureWidget", "Spot longitude", None))
        self.label_74.setText(_translate("SpotConfigureWidget", "LON", None))
        self.label_75.setToolTip(_translate("SpotConfigureWidget", "<html><head/><body><p>The angular radius of a star spot, in <span style=\" font-weight:600;\">degrees</span></p></body></html>", None))
        self.label_75.setText(_translate("SpotConfigureWidget", "RADSP", None))
        self.label_71.setToolTip(_translate("SpotConfigureWidget", "Set spot for A", None))
        self.label_71.setText(_translate("SpotConfigureWidget", "A", None))
        self.spotconfigsave_btn.setText(_translate("SpotConfigureWidget", "Save Spots", None))
        self.spotconfigload_btn.setText(_translate("SpotConfigureWidget", "Load Spots", None))
        self.label_2.setText(_translate("SpotConfigureWidget", "Star 1", None))
        self.label_3.setText(_translate("SpotConfigureWidget", "Star 2", None))
        self.label_4.setText(_translate("SpotConfigureWidget", "#", None))
        self.label_72.setToolTip(_translate("SpotConfigureWidget", "Set spot for B", None))
        self.label_72.setText(_translate("SpotConfigureWidget", "B", None))
        self.label_77.setToolTip(_translate("SpotConfigureWidget", "Ratio of local spot temperature to local temperature without the spot", None))
        self.label_77.setText(_translate("SpotConfigureWidget", "TEMSP", None))
        self.label_78.setToolTip(_translate("SpotConfigureWidget", "Spot longitude", None))
        self.label_78.setText(_translate("SpotConfigureWidget", "LON", None))
        self.label_73.setToolTip(_translate("SpotConfigureWidget", "Set spot for A", None))
        self.label_73.setText(_translate("SpotConfigureWidget", "A", None))
        self.label_8.setText(_translate("SpotConfigureWidget", "#", None))
        self.label_79.setToolTip(_translate("SpotConfigureWidget", "<html><head/><body><p>The angular radius of a star spot, in <span style=\" font-weight:600;\">degrees</span></p></body></html>", None))
        self.label_79.setText(_translate("SpotConfigureWidget", "RADSP", None))
        self.label_80.setToolTip(_translate("SpotConfigureWidget", "Set spot for B", None))
        self.label_80.setText(_translate("SpotConfigureWidget", "B", None))
        self.label_81.setToolTip(_translate("SpotConfigureWidget", "Spot latitude", None))
        self.label_81.setText(_translate("SpotConfigureWidget", "LAT", None))
        self.addspot2_btn.setText(_translate("SpotConfigureWidget", "Add Spot", None))
        self.addspot1_btn.setText(_translate("SpotConfigureWidget", "Add Spot", None))
        self.ifsmv1_chk.setToolTip(_translate("SpotConfigureWidget", "<html><head/><body><p>Allow spot A to move in longitude (IFSMV1)</p></body></html>", None))
        self.ifsmv1_chk.setText(_translate("SpotConfigureWidget", "Spot A Movement", None))
        self.label_5.setToolTip(_translate("SpotConfigureWidget", "<html><head/><body><p>Spot angular drift rate in longitude for star 1, rate 1.000 means that drift matches the mean orbital angular rate (IFSMV1)</p></body></html>", None))
        self.label_5.setText(_translate("SpotConfigureWidget", "Drift Rate for Star 1", None))
        self.ifsmv2_chk.setToolTip(_translate("SpotConfigureWidget", "<html><head/><body><p>Allow spot B to move in longitude (IFSMV2)</p></body></html>", None))
        self.ifsmv2_chk.setText(_translate("SpotConfigureWidget", "Spot B Movement", None))
        self.label_6.setToolTip(_translate("SpotConfigureWidget", "<html><head/><body><p>Spot angular drift rate in longitude for star 2, rate 1.000 means that drift matches the mean orbital angular rate (IFSMV2)</p></body></html>", None))
        self.label_6.setText(_translate("SpotConfigureWidget", "Drift Rate for Star 2", None))
        self.nomax_combobox.setItemText(0, _translate("SpotConfigureWidget", "Triangular", None))
        self.nomax_combobox.setItemText(1, _translate("SpotConfigureWidget", "Trapezoidal", None))
        self.label_7.setToolTip(_translate("SpotConfigureWidget", "<html><head/><body><p>Spot aging profile (NOMAX) [?]</p></body></html>", None))
        self.label_7.setWhatsThis(_translate("SpotConfigureWidget", "<html><head/><body><p>Tells whether the spot growth and decay timewise profile is trapezoidal or triangular. Setting this to triangular eliminates the interval of constant size that otherwise exists at spot maximum.</p></body></html>", None))
        self.label_7.setText(_translate("SpotConfigureWidget", "Aging Profile", None))
        self.kspot_chk.setToolTip(_translate("SpotConfigureWidget", "<html><head/><body><p>Use &quot;Vector Fractional Area&quot; algorithm (KSPOT) [?]</p></body></html>", None))
        self.kspot_chk.setWhatsThis(_translate("SpotConfigureWidget", "<html><head/><body><p>Controls whether the old simple spot algorithm or the much more precise Vector Fractional Area algorithm <span style=\" font-weight:600;\">(Wilson 2012b)</span> is applied.</p></body></html>", None))
        self.kspot_chk.setText(_translate("SpotConfigureWidget", "Use \"VFA\"", None))
        self.kspev_chk.setToolTip(_translate("SpotConfigureWidget", "<html><head/><body><p>Enable spot aging (KSPEV) [?]</p></body></html>", None))
        self.kspev_chk.setWhatsThis(_translate("SpotConfigureWidget", "<html><head/><body><p>Controls whether spots age (grow and decay) in radius. Currently there is no aging in spot temperature. Uncheck for no aging, check for aging. Solutions for spot aging need good starting estimates for spot parameters and careful monitoring of solution progress.</p></body></html>", None))
        self.kspev_chk.setText(_translate("SpotConfigureWidget", "Aging", None))
        self.whatsthis_btn.setText(_translate("SpotConfigureWidget", "?", None))
        self.label_9.setToolTip(_translate("SpotConfigureWidget", "Onset time of the spot", None))
        self.label_9.setText(_translate("SpotConfigureWidget", "TSTART", None))
        self.label_10.setToolTip(_translate("SpotConfigureWidget", "Start time of the constant maximum", None))
        self.label_10.setText(_translate("SpotConfigureWidget", "TMAX1", None))
        self.label_11.setToolTip(_translate("SpotConfigureWidget", "End time of the constant maximum", None))
        self.label_11.setText(_translate("SpotConfigureWidget", "TMAX2", None))
        self.label_12.setToolTip(_translate("SpotConfigureWidget", "End time of the spot", None))
        self.label_12.setText(_translate("SpotConfigureWidget", "TEND", None))
        self.label_13.setToolTip(_translate("SpotConfigureWidget", "Onset time of the spot", None))
        self.label_13.setText(_translate("SpotConfigureWidget", "TSTART", None))
        self.label_14.setToolTip(_translate("SpotConfigureWidget", "End time of the spot", None))
        self.label_14.setText(_translate("SpotConfigureWidget", "TEND", None))
        self.label_15.setToolTip(_translate("SpotConfigureWidget", "Start time of the constant maximum", None))
        self.label_15.setText(_translate("SpotConfigureWidget", "TMAX1", None))
        self.label_16.setToolTip(_translate("SpotConfigureWidget", "End time of the constant maximum", None))
        self.label_16.setText(_translate("SpotConfigureWidget", "TMAX2", None))
        self.label_17.setText(_translate("SpotConfigureWidget", "Configure spot parameters", None))

