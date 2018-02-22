# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'outputview.ui'
#
# Created: Thu Feb 22 11:23:55 2018
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

class Ui_OutputView(object):
    def setupUi(self, OutputView):
        OutputView.setObjectName(_fromUtf8("OutputView"))
        OutputView.resize(500, 250)
        OutputView.setMinimumSize(QtCore.QSize(500, 250))
        self.horizontalLayout = QtGui.QHBoxLayout(OutputView)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.output_textedit = QtGui.QPlainTextEdit(OutputView)
        self.output_textedit.setLineWrapMode(QtGui.QPlainTextEdit.NoWrap)
        self.output_textedit.setReadOnly(True)
        self.output_textedit.setObjectName(_fromUtf8("output_textedit"))
        self.horizontalLayout.addWidget(self.output_textedit)

        self.retranslateUi(OutputView)
        QtCore.QMetaObject.connectSlotsByName(OutputView)

    def retranslateUi(self, OutputView):
        OutputView.setWindowTitle(_translate("OutputView", "///", None))

