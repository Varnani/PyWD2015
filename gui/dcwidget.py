# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dcwidget.ui'
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

class Ui_DCWidget(object):
    def setupUi(self, DCWidget):
        DCWidget.setObjectName(_fromUtf8("DCWidget"))
        DCWidget.resize(830, 760)
        DCWidget.setMinimumSize(QtCore.QSize(830, 760))
        DCWidget.setMaximumSize(QtCore.QSize(830, 760))
        self.log_textview = QtGui.QPlainTextEdit(DCWidget)
        self.log_textview.setGeometry(QtCore.QRect(10, 140, 261, 191))
        self.log_textview.setReadOnly(True)
        self.log_textview.setObjectName(_fromUtf8("log_textview"))
        self.treeWidget = QtGui.QTreeWidget(DCWidget)
        self.treeWidget.setGeometry(QtCore.QRect(10, 380, 401, 271))
        self.treeWidget.setObjectName(_fromUtf8("treeWidget"))
        self.rundc2015_btn = QtGui.QPushButton(DCWidget)
        self.rundc2015_btn.setGeometry(QtCore.QRect(220, 20, 191, 81))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.rundc2015_btn.setFont(font)
        self.rundc2015_btn.setObjectName(_fromUtf8("rundc2015_btn"))
        self.pushButton_2 = QtGui.QPushButton(DCWidget)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 710, 191, 41))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_4 = QtGui.QPushButton(DCWidget)
        self.pushButton_4.setGeometry(QtCore.QRect(220, 710, 191, 41))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.label = QtGui.QLabel(DCWidget)
        self.label.setGeometry(QtCore.QRect(10, 110, 101, 31))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(DCWidget)
        self.label_2.setGeometry(QtCore.QRect(10, 350, 321, 31))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.pushButton_5 = QtGui.QPushButton(DCWidget)
        self.pushButton_5.setGeometry(QtCore.QRect(280, 240, 131, 91))
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.pushButton_6 = QtGui.QPushButton(DCWidget)
        self.pushButton_6.setGeometry(QtCore.QRect(280, 140, 131, 91))
        self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))
        self.line = QtGui.QFrame(DCWidget)
        self.line.setGeometry(QtCore.QRect(10, 340, 401, 21))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.line_2 = QtGui.QFrame(DCWidget)
        self.line_2.setGeometry(QtCore.QRect(410, 20, 21, 731))
        self.line_2.setFrameShape(QtGui.QFrame.VLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.configuresubsets_btn_2 = QtGui.QPushButton(DCWidget)
        self.configuresubsets_btn_2.setGeometry(QtCore.QRect(460, 200, 361, 31))
        self.configuresubsets_btn_2.setObjectName(_fromUtf8("configuresubsets_btn_2"))
        self.plainTextEdit = QtGui.QPlainTextEdit(DCWidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(460, 40, 221, 31))
        self.plainTextEdit.setObjectName(_fromUtf8("plainTextEdit"))
        self.configuresubsets_btn_3 = QtGui.QPushButton(DCWidget)
        self.configuresubsets_btn_3.setGeometry(QtCore.QRect(760, 40, 61, 31))
        self.configuresubsets_btn_3.setObjectName(_fromUtf8("configuresubsets_btn_3"))
        self.label_3 = QtGui.QLabel(DCWidget)
        self.label_3.setGeometry(QtCore.QRect(430, 10, 71, 31))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(DCWidget)
        self.label_4.setGeometry(QtCore.QRect(440, 40, 21, 31))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.configuresubsets_btn_4 = QtGui.QPushButton(DCWidget)
        self.configuresubsets_btn_4.setGeometry(QtCore.QRect(760, 80, 61, 31))
        self.configuresubsets_btn_4.setObjectName(_fromUtf8("configuresubsets_btn_4"))
        self.plainTextEdit_2 = QtGui.QPlainTextEdit(DCWidget)
        self.plainTextEdit_2.setGeometry(QtCore.QRect(460, 80, 221, 31))
        self.plainTextEdit_2.setObjectName(_fromUtf8("plainTextEdit_2"))
        self.label_5 = QtGui.QLabel(DCWidget)
        self.label_5.setGeometry(QtCore.QRect(440, 80, 21, 31))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.configuresubsets_btn_5 = QtGui.QPushButton(DCWidget)
        self.configuresubsets_btn_5.setGeometry(QtCore.QRect(760, 120, 61, 31))
        self.configuresubsets_btn_5.setObjectName(_fromUtf8("configuresubsets_btn_5"))
        self.plainTextEdit_3 = QtGui.QPlainTextEdit(DCWidget)
        self.plainTextEdit_3.setGeometry(QtCore.QRect(460, 120, 221, 31))
        self.plainTextEdit_3.setObjectName(_fromUtf8("plainTextEdit_3"))
        self.label_6 = QtGui.QLabel(DCWidget)
        self.label_6.setGeometry(QtCore.QRect(440, 120, 21, 31))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.configuresubsets_btn_6 = QtGui.QPushButton(DCWidget)
        self.configuresubsets_btn_6.setGeometry(QtCore.QRect(760, 160, 61, 31))
        self.configuresubsets_btn_6.setObjectName(_fromUtf8("configuresubsets_btn_6"))
        self.plainTextEdit_4 = QtGui.QPlainTextEdit(DCWidget)
        self.plainTextEdit_4.setGeometry(QtCore.QRect(460, 160, 221, 31))
        self.plainTextEdit_4.setObjectName(_fromUtf8("plainTextEdit_4"))
        self.label_7 = QtGui.QLabel(DCWidget)
        self.label_7.setGeometry(QtCore.QRect(440, 160, 21, 31))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.label_8 = QtGui.QLabel(DCWidget)
        self.label_8.setGeometry(QtCore.QRect(70, 20, 141, 20))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.spinBox = QtGui.QSpinBox(DCWidget)
        self.spinBox.setGeometry(QtCore.QRect(10, 20, 51, 21))
        self.spinBox.setMinimum(1)
        self.spinBox.setObjectName(_fromUtf8("spinBox"))
        self.configuresubsets_btn_7 = QtGui.QPushButton(DCWidget)
        self.configuresubsets_btn_7.setGeometry(QtCore.QRect(690, 40, 61, 31))
        self.configuresubsets_btn_7.setObjectName(_fromUtf8("configuresubsets_btn_7"))
        self.configuresubsets_btn_8 = QtGui.QPushButton(DCWidget)
        self.configuresubsets_btn_8.setGeometry(QtCore.QRect(690, 80, 61, 31))
        self.configuresubsets_btn_8.setObjectName(_fromUtf8("configuresubsets_btn_8"))
        self.configuresubsets_btn_9 = QtGui.QPushButton(DCWidget)
        self.configuresubsets_btn_9.setGeometry(QtCore.QRect(690, 120, 61, 31))
        self.configuresubsets_btn_9.setObjectName(_fromUtf8("configuresubsets_btn_9"))
        self.configuresubsets_btn_10 = QtGui.QPushButton(DCWidget)
        self.configuresubsets_btn_10.setGeometry(QtCore.QRect(690, 160, 61, 31))
        self.configuresubsets_btn_10.setObjectName(_fromUtf8("configuresubsets_btn_10"))
        self.checkBox = QtGui.QCheckBox(DCWidget)
        self.checkBox.setGeometry(QtCore.QRect(10, 50, 181, 25))
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.line_3 = QtGui.QFrame(DCWidget)
        self.line_3.setGeometry(QtCore.QRect(10, 100, 401, 21))
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.checkBox_2 = QtGui.QCheckBox(DCWidget)
        self.checkBox_2.setGeometry(QtCore.QRect(10, 80, 181, 25))
        self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))
        self.pushButton = QtGui.QPushButton(DCWidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 660, 401, 41))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))

        self.retranslateUi(DCWidget)
        QtCore.QMetaObject.connectSlotsByName(DCWidget)

    def retranslateUi(self, DCWidget):
        DCWidget.setWindowTitle(_translate("DCWidget", "DC2015", None))
        self.log_textview.setPlainText(_translate("DCWidget", "Ready", None))
        self.treeWidget.headerItem().setText(0, _translate("DCWidget", "Parameter", None))
        self.treeWidget.headerItem().setText(1, _translate("DCWidget", "Adjustment", None))
        self.treeWidget.headerItem().setText(2, _translate("DCWidget", "Standard Error", None))
        self.rundc2015_btn.setText(_translate("DCWidget", "RUN DC2015", None))
        self.pushButton_2.setText(_translate("DCWidget", "Copy Results to Inputs", None))
        self.pushButton_4.setText(_translate("DCWidget", "Export Results", None))
        self.label.setText(_translate("DCWidget", "Program Log", None))
        self.label_2.setText(_translate("DCWidget", "Differential Correction Results", None))
        self.pushButton_5.setText(_translate("DCWidget", "View dcout.active", None))
        self.pushButton_6.setText(_translate("DCWidget", "View dcin.active", None))
        self.configuresubsets_btn_2.setText(_translate("DCWidget", "Add Subset", None))
        self.configuresubsets_btn_3.setText(_translate("DCWidget", "Remove", None))
        self.label_3.setText(_translate("DCWidget", "Subset #", None))
        self.label_4.setText(_translate("DCWidget", "1", None))
        self.configuresubsets_btn_4.setText(_translate("DCWidget", "Remove", None))
        self.label_5.setText(_translate("DCWidget", "2", None))
        self.configuresubsets_btn_5.setText(_translate("DCWidget", "Remove", None))
        self.label_6.setText(_translate("DCWidget", "3", None))
        self.configuresubsets_btn_6.setText(_translate("DCWidget", "Remove", None))
        self.label_7.setText(_translate("DCWidget", "4", None))
        self.label_8.setText(_translate("DCWidget", "Number of iterations", None))
        self.configuresubsets_btn_7.setText(_translate("DCWidget", "Edit", None))
        self.configuresubsets_btn_8.setText(_translate("DCWidget", "Edit", None))
        self.configuresubsets_btn_9.setText(_translate("DCWidget", "Edit", None))
        self.configuresubsets_btn_10.setText(_translate("DCWidget", "Edit", None))
        self.checkBox.setToolTip(_translate("DCWidget", "<html><head/><body><p>If checked, all input/output operations will be done on memory, so no dcin.active or dcout.active will be written to disk. Memory usage impact should be negligible. <span style=\" font-weight:600;\">Archive functionality cannot be used while this is active.</span></p></body></html>", None))
        self.checkBox.setText(_translate("DCWidget", "Do not generate files", None))
        self.checkBox_2.setToolTip(_translate("DCWidget", "<html><head/><body><p>If checked, a copy of generated dcin/dcout files will also be saved on <span style=\" font-weight:600;\">wd/archive/</span> with <span style=\" font-weight:600;\">[yyyymmdd - hhmmss]</span> format.</p></body></html>", None))
        self.checkBox_2.setText(_translate("DCWidget", "Archive generated files", None))
        self.pushButton.setText(_translate("DCWidget", "Save to Analysis Tool", None))

