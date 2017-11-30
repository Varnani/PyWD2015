import sys
from PyQt4 import QtGui
from functools import partial
from bin import classes
import ConfigParser
import numpy as np
import itertools


def SaveSpotConfiguration(SpotConfigureWidget):
    dialog = QtGui.QFileDialog(SpotConfigureWidget)
    dialog.setDefaultSuffix("spotconfig")
    dialog.setNameFilter("Spot Configuration File (*.spotconfig)")
    dialog.setAcceptMode(1)
    returnCode = dialog.exec_()
    filePath = str((dialog.selectedFiles())[0])
    if filePath != "" and returnCode != 0:
        try:
            parser = ConfigParser.SafeConfigParser()
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
                i += 1
            with open(filePath, 'w') as f:
                parser.write(f)
            SpotConfigureWidget.spotconfigsave_label.setText("Spot config saved: " + filePath)
        except:
            msg = QtGui.QMessageBox()
            msg.setText("An error has ocurred: \n" + str(sys.exc_info()[1]))
            msg.exec_()


def LoadSpotConfiguration(SpotConfigureWidget):
    dialog = QtGui.QFileDialog(SpotConfigureWidget)
    dialog.setAcceptMode(0)
    dialog.setDefaultSuffix("spotconfig")
    dialog.setNameFilter("Spot Configuration File (*.spotconfig)")
    returnCode = dialog.exec_()
    filePath = (dialog.selectedFiles())[0]
    if filePath != "" and returnCode != 0:
        clearSpotConfigureWidget(SpotConfigureWidget)
        parser = ConfigParser.SafeConfigParser()
        with open(filePath, 'r') as f:
            parser.readfp(f)
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
            i += 1
        SpotConfigureWidget.radioButtonGroupA.setExclusive(True)
        SpotConfigureWidget.radioButtonGroupB.setExclusive(True)
        SpotConfigureWidget.spotconfigload_label.setText("Spot config loaded: " + filePath)


def clearSpotConfigureWidget(SpotConfigureWidget):
    # we'll just click every remove button
    for elementList in reversed(SpotConfigureWidget.star1ElementList):
        elementList[7].click()
    for elementList in reversed(SpotConfigureWidget.star2ElementList):
        elementList[7].click()


def addSpotRow(SpotConfigureWidget, starNumber):
    xshiftAmount = 0
    yshiftAmount = 0
    if starNumber == 1:
        SpotConfigureWidget.star1RowCount += 1
        SpotConfigureWidget.star1ElementList.append([])
        xshiftAmount = 0
        yshiftAmount = 30 * SpotConfigureWidget.star1RowCount
    if starNumber == 2:
        SpotConfigureWidget.star2RowCount += 1
        SpotConfigureWidget.star2ElementList.append([])
        xshiftAmount = 460
        yshiftAmount = 30 * SpotConfigureWidget.star2RowCount
    resizeSpotConfigureWidget(SpotConfigureWidget, starNumber)

    # add elements
    # label
    label = QtGui.QLabel(SpotConfigureWidget)
    label.setGeometry(10 + xshiftAmount, 130 + yshiftAmount, 45, 16)
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
    radioA.setGeometry(60 + xshiftAmount, 130 + yshiftAmount, 20, 20)
    radioB.setGeometry(90 + xshiftAmount, 130 + yshiftAmount, 20, 20)
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
    lat_input.setGeometry(120 + xshiftAmount, 130 + yshiftAmount, 51, 20)
    lon_input.setGeometry(190 + xshiftAmount, 130 + yshiftAmount, 51, 20)
    radsp_input.setGeometry(260 + xshiftAmount, 130 + yshiftAmount, 51, 20)
    temsp_input.setGeometry(330 + xshiftAmount, 130 + yshiftAmount, 51, 20)
    lat_input.setText("0")
    lon_input.setText("0")
    radsp_input.setText("0")
    temsp_input.setText("0")
    if starNumber == 1:
        lat_input.setObjectName("star1lat_input" + str(SpotConfigureWidget.star1RowCount - 1))
        lon_input.setObjectName("star1lon_input" + str(SpotConfigureWidget.star1RowCount - 1))
        radsp_input.setObjectName("star1radsp_input" + str(SpotConfigureWidget.star1RowCount - 1))
        temsp_input.setObjectName("star1temsp_input" + str(SpotConfigureWidget.star1RowCount - 1))
        SpotConfigureWidget.star1ElementList[SpotConfigureWidget.star1RowCount - 1].append(lat_input)
        SpotConfigureWidget.star1ElementList[SpotConfigureWidget.star1RowCount - 1].append(lon_input)
        SpotConfigureWidget.star1ElementList[SpotConfigureWidget.star1RowCount - 1].append(radsp_input)
        SpotConfigureWidget.star1ElementList[SpotConfigureWidget.star1RowCount - 1].append(temsp_input)
    if starNumber == 2:
        lat_input.setObjectName("star2lat_input" + str(SpotConfigureWidget.star2RowCount - 1))
        lon_input.setObjectName("star2lon_input" + str(SpotConfigureWidget.star2RowCount - 1))
        radsp_input.setObjectName("star2radsp_input" + str(SpotConfigureWidget.star2RowCount - 1))
        temsp_input.setObjectName("star2temsp_input" + str(SpotConfigureWidget.star2RowCount - 1))
        SpotConfigureWidget.star2ElementList[SpotConfigureWidget.star2RowCount - 1].append(lat_input)
        SpotConfigureWidget.star2ElementList[SpotConfigureWidget.star2RowCount - 1].append(lon_input)
        SpotConfigureWidget.star2ElementList[SpotConfigureWidget.star2RowCount - 1].append(radsp_input)
        SpotConfigureWidget.star2ElementList[SpotConfigureWidget.star2RowCount - 1].append(temsp_input)
    lat_input.show()
    lon_input.show()
    radsp_input.show()
    temsp_input.show()

    # remove button
    remove_button = QtGui.QPushButton(SpotConfigureWidget)
    remove_button.setGeometry(390 + xshiftAmount, 129 + yshiftAmount, 61, 21)
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
    if starNumber == 1:
        SpotConfigureWidget.star1RowCount -= 1
        for element in SpotConfigureWidget.star1ElementList[row]:
            element.hide()
        SpotConfigureWidget.star1ElementList.pop(row)
        i = 0
        for elementList in SpotConfigureWidget.star1ElementList:
            xshiftAmount = 0
            yshiftAmount = 30 * (i + 1)
            elementList[0].setGeometry(10 + xshiftAmount, 130 + yshiftAmount, 41, 16)
            elementList[0].setText("Spot " + str(i + 1))
            elementList[1].setGeometry(60 + xshiftAmount, 130 + yshiftAmount, 16, 17)
            elementList[1].row = i
            elementList[1].toggled.disconnect()
            elementList[1].toggled.connect(partial(
                radioButtonSameSpotCheck, elementList[1], SpotConfigureWidget, starNumber))
            elementList[2].setGeometry(90 + xshiftAmount, 130 + yshiftAmount, 16, 17)
            elementList[2].row = i
            elementList[2].toggled.disconnect()
            elementList[2].toggled.connect(partial(
                radioButtonSameSpotCheck, elementList[2], SpotConfigureWidget, starNumber))
            elementList[3].setGeometry(120 + xshiftAmount, 130 + yshiftAmount, 51, 20)
            elementList[4].setGeometry(190 + xshiftAmount, 130 + yshiftAmount, 51, 20)
            elementList[5].setGeometry(260 + xshiftAmount, 130 + yshiftAmount, 51, 20)
            elementList[6].setGeometry(330 + xshiftAmount, 130 + yshiftAmount, 51, 20)
            elementList[7].setGeometry(390 + xshiftAmount, 129 + yshiftAmount, 61, 21)
            elementList[7].row = int(i)
            elementList[7].clicked.disconnect()
            elementList[7].clicked.connect(partial(removeSpotRow, SpotConfigureWidget, elementList[7], starNumber))
            i += 1
    if starNumber == 2:
        SpotConfigureWidget.star2RowCount -= 1
        for element in SpotConfigureWidget.star2ElementList[row]:
            element.hide()
        SpotConfigureWidget.star2ElementList.pop(row)
        i = 0
        for elementList in SpotConfigureWidget.star2ElementList:
            xshiftAmount = 460
            yshiftAmount = 30 * (i + 1)
            elementList[0].setGeometry(10 + xshiftAmount, 130 + yshiftAmount, 41, 16)
            elementList[0].setText("Spot " + str(i + 1))
            elementList[1].setGeometry(60 + xshiftAmount, 130 + yshiftAmount, 16, 17)
            elementList[1].row = i
            elementList[1].toggled.disconnect()
            elementList[1].toggled.connect(partial(
                radioButtonSameSpotCheck, elementList[1], SpotConfigureWidget, starNumber))
            elementList[2].setGeometry(90 + xshiftAmount, 130 + yshiftAmount, 16, 17)
            elementList[2].row = i
            elementList[2].toggled.disconnect()
            elementList[2].toggled.connect(partial(
                radioButtonSameSpotCheck, elementList[2], SpotConfigureWidget, starNumber))
            elementList[3].setGeometry(120 + xshiftAmount, 130 + yshiftAmount, 51, 20)
            elementList[4].setGeometry(190 + xshiftAmount, 130 + yshiftAmount, 51, 20)
            elementList[5].setGeometry(260 + xshiftAmount, 130 + yshiftAmount, 51, 20)
            elementList[6].setGeometry(330 + xshiftAmount, 130 + yshiftAmount, 51, 20)
            elementList[7].setGeometry(390 + xshiftAmount, 129 + yshiftAmount, 61, 21)
            elementList[7].row = i
            elementList[7].clicked.disconnect()
            elementList[7].clicked.connect(partial(removeSpotRow, SpotConfigureWidget, elementList[7], starNumber))
            i += 1

    resizeSpotConfigureWidget(SpotConfigureWidget, starNumber)


def resizeSpotConfigureWidget(SpotConfigureWidget, starNumber):
    yshiftAmount = 0
    if SpotConfigureWidget.star1RowCount > SpotConfigureWidget.star2RowCount:
        yshiftAmount = 30 * SpotConfigureWidget.star1RowCount
    if SpotConfigureWidget.star1RowCount < SpotConfigureWidget.star2RowCount:
        yshiftAmount = 30 * SpotConfigureWidget.star2RowCount
    if SpotConfigureWidget.star1RowCount == SpotConfigureWidget.star2RowCount:
        yshiftAmount = 30 * SpotConfigureWidget.star2RowCount
    if starNumber == 1:
        y = SpotConfigureWidget.star1RowCount * 30
        SpotConfigureWidget.addspot1_btn.setGeometry(10, y + 160, 442, 25)
    if starNumber == 2:
        y = SpotConfigureWidget.star2RowCount * 30
        SpotConfigureWidget.addspot2_btn.setGeometry(469, y + 160, 442, 25)
    SpotConfigureWidget.line_3.setGeometry(441, 130, 41, 61 + yshiftAmount)
    SpotConfigureWidget.setMaximumHeight(yshiftAmount + 200)
    SpotConfigureWidget.setMinimumHeight(yshiftAmount + 200)
    SpotConfigureWidget.resize(920, yshiftAmount + 200)


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


def addLightCurve(LoadWidget):
    dialog = QtGui.QFileDialog(LoadWidget)
    dialog.setAcceptMode(0)
    returnCode = dialog.exec_()
    filePath = (dialog.selectedFiles())[0]
    if filePath != "" and returnCode != 0:
        exitcode = 0
        try:
            LoadWidget.EditLightCurveDialog.load(filePath)  # populate edit curve widget
            LoadWidget.EditLightCurveDialog.setWindowTitle("Load Light Curve")
            exitcode = LoadWidget.EditLightCurveDialog.exec_()  # wait for edit curve widget to finish
            LoadWidget.EditLightCurveDialog.setWindowTitle("Edit Light Curve")
        except IndexError:
            msg = QtGui.QMessageBox()
            msg.setText("File is not a valid data source:\n" + filePath)
            msg.exec_()
            exitcode = 0
        except:
            msg = QtGui.QMessageBox()
            msg.setText("Unknown exception is caught:\n" + sys.exc_info()[0])
            msg.exec_()
            exitcode = 0
        if exitcode == 1:
            lcprop = classes.LightCurveProperties(LoadWidget.EditLightCurveDialog)
            LoadWidget.lcPropertiesList.append(lcprop)  # store accepted lcprop

            # start adding row
            LoadWidget.lcElementList.append([])  # get a new row
            LoadWidget.lcCount += 1  # increment lc count since we are adding a row
            shiftAmount = (LoadWidget.lcCount * 40)  # shifting this number of pixels downwards
            resizeLoadWidget(LoadWidget)

            # add new elements
            # label
            label = QtGui.QLabel(LoadWidget)  # load element
            label.setGeometry(40, 140 + shiftAmount, 90, 21)  # set geometry
            label.setText("Light Curve " + str(LoadWidget.lcCount))  # set text
            label.setObjectName("lclabel" + str(LoadWidget.lcCount))  # set object name
            LoadWidget.lcElementList[LoadWidget.lcCount - 1].append(label)  # store element in the element list
            label.show()  # show the element

            # file path
            path = QtGui.QLineEdit(LoadWidget)  # load element
            path.setGeometry(130, 140 + shiftAmount, 381, 20)  # set geometry
            path.setText(filePath)  # set text
            path.setObjectName("lcpath" + str(LoadWidget.lcCount))  # set object name
            path.setReadOnly(True)  # set read only
            LoadWidget.lcElementList[LoadWidget.lcCount - 1].append(path)  # store element in the element list
            path.show()  # show the element

            # edit button
            row = LoadWidget.lcCount - 1  # current row index
            edit = QtGui.QPushButton(LoadWidget)
            edit.setGeometry(520, 140 + shiftAmount, 51, 21)
            edit.setText("Edit")
            edit.setObjectName("lcedit" + str(LoadWidget.lcCount))
            edit.clicked.connect(partial(editLightCurve, LoadWidget, row))
            LoadWidget.lcElementList[LoadWidget.lcCount - 1].append(edit)
            edit.show()

            # remove button
            remove = QtGui.QPushButton(LoadWidget)
            remove.setGeometry(580, 140 + shiftAmount, 61, 21)
            remove.setText("Remove")
            remove.setObjectName("lcload" + str(LoadWidget.lcCount))
            remove.clicked.connect(partial(removeLightCurve, LoadWidget, row))
            LoadWidget.lcElementList[LoadWidget.lcCount - 1].append(remove)
            remove.show()


def editLightCurve(LoadWidget, buttonRow):
    LoadWidget.EditLightCurveDialog.populate(LoadWidget.lcPropertiesList[buttonRow])  # populate ui from obj
    exitcode = LoadWidget.EditLightCurveDialog.exec_()  # enter dialog loop
    if exitcode == 1:  # if changes are accepted;
        lcprop = classes.LightCurveProperties(LoadWidget.EditLightCurveDialog)  # create object
        LoadWidget.lcPropertiesList[buttonRow] = lcprop  # assign it to the list


def removeLightCurve(LoadWidget, buttonRow):
    LoadWidget.lcCount -= 1  # decrement lcCount since we are removing a row

    # hide elements
    LoadWidget.lcElementList[buttonRow][0].hide()
    LoadWidget.lcElementList[buttonRow][1].hide()
    LoadWidget.lcElementList[buttonRow][2].hide()
    LoadWidget.lcElementList[buttonRow][3].hide()

    # remove elements
    LoadWidget.lcElementList[buttonRow][0].deleteLater()
    LoadWidget.lcElementList[buttonRow][1].deleteLater()
    LoadWidget.lcElementList[buttonRow][2].deleteLater()
    LoadWidget.lcElementList[buttonRow][3].deleteLater()
    LoadWidget.lcElementList.pop(buttonRow)

    # discard lc properties
    LoadWidget.lcPropertiesList.pop(buttonRow)

    # move elements
    row = 0
    for elementList in LoadWidget.lcElementList:
        for element in elementList:
            element.move(element.x(), 180 + (40 * row))
        row += 1

    # rename labels
    nlc = 1
    for elementList in LoadWidget.lcElementList:
        elementList[0].setText("Light Curve " + str(nlc))
        nlc += 1

    # reassing button.clicked and edit.clicked events with some black magic
    i = 0
    for elementList in LoadWidget.lcElementList:
        elementList[3].clicked.disconnect()
        elementList[2].clicked.disconnect()
        elementList[3].clicked.connect(partial(removeLightCurve, LoadWidget, i))
        elementList[2].clicked.connect(partial(editLightCurve, LoadWidget, i))
        i += 1

    # resize window
    resizeLoadWidget(LoadWidget)


def resizeLoadWidget(LoadWidget):
    shiftAmount = LoadWidget.lcCount * 40
    LoadWidget.nlc_label.setText("Light curve count: " + str(LoadWidget.lcCount))  # update nlc label

    # resize the widget
    LoadWidget.setMaximumHeight(shiftAmount + 215)
    LoadWidget.setMinimumHeight(shiftAmount + 215)
    LoadWidget.resize(650, shiftAmount + 215)

    # move existing elements
    LoadWidget.lcadd_btn.setGeometry(20, shiftAmount + 180, 115, 25)  # move 'add light curve' button
    LoadWidget.nlc_label.setGeometry(500, shiftAmount + 180, 141, 21)  # move 'light curve number' label


def editVelocityCurve(vcNumber, LoadWidget):
    if LoadWidget.vcPropertiesList[vcNumber - 1] is not 0:
        if vcNumber == 1:
            LoadWidget.EditVelocityCurveDialog.populate(LoadWidget.vcPropertiesList[0])
            exitcode = LoadWidget.EditVelocityCurveDialog.exec_()
            if exitcode == 1:
                vcprop = classes.VelocityCurveProperties(LoadWidget.EditVelocityCurveDialog)
                LoadWidget.vcPropertiesList[0] = vcprop
        if vcNumber == 2:
            LoadWidget.EditVelocityCurveDialog.populate(LoadWidget.vcPropertiesList[1])
            exitcode = LoadWidget.EditVelocityCurveDialog.exec_()
            if exitcode == 1:
                vcprop = classes.VelocityCurveProperties(LoadWidget.EditVelocityCurveDialog)
                LoadWidget.vcPropertiesList[1] = vcprop


def removeVelocityCurve(vcNumber, LoadWidget):
    if vcNumber == 1:
        LoadWidget.vcPropertiesList[0] = 0
        LoadWidget.vc1load_btn.setText("Load")
        LoadWidget.vc1load_btn.clicked.disconnect()
        LoadWidget.vc1load_btn.clicked.connect(partial(loadVelocityCurve, 1, LoadWidget))
        LoadWidget.vc1_fileline.setText("Load a file...")
    if vcNumber == 2:
        LoadWidget.vcPropertiesList[1] = 0
        LoadWidget.vc2load_btn.setText("Load")
        LoadWidget.vc2load_btn.clicked.disconnect()
        LoadWidget.vc2load_btn.clicked.connect(partial(loadVelocityCurve, 2, LoadWidget))
        LoadWidget.vc2_fileline.setText("Load a file...")


def loadVelocityCurve(vcNumber, LoadWidget):
    dialog = QtGui.QFileDialog(LoadWidget)
    dialog.setAcceptMode(0)
    returnCode = dialog.exec_()
    fileName = (dialog.selectedFiles())[0]
    if fileName != "" and returnCode != 0:
        exitcode = 0
        try:
            LoadWidget.EditVelocityCurveDialog.load(fileName)
            LoadWidget.EditVelocityCurveDialog.setWindowTitle("Load Velocity Curve")
            exitcode = LoadWidget.EditVelocityCurveDialog.exec_()
            LoadWidget.EditVelocityCurveDialog.setWindowTitle("Edit Velocity Curve")
        except IndexError:
            msg = QtGui.QMessageBox()
            msg.setText("File is not a valid data source:\n" + fileName)
            msg.exec_()
            exitcode = 0
        except:
            msg = QtGui.QMessageBox()
            msg.setText("Unknown exception is caught:\n" + str(sys.exc_info()[0]))
            msg.exec_()
            exitcode = 0
        if exitcode == 1:
            if vcNumber == 1:
                vcprop = classes.VelocityCurveProperties(LoadWidget.EditVelocityCurveDialog)
                LoadWidget.vcPropertiesList[0] = vcprop
                LoadWidget.vc1_fileline.setText(fileName)
                LoadWidget.vc1load_btn.clicked.disconnect()
                LoadWidget.vc1load_btn.clicked.connect(partial(removeVelocityCurve, 1, LoadWidget))
                LoadWidget.vc1load_btn.setText("Remove")
            if vcNumber == 2:
                vcprop = classes.VelocityCurveProperties(LoadWidget.EditVelocityCurveDialog)
                LoadWidget.vcPropertiesList[1] = vcprop
                LoadWidget.vc2_fileline.setText(fileName)
                LoadWidget.vc2load_btn.clicked.disconnect()
                LoadWidget.vc2load_btn.clicked.connect(partial(removeVelocityCurve, 2, LoadWidget))
                LoadWidget.vc2load_btn.setText("Remove")


def loadEclipseTimings(EclipseWidget):
    removeEclipseTimings(EclipseWidget)
    dialog = QtGui.QFileDialog(EclipseWidget)
    dialog.setAcceptMode(0)
    returnCode = dialog.exec_()
    fileName = str((dialog.selectedFiles())[0])
    if fileName != "" and returnCode != 0:
        try:
            lines = []
            with open(fileName) as f:
                for line in f:
                    i = line.split()
                    if len(i) is not 0:
                        lines.append(i)
            EclipseWidget.timeList = [x[0] for x in lines]
            EclipseWidget.typeList = [x[1] for x in lines]
            EclipseWidget.weightList = [x[2] for x in lines]
            EclipseWidget.lines = lines
            for x in lines:
                a = QtGui.QTreeWidgetItem(EclipseWidget.datawidget, x)
            EclipseWidget.filepath_label.setText(fileName)
            EclipseWidget.filepath_label.setToolTip(fileName)
        except IndexError:
            msg = QtGui.QMessageBox()
            msg.setText("File is not a valid data source:\n" + fileName)
            msg.exec_()
        except:
            msg = QtGui.QMessageBox()
            msg.setText("Unknown exception is caught:\n" + sys.exc_info()[0])
            msg.exec_()


def removeEclipseTimings(EclipseWidget):
    EclipseWidget.datawidget.clear()
    EclipseWidget.timeList = []
    EclipseWidget.typeList = []
    EclipseWidget.weighList = []
    EclipseWidget.lines = []
    EclipseWidget.filepath_label.setText("None")
    EclipseWidget.filepath_label.setToolTip("")
    EclipseWidget.sigma_ipt.setText("0")
    EclipseWidget.ksd_box.setValue(1)


def formatEcc(ipt):
    f_ipt = float(ipt)
    if f_ipt > 1 or f_ipt < 0:
        raise ValueError("Invalid eccentricity value: " + ipt)
    else:
        output = "{:6.5f}".format(f_ipt)
        return output[1:]


def formatInput(ipt, width, precision, exponent, isDeg=False):
    ipt = str(ipt)
    if ipt == "":
        raise IndexError("Inputs can't be blank.")
    f_ipt = float(ipt)
    if isDeg:
        f_ipt = f_ipt * np.pi / 180.0  # convert to radians
        ipt = str(f_ipt)
    output = ""
    if float(1) > f_ipt > float(-1):
        if f_ipt == float(0):
            return (" " * (width - 2 - precision)) + "0." + ("0" * precision)
        if width - 6 - precision >= 0:
            output = "{:> {width}.{precision}g}".format(f_ipt, width=width, precision=precision)
        else:
            output = "{:> {width}.{precision}f}".format(f_ipt, width=width, precision=precision)
    if f_ipt >= float(1) or f_ipt < float(0):
        output = "{:> {width}.{precision}f}".format(f_ipt, width=width, precision=precision)
    output = output.rstrip("0")
    if output[-1] == ".":
        output = output + "0"
    output = " " * (width - len(output)) + output
    if len(output) > width:
        raise IndexError("This input can't be formatted into dcin.active file: " + ipt +
                         "\nMaximum character lenght: " + str(width) +
                         "\nMaximum decimal precision: " + str(precision) +
                         "\nTried to write: " + output +
                         "\nLenght: " + str(len(output)) +
                         "\nPlease reformat your input parameter.")
    else:
        return output.replace("e", exponent)


def evalCheckBox(checkBox):
    if checkBox.isChecked():
        return "1"
    else:
        return "0"


def runDc(MainWindow):
    dcin = exportDc(MainWindow)
    msg = QtGui.QMessageBox(MainWindow)
    if dcin[0] != "":
        msg.setWindowTitle("PyWD - Fatal Error")
        msg.setText("There were errors while parsing inputs:\n" + dcin[0] + "\n")
        if dcin[1] != "":
            msg.setText(msg.text() + "\nPlus, warnings were encountered: \n" + dcin[1])
        msg.exec_()
    else:
        if dcin[1] != "":
            title = "PyWD - Warning"
            text = "Warnings are encountered while parsing inputs: \n" + dcin[1] + \
                   "\nDo you still want to run the DC Program?"
            answer = QtGui.QMessageBox.question(MainWindow, title, text, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if answer == QtGui.QMessageBox.Yes:
                try:
                    cwd = ""
                    import os
                    import platform
                    if platform.system() == "Windows":
                        cwd = os.getcwd() + "\wd\dcin.active"
                    if platform.system() == "Linux":
                        cwd = os.getcwd() + "/wd/dcin.active"
                    with open(cwd, "w") as f:
                        f.write(dcin[2])
                    # TODO continue implementing
                except IOError as ex:
                    msg.setWindowTitle("PyWD - IO Error")
                    msg.setText("An IO error has been caught:\n" + ex.strerror + "\n" +
                                ex.filename.rstrip("dcin.active"))
                    msg.exec_()
                except:
                    msg.setWindowTitle("PyWD - Unknown Exception")
                    msg.setText("Unknown exception has ben caught: " + str(sys.exc_info()))
                    msg.exec_()


def exportDc(MainWindow):
    """
    Constructs a dcin.active file from MainWindow object
    :param MainWindow: A MainWindow QtGui interface object
    :return: a list with 3 elements:
        [0]: Errors if any.
            If there is, [2] will be "FATAL"
        [1]: Warnings if any.
            This won't interrupt parsing the dcin.active file. These errors most likely break the DC program though.
        [2]: dcin.active itself, ready to write.
    """
    result = ["", "", ""]
    try:
        def _formatDels(ipt):  # only used in dcin.active
            error = "This del can't be formatted into 7 character limitation of dcin.active file: " + ipt
            ipt = str(ipt)  # convert to string from QString
            float(ipt)  # sanity check first
            if float(ipt) < 0:
                msg = "Del's must be larger than 0: " + ipt
                raise IndexError(msg)
            if ipt == "0":
                return "+0.0d-0"
            if 0 < float(ipt) < 0.1:
                if len(ipt) > 12:
                    msg = error + "\nMake sure your input is larger than 1x10^-8"
                    raise IndexError(msg)
                else:
                    a = ipt[2:]  # trim '0.'
                    i = 1
                    for char in a:
                        if char is "0":
                            i += 1
                    b = "+" + str(float(ipt) * pow(10, i)) + "d-" + str(i)
                    if len(b) > 7:
                        msg = error + "\nMake sure your input's non-zero fractional " \
                                      "part consist of 2 digits, ex. 0.00056"
                        raise IndexError(msg)
                    else:
                        return b
            if 0.1 <= float(ipt) < 10:
                if len(ipt) is 1:
                    ipt = ipt + ".0"
                a = "+" + ipt + "d-0"
                if len(a) > 7:
                    msg = error + "\nMake sure your input is made of 1 integer and 1 fractional part, ex. 8.3"
                    raise IndexError(msg)
                else:
                    return a
            if 10 <= float(ipt):
                a = str(float(ipt) / float(pow(10, (len(ipt) - 1))))
                if len(a) > 3 or len(ipt) > 10:
                    msg = error + "\nMake sure your input's every integer other than leftmost 2 are 0, with " \
                          + "maximum number of 8 trailing zeroes, ex. 120000"
                    raise IndexError(msg)
                else:
                    if len(a) == 1:
                        a = a + ".0"
                    return "+" + a + "d+" + str(len(ipt) - 1)

        def _formatKeeps(keep):  # only used in dcin.active
            if keep.isChecked():
                return "0"
            else:
                return "1"

        vunit = float(MainWindow.vunit_ipt.text())
        if vunit != float(1):
            result[1] = result[1] + "\nVUnit parameter is different than 1:" + \
                        "\nVGamma, velocity curve sigmas and all velocity observations " \
                        "will be divided by VUnit, as it is required by DC program.\n"

        line1 = " {0} {1} {2} {3} {4} {5} {6} {7}\n".format(
            _formatDels(MainWindow.del_s1lat_ipt.text()),
            _formatDels(MainWindow.del_s1lng_ipt.text()),
            _formatDels(MainWindow.del_s1agrad_ipt.text()),
            _formatDels(MainWindow.del_s1tmpf_ipt.text()),
            _formatDels(MainWindow.del_s2lat_ipt.text()),
            _formatDels(MainWindow.del_s2lng_ipt.text()),
            _formatDels(MainWindow.del_s2agrad_ipt.text()),
            _formatDels(MainWindow.del_s2tmpf_ipt.text())
        )
        line2 = " {0} {1} {2} {3} {4} {5} {6} {7} {8} {9} {10}\n".format(
            _formatDels(MainWindow.del_a_ipt.text()),
            _formatDels(MainWindow.del_e_ipt.text()),
            _formatDels(MainWindow.del_perr0_ipt.text()),
            _formatDels(MainWindow.del_f1_ipt.text()),
            _formatDels(MainWindow.del_f2_ipt.text()),
            _formatDels(MainWindow.del_pshift_ipt.text()),
            _formatDels(MainWindow.del_i_ipt.text()),
            _formatDels(MainWindow.del_g1_ipt.text()),
            _formatDels(MainWindow.del_g2_ipt.text()),
            _formatDels(MainWindow.del_t1_ipt.text()),
            _formatDels(MainWindow.del_t2_ipt.text())
        )
        line3 = " {0} {1} {2} {3} {4} {5} {6} {7} {8}\n".format(
            _formatDels(MainWindow.del_alb1_ipt.text()),
            _formatDels(MainWindow.del_alb2_ipt.text()),
            _formatDels(MainWindow.del_pot1_ipt.text()),
            _formatDels(MainWindow.del_pot2_ipt.text()),
            _formatDels(MainWindow.del_q_ipt.text()),
            _formatDels(MainWindow.del_l1_ipt.text()),
            _formatDels(MainWindow.del_l2_ipt.text()),
            _formatDels(MainWindow.del_x1_ipt.text()),
            _formatDels(MainWindow.del_x2_ipt.text())
        )
        block1 = "{0}{1}{2}{3}".format(
            _formatKeeps(MainWindow.s1lat_chk),
            _formatKeeps(MainWindow.s1long_chk),
            _formatKeeps(MainWindow.s1rad_chk),
            _formatKeeps(MainWindow.s1temp_chk),
        )
        block2 = "{0}{1}{2}{3}".format(
            _formatKeeps(MainWindow.s2lat_chk),
            _formatKeeps(MainWindow.s2long_chk),
            _formatKeeps(MainWindow.s2rad_chk),
            _formatKeeps(MainWindow.s2temp_chk)
        )
        block3 = "{0}{1}{2}{3}{4}{5}{6}".format(
            _formatKeeps(MainWindow.a_chk),
            _formatKeeps(MainWindow.e_chk),
            _formatKeeps(MainWindow.perr0_chk),
            _formatKeeps(MainWindow.f1_chk),
            _formatKeeps(MainWindow.f2_chk),
            _formatKeeps(MainWindow.pshift_chk),
            _formatKeeps(MainWindow.vgam_chk)
        )
        block4 = "{0}{1}{2}{3}{4}".format(
            _formatKeeps(MainWindow.incl_chk),
            _formatKeeps(MainWindow.g1_chk),
            _formatKeeps(MainWindow.g2_chk),
            _formatKeeps(MainWindow.t1_chk),
            _formatKeeps(MainWindow.t2_chk)
        )
        block5 = "{0}{1}{2}{3}{4}".format(
            _formatKeeps(MainWindow.alb1_chk),
            _formatKeeps(MainWindow.alb2_chk),
            _formatKeeps(MainWindow.pot1_chk),
            _formatKeeps(MainWindow.pot2_chk),
            _formatKeeps(MainWindow.q_chk)
        )
        block6 = "{0}{1}{2}{3}{4}".format(
            _formatKeeps(MainWindow.jd0_chk),
            _formatKeeps(MainWindow.p0_chk),
            _formatKeeps(MainWindow.dpdt_chk),
            _formatKeeps(MainWindow.dperdt_chk),
            _formatKeeps(MainWindow.a3b_chk),
        )
        block7 = "{0}{1}{2}{3}{4}".format(
            _formatKeeps(MainWindow.p3b_chk),
            _formatKeeps(MainWindow.xinc3b_chk),
            _formatKeeps(MainWindow.e3b_chk),
            _formatKeeps(MainWindow.perr3b_chk),
            _formatKeeps(MainWindow.tc3b_chk),
        )
        block8 = "11111"  # unused block
        block9 = "{0}{1}{2}{3}{4}".format(
            _formatKeeps(MainWindow.logd_chk),
            _formatKeeps(MainWindow.desextinc_chk),
            "1",  # will implement later
            "1",
            "1",
        )
        block10 = "11111"  # will implement later
        block11 = "11111"  # unused block
        block12 = "{0}{1}{2}{3}{4}".format(
            _formatKeeps(MainWindow.l1_chk),
            _formatKeeps(MainWindow.l2_chk),
            _formatKeeps(MainWindow.x1_chk),
            _formatKeeps(MainWindow.x2_chk),
            _formatKeeps(MainWindow.el3_chk)
        )
        line4 = " " + block1 + " " + block2 + " " + block3 + " " + block4 + " " + block5 + \
                " " + block6 + " " + block7 + " " + block8 + " " + block9 + " " + block10 + \
                " " + block11 + " " + block12 + " 01 1.000d-05 1.000\n"
        spot1 = "  0  0"
        spot2 = "  0  0"
        if len(MainWindow.SpotConfigureWidget.star1ElementList) != 0:
            i = 1
            for radioButtonAList in MainWindow.SpotConfigureWidget.star1ElementList:
                if radioButtonAList[1].isChecked():
                    spot1 = "  1  {0}".format(i)
                    break
                i += 1
            i = 1
            for radioButtonBList in MainWindow.SpotConfigureWidget.star1ElementList:
                if radioButtonBList[2].isChecked():
                    spot2 = "  1  {0}".format(i)
                    break
                i += 1
        if len(MainWindow.SpotConfigureWidget.star2ElementList) != 0:
            i = 1
            for radioButtonAList in MainWindow.SpotConfigureWidget.star2ElementList:
                if radioButtonAList[1].isChecked():
                    spot1 = "  2  {0}".format(i)
                    break
                i += 1
            i = 1
            for radioButtonBList in MainWindow.SpotConfigureWidget.star2ElementList:
                if radioButtonBList[2].isChecked():
                    spot2 = "  2  {0}".format(i)
                    break
                i += 1
        line5 = spot1 + spot2 + "\n"
        ifvc1 = "0"
        ifvc2 = "0"
        if MainWindow.LoadWidget.vcPropertiesList[0] != 0:
            ifvc1 = "1"
        if MainWindow.LoadWidget.vcPropertiesList[1] != 0:
            ifvc2 = "1"
        isymDict = {
            "Symmetrical": "1",
            "Asymmetrical": "0"
        }
        nlc = ((2 - len(str(MainWindow.LoadWidget.lcCount))) * "0") + str(MainWindow.LoadWidget.lcCount)
        line6 = ifvc1 + " " + ifvc2 + " " + nlc \
                + " 0" + " 2" + " 0" + " " + \
                isymDict[str(MainWindow.isym_combobox.currentText())] + " 1" + " " + \
                evalCheckBox(MainWindow.ifder_chk) + " " + evalCheckBox(MainWindow.iflcin_chk) \
                + " " + evalCheckBox(MainWindow.ifoc_chk) + "\n"
        ldDict = {
            "Linear Cosine": "1",
            "Logarithmic": "2",
            "Square Root": "3"
        }
        ld1_sign = ""
        ld2_sign = ""
        if MainWindow.ld1_chk.isChecked():
            ld1_sign = "+"
        else:
            ld1_sign = "-"

        if MainWindow.ld2_chk.isChecked():
            ld2_sign = "+"
        else:
            ld2_sign = "-"
        nomaxDict = {
            "Trapezoidal": "0",
            "Triangular": "1"
        }
        magliteDict = {
            "Flux": "0",
            "Magnitude": "1"
        }
        ld1 = ld1_sign + ldDict[str(MainWindow.ld1_combobox.currentText())]
        ld2 = ld2_sign + ldDict[str(MainWindow.ld2_combobox.currentText())]
        line7 = str(MainWindow.nref_spinbox.value()) + " " + evalCheckBox(MainWindow.mref_chk) + " " \
                + evalCheckBox(MainWindow.SpotConfigureWidget.ifsmv1_chk) + " " \
                + evalCheckBox(MainWindow.SpotConfigureWidget.ifsmv2_chk) + " " \
                + evalCheckBox(MainWindow.icor1_chk) + " " + evalCheckBox(MainWindow.icor2_chk) + " " \
                + evalCheckBox(MainWindow.if3b_chk) \
                + " " + ld1 + " " + ld2 + " " \
                + evalCheckBox(MainWindow.SpotConfigureWidget.kspev_chk) + " " \
                + evalCheckBox(MainWindow.SpotConfigureWidget.kspot_chk) + " " \
                + nomaxDict[str(MainWindow.SpotConfigureWidget.nomax_combobox.currentText())] + " " \
                + evalCheckBox(MainWindow.ifcgs_chk) + " " \
                + magliteDict[str(MainWindow.maglite_combobox.currentText())] + " " \
                + str(MainWindow.linkext_spinbox.value()) + " " \
                + formatInput(MainWindow.desextinc_ipt.text(), 7, 4, "F") + "\n"

        jdDict = {
            "Time": "1",
            "Phase": "2"
        }

        nga = " " * (3 - len(str(MainWindow.nga_spinbox.value()))) + str(MainWindow.nga_spinbox.value())

        line8 = jdDict[str(MainWindow.jdphs_combobox.currentText())] + \
                formatInput(MainWindow.jd0_ipt.text(), 15, 6, "F") + \
                formatInput(MainWindow.p0_ipt.text(), 17, 10, "D") + \
                formatInput(MainWindow.dpdt_ipt.text(), 14, 6, "D") + \
                formatInput(MainWindow.pshift_ipt.text(), 10, 5, "F") + \
                formatInput(MainWindow.delph_ipt.text(), 8, 5, "F") + nga + "\n"

        modeDict = {
            "Mode -1": "-1",
            "Mode 0": " 0",
            "Mode 1": " 1",
            "Mode 2": " 2",
            "Mode 3": " 3",
            "Mode 4": " 4",
            "Mode 5": " 5",
            "Mode 6": " 6"
        }

        ifatDict = {
            "Stellar Atmosphere": " 1",
            "Blackbody": " 0"
        }

        n1 = " " * (4 - len(str(MainWindow.n1_spinbox.value()))) + str(MainWindow.n1_spinbox.value())
        n2 = " " * (4 - len(str(MainWindow.n2_spinbox.value()))) + str(MainWindow.n2_spinbox.value())
        n1l = " " * (4 - len(str(MainWindow.n1l_spinbox.value()))) + str(MainWindow.n1l_spinbox.value())
        n2l = " " * (4 - len(str(MainWindow.n2l_spinbox.value()))) + str(MainWindow.n2l_spinbox.value())

        line9 = modeDict[str(MainWindow.mode_combobox.currentText())] + " " + evalCheckBox(MainWindow.ipb_chk) + \
                ifatDict[str(MainWindow.ifat1_combobox.currentText())] + \
                ifatDict[str(MainWindow.ifat2_combobox.currentText())] + n1 + n2 + n1l + n2l + \
                formatInput(MainWindow.perr0_ipt.text(), 13, 6, "F", isDeg=True) + \
                formatInput(MainWindow.dperdt_ipt.text(), 13, 5, "D") + \
                formatInput(MainWindow.the_ipt.text(), 8, 5, "F") + \
                formatInput(MainWindow.vunit_ipt.text(), 9, 3, "F") + "\n"

        line10 = formatEcc(MainWindow.e_ipt.text()) + formatInput(MainWindow.a_ipt.text(), 13, 6, "D") + \
                 formatInput(MainWindow.f1_ipt.text(), 10, 4, "F") + \
                 formatInput(MainWindow.f2_ipt.text(), 10, 4, "F") + \
                 formatInput((float(MainWindow.vgam_ipt.text())/vunit), 10, 4, "F") + \
                 formatInput(MainWindow.xincl_ipt.text(), 9, 3, "F") + \
                 formatInput(MainWindow.gr1_spinbox.value(), 7, 3, "F") + \
                 formatInput(MainWindow.gr2_spinbox.value(), 7, 3, "F") + \
                 formatInput(MainWindow.abunin_ipt.text(), 7, 2, "F") + \
                 formatInput(MainWindow.SpotConfigureWidget.fspot1_ipt.text(), 10, 4, "F") + \
                 formatInput(MainWindow.SpotConfigureWidget.fspot2_ipt.text(), 10, 4, "F") + "\n"

        if float(MainWindow.tavh_ipt.text()) < float(1000) or float(MainWindow.tavc_ipt.text()) < float(1000):
            result[1] = result[1] + "\nEntered surface temperature value is lower than 1000 Kelvin:" + \
                        "\nKeep in mind that surface temperature parameters will be " + \
                        "divided by 10,000 before writing into dcin.active file, as it is required by DC program." + \
                        "\nMake sure you provide surface temperatures as it is, not in [T/10,000] format.\n"

        line11 = formatInput(float(MainWindow.tavh_ipt.text()) / 10000.0, 7, 4, "F") + \
                 formatInput(float(MainWindow.tavc_ipt.text()) / 10000.0, 8, 4, "F") + \
                 formatInput(MainWindow.alb1_spinbox.value(), 7, 3, "F") + \
                 formatInput(MainWindow.alb2_spinbox.value(), 7, 3, "F") + \
                 formatInput(MainWindow.phsv_ipt.text(), 13, 6, "D") + \
                 formatInput(MainWindow.pcsv_ipt.text(), 13, 6, "D") + \
                 formatInput(MainWindow.rm_ipt.text(), 13, 6, "D") + \
                 formatInput(MainWindow.xbol1_ipt.text(), 7, 3, "F") + \
                 formatInput(MainWindow.xbol2_ipt.text(), 7, 3, "F") + \
                 formatInput(MainWindow.ybol1_ipt.text(), 7, 3, "F") + \
                 formatInput(MainWindow.ybol2_ipt.text(), 7, 3, "F") + \
                 formatInput(MainWindow.dpclog_ipt.text(), 9, 5, "F") + "\n"

        line12 = formatInput(MainWindow.a3b_ipt.text(), 12, 6, "D") + \
                 formatInput(MainWindow.p3b_ipt.text(), 14, 7, "D") + \
                 formatInput(MainWindow.xinc3b_ipt.text(), 11, 5, "F") + \
                 formatInput(MainWindow.e3b_ipt.text(), 9, 6, "F") + \
                 formatInput(MainWindow.perr3b_ipt.text(), 10, 7, "F", isDeg=True) + \
                 formatInput(MainWindow.tc3b_ipt.text(), 17, 8, "F") + "\n"

        vclines = ""
        vcList = []
        if ifvc1 == "1":
            vcList.append(MainWindow.LoadWidget.vcPropertiesList[0])
        if ifvc2 == "1":
            vcList.append(MainWindow.LoadWidget.vcPropertiesList[1])
        if len(vcList) != 0:
            for vcprop in vcList:
                iband = (" " * (3 - len(vcprop.band))) + vcprop.band
                vclines = vclines + iband + formatInput(vcprop.l1, 13, 6, "D") \
                          + formatInput(vcprop.l2, 13, 6, "D") \
                          + formatInput(vcprop.x1, 7, 3, "F") \
                          + formatInput(vcprop.x2, 7, 3, "F") \
                          + formatInput(vcprop.y1, 7, 3, "F") \
                          + formatInput(vcprop.y2, 7, 3, "F") \
                          + formatInput(vcprop.opsf, 10, 3, "D") \
                          + formatInput(float(vcprop.sigma) / vunit, 12, 5, "D") \
                          + formatInput(vcprop.e1, 8, 5, "F") \
                          + formatInput(vcprop.e2, 8, 5, "F") \
                          + formatInput(vcprop.e3, 8, 5, "F") \
                          + formatInput(vcprop.e4, 8, 5, "F") \
                          + formatInput(vcprop.wla, 10, 6, "F") + " " + vcprop.ksd + "\n"

        lclines = ""
        lcextralines = ""
        if len(MainWindow.LoadWidget.lcPropertiesList) != 0:
            lcparamsList = []
            lcextraparamsList = []
            for lcprop in MainWindow.LoadWidget.lcPropertiesList:
                iband = (" " * (3 - len(lcprop.band))) + lcprop.band
                lcparams = iband + formatInput(lcprop.l1, 13, 6, "F") + \
                           formatInput(lcprop.l2, 13, 6, "F") + \
                           formatInput(lcprop.x1, 7, 3, "F") + \
                           formatInput(lcprop.x2, 7, 3, "F") + \
                           formatInput(lcprop.y1, 7, 3, "F") + \
                           formatInput(lcprop.y2, 7, 3, "F") + \
                           formatInput(lcprop.el3a, 12, 4, "D") + formatInput(lcprop.opsf, 10, 3, "D") + " " + \
                           lcprop.noise + formatInput(lcprop.sigma, 12, 5, "D") + \
                           formatInput(lcprop.e1, 8, 5, "F") + \
                           formatInput(lcprop.e2, 8, 5, "F") + \
                           formatInput(lcprop.e3, 8, 5, "F") + \
                           formatInput(lcprop.e4, 8, 5, "F") + " " + lcprop.ksd + "\n"
                lcextraparams = formatInput(lcprop.wla, 9, 6, "F") + \
                                formatInput(lcprop.aextinc, 8, 4, "F") + \
                                formatInput(lcprop.xunit, 11, 4, "D") +\
                                formatInput(lcprop.calib, 12, 5, "D") + "\n"
                lcparamsList.append(lcparams)
                lcextraparamsList.append(lcextraparams)
            for lcparams in lcparamsList:
                lclines = lclines + lcparams
            for lcextraparams in lcextraparamsList:
                lcextralines = lcextralines + lcextraparams
        eclipseline = ""
        if evalCheckBox(MainWindow.EclipseWidget.iftime_chk) == "1":
            eclipseline = (" " * 82) + \
                          formatInput(MainWindow.EclipseWidget.sigma_ipt.text(), 11, 5, "D") + \
                          (" " * 32) + \
                          " " + str(MainWindow.EclipseWidget.ksd_box.value()) + "\n"

        star1spotline = ""
        star2spotline = ""
        if MainWindow.SpotConfigureWidget.star1RowCount != 0:
            star1spotparams = MainWindow.SpotConfigureWidget.star1ElementList
            for spot in star1spotparams:
                star1spotline = star1spotline + \
                                formatInput(spot[3].text(), 9, 5, "F", isDeg=True) + \
                                formatInput(spot[4].text(), 9, 5, "F", isDeg=True) + \
                                formatInput(spot[5].text(), 9, 5, "F", isDeg=True) + \
                                formatInput(spot[6].text(), 9, 5, "F") + \
                                "   50800.00000   50900.00000   50930.00000   51100.00000\n"  # TODO implement in ui

        if MainWindow.SpotConfigureWidget.star2RowCount != 0:
            star2spotparams = MainWindow.SpotConfigureWidget.star2ElementList
            for spot in star2spotparams:
                star2spotline = star2spotline + \
                                formatInput(spot[3].text(), 9, 5, "F", isDeg=True) + \
                                formatInput(spot[4].text(), 9, 5, "F", isDeg=True) + \
                                formatInput(spot[5].text(), 9, 5, "F", isDeg=True) + \
                                formatInput(spot[6].text(), 9, 5, "F") + \
                                "   50800.00000   50900.00000   50930.00000   51100.00000\n"  # TODO implement in ui
        vc1dataline = ""
        if ifvc1 == "1":
            vc1prop = MainWindow.LoadWidget.vcPropertiesList[0]
            for time, observation, weight in itertools.izip(vc1prop.timeList,
                                                            vc1prop.observationList,
                                                            vc1prop.weightList):
                vc1dataline = vc1dataline + \
                              formatInput(time, 14, 5, "F") + \
                              formatInput((float(observation)/vunit), 11, 6, "F") + \
                              formatInput(weight, 8, 3, "F") + "\n"
        vc2dataline = ""
        if ifvc2 == "1":
            vc2prop = MainWindow.LoadWidget.vcPropertiesList[1]
            for time, observation, weight in itertools.izip(vc2prop.timeList,
                                                            vc2prop.observationList,
                                                            vc2prop.weightList):
                vc2dataline = vc2dataline + \
                              formatInput(time, 14, 5, "F") + \
                              formatInput((float(observation)/vunit), 11, 6, "F") + \
                              formatInput(weight, 8, 3, "F") + "\n"

        lcdataline = ""
        if len(MainWindow.LoadWidget.lcPropertiesList) != 0:
            for lcprop in MainWindow.LoadWidget.lcPropertiesList:
                for time, observation, weight in itertools.izip(lcprop.timeList,
                                                             lcprop.observationList,
                                                             lcprop.weightList):
                    lcdataline = lcdataline + formatInput(time, 14, 5, "F") + \
                                 formatInput(observation, 11, 6, "F") + \
                                 formatInput(weight, 8, 3, "F") + "\n"
                lcdataline = lcdataline + "  -10001.00000\n"

        ecdataline = ""
        if len(MainWindow.EclipseWidget.lines) != 0:
            for time, type, weight in itertools.izip(MainWindow.EclipseWidget.timeList,
                                                    MainWindow.EclipseWidget.typeList,
                                                    MainWindow.EclipseWidget.weightList):
                ecdataline = ecdataline + \
                             formatInput(time, 14, 5, "F") + (" " * 5 + type) + formatInput(weight, 13, 3, "F") + "\n"
            ecdataline = ecdataline + "  -10001.00000\n"

        result[2] = line1 + line2 + line3 + line4 + line5 + line6 + line7 + line8 + line9 + line10 + line11 + line12 \
                    + vclines + lclines + eclipseline + lcextralines + \
                    "300.00000\n" + star1spotline + "300.00000\n" + star2spotline + \
                    "150.\n" + vc1dataline + "  -10001.00000\n" + vc2dataline + "  -10001.00000\n" + lcdataline  + \
                    "  -10001.00000\n" + ecdataline + "  -10001.00000\n" + " 2\n"
        if vc1dataline == "" and vc2dataline == "":
            result[1] = result[1] + "\nThere aren't any velocity curves loaded.\n"
        if lcdataline == "":
            result[1] = result[1] + "\nThere aren't any light curves loaded.\n"
        if evalCheckBox(MainWindow.EclipseWidget.iftime_chk) and ecdataline == "":
            result[1] = result[1] + "\nIFTIMES is checked, but eclipse timings are not provided.\n"

    except ValueError as ex:
        result[0] = "Value Error - Can't cast input into a numeric value: \n" + ex.message
        result[2] = "FATAL"
    except IndexError as ex:
        result[0] = "Wrong Input: \n" + ex.message
        result[2] = "FATAL"
    except:
        result[0] = "Unknown exception has been caught. This is most likely a programming error: \n" + \
                    str(sys.exc_info())
        result[2] = "FATAL"
    return result


if __name__ == "__main__":
    pass
