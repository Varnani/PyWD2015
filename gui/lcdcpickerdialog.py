# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'lcdcpickerdialog.ui'
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

class Ui_LCDCPickerDialog(object):
    def setupUi(self, LCDCPickerDialog):
        LCDCPickerDialog.setObjectName(_fromUtf8("LCDCPickerDialog"))
        LCDCPickerDialog.resize(680, 450)
        LCDCPickerDialog.setMinimumSize(QtCore.QSize(680, 450))
        LCDCPickerDialog.setMaximumSize(QtCore.QSize(680, 450))
        self.label = QtGui.QLabel(LCDCPickerDialog)
        self.label.setGeometry(QtCore.QRect(20, 0, 281, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.line = QtGui.QFrame(LCDCPickerDialog)
        self.line.setGeometry(QtCore.QRect(20, 30, 641, 21))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.label_2 = QtGui.QLabel(LCDCPickerDialog)
        self.label_2.setGeometry(QtCore.QRect(20, 50, 641, 141))
        self.label_2.setTextFormat(QtCore.Qt.PlainText)
        self.label_2.setScaledContents(False)
        self.label_2.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignTop)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.pickdc_btn = QtGui.QPushButton(LCDCPickerDialog)
        self.pickdc_btn.setGeometry(QtCore.QRect(560, 230, 98, 31))
        self.pickdc_btn.setObjectName(_fromUtf8("pickdc_btn"))
        self.label_67 = QtGui.QLabel(LCDCPickerDialog)
        self.label_67.setGeometry(QtCore.QRect(20, 230, 71, 31))
        self.label_67.setObjectName(_fromUtf8("label_67"))
        self.dcpath_label = QtGui.QLabel(LCDCPickerDialog)
        self.dcpath_label.setGeometry(QtCore.QRect(100, 230, 441, 31))
        self.dcpath_label.setText(_fromUtf8(""))
        self.dcpath_label.setObjectName(_fromUtf8("dcpath_label"))
        self.label_65 = QtGui.QLabel(LCDCPickerDialog)
        self.label_65.setGeometry(QtCore.QRect(140, 320, 111, 31))
        self.label_65.setObjectName(_fromUtf8("label_65"))
        self.lineEdit = QtGui.QLineEdit(LCDCPickerDialog)
        self.lineEdit.setGeometry(QtCore.QRect(280, 280, 261, 30))
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.lineEdit_2 = QtGui.QLineEdit(LCDCPickerDialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(280, 320, 261, 30))
        self.lineEdit_2.setReadOnly(True)
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.label_66 = QtGui.QLabel(LCDCPickerDialog)
        self.label_66.setGeometry(QtCore.QRect(140, 280, 101, 31))
        self.label_66.setObjectName(_fromUtf8("label_66"))
        self.save_btn = QtGui.QPushButton(LCDCPickerDialog)
        self.save_btn.setGeometry(QtCore.QRect(130, 380, 200, 50))
        self.save_btn.setObjectName(_fromUtf8("save_btn"))
        self.exit_btn = QtGui.QPushButton(LCDCPickerDialog)
        self.exit_btn.setGeometry(QtCore.QRect(350, 380, 200, 50))
        self.exit_btn.setObjectName(_fromUtf8("exit_btn"))
        self.picklc_btn = QtGui.QPushButton(LCDCPickerDialog)
        self.picklc_btn.setGeometry(QtCore.QRect(560, 189, 98, 31))
        self.picklc_btn.setObjectName(_fromUtf8("picklc_btn"))
        self.label_68 = QtGui.QLabel(LCDCPickerDialog)
        self.label_68.setGeometry(QtCore.QRect(20, 189, 71, 31))
        self.label_68.setObjectName(_fromUtf8("label_68"))
        self.lcpath_label = QtGui.QLabel(LCDCPickerDialog)
        self.lcpath_label.setGeometry(QtCore.QRect(100, 190, 441, 31))
        self.lcpath_label.setText(_fromUtf8(""))
        self.lcpath_label.setObjectName(_fromUtf8("lcpath_label"))

        self.retranslateUi(LCDCPickerDialog)
        QtCore.QMetaObject.connectSlotsByName(LCDCPickerDialog)

    def retranslateUi(self, LCDCPickerDialog):
        LCDCPickerDialog.setWindowTitle(_translate("LCDCPickerDialog", "PyWD2015", None))
        self.label.setText(_translate("LCDCPickerDialog", "Welcome to PyWD2015", None))
        self.label_2.setText(_translate("LCDCPickerDialog", "PyWD2015 is a GUI for LC and DC programs of Wilson - Devinney eclipsing binary modeling software. PyWD2015 needs these programs to function. Please provide their paths below.\n"
"\n"
"If you got this program from the GitHub release page, you probably have them in /PyWD2015/wd/ path with necessary files. If you don\'t, you can grab them from GitHub or compile the source code from WD Homepage yourself.", None))
        self.pickdc_btn.setText(_translate("LCDCPickerDialog", "Pick File", None))
        self.label_67.setText(_translate("LCDCPickerDialog", "DC Binary:", None))
        self.label_65.setText(_translate("LCDCPickerDialog", "WD Homepage:", None))
        self.lineEdit.setText(_translate("LCDCPickerDialog", "github.com/Varnani/PyWD2015", None))
        self.lineEdit_2.setText(_translate("LCDCPickerDialog", "ftp://ftp.astro.ufl.edu/pub/wilson/", None))
        self.label_66.setText(_translate("LCDCPickerDialog", "GitHub:", None))
        self.save_btn.setText(_translate("LCDCPickerDialog", "Save", None))
        self.exit_btn.setText(_translate("LCDCPickerDialog", "Exit", None))
        self.picklc_btn.setText(_translate("LCDCPickerDialog", "Pick File", None))
        self.label_68.setText(_translate("LCDCPickerDialog", "LC Binary:", None))

