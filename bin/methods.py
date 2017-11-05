import sys
from PyQt4 import QtGui
from functools import partial
from bin import classes
import ConfigParser


def SaveSpotConfiguration(SpotConfigureWidget):
    dialog = QtGui.QFileDialog(SpotConfigureWidget)
    dialog.setDefaultSuffix("spotconfig")
    dialog.setNameFilter("Spot Configuration File (*.spotconfig)")
    dialog.setAcceptMode(1)
    returnCode = dialog.exec_()
    filePath = (dialog.selectedFiles())[0]
    if filePath != "" and returnCode != 0:
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
    label.setGeometry(10 + xshiftAmount, 130 + yshiftAmount, 41, 16)
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
    radioA.setGeometry(60 + xshiftAmount, 130 + yshiftAmount, 16, 17)
    radioB.setGeometry(90 + xshiftAmount, 130 + yshiftAmount, 16, 17)
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
            label.setGeometry(50, 140 + shiftAmount, 80, 21)  # set geometry
            label.setText("Light Curve " + str(LoadWidget.lcCount))  # set text
            label.setObjectName("lclabel" + str(LoadWidget.lcCount))  # set object name
            LoadWidget.lcElementList[LoadWidget.lcCount - 1].append(label)  # store element in the element list
            label.show()  # show the element

            # file path
            path = QtGui.QLineEdit(LoadWidget)  # load element
            path.setGeometry(140, 140 + shiftAmount, 381, 20)  # set geometry
            path.setText(filePath)  # set text
            path.setObjectName("lcpath" + str(LoadWidget.lcCount))  # set object name
            path.setReadOnly(True)  # set read only
            LoadWidget.lcElementList[LoadWidget.lcCount - 1].append(path)  # store element in the element list
            path.show()  # show the element

            # edit button
            row = LoadWidget.lcCount - 1  # current row index
            edit = QtGui.QPushButton(LoadWidget)
            edit.setGeometry(530, 140 + shiftAmount, 51, 21)
            edit.setText("Edit")
            edit.setObjectName("lcedit" + str(LoadWidget.lcCount))
            edit.clicked.connect(partial(editLightCurve, LoadWidget, row))
            LoadWidget.lcElementList[LoadWidget.lcCount - 1].append(edit)
            edit.show()

            # remove button
            remove = QtGui.QPushButton(LoadWidget)
            remove.setGeometry(590, 140 + shiftAmount, 51, 21)
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
    LoadWidget.lcadd_btn.setGeometry(20, shiftAmount + 180, 111, 21)  # move 'add light curve' button
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


def formatDels(ipt):
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
                msg = error + "\nMake sure your input's non-zero fractional part consist of 2 digits, ex. 0.00056"
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


def exportDc(MainWindow):
    dialog = QtGui.QFileDialog(MainWindow)
    dialog.setAcceptMode(1)
    dialog.selectFile("dcin.active")
    returnCode = dialog.exec_()
    filePath = (dialog.selectedFiles())[0]
    if filePath != "" and returnCode != 0:
        with open(filePath, 'w') as dcin:
            try:
                line1 = " {0} {1} {2} {3} {4} {5} {6} {7}\n".format(
                    formatDels(MainWindow.del_s1lat_ipt.text()),
                    formatDels(MainWindow.del_s1lng_ipt.text()),
                    formatDels(MainWindow.del_s1agrad_ipt.text()),
                    formatDels(MainWindow.del_s1tmpf_ipt.text()),
                    formatDels(MainWindow.del_s2lat_ipt.text()),
                    formatDels(MainWindow.del_s2lng_ipt.text()),
                    formatDels(MainWindow.del_s2agrad_ipt.text()),
                    formatDels(MainWindow.del_s2tmpf_ipt.text())
                )
                line2 = " {0} {1} {2} {3} {4} {5} {6} {7} {8} {9} {10}\n".format(
                    formatDels(MainWindow.del_a_ipt.text()),
                    formatDels(MainWindow.del_e_ipt.text()),
                    formatDels(MainWindow.del_perr0_ipt.text()),
                    formatDels(MainWindow.del_f1_ipt.text()),
                    formatDels(MainWindow.del_f2_ipt.text()),
                    formatDels(MainWindow.del_pshift_ipt.text()),
                    formatDels(MainWindow.del_i_ipt.text()),
                    formatDels(MainWindow.del_g1_ipt.text()),
                    formatDels(MainWindow.del_g2_ipt.text()),
                    formatDels(MainWindow.del_t1_ipt.text()),
                    formatDels(MainWindow.del_t2_ipt.text())
                )
                line3 = " {0} {1} {2} {3} {4} {5} {6} {7} {8}\n".format(
                    formatDels(MainWindow.del_alb1_ipt.text()),
                    formatDels(MainWindow.del_alb2_ipt.text()),
                    formatDels(MainWindow.del_pot1_ipt.text()),
                    formatDels(MainWindow.del_pot2_ipt.text()),
                    formatDels(MainWindow.del_q_ipt.text()),
                    formatDels(MainWindow.del_l1_ipt.text()),
                    formatDels(MainWindow.del_l2_ipt.text()),
                    formatDels(MainWindow.del_x1_ipt.text()),
                    formatDels(MainWindow.del_x2_ipt.text())
                )

                def _formatKeeps(keep):
                    if keep.isChecked():
                        return "0"
                    else:
                        return "1"

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

                # write lines into file
                dcin.write(line1)
                dcin.write(line2)
                dcin.write(line3)
                dcin.write(line4)
                dcin.write(line5)
            except ValueError as ex:
                msg = QtGui.QMessageBox()
                msg.setWindowTitle("pywd - ValueError")
                msg.setText("Can't cast your input into a numeric value;" + "\n" + ex.message)
                msg.exec_()
            except IndexError as ex:
                msg = QtGui.QMessageBox()
                msg.setWindowTitle("pywd - Wrong Input")
                msg.setText(ex.message)  # most exceptions store their first arguments in (exception).message field
                msg.exec_()
            except:
                msg = QtGui.QMessageBox()
                msg.setWindowTitle("pywd - UnknownError")
                msg.setText("Unknown exception is caught:\n" + str(sys.exc_info()))
                msg.exec_()


if __name__ == "__main__":
    pass
