# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dimensionwidget.ui'
#
# Created: Wed Jul 25 16:20:19 2018
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

class Ui_DimensionWidget(object):
    def setupUi(self, DimensionWidget):
        DimensionWidget.setObjectName(_fromUtf8("DimensionWidget"))
        DimensionWidget.resize(750, 600)
        self.horizontalLayout = QtGui.QHBoxLayout(DimensionWidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.s2_pole_chk = QtGui.QCheckBox(DimensionWidget)
        self.s2_pole_chk.setText(_fromUtf8(""))
        self.s2_pole_chk.setChecked(True)
        self.s2_pole_chk.setObjectName(_fromUtf8("s2_pole_chk"))
        self.gridLayout_2.addWidget(self.s2_pole_chk, 2, 1, 1, 1)
        self.label_10 = QtGui.QLabel(DimensionWidget)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(144, 141, 139))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.label_10.setPalette(palette)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout_2.addWidget(self.label_10, 4, 0, 1, 1)
        self.label_9 = QtGui.QLabel(DimensionWidget)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(144, 141, 139))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.label_9.setPalette(palette)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout_2.addWidget(self.label_9, 2, 0, 1, 1)
        self.label_7 = QtGui.QLabel(DimensionWidget)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(144, 141, 139))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.label_7.setPalette(palette)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_2.addWidget(self.label_7, 5, 0, 1, 1)
        self.s2_back_chk = QtGui.QCheckBox(DimensionWidget)
        self.s2_back_chk.setText(_fromUtf8(""))
        self.s2_back_chk.setObjectName(_fromUtf8("s2_back_chk"))
        self.gridLayout_2.addWidget(self.s2_back_chk, 5, 1, 1, 1)
        self.label_8 = QtGui.QLabel(DimensionWidget)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout_2.addWidget(self.label_8, 3, 0, 1, 1)
        self.s2_side_chk = QtGui.QCheckBox(DimensionWidget)
        self.s2_side_chk.setText(_fromUtf8(""))
        self.s2_side_chk.setObjectName(_fromUtf8("s2_side_chk"))
        self.gridLayout_2.addWidget(self.s2_side_chk, 4, 1, 1, 1)
        self.s2_point_chk = QtGui.QCheckBox(DimensionWidget)
        self.s2_point_chk.setText(_fromUtf8(""))
        self.s2_point_chk.setObjectName(_fromUtf8("s2_point_chk"))
        self.gridLayout_2.addWidget(self.s2_point_chk, 3, 1, 1, 1)
        self.line_3 = QtGui.QFrame(DimensionWidget)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.gridLayout_2.addWidget(self.line_3, 1, 0, 1, 2)
        self.label_2 = QtGui.QLabel(DimensionWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 2)
        self.gridLayout_3.addLayout(self.gridLayout_2, 3, 0, 1, 1)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.s1_side_chk = QtGui.QCheckBox(DimensionWidget)
        self.s1_side_chk.setText(_fromUtf8(""))
        self.s1_side_chk.setObjectName(_fromUtf8("s1_side_chk"))
        self.gridLayout.addWidget(self.s1_side_chk, 4, 1, 1, 1)
        self.label_6 = QtGui.QLabel(DimensionWidget)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(144, 141, 139))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.label_6.setPalette(palette)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 5, 0, 1, 1)
        self.s1_pole_chk = QtGui.QCheckBox(DimensionWidget)
        self.s1_pole_chk.setText(_fromUtf8(""))
        self.s1_pole_chk.setChecked(True)
        self.s1_pole_chk.setObjectName(_fromUtf8("s1_pole_chk"))
        self.gridLayout.addWidget(self.s1_pole_chk, 2, 1, 1, 1)
        self.s1_back_chk = QtGui.QCheckBox(DimensionWidget)
        self.s1_back_chk.setText(_fromUtf8(""))
        self.s1_back_chk.setObjectName(_fromUtf8("s1_back_chk"))
        self.gridLayout.addWidget(self.s1_back_chk, 5, 1, 1, 1)
        self.label_4 = QtGui.QLabel(DimensionWidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.label_3 = QtGui.QLabel(DimensionWidget)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(144, 141, 139))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.label_3.setPalette(palette)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.s1_point_chk = QtGui.QCheckBox(DimensionWidget)
        self.s1_point_chk.setText(_fromUtf8(""))
        self.s1_point_chk.setObjectName(_fromUtf8("s1_point_chk"))
        self.gridLayout.addWidget(self.s1_point_chk, 3, 1, 1, 1)
        self.label_5 = QtGui.QLabel(DimensionWidget)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(144, 141, 139))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.label_5.setPalette(palette)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)
        self.line_2 = QtGui.QFrame(DimensionWidget)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout.addWidget(self.line_2, 1, 0, 1, 2)
        self.label = QtGui.QLabel(DimensionWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        self.gridLayout_3.addLayout(self.gridLayout, 1, 0, 1, 1)
        self.line = QtGui.QFrame(DimensionWidget)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout_3.addWidget(self.line, 2, 0, 1, 3)
        self.plot_btn = QtGui.QPushButton(DimensionWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plot_btn.sizePolicy().hasHeightForWidth())
        self.plot_btn.setSizePolicy(sizePolicy)
        self.plot_btn.setObjectName(_fromUtf8("plot_btn"))
        self.gridLayout_3.addWidget(self.plot_btn, 0, 2, 1, 1)
        self.s1_plot_widget = QtGui.QWidget(DimensionWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.s1_plot_widget.sizePolicy().hasHeightForWidth())
        self.s1_plot_widget.setSizePolicy(sizePolicy)
        self.s1_plot_widget.setMinimumSize(QtCore.QSize(300, 200))
        self.s1_plot_widget.setObjectName(_fromUtf8("s1_plot_widget"))
        self.gridLayout_3.addWidget(self.s1_plot_widget, 1, 1, 1, 2)
        self.s2_plot_widget = QtGui.QWidget(DimensionWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.s2_plot_widget.sizePolicy().hasHeightForWidth())
        self.s2_plot_widget.setSizePolicy(sizePolicy)
        self.s2_plot_widget.setMinimumSize(QtCore.QSize(300, 200))
        self.s2_plot_widget.setObjectName(_fromUtf8("s2_plot_widget"))
        self.gridLayout_3.addWidget(self.s2_plot_widget, 3, 1, 1, 2)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 0, 1, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout_3)

        self.retranslateUi(DimensionWidget)
        QtCore.QMetaObject.connectSlotsByName(DimensionWidget)

    def retranslateUi(self, DimensionWidget):
        DimensionWidget.setWindowTitle(_translate("DimensionWidget", "Component Dimensions", None))
        self.label_10.setText(_translate("DimensionWidget", "Side", None))
        self.label_9.setText(_translate("DimensionWidget", "Pole", None))
        self.label_7.setText(_translate("DimensionWidget", "Back", None))
        self.label_8.setText(_translate("DimensionWidget", "Point", None))
        self.label_2.setText(_translate("DimensionWidget", "Star 2", None))
        self.label_6.setText(_translate("DimensionWidget", "Back", None))
        self.label_4.setText(_translate("DimensionWidget", "Point", None))
        self.label_3.setText(_translate("DimensionWidget", "Pole", None))
        self.label_5.setText(_translate("DimensionWidget", "Side", None))
        self.label.setText(_translate("DimensionWidget", "Star 1", None))
        self.plot_btn.setText(_translate("DimensionWidget", "Calculate Component Radii", None))
