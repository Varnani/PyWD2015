# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'syntheticcurvewidget.ui'
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

class Ui_SyntheticCurveWidget(object):
    def setupUi(self, SyntheticCurveWidget):
        SyntheticCurveWidget.setObjectName(_fromUtf8("SyntheticCurveWidget"))
        SyntheticCurveWidget.resize(900, 650)
        self.gridLayout_3 = QtGui.QGridLayout(SyntheticCurveWidget)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.line = QtGui.QFrame(SyntheticCurveWidget)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout_3.addWidget(self.line, 1, 0, 1, 1)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label = QtGui.QLabel(SyntheticCurveWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 0, 1, 1, 1)
        self.loaded_treewidget = QtGui.QTreeWidget(SyntheticCurveWidget)
        self.loaded_treewidget.setMaximumSize(QtCore.QSize(16777215, 200))
        self.loaded_treewidget.setObjectName(_fromUtf8("loaded_treewidget"))
        self.loaded_treewidget.header().setDefaultSectionSize(120)
        self.gridLayout_2.addWidget(self.loaded_treewidget, 2, 1, 1, 1)
        self.line_2 = QtGui.QFrame(SyntheticCurveWidget)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout_2.addWidget(self.line_2, 1, 1, 1, 1)
        self.synthetic_treewidget = QtGui.QTreeWidget(SyntheticCurveWidget)
        self.synthetic_treewidget.setMaximumSize(QtCore.QSize(16777215, 200))
        self.synthetic_treewidget.setObjectName(_fromUtf8("synthetic_treewidget"))
        self.synthetic_treewidget.header().setDefaultSectionSize(150)
        self.gridLayout_2.addWidget(self.synthetic_treewidget, 2, 3, 1, 1)
        self.line_5 = QtGui.QFrame(SyntheticCurveWidget)
        self.line_5.setFrameShape(QtGui.QFrame.VLine)
        self.line_5.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_5.setObjectName(_fromUtf8("line_5"))
        self.gridLayout_2.addWidget(self.line_5, 2, 2, 1, 1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.add_btn = QtGui.QPushButton(SyntheticCurveWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.add_btn.sizePolicy().hasHeightForWidth())
        self.add_btn.setSizePolicy(sizePolicy)
        self.add_btn.setObjectName(_fromUtf8("add_btn"))
        self.verticalLayout.addWidget(self.add_btn)
        self.edit_btn = QtGui.QPushButton(SyntheticCurveWidget)
        self.edit_btn.setObjectName(_fromUtf8("edit_btn"))
        self.verticalLayout.addWidget(self.edit_btn)
        self.remove_btn = QtGui.QPushButton(SyntheticCurveWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.remove_btn.sizePolicy().hasHeightForWidth())
        self.remove_btn.setSizePolicy(sizePolicy)
        self.remove_btn.setObjectName(_fromUtf8("remove_btn"))
        self.verticalLayout.addWidget(self.remove_btn)
        self.plot_btn = QtGui.QPushButton(SyntheticCurveWidget)
        self.plot_btn.setObjectName(_fromUtf8("plot_btn"))
        self.verticalLayout.addWidget(self.plot_btn)
        self.pop_btn = QtGui.QPushButton(SyntheticCurveWidget)
        self.pop_btn.setObjectName(_fromUtf8("pop_btn"))
        self.verticalLayout.addWidget(self.pop_btn)
        self.gridLayout_2.addLayout(self.verticalLayout, 2, 4, 1, 1)
        self.line_3 = QtGui.QFrame(SyntheticCurveWidget)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.gridLayout_2.addWidget(self.line_3, 1, 3, 1, 2)
        self.label_2 = QtGui.QLabel(SyntheticCurveWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 0, 3, 1, 2)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.plot_widget = QtGui.QWidget(SyntheticCurveWidget)
        self.plot_widget.setMinimumSize(QtCore.QSize(600, 250))
        self.plot_widget.setObjectName(_fromUtf8("plot_widget"))
        self.gridLayout_3.addWidget(self.plot_widget, 2, 0, 1, 1)

        self.retranslateUi(SyntheticCurveWidget)
        QtCore.QMetaObject.connectSlotsByName(SyntheticCurveWidget)

    def retranslateUi(self, SyntheticCurveWidget):
        SyntheticCurveWidget.setWindowTitle(_translate("SyntheticCurveWidget", "Compute Synthetic Curves", None))
        self.label.setText(_translate("SyntheticCurveWidget", "Loaded Curves", None))
        self.loaded_treewidget.headerItem().setText(0, _translate("SyntheticCurveWidget", "Filename", None))
        self.loaded_treewidget.headerItem().setText(1, _translate("SyntheticCurveWidget", "Type", None))
        self.loaded_treewidget.headerItem().setText(2, _translate("SyntheticCurveWidget", "Band", None))
        self.synthetic_treewidget.headerItem().setText(0, _translate("SyntheticCurveWidget", "Type", None))
        self.synthetic_treewidget.headerItem().setText(1, _translate("SyntheticCurveWidget", "Band", None))
        self.add_btn.setText(_translate("SyntheticCurveWidget", "Add ", None))
        self.edit_btn.setText(_translate("SyntheticCurveWidget", "Edit", None))
        self.remove_btn.setText(_translate("SyntheticCurveWidget", "Remove", None))
        self.plot_btn.setText(_translate("SyntheticCurveWidget", "Plot Selected", None))
        self.pop_btn.setText(_translate("SyntheticCurveWidget", "Pop Plot Window", None))
        self.label_2.setText(_translate("SyntheticCurveWidget", "Synthetic Curves", None))

