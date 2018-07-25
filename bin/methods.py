import ConfigParser
import StringIO
from itertools import izip
from functools import partial
from PyQt4 import QtGui
from bin import classes
import numpy
from scipy.optimize import fsolve


__configver__ = "0.1.0"
__dclcver__ = "2015"


def SaveSpotConfiguration(SpotConfigureWidget):
    parser = ConfigParser.SafeConfigParser()
    # parse spot config
    parser.add_section("Spot Configuration")
    parser.set("Spot Configuration", "ifsmv1", str(SpotConfigureWidget.ifsmv1_chk.isChecked()))
    parser.set("Spot Configuration", "ifsmv2", str(SpotConfigureWidget.ifsmv2_chk.isChecked()))
    parser.set("Spot Configuration", "kspev", str(SpotConfigureWidget.kspev_chk.isChecked()))
    parser.set("Spot Configuration", "kspot", str(SpotConfigureWidget.kspot_chk.isChecked()))
    parser.set("Spot Configuration", "fspot1", str(SpotConfigureWidget.fspot1_ipt.value()))
    parser.set("Spot Configuration", "fspot2", str(SpotConfigureWidget.fspot2_ipt.value()))
    parser.set("Spot Configuration", "nomax", str(SpotConfigureWidget.nomax_combobox.currentIndex()))
    # parse row info
    parser.add_section("Spot Count")
    parser.set("Spot Count", "star 1", str(SpotConfigureWidget.star1RowCount))
    parser.set("Spot Count", "star 2", str(SpotConfigureWidget.star2RowCount))

    # parse actual spot rows
    i = 0
    while i < SpotConfigureWidget.star1RowCount:
        section = "Star 1 Spot " + str(i + 1)
        parser.add_section(section)
        parser.set(section, "a", str(SpotConfigureWidget.star1ElementList[i][1].isChecked()))
        parser.set(section, "b", str(SpotConfigureWidget.star1ElementList[i][2].isChecked()))
        parser.set(section, "latitude", str(SpotConfigureWidget.star1ElementList[i][3].text()))
        parser.set(section, "longitude", str(SpotConfigureWidget.star1ElementList[i][4].text()))
        parser.set(section, "angular radius", str(SpotConfigureWidget.star1ElementList[i][5].text()))
        parser.set(section, "temperature factor", str(SpotConfigureWidget.star1ElementList[i][6].text()))
        parser.set(section, "onset start", str(SpotConfigureWidget.star1ElementList[i][7].text()))
        parser.set(section, "maximum start", str(SpotConfigureWidget.star1ElementList[i][8].text()))
        parser.set(section, "maximum end", str(SpotConfigureWidget.star1ElementList[i][9].text()))
        parser.set(section, "onset end", str(SpotConfigureWidget.star1ElementList[i][10].text()))
        i += 1
    i = 0
    while i < SpotConfigureWidget.star2RowCount:
        section = "Star 2 Spot " + str(i + 1)
        parser.add_section(section)
        parser.set(section, "a", str(SpotConfigureWidget.star2ElementList[i][1].isChecked()))
        parser.set(section, "b", str(SpotConfigureWidget.star2ElementList[i][2].isChecked()))
        parser.set(section, "latitude", str(SpotConfigureWidget.star2ElementList[i][3].text()))
        parser.set(section, "longitude", str(SpotConfigureWidget.star2ElementList[i][4].text()))
        parser.set(section, "angular radius", str(SpotConfigureWidget.star2ElementList[i][5].text()))
        parser.set(section, "temperature factor", str(SpotConfigureWidget.star2ElementList[i][6].text()))
        parser.set(section, "onset start", str(SpotConfigureWidget.star2ElementList[i][7].text()))
        parser.set(section, "maximum start", str(SpotConfigureWidget.star2ElementList[i][8].text()))
        parser.set(section, "maximum end", str(SpotConfigureWidget.star2ElementList[i][9].text()))
        parser.set(section, "onset end", str(SpotConfigureWidget.star2ElementList[i][10].text()))
        i += 1
    return parser


def LoadSpotConfiguration(SpotConfigureWidget, parser):
    clearSpotConfigureWidget(SpotConfigureWidget)
    if parser.getboolean("Spot Configuration", "ifsmv1"):
        SpotConfigureWidget.ifsmv1_chk.toggle()
    if parser.getboolean("Spot Configuration", "ifsmv2"):
        SpotConfigureWidget.ifsmv2_chk.toggle()
    if parser.getboolean("Spot Configuration", "kspev"):
        SpotConfigureWidget.kspev_chk.toggle()
    if parser.getboolean("Spot Configuration", "kspot"):
        SpotConfigureWidget.kspot_chk.toggle()
    SpotConfigureWidget.fspot1_ipt.setValue(parser.getfloat("Spot Configuration", "fspot1"))
    SpotConfigureWidget.fspot2_ipt.setValue(parser.getfloat("Spot Configuration", "fspot2"))
    SpotConfigureWidget.nomax_combobox.setCurrentIndex(parser.getint("Spot Configuration", "nomax"))
    star1spotcount = parser.getint("Spot Count", "star 1")
    star2spotcount = parser.getint("Spot Count", "star 2")
    i = 0
    SpotConfigureWidget.radioButtonGroupA.setExclusive(False)
    SpotConfigureWidget.radioButtonGroupB.setExclusive(False)
    while i < star1spotcount:
        SpotConfigureWidget.addspot1_btn.click()
        section = "Star 1 Spot " + str(i + 1)
        if parser.getboolean(section, "a"):
            SpotConfigureWidget.star1ElementList[i][1].toggle()
        if parser.getboolean(section, "b"):
            SpotConfigureWidget.star1ElementList[i][2].toggle()
        SpotConfigureWidget.star1ElementList[i][3].setText(parser.get(section, "latitude"))
        SpotConfigureWidget.star1ElementList[i][4].setText(parser.get(section, "longitude"))
        SpotConfigureWidget.star1ElementList[i][5].setText(parser.get(section, "angular radius"))
        SpotConfigureWidget.star1ElementList[i][6].setText(parser.get(section, "temperature factor"))
        SpotConfigureWidget.star1ElementList[i][7].setText(parser.get(section, "onset start"))
        SpotConfigureWidget.star1ElementList[i][8].setText(parser.get(section, "maximum start"))
        SpotConfigureWidget.star1ElementList[i][9].setText(parser.get(section, "maximum end"))
        SpotConfigureWidget.star1ElementList[i][10].setText(parser.get(section, "onset end"))
        i += 1
    i = 0
    while i < star2spotcount:
        SpotConfigureWidget.addspot2_btn.click()
        section = "Star 2 Spot " + str(i + 1)
        if parser.getboolean(section, "a"):
            SpotConfigureWidget.star2ElementList[i][1].toggle()
        if parser.getboolean(section, "b"):
            SpotConfigureWidget.star2ElementList[i][2].toggle()
        SpotConfigureWidget.star2ElementList[i][3].setText(parser.get(section, "latitude"))
        SpotConfigureWidget.star2ElementList[i][4].setText(parser.get(section, "longitude"))
        SpotConfigureWidget.star2ElementList[i][5].setText(parser.get(section, "angular radius"))
        SpotConfigureWidget.star2ElementList[i][6].setText(parser.get(section, "temperature factor"))
        SpotConfigureWidget.star2ElementList[i][7].setText(parser.get(section, "onset start"))
        SpotConfigureWidget.star2ElementList[i][8].setText(parser.get(section, "maximum start"))
        SpotConfigureWidget.star2ElementList[i][9].setText(parser.get(section, "maximum end"))
        SpotConfigureWidget.star2ElementList[i][10].setText(parser.get(section, "onset end"))
        i += 1
    SpotConfigureWidget.radioButtonGroupA.setExclusive(True)
    SpotConfigureWidget.radioButtonGroupB.setExclusive(True)


def clearSpotConfigureWidget(SpotConfigureWidget):
    if SpotConfigureWidget.ifsmv1_chk.isChecked():
        SpotConfigureWidget.ifsmv1_chk.toggle()
    if SpotConfigureWidget.ifsmv2_chk.isChecked():
        SpotConfigureWidget.ifsmv2_chk.toggle()
    if SpotConfigureWidget.kspev_chk.isChecked():
        SpotConfigureWidget.kspev_chk.toggle()
    if SpotConfigureWidget.kspot_chk.isChecked():
        SpotConfigureWidget.kspot_chk.toggle()
    SpotConfigureWidget.fspot1_ipt.setValue(1)
    SpotConfigureWidget.fspot1_ipt.setValue(1)
    SpotConfigureWidget.nomax_combobox.setCurrentIndex(0)
    # we'll just click every remove button
    for elementList in reversed(SpotConfigureWidget.star1ElementList):
        elementList[11].click()
    for elementList in reversed(SpotConfigureWidget.star2ElementList):
        elementList[11].click()


def addSpotRow(SpotConfigureWidget, starNumber):
    xshiftAmount = 0
    yshiftAmount = 0
    if starNumber == 1:
        SpotConfigureWidget.star1RowCount += 1
        SpotConfigureWidget.star1ElementList.append([])
        xshiftAmount = 0
        yshiftAmount = 60 * SpotConfigureWidget.star1RowCount
    if starNumber == 2:
        SpotConfigureWidget.star2RowCount += 1
        SpotConfigureWidget.star2ElementList.append([])
        xshiftAmount = 460
        yshiftAmount = 60 * SpotConfigureWidget.star2RowCount
    resizeSpotConfigureWidget(SpotConfigureWidget, starNumber)

    # add elements
    # label
    label = QtGui.QLabel(SpotConfigureWidget)
    label.setGeometry(10 + xshiftAmount, 100 + yshiftAmount, 45, 16)
    if starNumber == 1:
        label.setText("Spot " + str(SpotConfigureWidget.star1RowCount))
        label.setObjectName("star1spotlabel" + str(SpotConfigureWidget.star1RowCount - 1))
        SpotConfigureWidget.star1ElementList[(SpotConfigureWidget.star1RowCount - 1)].append(label)
    if starNumber == 2:
        label.setText("Spot " + str(SpotConfigureWidget.star2RowCount))
        label.setObjectName("star2spotlabel" + str(SpotConfigureWidget.star2RowCount))
        SpotConfigureWidget.star2ElementList[(SpotConfigureWidget.star2RowCount - 1)].append(label)
    label.show()

    # radio buttons
    radioA = QtGui.QRadioButton(SpotConfigureWidget)
    radioB = QtGui.QRadioButton(SpotConfigureWidget)
    radioA.setGeometry(60 + xshiftAmount, 100 + yshiftAmount, 20, 20)
    radioB.setGeometry(90 + xshiftAmount, 100 + yshiftAmount, 20, 20)
    radioA.type = "A"
    radioB.type = "B"
    if starNumber == 1:
        radioA.row = SpotConfigureWidget.star1RowCount - 1
        radioB.row = SpotConfigureWidget.star1RowCount - 1
        radioA.setObjectName("star1radioA" + str(SpotConfigureWidget.star1RowCount - 1))
        radioB.setObjectName("star1radioB" + str(SpotConfigureWidget.star1RowCount - 1))
        SpotConfigureWidget.star1ElementList[(SpotConfigureWidget.star1RowCount - 1)].append(radioA)
        SpotConfigureWidget.star1ElementList[(SpotConfigureWidget.star1RowCount - 1)].append(radioB)
    if starNumber == 2:
        radioA.row = SpotConfigureWidget.star2RowCount - 1
        radioB.row = SpotConfigureWidget.star2RowCount - 1
        radioA.setObjectName("star1radioA" + str(SpotConfigureWidget.star2RowCount - 1))
        radioB.setObjectName("star1radioB" + str(SpotConfigureWidget.star2RowCount - 1))
        SpotConfigureWidget.star2ElementList[(SpotConfigureWidget.star2RowCount - 1)].append(radioA)
        SpotConfigureWidget.star2ElementList[(SpotConfigureWidget.star2RowCount - 1)].append(radioB)
    radioA.toggled.connect(partial(radioButtonSameSpotCheck, radioA, SpotConfigureWidget, starNumber))
    radioB.toggled.connect(partial(radioButtonSameSpotCheck, radioB, SpotConfigureWidget, starNumber))
    SpotConfigureWidget.radioButtonGroupA.addButton(radioA)
    SpotConfigureWidget.radioButtonGroupB.addButton(radioB)
    radioA.show()
    radioB.show()

    # input boxes
    lat_input = QtGui.QLineEdit(SpotConfigureWidget)
    lon_input = QtGui.QLineEdit(SpotConfigureWidget)
    radsp_input = QtGui.QLineEdit(SpotConfigureWidget)
    temsp_input = QtGui.QLineEdit(SpotConfigureWidget)
    tstart_input = QtGui.QLineEdit(SpotConfigureWidget)
    tmax1_input = QtGui.QLineEdit(SpotConfigureWidget)
    tmax2_input = QtGui.QLineEdit(SpotConfigureWidget)
    tend_input = QtGui.QLineEdit(SpotConfigureWidget)
    width = 60
    height = 20
    lat_input.setGeometry(120 + xshiftAmount, 100 + yshiftAmount, width, height)
    lon_input.setGeometry(190 + xshiftAmount, 100 + yshiftAmount, width, height)
    radsp_input.setGeometry(260 + xshiftAmount, 100 + yshiftAmount, width, height)
    temsp_input.setGeometry(330 + xshiftAmount, 100 + yshiftAmount, width, height)
    tstart_input.setGeometry(120 + xshiftAmount, 130 + yshiftAmount, width, height)
    tmax1_input.setGeometry(190 + xshiftAmount, 130 + yshiftAmount, width, height)
    tmax2_input.setGeometry(260 + xshiftAmount, 130 + yshiftAmount, width, height)
    tend_input.setGeometry(330 + xshiftAmount, 130 + yshiftAmount, width, height)
    lat_input.setText("0")
    lon_input.setText("0")
    radsp_input.setText("0")
    temsp_input.setText("0")
    tstart_input.setText("50800")
    tmax1_input.setText("50900")
    tmax2_input.setText("50930")
    tend_input.setText("51100")
    if starNumber == 1:
        lat_input.setObjectName("star1lat_input" + str(SpotConfigureWidget.star1RowCount - 1))
        lon_input.setObjectName("star1lon_input" + str(SpotConfigureWidget.star1RowCount - 1))
        radsp_input.setObjectName("star1radsp_input" + str(SpotConfigureWidget.star1RowCount - 1))
        temsp_input.setObjectName("star1temsp_input" + str(SpotConfigureWidget.star1RowCount - 1))
        tstart_input.setObjectName("star1tstart_input" + str(SpotConfigureWidget.star1RowCount - 1))
        tmax1_input.setObjectName("star1tmax1_input" + str(SpotConfigureWidget.star1RowCount - 1))
        tmax2_input.setObjectName("star1tmax2_input" + str(SpotConfigureWidget.star1RowCount - 1))
        tend_input.setObjectName("star1tend_input" + str(SpotConfigureWidget.star1RowCount - 1))
        SpotConfigureWidget.star1ElementList[SpotConfigureWidget.star1RowCount - 1].append(lat_input)
        SpotConfigureWidget.star1ElementList[SpotConfigureWidget.star1RowCount - 1].append(lon_input)
        SpotConfigureWidget.star1ElementList[SpotConfigureWidget.star1RowCount - 1].append(radsp_input)
        SpotConfigureWidget.star1ElementList[SpotConfigureWidget.star1RowCount - 1].append(temsp_input)
        SpotConfigureWidget.star1ElementList[SpotConfigureWidget.star1RowCount - 1].append(tstart_input)
        SpotConfigureWidget.star1ElementList[SpotConfigureWidget.star1RowCount - 1].append(tmax1_input)
        SpotConfigureWidget.star1ElementList[SpotConfigureWidget.star1RowCount - 1].append(tmax2_input)
        SpotConfigureWidget.star1ElementList[SpotConfigureWidget.star1RowCount - 1].append(tend_input)
    if starNumber == 2:
        lat_input.setObjectName("star2lat_input" + str(SpotConfigureWidget.star2RowCount - 1))
        lon_input.setObjectName("star2lon_input" + str(SpotConfigureWidget.star2RowCount - 1))
        radsp_input.setObjectName("star2radsp_input" + str(SpotConfigureWidget.star2RowCount - 1))
        temsp_input.setObjectName("star2temsp_input" + str(SpotConfigureWidget.star2RowCount - 1))
        tstart_input.setObjectName("star1tstart_input" + str(SpotConfigureWidget.star2RowCount - 1))
        tmax1_input.setObjectName("star1tmax1_input" + str(SpotConfigureWidget.star2RowCount - 1))
        tmax2_input.setObjectName("star1tmax2_input" + str(SpotConfigureWidget.star2RowCount - 1))
        tend_input.setObjectName("star1tend_input" + str(SpotConfigureWidget.star2RowCount - 1))
        SpotConfigureWidget.star2ElementList[SpotConfigureWidget.star2RowCount - 1].append(lat_input)
        SpotConfigureWidget.star2ElementList[SpotConfigureWidget.star2RowCount - 1].append(lon_input)
        SpotConfigureWidget.star2ElementList[SpotConfigureWidget.star2RowCount - 1].append(radsp_input)
        SpotConfigureWidget.star2ElementList[SpotConfigureWidget.star2RowCount - 1].append(temsp_input)
        SpotConfigureWidget.star2ElementList[SpotConfigureWidget.star2RowCount - 1].append(tstart_input)
        SpotConfigureWidget.star2ElementList[SpotConfigureWidget.star2RowCount - 1].append(tmax1_input)
        SpotConfigureWidget.star2ElementList[SpotConfigureWidget.star2RowCount - 1].append(tmax2_input)
        SpotConfigureWidget.star2ElementList[SpotConfigureWidget.star2RowCount - 1].append(tend_input)
    lat_input.show()
    lon_input.show()
    radsp_input.show()
    temsp_input.show()
    tstart_input.show()
    tmax1_input.show()
    tmax2_input.show()
    tend_input.show()

    # remove button
    remove_button = QtGui.QPushButton(SpotConfigureWidget)
    remove_button.setGeometry(390 + xshiftAmount, 100 + yshiftAmount, 60, 50)
    remove_button.setText("Remove")
    if starNumber == 1:
        remove_button.setObjectName("star1remove_button" + str(SpotConfigureWidget.star1RowCount - 1))
        remove_button.row = SpotConfigureWidget.star1RowCount - 1
        remove_button.clicked.connect(partial(removeSpotRow, SpotConfigureWidget, remove_button, starNumber))
        SpotConfigureWidget.star1ElementList[SpotConfigureWidget.star1RowCount - 1].append(remove_button)
    if starNumber == 2:
        remove_button.setObjectName("star2remove_button" + str(SpotConfigureWidget.star2RowCount - 1))
        remove_button.row = SpotConfigureWidget.star2RowCount - 1
        remove_button.clicked.connect(partial(removeSpotRow, SpotConfigureWidget, remove_button, starNumber))
        SpotConfigureWidget.star2ElementList[SpotConfigureWidget.star2RowCount - 1].append(remove_button)
    remove_button.show()


def removeSpotRow(SpotConfigureWidget, removeButton, starNumber):
    row = int(removeButton.row)
    xshiftAmount = 0
    yshiftAmount = 0
    width = 60
    height = 20
    if starNumber == 1:
        SpotConfigureWidget.star1RowCount -= 1
        for element in SpotConfigureWidget.star1ElementList[row]:
            element.hide()
        SpotConfigureWidget.star1ElementList.pop(row)
        i = 0
        for elementList in SpotConfigureWidget.star1ElementList:
            xshiftAmount = 0
            yshiftAmount = 60 * (i + 1)
            elementList[0].setGeometry(10 + xshiftAmount, 100 + yshiftAmount, 45, 16)
            elementList[0].setText("Spot " + str(i + 1))
            elementList[1].setGeometry(60 + xshiftAmount, 100 + yshiftAmount, 20, 20)
            elementList[1].row = i
            elementList[1].toggled.disconnect()
            elementList[1].toggled.connect(partial(
                radioButtonSameSpotCheck, elementList[1], SpotConfigureWidget, starNumber))
            elementList[2].setGeometry(90 + xshiftAmount, 100 + yshiftAmount, 20, 20)
            elementList[2].row = i
            elementList[2].toggled.disconnect()
            elementList[2].toggled.connect(partial(
                radioButtonSameSpotCheck, elementList[2], SpotConfigureWidget, starNumber))
            elementList[3].setGeometry(120 + xshiftAmount, 100 + yshiftAmount, width, height)
            elementList[4].setGeometry(190 + xshiftAmount, 100 + yshiftAmount, width, height)
            elementList[5].setGeometry(260 + xshiftAmount, 100 + yshiftAmount, width, height)
            elementList[6].setGeometry(330 + xshiftAmount, 100 + yshiftAmount, width, height)
            elementList[7].setGeometry(120 + xshiftAmount, 130 + yshiftAmount, width, height)
            elementList[8].setGeometry(190 + xshiftAmount, 130 + yshiftAmount, width, height)
            elementList[9].setGeometry(260 + xshiftAmount, 130 + yshiftAmount, width, height)
            elementList[10].setGeometry(330 + xshiftAmount, 130 + yshiftAmount, width, height)
            elementList[11].setGeometry(390 + xshiftAmount, 100 + yshiftAmount, 60, 50)
            elementList[11].row = int(i)
            elementList[11].clicked.disconnect()
            elementList[11].clicked.connect(partial(removeSpotRow, SpotConfigureWidget, elementList[11], starNumber))
            i += 1
    if starNumber == 2:
        SpotConfigureWidget.star2RowCount -= 1
        for element in SpotConfigureWidget.star2ElementList[row]:
            element.hide()
        SpotConfigureWidget.star2ElementList.pop(row)
        i = 0
        for elementList in SpotConfigureWidget.star2ElementList:
            xshiftAmount = 460
            yshiftAmount = 60 * (i + 1)
            elementList[0].setGeometry(10 + xshiftAmount, 100 + yshiftAmount, 45, 16)
            elementList[0].setText("Spot " + str(i + 1))
            elementList[1].setGeometry(60 + xshiftAmount, 100 + yshiftAmount, 20, 20)
            elementList[1].row = i
            elementList[1].toggled.disconnect()
            elementList[1].toggled.connect(partial(
                radioButtonSameSpotCheck, elementList[1], SpotConfigureWidget, starNumber))
            elementList[2].setGeometry(90 + xshiftAmount, 100 + yshiftAmount, 20, 20)
            elementList[2].row = i
            elementList[2].toggled.disconnect()
            elementList[2].toggled.connect(partial(
                radioButtonSameSpotCheck, elementList[2], SpotConfigureWidget, starNumber))
            elementList[3].setGeometry(120 + xshiftAmount, 100 + yshiftAmount, width, height)
            elementList[4].setGeometry(190 + xshiftAmount, 100 + yshiftAmount, width, height)
            elementList[5].setGeometry(260 + xshiftAmount, 100 + yshiftAmount, width, height)
            elementList[6].setGeometry(330 + xshiftAmount, 100 + yshiftAmount, width, height)
            elementList[7].setGeometry(120 + xshiftAmount, 130 + yshiftAmount, width, height)
            elementList[8].setGeometry(190 + xshiftAmount, 130 + yshiftAmount, width, height)
            elementList[9].setGeometry(260 + xshiftAmount, 130 + yshiftAmount, width, height)
            elementList[10].setGeometry(330 + xshiftAmount, 130 + yshiftAmount, 50, 20)
            elementList[11].setGeometry(390 + xshiftAmount, 100 + yshiftAmount, 60, 50)
            elementList[11].row = i
            elementList[11].clicked.disconnect()
            elementList[11].clicked.connect(partial(removeSpotRow, SpotConfigureWidget, elementList[11], starNumber))
            i += 1

    resizeSpotConfigureWidget(SpotConfigureWidget, starNumber)


def resizeSpotConfigureWidget(SpotConfigureWidget, starNumber):
    yshiftAmount = 0
    if SpotConfigureWidget.star1RowCount > SpotConfigureWidget.star2RowCount:
        yshiftAmount = 60 * SpotConfigureWidget.star1RowCount
    if SpotConfigureWidget.star1RowCount < SpotConfigureWidget.star2RowCount:
        yshiftAmount = 60 * SpotConfigureWidget.star2RowCount
    if SpotConfigureWidget.star1RowCount == SpotConfigureWidget.star2RowCount:
        yshiftAmount = 60 * SpotConfigureWidget.star2RowCount
    if starNumber == 1:
        y = SpotConfigureWidget.star1RowCount * 60
        SpotConfigureWidget.addspot1_btn.setGeometry(10, y + 160, 442, 25)
    if starNumber == 2:
        y = SpotConfigureWidget.star2RowCount * 60
        SpotConfigureWidget.addspot2_btn.setGeometry(469, y + 160, 442, 25)
    SpotConfigureWidget.line_3.setGeometry(441, 130, 41, 61 + yshiftAmount)
    SpotConfigureWidget.setMaximumHeight(yshiftAmount + 200)
    SpotConfigureWidget.setMinimumHeight(yshiftAmount + 200)
    SpotConfigureWidget.resize(925, yshiftAmount + 200)


def radioButtonSameSpotCheck(radioButton, SpotConfigureWidget, starNumber):
    if radioButton.isChecked() is True:
        test = False
        if starNumber == 1:
            if radioButton.type == "A":
                test = SpotConfigureWidget.star1ElementList[radioButton.row][2].isChecked()
            if radioButton.type == "B":
                test = SpotConfigureWidget.star1ElementList[radioButton.row][1].isChecked()
        if starNumber == 2:
            if radioButton.type == "A":
                test = SpotConfigureWidget.star2ElementList[radioButton.row][2].isChecked()
            if radioButton.type == "B":
                test = SpotConfigureWidget.star2ElementList[radioButton.row][1].isChecked()
        if test is True:
            SpotConfigureWidget.radioButtonGroupA.setExclusive(False)
            SpotConfigureWidget.radioButtonGroupB.setExclusive(False)
            if starNumber == 1:
                if radioButton.type == "A":
                    SpotConfigureWidget.star1ElementList[radioButton.row][2].toggle()
                if radioButton.type == "B":
                    SpotConfigureWidget.star1ElementList[radioButton.row][1].toggle()
            if starNumber == 2:
                if radioButton.type == "A":
                    SpotConfigureWidget.star2ElementList[radioButton.row][2].toggle()
                if radioButton.type == "B":
                    SpotConfigureWidget.star2ElementList[radioButton.row][1].toggle()
            SpotConfigureWidget.radioButtonGroupA.setExclusive(True)
            SpotConfigureWidget.radioButtonGroupB.setExclusive(True)


def loadEclipseTimings(EclipseWidget):
    dialog = QtGui.QFileDialog(EclipseWidget)
    dialog.setAcceptMode(0)
    returnCode = dialog.exec_()
    fileName = str((dialog.selectedFiles())[0])
    if fileName != "" and returnCode != 0:
        curve = classes.Curve(fileName)
        if curve.hasError:
            if curve.hasError:
                msg = QtGui.QMessageBox()
                msg.setText(curve.error)
                msg.setWindowTitle("PyWD - Error")
                msg.exec_()
        else:
            EclipseWidget.datawidget.clear()
            for x in curve.lines:
                a = QtGui.QTreeWidgetItem(EclipseWidget.datawidget, x)
            EclipseWidget.filepath_label.setText(fileName)
            EclipseWidget.filepath_label.setToolTip(fileName)


def removeEclipseTimings(EclipseWidget):
    EclipseWidget.datawidget.clear()
    EclipseWidget.filepath_label.setText("None")
    EclipseWidget.filepath_label.setToolTip("")
    EclipseWidget.sigma_ipt.setText("0")
    EclipseWidget.ksd_box.setValue(1)


def saveProject(MainWindow):
    output = StringIO.StringIO()
    MainWindowParameters = saveMainWindowParameters(MainWindow)
    SpotConfiguration = SaveSpotConfiguration(MainWindow.SpotConfigureWidget)
    CurveParameters = saveCurveParameters(MainWindow)
    EclipseParameters = saveEclipseTimings(MainWindow)

    MainWindowParameters.write(output)
    SpotConfiguration.write(output)
    CurveParameters.write(output)
    EclipseParameters.write(output)
    return output.getvalue()


def saveCurveParameters(MainWindow):
    vcpropList = MainWindow.LoadObservationWidget.vcPropertiesList
    lcpropList = MainWindow.LoadObservationWidget.lcPropertiesList
    propList = vcpropList + lcpropList
    parser = ConfigParser.SafeConfigParser()
    vcCount = 0
    lcCount = 0
    parser.add_section("Curve Count")
    for prop in propList:
        if prop == 0:
            pass
        else:
            if prop.type == "vc":
                section = "Velocity Curve " + str(vcCount + 1)
                vcCount = vcCount + 1
            if prop.type == "lc":
                section = "Light Curve " + str(lcCount + 1)
                lcCount = lcCount + 1
            parser.add_section(section)
            parser.set(section, "filepath", prop.FilePath)
            parser.set(section, "band", prop.band)
            parser.set(section, "ksd", prop.ksd)
            parser.set(section, "l1", prop.l1)
            parser.set(section, "l2", prop.l2)
            parser.set(section, "x1", prop.x1)
            parser.set(section, "x2", prop.x2)
            parser.set(section, "y1", prop.y1)
            parser.set(section, "y2", prop.y2)
            parser.set(section, "e1", prop.e1)
            parser.set(section, "e2", prop.e2)
            parser.set(section, "e3", prop.e3)
            parser.set(section, "e4", prop.e4)
            parser.set(section, "wla", prop.wla)
            parser.set(section, "opsf", prop.opsf)
            parser.set(section, "sigma", prop.sigma)
            if prop.type == "lc":
                parser.set(section, "noise", prop.noise)
                parser.set(section, "el3a", prop.el3a)
                parser.set(section, "aextinc", prop.aextinc)
                parser.set(section, "xunit", prop.xunit)
                parser.set(section, "calib", prop.calib)
            if prop.type == "vc":
                parser.set(section, "star", str(prop.star))
    parser.set("Curve Count", "velocity curves", str(vcCount))
    parser.set("Curve Count", "light curves", str(lcCount))
    return parser


def saveEclipseTimings(MainWindow):
    eclipse = MainWindow.EclipseWidget
    parser = ConfigParser.SafeConfigParser()
    parser.add_section("Eclipse Timing")
    parser.set("Eclipse Timing", "filepath", str(eclipse.filepath_label.text()))
    parser.set("Eclipse Timing", "iftime", str(eclipse.iftime_chk.isChecked()))
    parser.set("Eclipse Timing", "ksd", str(eclipse.ksd_box.value()))
    parser.set("Eclipse Timing", "sigma", str(eclipse.sigma_ipt.text()))
    return parser


def saveMainWindowParameters(MainWindow):
    parser = ConfigParser.SafeConfigParser()
    # info
    parser.add_section("Info")
    parser.set("Info", "version", "2015")
    parser.set("Info", "config", __configver__)
    # main tab
    parser.add_section("Main")
    parser.set("Main", "system", str(MainWindow.systemname_ipt.text()))
    parser.set("Main", "operation mode", str(MainWindow.mode_combobox.currentIndex()))
    parser.set("Main", "jdphs", str(MainWindow.jdphs_combobox.currentIndex()))
    parser.set("Main", "icor1", str(MainWindow.icor1_chk.isChecked()))
    parser.set("Main", "icor2", str(MainWindow.icor2_chk.isChecked()))
    parser.set("Main", "ifcgs", str(MainWindow.ifcgs_chk.isChecked()))
    # system tab
    parser.add_section("System")
    parser.set("System", "jd0", str(MainWindow.jd0_ipt.text()))
    parser.set("System", "p0", str(MainWindow.p0_ipt.text()))
    parser.set("System", "dpdt", str(MainWindow.dpdt_ipt.text()))
    parser.set("System", "pshift", str(MainWindow.pshift_ipt.text()))
    parser.set("System", "delph", str(MainWindow.delph_ipt.text()))
    parser.set("System", "a", str(MainWindow.a_ipt.text()))
    parser.set("System", "e", str(MainWindow.e_ipt.text()))
    parser.set("System", "perr0", str(MainWindow.perr0_ipt.text()))
    parser.set("System", "dperdt", str(MainWindow.dperdt_ipt.text()))
    parser.set("System", "xincl", str(MainWindow.xincl_ipt.text()))
    parser.set("System", "vgam", str(MainWindow.vgam_ipt.text()))
    parser.set("System", "rm", str(MainWindow.rm_ipt.text()))
    parser.set("System", "abunin", str(MainWindow.abunin_ipt.text()))
    parser.set("System", "tavh", str(MainWindow.tavh_ipt.text()))
    parser.set("System", "tavc", str(MainWindow.tavc_ipt.text()))
    parser.set("System", "pot1", str(MainWindow.phsv_ipt.text()))
    parser.set("System", "pot2", str(MainWindow.pcsv_ipt.text()))
    parser.set("System", "f1", str(MainWindow.f1_ipt.text()))
    parser.set("System", "f2", str(MainWindow.f2_ipt.text()))
    parser.set("System", "th e", str(MainWindow.the_ipt.text()))
    parser.set("System", "vunit", str(MainWindow.vunit_ipt.text()))
    parser.set("System", "dpclog", str(MainWindow.dpclog_ipt.text()))
    parser.set("System", "nga", str(MainWindow.nga_spinbox.value()))
    # surface tab
    parser.add_section("Surface")
    parser.set("Surface", "ifat1", str(MainWindow.ifat1_combobox.currentIndex()))
    parser.set("Surface", "ifat2", str(MainWindow.ifat2_combobox.currentIndex()))
    parser.set("Surface", "alb1", str(MainWindow.alb1_spinbox.value()))
    parser.set("Surface", "alb2", str(MainWindow.alb2_spinbox.value()))
    parser.set("Surface", "gr1", str(MainWindow.gr1_spinbox.value()))
    parser.set("Surface", "gr2", str(MainWindow.gr2_spinbox.value()))
    parser.set("Surface", "ld1", str(MainWindow.ld1_combobox.currentIndex()))
    parser.set("Surface", "ld2", str(MainWindow.ld2_combobox.currentIndex()))
    parser.set("Surface", "ld1_fixed", str(MainWindow.ld1_chk.isChecked()))
    parser.set("Surface", "ld2_fixed", str(MainWindow.ld2_chk.isChecked()))
    parser.set("Surface", "xbol1", str(MainWindow.xbol1_ipt.text()))
    parser.set("Surface", "xbol2", str(MainWindow.xbol2_ipt.text()))
    parser.set("Surface", "ybol1", str(MainWindow.ybol1_ipt.text()))
    parser.set("Surface", "ybol2", str(MainWindow.ybol2_ipt.text()))
    parser.set("Surface", "n1", str(MainWindow.n1_spinbox.value()))
    parser.set("Surface", "n2", str(MainWindow.n2_spinbox.value()))
    parser.set("Surface", "n1l", str(MainWindow.n1l_spinbox.value()))
    parser.set("Surface", "n2l", str(MainWindow.n2l_spinbox.value()))
    parser.set("Surface", "mref", str(MainWindow.mref_chk.isChecked()))
    parser.set("Surface", "nref", str(MainWindow.nref_spinbox.value()))
    parser.set("Surface", "ipb", str(MainWindow.ipb_chk.isChecked()))
    # 3rd body tab
    parser.add_section("Third Body")
    parser.set("Third Body", "if3b", str(MainWindow.if3b_chk.isChecked()))
    parser.set("Third Body", "a3b", str(MainWindow.a3b_ipt.text()))
    parser.set("Third Body", "p3b", str(MainWindow.p3b_ipt.text()))
    parser.set("Third Body", "xinc3b", str(MainWindow.xinc3b_ipt.text()))
    parser.set("Third Body", "e3b", str(MainWindow.e3b_ipt.text()))
    parser.set("Third Body", "perr3b", str(MainWindow.perr3b_ipt.text()))
    parser.set("Third Body", "tc3b", str(MainWindow.tc3b_ipt.text()))
    # del tab
    parser.add_section("DEL's")
    parser.set("DEL's", "del_s1lat", str(MainWindow.DCWidget.del_s1lat_ipt.text()))
    parser.set("DEL's", "del_s1lng", str(MainWindow.DCWidget.del_s1lng_ipt.text()))
    parser.set("DEL's", "del_s1rad", str(MainWindow.DCWidget.del_s1agrad_ipt.text()))
    parser.set("DEL's", "del_s1tmp", str(MainWindow.DCWidget.del_s1tmpf_ipt.text()))
    parser.set("DEL's", "del_s2lat", str(MainWindow.DCWidget.del_s2lat_ipt.text()))
    parser.set("DEL's", "del_s2lng", str(MainWindow.DCWidget.del_s2lng_ipt.text()))
    parser.set("DEL's", "del_s2rad", str(MainWindow.DCWidget.del_s2agrad_ipt.text()))
    parser.set("DEL's", "del_s2tmp", str(MainWindow.DCWidget.del_s2tmpf_ipt.text()))
    parser.set("DEL's", "del_a", str(MainWindow.DCWidget.del_a_ipt.text()))
    parser.set("DEL's", "del_e", str(MainWindow.DCWidget.del_e_ipt.text()))
    parser.set("DEL's", "del_f1", str(MainWindow.DCWidget.del_f1_ipt.text()))
    parser.set("DEL's", "del_f2", str(MainWindow.DCWidget.del_f2_ipt.text()))
    parser.set("DEL's", "del_pshift", str(MainWindow.DCWidget.del_pshift_ipt.text()))
    parser.set("DEL's", "del_perr0", str(MainWindow.DCWidget.del_perr0_ipt.text()))
    parser.set("DEL's", "del_incl", str(MainWindow.DCWidget.del_i_ipt.text()))
    parser.set("DEL's", "del_rm", str(MainWindow.DCWidget.del_q_ipt.text()))
    parser.set("DEL's", "del_g1", str(MainWindow.DCWidget.del_g1_ipt.text()))
    parser.set("DEL's", "del_g2", str(MainWindow.DCWidget.del_g2_ipt.text()))
    parser.set("DEL's", "del_tavh", str(MainWindow.DCWidget.del_t1_ipt.text()))
    parser.set("DEL's", "del_tavc", str(MainWindow.DCWidget.del_t2_ipt.text()))
    parser.set("DEL's", "del_alb1", str(MainWindow.DCWidget.del_alb1_ipt.text()))
    parser.set("DEL's", "del_alb2", str(MainWindow.DCWidget.del_alb2_ipt.text()))
    parser.set("DEL's", "del_pot1", str(MainWindow.DCWidget.del_pot1_ipt.text()))
    parser.set("DEL's", "del_pot2", str(MainWindow.DCWidget.del_pot2_ipt.text()))
    parser.set("DEL's", "del_l1", str(MainWindow.DCWidget.del_l1_ipt.text()))
    parser.set("DEL's", "del_l2", str(MainWindow.DCWidget.del_l2_ipt.text()))
    parser.set("DEL's", "del_xbol1", str(MainWindow.DCWidget.del_x1_ipt.text()))
    parser.set("DEL's", "del_xbol2", str(MainWindow.DCWidget.del_x2_ipt.text()))
    # keep tab
    parser.add_section("KEEP's")
    parser.set("KEEP's", "jd0", str(MainWindow.DCWidget.jd0_chk.isChecked()))
    parser.set("KEEP's", "p0", str(MainWindow.DCWidget.p0_chk.isChecked()))
    parser.set("KEEP's", "dpdt", str(MainWindow.DCWidget.dpdt_chk.isChecked()))
    parser.set("KEEP's", "perr0", str(MainWindow.DCWidget.perr0_chk.isChecked()))
    parser.set("KEEP's", "dperdt", str(MainWindow.DCWidget.dperdt_chk.isChecked()))
    parser.set("KEEP's", "pshift", str(MainWindow.DCWidget.pshift_chk.isChecked()))
    parser.set("KEEP's", "a", str(MainWindow.DCWidget.a_chk.isChecked()))
    parser.set("KEEP's", "e", str(MainWindow.DCWidget.e_chk.isChecked()))
    parser.set("KEEP's", "logd", str(MainWindow.DCWidget.logd_chk.isChecked()))
    parser.set("KEEP's", "vgam", str(MainWindow.DCWidget.vgam_chk.isChecked()))
    parser.set("KEEP's", "incl", str(MainWindow.DCWidget.incl_chk.isChecked()))
    parser.set("KEEP's", "rm", str(MainWindow.DCWidget.q_chk.isChecked()))
    parser.set("KEEP's", "tavh", str(MainWindow.DCWidget.t1_chk.isChecked()))
    parser.set("KEEP's", "tavc", str(MainWindow.DCWidget.t2_chk.isChecked()))
    parser.set("KEEP's", "g1", str(MainWindow.DCWidget.g1_chk.isChecked()))
    parser.set("KEEP's", "g2", str(MainWindow.DCWidget.g2_chk.isChecked()))
    parser.set("KEEP's", "alb1", str(MainWindow.DCWidget.alb1_chk.isChecked()))
    parser.set("KEEP's", "alb2", str(MainWindow.DCWidget.alb2_chk.isChecked()))
    parser.set("KEEP's", "desext", str(MainWindow.DCWidget.desextinc_chk.isChecked()))
    parser.set("KEEP's", "f1", str(MainWindow.DCWidget.f1_chk.isChecked()))
    parser.set("KEEP's", "f2", str(MainWindow.DCWidget.f2_chk.isChecked()))
    parser.set("KEEP's", "l1", str(MainWindow.DCWidget.l1_chk.isChecked()))
    parser.set("KEEP's", "l2", str(MainWindow.DCWidget.l2_chk.isChecked()))
    parser.set("KEEP's", "xbol1", str(MainWindow.DCWidget.x1_chk.isChecked()))
    parser.set("KEEP's", "xbol2", str(MainWindow.DCWidget.x2_chk.isChecked()))
    parser.set("KEEP's", "pot1", str(MainWindow.DCWidget.pot1_chk.isChecked()))
    parser.set("KEEP's", "pot2", str(MainWindow.DCWidget.pot2_chk.isChecked()))
    parser.set("KEEP's", "a3b", str(MainWindow.DCWidget.a3b_chk.isChecked()))
    parser.set("KEEP's", "p3b", str(MainWindow.DCWidget.p3b_chk.isChecked()))
    parser.set("KEEP's", "xinc3b", str(MainWindow.DCWidget.xinc3b_chk.isChecked()))
    parser.set("KEEP's", "e3b", str(MainWindow.DCWidget.e3b_chk.isChecked()))
    parser.set("KEEP's", "tc3b", str(MainWindow.DCWidget.tc3b_chk.isChecked()))
    parser.set("KEEP's", "perr3b", str(MainWindow.DCWidget.perr3b_chk.isChecked()))
    parser.set("KEEP's", "el3", str(MainWindow.DCWidget.el3_chk.isChecked()))
    parser.set("KEEP's", "s1lat", str(MainWindow.DCWidget.s1lat_chk.isChecked()))
    parser.set("KEEP's", "s1lng", str(MainWindow.DCWidget.s1long_chk.isChecked()))
    parser.set("KEEP's", "s1rad", str(MainWindow.DCWidget.s1rad_chk.isChecked()))
    parser.set("KEEP's", "s1tstart", str(MainWindow.DCWidget.s1tstart_chk.isChecked()))
    parser.set("KEEP's", "s1max1", str(MainWindow.DCWidget.s1tmax1_chk.isChecked()))
    parser.set("KEEP's", "s1max2", str(MainWindow.DCWidget.s1tmax2_chk.isChecked()))
    parser.set("KEEP's", "s1tend", str(MainWindow.DCWidget.s1tend_chk.isChecked()))
    parser.set("KEEP's", "s1temp", str(MainWindow.DCWidget.s1temp_chk.isChecked()))
    parser.set("KEEP's", "s2lat", str(MainWindow.DCWidget.s2lat_chk.isChecked()))
    parser.set("KEEP's", "s2lng", str(MainWindow.DCWidget.s2long_chk.isChecked()))
    parser.set("KEEP's", "s2rad", str(MainWindow.DCWidget.s2rad_chk.isChecked()))
    parser.set("KEEP's", "s2temp", str(MainWindow.DCWidget.s2temp_chk.isChecked()))
    parser.set("KEEP's", "s2tstart", str(MainWindow.DCWidget.s2tstart_chk.isChecked()))
    parser.set("KEEP's", "s2max1", str(MainWindow.DCWidget.s2tmax1_chk.isChecked()))
    parser.set("KEEP's", "s2max2", str(MainWindow.DCWidget.s2tmax2_chk.isChecked()))
    parser.set("KEEP's", "s2tend", str(MainWindow.DCWidget.s2tend_chk.isChecked()))
    # dc
    parser.add_section("DC2015")
    parser.set("DC2015", "maglite", str(MainWindow.maglite_combobox.currentIndex()))
    parser.set("DC2015", "isym", str(MainWindow.isym_combobox.currentIndex()))
    parser.set("DC2015", "linkext", str(MainWindow.linkext_spinbox.value()))
    parser.set("DC2015", "desextinc", str(MainWindow.desextinc_ipt.text()))

    return parser


def loadMainWindowParameters(MainWindow, parser):
    # main tab
    MainWindow.systemname_ipt.setText(parser.get("Main", "system"))
    MainWindow.mode_combobox.setCurrentIndex(parser.getint("Main", "operation mode"))
    MainWindow.jdphs_combobox.setCurrentIndex(parser.getint("Main", "jdphs"))
    MainWindow.ifcgs_chk.setChecked(parser.getboolean("Main", "ifcgs"))
    MainWindow.icor1_chk.setChecked(parser.getboolean("Main", "icor1"))
    MainWindow.icor2_chk.setChecked(parser.getboolean("Main", "icor2"))
    # system tab
    MainWindow.jd0_ipt.setText(parser.get("System", "jd0"))
    MainWindow.p0_ipt.setText(parser.get("System", "p0"))
    MainWindow.dpdt_ipt.setText(parser.get("System", "dpdt"))
    MainWindow.pshift_ipt.setText(parser.get("System", "pshift"))
    MainWindow.delph_ipt.setText(parser.get("System", "delph"))
    MainWindow.a_ipt.setText(parser.get("System", "a"))
    MainWindow.e_ipt.setText(parser.get("System", "e"))
    MainWindow.perr0_ipt.setText(parser.get("System", "perr0"))
    MainWindow.dperdt_ipt.setText(parser.get("System", "dperdt"))
    MainWindow.xincl_ipt.setText(parser.get("System", "xincl"))
    MainWindow.vgam_ipt.setText(parser.get("System", "vgam"))
    MainWindow.rm_ipt.setText(parser.get("System", "rm"))
    MainWindow.abunin_ipt.setText(parser.get("System", "abunin"))
    MainWindow.tavh_ipt.setText(parser.get("System", "tavh"))
    MainWindow.tavc_ipt.setText(parser.get("System", "tavc"))
    MainWindow.phsv_ipt.setText(parser.get("System", "pot1"))
    MainWindow.pcsv_ipt.setText(parser.get("System", "pot2"))
    MainWindow.f1_ipt.setText(parser.get("System", "f1"))
    MainWindow.f2_ipt.setText(parser.get("System", "f2"))
    MainWindow.the_ipt.setText(parser.get("System", "th e"))
    MainWindow.vunit_ipt.setText(parser.get("System", "vunit"))
    MainWindow.dpclog_ipt.setText(parser.get("System", "dpclog"))
    MainWindow.nga_spinbox.setValue(parser.getint("System", "nga"))
    # surface tab
    MainWindow.ifat1_combobox.setCurrentIndex(parser.getint("Surface", "ifat1"))
    MainWindow.ifat2_combobox.setCurrentIndex(parser.getint("Surface", "ifat2"))
    MainWindow.alb1_spinbox.setValue(parser.getfloat("Surface", "alb1"))
    MainWindow.alb2_spinbox.setValue(parser.getfloat("Surface", "alb2"))
    MainWindow.gr1_spinbox.setValue(parser.getfloat("Surface", "gr1"))
    MainWindow.gr2_spinbox.setValue(parser.getfloat("Surface", "gr2"))
    MainWindow.ld1_combobox.setCurrentIndex(parser.getint("Surface", "ld1"))
    MainWindow.ld2_combobox.setCurrentIndex(parser.getint("Surface", "ld2"))
    MainWindow.ld1_chk.setChecked(parser.getboolean("Surface", "ld1_fixed"))
    MainWindow.ld2_chk.setChecked(parser.getboolean("Surface", "ld2_fixed"))
    MainWindow.xbol1_ipt.setText(parser.get("Surface", "xbol1"))
    MainWindow.xbol2_ipt.setText(parser.get("Surface", "xbol2"))
    MainWindow.ybol1_ipt.setText(parser.get("Surface", "ybol1"))
    MainWindow.ybol2_ipt.setText(parser.get("Surface", "ybol2"))
    MainWindow.n1_spinbox.setValue(parser.getfloat("Surface", "n1"))
    MainWindow.n2_spinbox.setValue(parser.getfloat("Surface", "n2"))
    MainWindow.n1l_spinbox.setValue(parser.getfloat("Surface", "n1l"))
    MainWindow.n2l_spinbox.setValue(parser.getfloat("Surface", "n2l"))
    MainWindow.mref_chk.setChecked(parser.getboolean("Surface", "mref"))
    MainWindow.nref_spinbox.setValue(parser.getfloat("Surface", "nref"))
    MainWindow.ipb_chk.setChecked(parser.getboolean("Surface", "ipb"))
    # 3rd body tab
    MainWindow.if3b_chk.setChecked(parser.getboolean("Third Body", "if3b"))
    MainWindow.a3b_ipt.setText(parser.get("Third Body", "a3b"))
    MainWindow.p3b_ipt.setText(parser.get("Third Body", "p3b"))
    MainWindow.xinc3b_ipt.setText(parser.get("Third Body", "xinc3b"))
    MainWindow.e3b_ipt.setText(parser.get("Third Body", "e3b"))
    MainWindow.perr3b_ipt.setText(parser.get("Third Body", "perr3b"))
    MainWindow.tc3b_ipt.setText(parser.get("Third Body", "tc3b"))
    # del tab
    MainWindow.DCWidget.del_s1lat_ipt.setText(parser.get("DEL's", "del_s1lat"))
    MainWindow.DCWidget.del_s1lng_ipt.setText(parser.get("DEL's", "del_s1lng"))
    MainWindow.DCWidget.del_s1agrad_ipt.setText(parser.get("DEL's", "del_s1rad"))
    MainWindow.DCWidget.del_s1tmpf_ipt.setText(parser.get("DEL's", "del_s1tmp"))
    MainWindow.DCWidget.del_s2lat_ipt.setText(parser.get("DEL's", "del_s2lat"))
    MainWindow.DCWidget.del_s2lng_ipt.setText(parser.get("DEL's", "del_s2lng"))
    MainWindow.DCWidget.del_s2agrad_ipt.setText(parser.get("DEL's", "del_s2rad"))
    MainWindow.DCWidget.del_s2tmpf_ipt.setText(parser.get("DEL's", "del_s2tmp"))
    MainWindow.DCWidget.del_a_ipt.setText(parser.get("DEL's", "del_a"))
    MainWindow.DCWidget.del_e_ipt.setText(parser.get("DEL's", "del_e"))
    MainWindow.DCWidget.del_f1_ipt.setText(parser.get("DEL's", "del_f1"))
    MainWindow.DCWidget.del_f2_ipt.setText(parser.get("DEL's", "del_f2"))
    MainWindow.DCWidget.del_pshift_ipt.setText(parser.get("DEL's", "del_pshift"))
    MainWindow.DCWidget.del_perr0_ipt.setText(parser.get("DEL's", "del_perr0"))
    MainWindow.DCWidget.del_i_ipt.setText(parser.get("DEL's", "del_incl"))
    MainWindow.DCWidget.del_q_ipt.setText(parser.get("DEL's", "del_rm"))
    MainWindow.DCWidget.del_g1_ipt.setText(parser.get("DEL's", "del_g1"))
    MainWindow.DCWidget.del_g2_ipt.setText(parser.get("DEL's", "del_g2"))
    MainWindow.DCWidget.del_t1_ipt.setText(parser.get("DEL's", "del_tavh"))
    MainWindow.DCWidget.del_t2_ipt.setText(parser.get("DEL's", "del_tavc"))
    MainWindow.DCWidget.del_alb1_ipt.setText(parser.get("DEL's", "del_alb1"))
    MainWindow.DCWidget.del_alb2_ipt.setText(parser.get("DEL's", "del_alb2"))
    MainWindow.DCWidget.del_pot1_ipt.setText(parser.get("DEL's", "del_pot1"))
    MainWindow.DCWidget.del_pot2_ipt.setText(parser.get("DEL's", "del_pot2"))
    MainWindow.DCWidget.del_l1_ipt.setText(parser.get("DEL's", "del_l1"))
    MainWindow.DCWidget.del_l2_ipt.setText(parser.get("DEL's", "del_l2"))
    MainWindow.DCWidget.del_x1_ipt.setText(parser.get("DEL's", "del_xbol1"))
    MainWindow.DCWidget.del_x2_ipt.setText(parser.get("DEL's", "del_xbol2"))
    # keep tab
    MainWindow.DCWidget.jd0_chk.setChecked(parser.getboolean("KEEP's", "jd0"))
    MainWindow.DCWidget.p0_chk.setChecked(parser.getboolean("KEEP's", "p0"))
    MainWindow.DCWidget.dpdt_chk.setChecked(parser.getboolean("KEEP's", "dpdt"))
    MainWindow.DCWidget.perr0_chk.setChecked(parser.getboolean("KEEP's", "perr0"))
    MainWindow.DCWidget.dperdt_chk.setChecked(parser.getboolean("KEEP's", "dperdt"))
    MainWindow.DCWidget.pshift_chk.setChecked(parser.getboolean("KEEP's", "pshift"))
    MainWindow.DCWidget.a_chk.setChecked(parser.getboolean("KEEP's", "a"))
    MainWindow.DCWidget.e_chk.setChecked(parser.getboolean("KEEP's", "e"))
    MainWindow.DCWidget.logd_chk.setChecked(parser.getboolean("KEEP's", "logd"))
    MainWindow.DCWidget.vgam_chk.setChecked(parser.getboolean("KEEP's", "vgam"))
    MainWindow.DCWidget.incl_chk.setChecked(parser.getboolean("KEEP's", "incl"))
    MainWindow.DCWidget.q_chk.setChecked(parser.getboolean("KEEP's", "rm"))
    MainWindow.DCWidget.t1_chk.setChecked(parser.getboolean("KEEP's", "tavh"))
    MainWindow.DCWidget.t2_chk.setChecked(parser.getboolean("KEEP's", "tavc"))
    MainWindow.DCWidget.g1_chk.setChecked(parser.getboolean("KEEP's", "g1"))
    MainWindow.DCWidget.g2_chk.setChecked(parser.getboolean("KEEP's", "g2"))
    MainWindow.DCWidget.alb1_chk.setChecked(parser.getboolean("KEEP's", "alb1"))
    MainWindow.DCWidget.alb2_chk.setChecked(parser.getboolean("KEEP's", "alb2"))
    MainWindow.DCWidget.desextinc_chk.setChecked(parser.getboolean("KEEP's", "desext"))
    MainWindow.DCWidget.f1_chk.setChecked(parser.getboolean("KEEP's", "f1"))
    MainWindow.DCWidget.f2_chk.setChecked(parser.getboolean("KEEP's", "f2"))
    MainWindow.DCWidget.l1_chk.setChecked(parser.getboolean("KEEP's", "l1"))
    MainWindow.DCWidget.l2_chk.setChecked(parser.getboolean("KEEP's", "l2"))
    MainWindow.DCWidget.x1_chk.setChecked(parser.getboolean("KEEP's", "xbol1"))
    MainWindow.DCWidget.x2_chk.setChecked(parser.getboolean("KEEP's", "xbol2"))
    MainWindow.DCWidget.pot1_chk.setChecked(parser.getboolean("KEEP's", "pot1"))
    MainWindow.DCWidget.pot2_chk.setChecked(parser.getboolean("KEEP's", "pot2"))
    MainWindow.DCWidget.a3b_chk.setChecked(parser.getboolean("KEEP's", "a3b"))
    MainWindow.DCWidget.p3b_chk.setChecked(parser.getboolean("KEEP's", "p3b"))
    MainWindow.DCWidget.xinc3b_chk.setChecked(parser.getboolean("KEEP's", "xinc3b"))
    MainWindow.DCWidget.e3b_chk.setChecked(parser.getboolean("KEEP's", "e3b"))
    MainWindow.DCWidget.tc3b_chk.setChecked(parser.getboolean("KEEP's", "tc3b"))
    MainWindow.DCWidget.perr3b_chk.setChecked(parser.getboolean("KEEP's", "perr3b"))
    MainWindow.DCWidget.el3_chk.setChecked(parser.getboolean("KEEP's", "el3"))
    MainWindow.DCWidget.s1lat_chk.setChecked(parser.getboolean("KEEP's", "s1lat"))
    MainWindow.DCWidget.s1long_chk.setChecked(parser.getboolean("KEEP's", "s1lng"))
    MainWindow.DCWidget.s1rad_chk.setChecked(parser.getboolean("KEEP's", "s1rad"))
    MainWindow.DCWidget.s1temp_chk.setChecked(parser.getboolean("KEEP's", "s1temp"))
    MainWindow.DCWidget.s2lat_chk.setChecked(parser.getboolean("KEEP's", "s2lat"))
    MainWindow.DCWidget.s2long_chk.setChecked(parser.getboolean("KEEP's", "s2lng"))
    MainWindow.DCWidget.s2rad_chk.setChecked(parser.getboolean("KEEP's", "s2rad"))
    MainWindow.DCWidget.s2temp_chk.setChecked(parser.getboolean("KEEP's", "s2temp"))
    MainWindow.DCWidget.s1tstart_chk.setChecked(parser.getboolean("KEEP's", "s1tstart"))
    MainWindow.DCWidget.s1tmax1_chk.setChecked(parser.getboolean("KEEP's", "s1max1"))
    MainWindow.DCWidget.s1tmax2_chk.setChecked(parser.getboolean("KEEP's", "s1max2"))
    MainWindow.DCWidget.s1tend_chk.setChecked(parser.getboolean("KEEP's", "s1tend"))
    MainWindow.DCWidget.s2tstart_chk.setChecked(parser.getboolean("KEEP's", "s2tstart"))
    MainWindow.DCWidget.s2tmax1_chk.setChecked(parser.getboolean("KEEP's", "s2max1"))
    MainWindow.DCWidget.s2tmax2_chk.setChecked(parser.getboolean("KEEP's", "s2max2"))
    MainWindow.DCWidget.s2tend_chk.setChecked(parser.getboolean("KEEP's", "s2tend"))
    # dc section
    MainWindow.maglite_combobox.setCurrentIndex(parser.getint("DC2015", "maglite"))
    MainWindow.isym_combobox.setCurrentIndex(parser.getint("DC2015", "isym"))
    MainWindow.linkext_spinbox.setValue(parser.getfloat("DC2015", "linkext"))
    MainWindow.desextinc_ipt.setText(parser.get("DC2015", "desextinc"))


def loadCurveParameters(MainWindow, parser):
    vcCount = parser.getint("Curve Count", "velocity curves")
    lcCount = parser.getint("Curve Count", "light curves")

    MainWindow.LoadObservationWidget.vcPropertiesList = [0, 0]
    MainWindow.LoadObservationWidget.lcPropertiesList = []

    i = 0
    while i < vcCount:
        section = "Velocity Curve " + str(i + 1)
        vcprop = classes.CurveProperties("vc")
        vcprop.populateFromParserSection(parser, section)
        vcNumber = vcprop.star
        MainWindow.LoadObservationWidget.vcPropertiesList[vcNumber - 1] = vcprop
        i = i + 1
    i = 0
    while i < lcCount:
        section = "Light Curve " + str(i + 1)
        lcprop = classes.CurveProperties("lc")
        lcprop.populateFromParserSection(parser, section)
        MainWindow.LoadObservationWidget.lcPropertiesList.append(lcprop)
        i = i + 1


def loadEclipseParameters(MainWindow, parser):
    MainWindow.EclipseWidget.filepath_label.setText(parser.get("Eclipse Timing", "filepath"))
    MainWindow.EclipseWidget.filepath_label.setToolTip(parser.get("Eclipse Timing", "filepath"))
    MainWindow.EclipseWidget.iftime_chk.setChecked(parser.getboolean("Eclipse Timing", "iftime"))
    MainWindow.EclipseWidget.ksd_box.setValue(parser.getint("Eclipse Timing", "ksd"))
    MainWindow.EclipseWidget.sigma_ipt.setText(parser.get("Eclipse Timing", "sigma"))
    if parser.get("Eclipse Timing", "filepath") != "None":
        curve = classes.Curve(parser.get("Eclipse Timing", "filepath"))
        if curve.hasError:
            raise ValueError("Eclipse timings caught an error:" + curve.error)
        else:
            MainWindow.EclipseWidget.datawidget.clear()
            for x in curve.lines:
                a = QtGui.QTreeWidgetItem(MainWindow.EclipseWidget.datawidget, x)


def loadProject(MainWindow, parser):
    # check version
    if parser.get("Info", "version") != __dclcver__:
        raise RuntimeError("This project file is for another version of PyWD.\n" +
                           "Current Version: " + __dclcver__ + "\n" + "Project File Version: " +
                           parser.get("Info", "version"))
    if parser.get("Info", "config") != __configver__:
        raise RuntimeError("This config file is incompatible with current version of PyWD.")
    # check for filepaths before modifying ui
    eclipsePath = parser.get("Eclipse Timing", "filepath")
    import os
    if os.path.isfile(eclipsePath) is not True and eclipsePath != "None":
        raise RuntimeError("Can't read eclipse data, file does not exists: " + eclipsePath)
    lcCount = parser.getint("Curve Count", "light curves")
    vcCount = parser.getint("Curve Count", "velocity Curves")
    i = 0
    while i < vcCount:
        section = "Velocity Curve " + str(i + 1)
        filepath = parser.get(section, "filepath")
        if os.path.isfile(filepath) is not True:
            raise RuntimeError("Can't read velocity curve data, file does not exist: " + filepath)
        i = i + 1
    i = 0
    while i < lcCount:
        section = "Light Curve " + str(i + 1)
        filepath = parser.get(section, "filepath")
        if os.path.isfile(filepath) is not True:
            raise RuntimeError("Can't read light curve data, file does not exist: " + filepath)
        i = i + 1
    # modify the ui
    loadMainWindowParameters(MainWindow, parser)
    LoadSpotConfiguration(MainWindow.SpotConfigureWidget, parser)
    loadCurveParameters(MainWindow, parser)
    loadEclipseParameters(MainWindow, parser)


def getTableFromOutput(path, target, offset=3, splitmap=None, occurence=1):
    """
    extract a table from a dc/lc output file.
    :param occurence: which occurence?
    :param path: output file path
    :param target: target string to find
    :param offset: offset of data from target
    :param splitmap: a list that contains cursor positions to slice table manually
    :return: a list of lists containing outputs
    for results:
     [
        [id, curveid, input, corr, output, stderr, l1/(l1+l2), se]
     ]
     for curvestat:
     [
        [curveid, n.obs, std.dev, n.obs in pgs rng, std.dev in phs rng, ref.flux, ref.mag]
     ]
     for o - c:
     [
        [phase, obs, calc, ..., [o-c]]
        or
        [time, phase, obs, calc, ..., [o-c]]
     ]
    """

    table = []
    flag = False
    start = 0
    occured = 0
    with open(path, "r") as dcout:
        for line in dcout:
            if target in line:
                occured = occured + 1
                if occured == occurence:
                    flag = True
            if flag is True:
                if start < offset:
                    start = start + 1
                else:
                    if line == "\n":
                        break
                    else:
                        if splitmap is not None:
                            if splitmap[0] != 0:
                                splitmap.insert(0, 0)
                            tempLine = []
                            i = 0
                            while i < len(splitmap) - 1:
                                value = line[splitmap[i]:splitmap[i+1]]
                                value = value.rstrip(" ")
                                value = value.strip(" ")
                                tempLine.append(value)
                                i = i + 1
                            table.append(tempLine)
                        else:
                            table.append(line.split())
    return table


def getAllTablesFromOutput(path, target, secondTarget, offset=3):
    with open(path, "r") as f:
        rawdata = f.read().split(target)
    rawdata.pop(0)
    data = []
    for list in rawdata:
        a = list.split("\n")
        # trim front
        currentOffset = offset
        while currentOffset > 0:
            a.pop(currentOffset - 1)
            currentOffset = currentOffset - 1
        b = []
        for line in a:
            if line == "":
                break
            else:
                b.append(line.split())
        data.append(b)
    return data


def computeRochePotentials(MainWindow, phase, plotAxis, getPotentials=False):
    # This snippet is only for f1, f2 = 1 for now
    # For in-depth discussion about calculating Roche potentials, refer to:
    #  - Eclipsing Binary Stars: Modeling and Analysis (Kallrath & Milone, 2009, Springer)

    w = float(MainWindow.perr0_ipt.text())
    e = float(MainWindow.e_ipt.text())
    phase_shift = float(MainWindow.pshift_ipt.text())

    true_anomaly = (numpy.pi / 2.0) - w
    eccentric_anomaly = 2.0 * numpy.arctan(numpy.sqrt((1.0 - e) / (1.0 + e)) * numpy.tan(true_anomaly / 2.0))
    mean_anomaly = eccentric_anomaly - e * numpy.sin(eccentric_anomaly)
    conjunction = ((mean_anomaly + w) / (2.0 * numpy.pi)) - 0.25 + phase_shift  # superior conjunction phase
    periastron_passage = 1.0 - mean_anomaly / (2.0 * numpy.pi)
    periastron_phase = conjunction + periastron_passage  # phase of periastron
    while periastron_phase > 1.0:
        periastron_phase = periastron_phase - int(periastron_phase)
    M = 2.0 * numpy.pi * (phase - periastron_phase)
    while M < 0.0:
        M = M + 2.0 * numpy.pi
    f_E = lambda E: E - e * numpy.sin(E) - M
    E = fsolve(f_E, M)
    separation_at_phase = 1.0 - e * numpy.cos(E)

    q = float(MainWindow.rm_ipt.text())
    qIsInverse = False
    if q > 1.0:
        q = 1.0 / q
        qIsInverse = True
    f = 1.0
    f_critical = lambda x: (-1 / x ** 2) - \
                           (q * ((x - separation_at_phase) / pow(numpy.absolute(separation_at_phase - x), 3))) + \
                           (x * f ** 2 * (q + 1)) - (q / separation_at_phase ** 2)  # Appendix E.12.4
    inner_critical_x = fsolve(f_critical, separation_at_phase / 2.0)
    inner_potential = (1 / inner_critical_x) + (q * (
    (1 / numpy.absolute(separation_at_phase - inner_critical_x)) - (inner_critical_x / (separation_at_phase ** 2)))) + (
                          ((q + 1) / 2) * (f ** 2) * (inner_critical_x ** 2))  # Appendix E.12.8

    mu = (1.0 / 3.0) * q / (1.0 + q)
    outer_critical_estimation = 1.0 + mu ** (1.0 / 3.0) + (1.0 / 3.0) * mu ** (2.0 / 3.0) + (1.0 / 9.0) * mu ** \
                                (3.0 / 3.0)
    outer_critical_x = fsolve(f_critical, outer_critical_estimation)
    outer_potential = (1.0 / outer_critical_x) + (q * (
        (1.0 / numpy.absolute(separation_at_phase - outer_critical_x)) - (
        outer_critical_x / (separation_at_phase ** 2)))) + (
                            ((q + 1.0) / 2.0) * (f ** 2) * (outer_critical_x ** 2))  # Appendix E.12.8

    if getPotentials is True:
        return inner_potential, outer_potential

    f_outer_critical = lambda x: 1.0 / (numpy.sqrt(x ** 2)) + q * (1.0 / (numpy.sqrt(
        separation_at_phase ** 2 - 2.0 * x * separation_at_phase + x ** 2)) - x / separation_at_phase ** 2) + f ** 2 * (
    (q + 1.0) / 2.0) * (x ** 2) - outer_potential
    left_limit = fsolve(f_outer_critical, -1.0 * (separation_at_phase / 2.0))
    right_limit = outer_critical_x
    x_axis = numpy.linspace(left_limit, right_limit, 2000)
    z_axis = numpy.linspace(-1, 2, 2000)
    (X, Z) = numpy.meshgrid(x_axis, z_axis)
    all_pots = ((1 / numpy.sqrt(X ** 2 + Z ** 2)) + (q * (
        (1 / numpy.sqrt(
            (separation_at_phase ** 2) - (2 * X * separation_at_phase) + (numpy.sqrt(X ** 2 + Z ** 2) ** 2))) - (
            X / (separation_at_phase ** 2)))) + (0.5 * (f ** 2) * (q + 1) * (X ** 2)))

    if qIsInverse:
        q = 1 / q
    center_of_mass = (separation_at_phase / (1 + (1 / q)))

    x_axis_primary = numpy.linspace(left_limit, inner_critical_x, 2000)
    z_axis_primary = numpy.linspace(-1, 2, 2000)
    (X_primary, Z_primary) = numpy.meshgrid(x_axis_primary, z_axis_primary)
    x_axis_secondary = numpy.linspace(inner_critical_x, right_limit  + 0.2, 2000)
    z_axis_secondary = numpy.linspace(-1, 2, 2000)
    (X_secondary, Z_secondary) = numpy.meshgrid(x_axis_secondary, z_axis_secondary)
    all_pots_primary = ((1 / numpy.sqrt(X_primary ** 2 + Z_primary ** 2)) + (q * (
        (1 / numpy.sqrt(
            (separation_at_phase ** 2) - (2 * X_primary * separation_at_phase) +
            (numpy.sqrt(X_primary ** 2 + Z_primary ** 2) ** 2))) - (
            X_primary / (separation_at_phase ** 2)))) + (0.5 * (f ** 2) * (q + 1) * (X_primary ** 2)))
    all_pots_secondary = ((1 / numpy.sqrt(X_secondary ** 2 + Z_secondary ** 2)) + (q * (
        (1 / numpy.sqrt(
            (separation_at_phase ** 2) - (2 * X_secondary * separation_at_phase) +
            (numpy.sqrt(X_secondary ** 2 + Z_secondary ** 2) ** 2))) - (
            X_secondary / (separation_at_phase ** 2)))) + (0.5 * (f ** 2) * (q + 1) * (X_secondary ** 2)))

    if plotAxis is not None:
        if qIsInverse:
            X = -1.0 * X + separation_at_phase
        plotAxis.contour(X, Z, all_pots, inner_potential, colors="red")
        if e == 0.0:
            plotAxis.contour(X, Z, all_pots, outer_potential, colors="blue")
        plotAxis.contourf(X_primary, Z_primary, all_pots_primary, [float(MainWindow.phsv_ipt.text()),
                                                   float(MainWindow.phsv_ipt.text()) * 1000], cmap='Dark2', vmin=0, vmax=1)
        plotAxis.contourf(X_secondary, Z_secondary, all_pots_secondary, [float(MainWindow.pcsv_ipt.text()),
                                                   float(MainWindow.pcsv_ipt.text()) * 1000], cmap='Dark2', vmin=0, vmax=1)
        plotAxis.plot([0, separation_at_phase, center_of_mass], [0, 0, 0], linestyle="", marker="+",
                                   markersize=10, color="#ff3a3a")
        print "Separation at phase {0}: {1}".format(phase, separation_at_phase)
        print "Inner critical potential: {0}".format(inner_potential)
        print "Outer critical potential: {0}".format(outer_potential)


def computeFillOutFactor(MainWindow):
    e = float(MainWindow.e_ipt.text())
    f1 = float(MainWindow.f1_ipt.text())
    f2 = float(MainWindow.f2_ipt.text())
    if e != 0.0 or f1 != 1.0 or f2 != 1.0 or str(MainWindow.mode_combobox.currentText()) not in ("Mode 0", "Mode 1", "Mode 3"):
        return "N/A"
    else:
        inner_potential, outer_potential = computeRochePotentials(MainWindow, 0.25, None, getPotentials=True)
        inner_potential = inner_potential[0]
        outer_potential = outer_potential[0]
        primary_potential = float(MainWindow.phsv_ipt.text())
        primary_fillout_BM = None

        # Bradstreet 1993 - BinaryMaker
        # for primary component
        if primary_potential > inner_potential:
            primary_fillout_BM = (inner_potential / primary_potential) - 1.0
        if primary_potential <= inner_potential:
            primary_fillout_BM = (inner_potential - primary_potential) / (inner_potential - outer_potential)

        return "{:0.5f}".format(primary_fillout_BM)


def computeConjunctionPhases(MainWindow):
    w = float(MainWindow.perr0_ipt.text())
    e = float(MainWindow.e_ipt.text())
    phase_shift = float(MainWindow.pshift_ipt.text())

    # Calculations below are adopted from JKTEBOP code;
    #  - The equation for phase difference comes from Hilditch (2001) page 238 equation 5.66,
    #  - originally credited to the monograph by Kopal (1959).

    e_fac = numpy.sqrt(1.0 - e**2)
    term1 = 2.0 * numpy.arctan((e * numpy.cos(w)) / e_fac)
    term2 = 2.0 * e * numpy.cos(w) * e_fac / (1.0 - (e * numpy.sin(w)) ** 2)
    phase_diff = (numpy.pi + term1 + term2) / (2.0 * numpy.pi)

    # Calculations below are adopted from;
    #  - Eclipsing Binary Stars: Modeling and Analysis (Kallrath & Milone, 2009, Springer)

    true_anomaly = (numpy.pi / 2.0) - w
    eccentric_anomaly = 2.0 * numpy.arctan(numpy.sqrt((1.0 - e) / (1.0 + e)) * numpy.tan(true_anomaly / 2.0))
    mean_anomaly = eccentric_anomaly - e * numpy.sin(eccentric_anomaly)
    conjunction = ((mean_anomaly + w) / (2.0 * numpy.pi)) - 0.25 + phase_shift
    periastron_passage = 1.0 - mean_anomaly / (2.0 * numpy.pi)
    periastron_phase = conjunction + periastron_passage
    while periastron_phase > 1.0:
        periastron_phase = periastron_phase - int(periastron_phase)

    phase_of_primary_eclipse = conjunction
    phase_of_first_quadrature = conjunction + phase_diff / 2.0
    phase_of_secondary_eclipse = conjunction + phase_diff
    phase_of_second_quadrature = conjunction + (phase_diff / 2.0) + 0.5
    phase_of_periastron = periastron_phase
    phase_of_apastron = periastron_phase + 0.5
    while phase_of_apastron > 1.0:
        phase_of_apastron = phase_of_apastron - int(phase_of_apastron)
    if e == 0.0:
        phase_of_periastron = 0.25
        phase_of_apastron = 0.25

    return phase_of_primary_eclipse, \
           phase_of_first_quadrature, \
           phase_of_secondary_eclipse, \
           phase_of_second_quadrature, \
           phase_of_periastron, \
           phase_of_apastron


def aliasObservations(x, y, start, end):
    """
    :param x: a list containing phases
    :param y: a list containing observations
    :param start: start phase
    :param end: end phase
    :return: aliased observation with the same input format
    """
    if start > end:
        raise ValueError("Start phase can't be larger than stop phase.")

    x = [float(i) for i in x]
    y = [float(i) for i in y]

    distance = int(start - min(x))
    if (distance == 0 and min(x) > start) or (distance < 0 < min(x)):
        distance = distance - 1

    x = [phase + distance for phase in x]

    new_x = x[:]
    new_y = y[:]

    i = 1
    while max(new_x) < end:
        x_temp = [phase + i for phase in x]
        new_x = new_x + x_temp
        new_y = new_y + y[:]
        i = i + 1

    _x = []
    _y = []

    for phase, value in izip(new_x, new_y):
        if start <= phase <= end:
            _x.append(phase)
            _y.append(value)

    return _x, _y


if __name__ == "__main__":
    pass
