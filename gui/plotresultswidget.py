# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plotresultswidget.ui'
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

class Ui_PlotResultsWidget(object):
    def setupUi(self, PlotResultsWidget):
        PlotResultsWidget.setObjectName(_fromUtf8("PlotResultsWidget"))
        PlotResultsWidget.resize(800, 700)
        PlotResultsWidget.setMinimumSize(QtCore.QSize(800, 700))
        PlotResultsWidget.setMaximumSize(QtCore.QSize(800, 700))
        self.line = QtGui.QFrame(PlotResultsWidget)
        self.line.setGeometry(QtCore.QRect(10, 51, 781, 31))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.label = QtGui.QLabel(PlotResultsWidget)
        self.label.setGeometry(QtCore.QRect(10, 440, 71, 31))
        self.label.setObjectName(_fromUtf8("label"))
        self.line_2 = QtGui.QFrame(PlotResultsWidget)
        self.line_2.setGeometry(QtCore.QRect(80, 440, 711, 31))
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.data_combobox = QtGui.QComboBox(PlotResultsWidget)
        self.data_combobox.setGeometry(QtCore.QRect(10, 23, 251, 30))
        self.data_combobox.setObjectName(_fromUtf8("data_combobox"))
        self.plot_btn = QtGui.QPushButton(PlotResultsWidget)
        self.plot_btn.setGeometry(QtCore.QRect(275, 20, 100, 35))
        self.plot_btn.setObjectName(_fromUtf8("plot_btn"))
        self.autoupdate_chk = QtGui.QCheckBox(PlotResultsWidget)
        self.autoupdate_chk.setGeometry(QtCore.QRect(390, 27, 111, 21))
        self.autoupdate_chk.setObjectName(_fromUtf8("autoupdate_chk"))
        self.popmain_btn = QtGui.QPushButton(PlotResultsWidget)
        self.popmain_btn.setGeometry(QtCore.QRect(560, 20, 100, 35))
        self.popmain_btn.setObjectName(_fromUtf8("popmain_btn"))
        self.popresiduals_btn = QtGui.QPushButton(PlotResultsWidget)
        self.popresiduals_btn.setGeometry(QtCore.QRect(670, 20, 101, 35))
        self.popresiduals_btn.setObjectName(_fromUtf8("popresiduals_btn"))
        self.line_3 = QtGui.QFrame(PlotResultsWidget)
        self.line_3.setGeometry(QtCore.QRect(500, 17, 61, 41))
        self.line_3.setFrameShape(QtGui.QFrame.VLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.mainwidget = QtGui.QWidget(PlotResultsWidget)
        self.mainwidget.setGeometry(QtCore.QRect(10, 70, 781, 371))
        self.mainwidget.setObjectName(_fromUtf8("mainwidget"))
        self.residualwidget = QtGui.QWidget(PlotResultsWidget)
        self.residualwidget.setGeometry(QtCore.QRect(10, 470, 781, 221))
        self.residualwidget.setObjectName(_fromUtf8("residualwidget"))

        self.retranslateUi(PlotResultsWidget)
        QtCore.QMetaObject.connectSlotsByName(PlotResultsWidget)

    def retranslateUi(self, PlotResultsWidget):
        PlotResultsWidget.setWindowTitle(_translate("PlotResultsWidget", "Plot Results", None))
        self.label.setText(_translate("PlotResultsWidget", "Residuals", None))
        self.plot_btn.setText(_translate("PlotResultsWidget", "Plot", None))
        self.autoupdate_chk.setText(_translate("PlotResultsWidget", "Auto update", None))
        self.popmain_btn.setText(_translate("PlotResultsWidget", "Pop Main", None))
        self.popresiduals_btn.setText(_translate("PlotResultsWidget", "Pop Residuals", None))

