from PyQt4 import QtGui, QtCore
from gui import mainwindow, spotconfigurewidget, eclipsewidget, curvepropertiesdialog, \
    dcwidget, lcdcpickerdialog, outputview, loadobservationwidget, plotresultswidget
from functools import partial
from bin import methods, classes
import numpy as np
from matplotlib import pyplot
import sys
import ConfigParser
import os


class MainWindow(QtGui.QMainWindow, mainwindow.Ui_MainWindow):  # main window class
    def __init__(self):  # constructor
        super(MainWindow, self).__init__()
        self.setupUi(self)  # setup ui from mainwindow.py
        self.setWindowIcon(QtGui.QIcon("resources/pywd.ico"))  # set app icon
        self.LoadObservationWidget = LoadObservationWidget()  # get loadwidget
        self.LoadObservationWidget.MainWindow = self
        self.SpotConfigureWidget = SpotConfigureWidget()  # get spotconfigurewidget
        self.EclipseWidget = EclipseWidget()
        self.DCWidget = DCWidget()
        self.DCWidget.MainWindow = self
        self.LCDCPickerWidget = LCDCPickerWidget()
        self.LCDCPickerWidget.MainWindow = self
        # variables
        self.lcpath = None
        self.lcinpath = None
        self.lcoutpath = None
        self.lastProjectPath = None
        self.populateStyles()  # populate theme combobox
        self.connectSignals()  # connect events with method

    def connectSignals(self):
        self.whatsthis_btn.clicked.connect(QtGui.QWhatsThis.enterWhatsThisMode)  # enters what's this mode
        self.loadwidget_btn.clicked.connect(self.LoadObservationWidget.show)  # opens loadwidget
        self.spotconfigure_btn.clicked.connect(self.SpotConfigureWidget.show)  # opens spotconfigurewidget
        self.dc_rundc_btn.clicked.connect(partial(self.DCWidget.show))
        self.theme_combobox.currentIndexChanged.connect(self.changeStyle)
        self.eclipsewidget_btn.clicked.connect(self.EclipseWidget.show)
        self.saveproject_btn.clicked.connect(self.overwriteProject)
        self.loadproject_btn.clicked.connect(self.loadProjectDialog)
        self.saveas_btn.clicked.connect(self.saveProjectDialog)

    def closeEvent(self, *args, **kwargs):  # overriding QMainWindow's closeEvent
        self.LoadObservationWidget.close()  # close loadwidget if we exit
        self.SpotConfigureWidget.close()  # close spotconfigurewidget if we exit
        self.EclipseWidget.close()
        self.DCWidget.close()

    def setPaths(self, lcpath, dcpath):
        self.lcpath = lcpath
        self.lcinpath = os.path.join(os.path.dirname(lcpath), "lcin.active")
        self.lcoutpath = os.path.join(os.path.dirname(lcpath), "lcout.active")
        self.DCWidget.dcpath = dcpath
        self.DCWidget.dcinpath = os.path.join(os.path.dirname(dcpath), "dcin.active")
        self.DCWidget.dcoutpath = os.path.join(os.path.dirname(dcpath), "dcout.active")

    def clearWidgets(self):
        # TODO add proper cleaning here (plots, trees, widgets which depend on current project)
        self.DCWidget.result_treewidget.clear()
        self.DCWidget.lastBaseSet = None
        self.DCWidget.lastSubSets = None
        self.DCWidget.curvestat_treewidget.clear()

    def begin(self):  # check for wd.conf
        wdconf = "wd.conf"
        parser = ConfigParser.SafeConfigParser()
        if os.path.isfile(wdconf):
            with open(wdconf, "r") as f:
                parser.readfp(f)
            self.setPaths(parser.get("Paths", "lc"), parser.get("Paths", "dc"))
            self.show()
            return 0
        else:
            returnCode = self.LCDCPickerWidget.exec_()
            if returnCode == 15:
                parser.add_section("Paths")
                parser.set("Paths", "lc", str(self.LCDCPickerWidget.lcpath_label.text()))
                parser.set("Paths", "dc", str(self.LCDCPickerWidget.dcpath_label.text()))
                with open(wdconf, "w") as f:
                    parser.write(f)
                self.setPaths(str(self.LCDCPickerWidget.lcpath_label.text()),
                              str(self.LCDCPickerWidget.dcpath_label.text()))
                self.show()
                return 0
            else:
                return 1

    def overwriteProject(self):
        if self.lastProjectPath is None:
            self.saveas_btn.click()
        else:
            msg = QtGui.QMessageBox()
            try:
                project = methods.saveProject(self)
                with open(self.lastProjectPath, "w") as f:
                    f.write(project)
                    fi = QtCore.QFileInfo(self.lastProjectPath)
                    msg.setText("Project file \"" + fi.fileName() + "\" saved.")
                    msg.setWindowTitle("PyWD - Project Saved")
                    msg.exec_()
            except:
                msg.setText("An error has ocurred: \n" + str(sys.exc_info()[1]))
                msg.exec_()

    def saveProjectDialog(self):
        dialog = QtGui.QFileDialog(self)
        dialog.setDefaultSuffix("pywdproject")
        dialog.setNameFilter("PyWD2015 Project File (*pywdproject)")
        dialog.setAcceptMode(1)
        returnCode = dialog.exec_()
        filePath = str((dialog.selectedFiles())[0])
        if filePath != "" and returnCode != 0:
            msg = QtGui.QMessageBox()
            fi = QtCore.QFileInfo(filePath)
            try:
                project = methods.saveProject(self)
                with open(filePath, "w") as f:
                    f.write(project)
                self.lastProjectPath = filePath
                msg.setText("Project file \"" + fi.fileName() + "\" saved.")
                msg.setWindowTitle("PyWD - Project Saved")
                msg.exec_()
            except:
                msg.setText("An error has ocurred: \n" + str(sys.exc_info()[1]))
                msg.exec_()

    def loadProjectDialog(self):
        msg = QtGui.QMessageBox()
        dialog = QtGui.QFileDialog(self)
        dialog.setDefaultSuffix("pywdproject")
        dialog.setNameFilter("PyWD2015 Project File (*pywdproject)")
        dialog.setAcceptMode(0)
        returnCode = dialog.exec_()
        filePath = str((dialog.selectedFiles())[0])
        fi = QtCore.QFileInfo(filePath)
        if filePath != "" and returnCode != 0:
            title = "PyWD - Warning"
            text = "Loading a project file will erase all unsaved changes, results and plots. " \
                   + "Do you want to load \"" + fi.fileName() + "\" ?"
            answer = QtGui.QMessageBox.question(self, title, text, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if answer == QtGui.QMessageBox.Yes:
                try:
                    parser = ConfigParser.SafeConfigParser()
                    with open(filePath, "r") as f:
                        parser.readfp(f)
                    methods.loadProject(self, parser)
                    self.clearWidgets()
                    self.LoadObservationWidget.updateCurveWidget()
                    self.lastProjectPath = filePath
                    msg.setText("Project file \"" + fi.fileName() + "\" loaded.")
                    msg.setWindowTitle("PyWD - Project Loaded")
                    msg.exec_()
                except RuntimeError as ex:
                    msg.setText(ex.message)
                    msg.setWindowTitle("PyWD - Error Loading Project")
                    msg.exec_()
                except:
                    msg.setText("An error has ocurred: \n" + str(sys.exc_info()[1]))
                    msg.exec_()

    def populateStyles(self):
        styleFactory = QtGui.QStyleFactory()
        styleKeys = styleFactory.keys()
        for style in styleKeys:
            self.theme_combobox.addItem(str(style))

    def changeStyle(self):
        styleFactory = QtGui.QStyleFactory()
        style = styleFactory.create(self.theme_combobox.currentText())
        self.app.setStyle(style)


class LCDCPickerWidget(QtGui.QDialog, lcdcpickerdialog.Ui_LCDCPickerDialog):
    def __init__(self):
        super(LCDCPickerWidget, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon("resources/pywd.ico"))
        self.MainWindow = None
        self.connectSignals()
        self.save_btn.setDisabled(True)

    def connectSignals(self):
        self.save_btn.clicked.connect(partial(self.done, 15))
        self.exit_btn.clicked.connect(partial(self.done, 0))
        self.pickdc_btn.clicked.connect(partial(self.pickFile, "dc"))
        self.picklc_btn.clicked.connect(partial(self.pickFile, "lc"))

    def pickFile(self, ftype):
        picker = QtGui.QFileDialog(self)
        picker.setFileMode(QtGui.QFileDialog.ExistingFile)
        picker.exec_()
        filepath = picker.selectedFiles()[0]
        if os.path.isfile(filepath):
            if ftype == "lc":
                self.lcpath_label.setText(filepath)
                self.lcpath_label.setToolTip(filepath)
            if ftype == "dc":
                self.dcpath_label.setText(filepath)
                self.dcpath_label.setToolTip(filepath)
        if os.path.isfile(str(self.lcpath_label.text())) and os.path.isfile(str(self.dcpath_label.text())):
            self.save_btn.setDisabled(False)


class EclipseWidget(QtGui.QWidget, eclipsewidget.Ui_EclipseWidget):
    def __init__(self):
        super(EclipseWidget, self).__init__()
        self.setupUi(self)  # setup ui from eclipsewidget.py
        self.setWindowIcon(QtGui.QIcon("resources/pywd.ico"))
        self.connectSignals()

    def connectSignals(self):
        self.load_btn.clicked.connect(partial(methods.loadEclipseTimings, self))
        self.clear_btn.clicked.connect(partial(methods.removeEclipseTimings, self))


class LoadObservationWidget(QtGui.QWidget, loadobservationwidget.Ui_ObservationWidget):
    def __init__(self):
        super(LoadObservationWidget, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon("resources/pywd.ico"))
        # variables
        self.vcPropertiesList = [0, 0]
        self.lcPropertiesList = []
        self.MainWindow = None
        self.connectSignals()

    def connectSignals(self):
        self.add_btn.clicked.connect(self.openAddMenu)
        self.edit_btn.clicked.connect(self.editCurve)
        self.remove_btn.clicked.connect(self.removeCurve)
        self.plot_btn.clicked.connect(self.plotCurve)

    def Curves(self):
        curves = []
        for curve in (self.vcPropertiesList + self.lcPropertiesList):
            if curve is not 0:
                curves.append(curve)
        return curves

    def createCurveDialog(self, type):
        curvedialog = CurvePropertiesDialog()
        curvedialog.type = type
        if type == "lc":
            curvedialog.label_53.setText("Load or edit a light curve")
            curvedialog.type = "lc"
            return curvedialog
        if type == "vc":
            curvedialog.label_53.setText("Load or edit a velocity curve")
            curvedialog.type = "vc"
            curvedialog.noise_combobox.setDisabled(True)
            curvedialog.noise_combobox.addItem("N/A")
            curvedialog.noise_combobox.setCurrentIndex(3)
            curvedialog.el3a_ipt.setDisabled(True)
            curvedialog.el3a_ipt.setText("N/A")
            curvedialog.aextinc_ipt.setDisabled(True)
            curvedialog.aextinc_ipt.setText("N/A")
            curvedialog.calib_ipt.setDisabled(True)
            curvedialog.calib_ipt.setText("N/A")
            curvedialog.xunit_ipt.setDisabled(True)
            curvedialog.xunit_ipt.setText("N/A")
            return curvedialog

    def loadCurveDialog(self, type, vcNumber):
        dialog = QtGui.QFileDialog(self)
        dialog.setAcceptMode(0)
        returnCode = dialog.exec_()
        filePath = (dialog.selectedFiles())[0]
        if filePath != "" and returnCode != 0:
            try:
                curvedialog = self.createCurveDialog(type)
                curvedialog.populateFromFile(filePath)
                if curvedialog.hasError:
                    pass
                else:
                    result = curvedialog.exec_()
                    if result == 1:
                        curveprop = classes.CurveProperties(type)
                        curveprop.populateFromInterface(curvedialog)
                        if type == "lc":
                            self.lcPropertiesList.append(curveprop)
                        if type == "vc":
                            curveprop.star = vcNumber
                            self.vcPropertiesList[vcNumber-1] = curveprop
                        self.updateCurveWidget()
            except:
                msg = QtGui.QMessageBox()
                msg.setText("An error has ocurred: \n" + str(sys.exc_info()[1]))
                msg.exec_()

    def openAddMenu(self):
        menu = QtGui.QMenu(self)
        addvc = QtGui.QMenu("Velocity Curve")
        menu.addMenu(addvc)
        pri = addvc.addAction("Primary")
        pri.setObjectName("primary")
        sec = addvc.addAction("Secondary")
        sec.setObjectName("secondary")
        if self.vcPropertiesList[0] is not 0:
            pri.setDisabled(True)
        if self.vcPropertiesList[1] is not 0:
            sec.setDisabled(True)
        addlc = menu.addAction("Light Curve")
        addlc.setObjectName("lightcurve")
        selection = menu.exec_(QtGui.QCursor.pos())
        if selection is not None:
            if selection.objectName() == "primary":
                self.loadCurveDialog("vc", 1)
            if selection.objectName() == "secondary":
                self.loadCurveDialog("vc", 2)
            if selection.objectName() == "lightcurve":
                self.loadCurveDialog("lc", -1)

    def getSelectedLightCurveIndex(self, item):
        invindex = self.curve_treewidget.invisibleRootItem().indexOfChild(item)
        return invindex - (len(self.Curves()) - len(self.lcPropertiesList))

    def selectedItem(self):
        selecteditem = self.curve_treewidget.selectedItems()
        if len(selecteditem) > 0:
            return selecteditem[0]
        else:
            return None

    def editCurve(self):
        item = self.selectedItem()
        if item is not None:
            curvedialog = None
            if item.text(1) == "Velocity Curve (#1)":
                curvedialog = self.createCurveDialog("vc")
                curvedialog.populateFromObject(self.vcPropertiesList[0])
            if item.text(1) == "Velocity Curve (#2)":
                curvedialog = self.createCurveDialog("vc")
                curvedialog.populateFromObject(self.vcPropertiesList[1])
            if item.text(1) == "Light Curve":
                curvedialog = self.createCurveDialog("lc")
                curvedialog.populateFromObject(self.lcPropertiesList[self.getSelectedLightCurveIndex(item)])
            returnCode = curvedialog.exec_()
            if returnCode == 1:
                if item.text(1) == "Velocity Curve (#1)":
                    curveprop = classes.CurveProperties("vc")
                    curveprop.star = 1
                    curveprop.populateFromInterface(curvedialog)
                    self.vcPropertiesList[0] = curveprop
                if item.text(1) == "Velocity Curve (#2)":
                    curveprop = classes.CurveProperties("vc")
                    curveprop.star = 2
                    curveprop.populateFromInterface(curvedialog)
                    self.vcPropertiesList[1] = curveprop
                if item.text(1) == "Light Curve":
                    curveprop = classes.CurveProperties("lc")
                    curveprop.populateFromInterface(curvedialog)
                    self.lcPropertiesList[self.getSelectedLightCurveIndex(item)] = curveprop
                self.updateCurveWidget()

    def removeCurve(self):
        item = self.selectedItem()
        if item is not None:
            if item.text(1) == "Velocity Curve (#1)":
                self.vcPropertiesList[0] = 0
            if item.text(1) == "Velocity Curve (#2)":
                self.vcPropertiesList[1] = 0
            if item.text(1) == "Light Curve":
                self.lcPropertiesList.pop(self.getSelectedLightCurveIndex(item))
            self.updateCurveWidget()

    def plotCurve(self):
        item = self.selectedItem()
        pyplot.cla()
        if item is not None:
            curve = classes.Curve(item.toolTip(0))
            x = [float(x) for x in curve.timeList]
            y = [float(y) for y in curve.observationList]
            pyplot.scatter(x, y)
            pyplot.title(item.text(0))
            pyplot.get_current_fig_manager().set_window_title("Matplotlib - " + item.text(0))
            pyplot.show()

    def updateCurveWidget(self):
        self.curve_treewidget.clear()
        for curve in self.Curves():
            item = QtGui.QTreeWidgetItem(self.curve_treewidget)
            item.setText(0, os.path.basename(curve.FilePath))
            item.setToolTip(0, curve.FilePath)
            curvetype = ""
            if curve.type == "lc":
                curvetype = "Light Curve"
            else:
                if curve.type == "vc":
                    if curve.star == 1:
                        curvetype = "Velocity Curve (#1)"
                    if curve.star == 2:
                        curvetype = "Velocity Curve (#2)"
            item.setText(1, curvetype)
            item.setText(2, self.MainWindow.DCWidget.bandpassDict[curve.band])


class CurvePropertiesDialog(QtGui.QDialog, curvepropertiesdialog.Ui_CurvePropertiesDialog):
    def __init__(self):
        super(CurvePropertiesDialog, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon("resources/pywd.ico"))
        self.type = ""
        self.hasError = False
        self.bandpassdict = {
            "Stromgren u": "1",
            "Stromgren v": "2",
            "Stromgren b": "3",
            "Stromgren y": "4",
            "Johnson U": "5",
            "Johnson B": "6",
            "Johnson V": "7",
            "Johnson R": "8",
            "Johnson I": "9",
            "Johnson J": "10",
            "Johnson K": "11",
            "Johnson L": "12",
            "Johnson M": "13",
            "Johnson N": "14",
            "Cousins Rc": "15",
            "Cousins Ic": "16",
            "Bessel UX": "17",
            "Bessel BX": "18",
            "Bessel B": "19",
            "Bessel V": "20",
            "Bessel R": "21",
            "Bessel I": "22",
            "Tycho Bt": "23",
            "Tycho Vt": "24",
            "Hipparchos Hp": "25",
            "KEPLER": "26",
            "COROT SIS": "27",
            "COROT EXO": "28",
            "Geneva U": "29",
            "Geneva B": "30",
            "Geneva B1": "31",
            "Geneva B2": "32",
            "Geneva V": "33",
            "Geneva V1": "34",
            "Geneva G": "35",
            "Vilnius U": "36",
            "Vilnius P": "37",
            "Vilnius X": "38",
            "Vilnius Y": "39",
            "Vilnius Z": "40",
            "Vilnius V": "41",
            "Vilnius S": "42",
            "Milone iz": "43",
            "Milone iJ": "44",
            "Milone iH": "45",
            "Milone iK": "46",
            "YMS94 iz": "47",
            "YMS94 iJ": "48",
            "YMS94 iH": "49",
            "YMS94 iK": "50",
            "YMS94 iL": "51",
            "YMS94 iL'": "52",
            "YMS94 iM": "53",
            "YMS94 in": "54",
            "YMS94 iN": "55",
            "Sloan DDS u'": "56",
            "Sloan DDS g'": "57",
            "Sloan DDS r'": "58",
            "Sloan DDS i'": "59",
            "Sloan DDS z'": "60",
            "HST STIS Ly alpha": "61",
            "HST STIS Fclear": "62",
            "HST STIS Fsrf2": "63",
            "HST STIS Fqtz": "64",
            "HST STIS C III": "65",
            "HST STIS Mg II": "66",
            "HST STIS Nclear": "67",
            "HST STIS Nsrf2": "68",
            "HST STIS Nqtz": "69",
            "HST STIS cn182": "70",
            "HST STIS cn270": "71",
            "HST STIS Oclear": "72",
            "HST STIS Oclear-lp": "73",
            "HST STIS [O II]": "74",
            "HST STIS [O III]": "75",
            "2MASS J": "76",
            "2MASS H": "77",
            "2MASS Ks": "78",
            "SWASP": "79",
            "MOST": "80",
            "Gaia G (2006)": "81",
            "Gaia G (2010)": "82",
            "Gaia Gbp": "83",
            "Gaia Grp": "84",
            "Gaia Grvs": "85",
            "Milone 230": "86",
            "Milone 250": "87",
            "Milone 270": "88",
            "Milone 290": "89",
            "Milone 310": "90",
            "Milone 330": "91",
            "Ca II triplet": "92",
            "WIRE V+R": "93",
            "Lunar Ultraviolet Telescope": "94"
        }
        self.bandpassContextMenu = self.createBandpassContextMenu()
        self.connectSignals()

    def connectSignals(self):
        self.accept_btn.clicked.connect(partial(self.done, 1))
        self.discard_btn.clicked.connect(partial(self.done, 2))
        self.whatsthis_btn.clicked.connect(QtGui.QWhatsThis.enterWhatsThisMode)
        self.repick_btn.clicked.connect(self.repick)
        # this gets fired when we right click
        self.bandpasscontextlist_btn.customContextMenuRequested.connect(self.openBandpassContextMenu)
        self.bandpasscontextlist_btn.clicked.connect(self.openBandpassContextMenu)

    def openBandpassContextMenu(self):
        band = self.bandpassContextMenu.exec_(QtGui.QCursor.pos())
        if band is not None:
            self.band_box.setValue(int(self.bandpassdict[str(band.objectName())]))

    def createBandpassContextMenu(self):
        rootmenu = QtGui.QMenu(self)
        # johnson
        johnson = rootmenu.addMenu("Johnson")
        ju = johnson.addAction("U")
        ju.setObjectName("Johnson U")
        jb = johnson.addAction("B")
        jb.setObjectName("Johnson B")
        jv = johnson.addAction("V")
        jv.setObjectName("Johnson V")
        jr = johnson.addAction("R")
        jr.setObjectName("Johnson R")
        ji = johnson.addAction("I")
        ji.setObjectName("Johnson I")

        # stromgren
        stromgren = rootmenu.addMenu("Stromgren")
        su = stromgren.addAction("u")
        su.setObjectName("Stromgren u")
        sv = stromgren.addAction("v")
        sv.setObjectName("Stromgren v")
        sb = stromgren.addAction("b")
        sb.setObjectName("Stromgren b")
        sy = stromgren.addAction("y")
        sy.setObjectName("Stromgren y")

        # cousins
        cousins = rootmenu.addMenu("Cousins")
        crc = cousins.addAction("Rc")
        crc.setObjectName("Cousins Rc")
        cic = cousins.addAction("Ic")
        cic.setObjectName("Cousins Ic")

        # bessel
        bessel = rootmenu.addMenu("Bessel")
        bux = bessel.addAction("UX")
        bux.setObjectName("Bessel UX")
        bbx = bessel.addAction("BX")
        bbx.setObjectName("Bessel BX")
        bb = bessel.addAction("B")
        bb.setObjectName("Bessel B")
        bv = bessel.addAction("B")
        bv.setObjectName("Bessel V")
        br = bessel.addAction("V")
        br.setObjectName("Bessel R")
        bi = bessel.addAction("I")
        bi.setObjectName("Bessel I")

        # tycho
        tycho = rootmenu.addMenu("Tycho")
        tbt = tycho.addAction("Bt")
        tbt.setObjectName("Tycho Bt")
        tvt = tycho.addAction("Vt")
        tvt.setObjectName("Tycho Vt")

        # corot
        corot = rootmenu.addMenu("Corot")
        csis = corot.addAction("SIS")
        csis.setObjectName("COROT SIS")
        cexo = corot.addAction("EXO")
        cexo.setObjectName("COROT EXO")

        # geneva
        geneva = rootmenu.addMenu("Geneva")
        gu = geneva.addAction("U")
        gu.setObjectName("Geneva U")
        gb = geneva.addAction("B")
        gb.setObjectName("Geneva B")
        gb1 = geneva.addAction("B1")
        gb1.setObjectName("Geneva B1")
        gb2 = geneva.addAction("B2")
        gb2.setObjectName("Geneva B2")
        gv = geneva.addAction("V")
        gv.setObjectName("Geneva V")
        gv1 = geneva.addAction("V1")
        gv1.setObjectName("Geneva V1")
        gg = geneva.addAction("G")
        gg.setObjectName("Geneva G")

        # vilnius
        vilnius = rootmenu.addMenu("Vilnius")
        vu = vilnius.addAction("U")
        vu.setObjectName("Vilnius U")
        vp = vilnius.addAction("P")
        vp.setObjectName("Vilnius P")
        vx = vilnius.addAction("X")
        vx.setObjectName("Vilnius X")
        vy = vilnius.addAction("Y")
        vy.setObjectName("Vilnius Y")
        vz = vilnius.addAction("Z")
        vz.setObjectName("Vilnius Z")
        vv = vilnius.addAction("V")
        vv.setObjectName("Vilnius V")
        vs = vilnius.addAction("S")
        vs.setObjectName("Vilnius S")

        # milone
        milone = rootmenu.addMenu("Milone")
        miz = milone.addAction("iz")
        miz.setObjectName("Milone iz")
        mij = milone.addAction("iJ")
        mij.setObjectName("Milone iJ")
        mih = milone.addAction("iH")
        mih.setObjectName("Milone iH")
        mik = milone.addAction("iK")
        mik.setObjectName("Milone iK")
        m230 = milone.addAction("230")
        m230.setObjectName("Milone 230")
        m250 = milone.addAction("250")
        m250.setObjectName("Milone 250")
        m270 = milone.addAction("270")
        m270.setObjectName("Milone 270")
        m290 = milone.addAction("290")
        m290.setObjectName("Milone 290")
        m310 = milone.addAction("310")
        m310.setObjectName("Milone 310")
        m330 = milone.addAction("330")
        m330.setObjectName("Milone 330")

        # yms94
        yms94 = rootmenu.addMenu("YMS94")
        yiz = yms94.addAction("iz")
        yiz.setObjectName("YMS94 iz")
        yij = yms94.addAction("iJ")
        yij.setObjectName("YMS94 iJ")
        yih = yms94.addAction("iH")
        yih.setObjectName("YMS94 iH")
        yik = yms94.addAction("iK")
        yik.setObjectName("YMS94 iK")
        yil = yms94.addAction("iL")
        yil.setObjectName("YMS94 iL")
        yill = yms94.addAction("iL'")
        yill.setObjectName("YMS94 iL'")
        yim = yms94.addAction("iM")
        yim.setObjectName("YMS94 iM")
        yin = yms94.addAction("in")
        yin.setObjectName("YMS94 in")
        yinn = yms94.addAction("iN")
        yinn.setObjectName("YMS94 iN")

        # sloandds
        sloandds = rootmenu.addMenu("Sloan DDS")
        sdu = sloandds.addAction("u'")
        sdu.setObjectName("Sloan DDS u'")
        sdg = sloandds.addAction("g'")
        sdg.setObjectName("Sloan DDS g'")
        sdr = sloandds.addAction("r'")
        sdr.setObjectName("Sloan DDS r'")
        sdi = sloandds.addAction("i'")
        sdi.setObjectName("Sloan DDS i'")
        sdz = sloandds.addAction("z'")
        sdz.setObjectName("Sloan DDS z'")

        # hststis
        hststis = rootmenu.addMenu("HST STIS")
        hly = hststis.addAction("Ly alpha")
        hly.setObjectName("HST STIS Ly alpha")
        hlf = hststis.addAction("Fclear")
        hlf.setObjectName("HST STIS Fclear")
        hlfc = hststis.addAction("Fsrf2")
        hlfc.setObjectName("HST STIS Fsrf2")
        hlfq = hststis.addAction("Fqtz")
        hlfq.setObjectName("HST STIS Fqtz")
        hlc3 = hststis.addAction("C III")
        hlc3.setObjectName("HST STIS C III")
        hlm2 = hststis.addAction("Mg II")
        hlm2.setObjectName("HST STIS Mg II")
        hlnc = hststis.addAction("Nclear")
        hlnc.setObjectName("HST STIS Nclear")
        hlns = hststis.addAction("Nsfr2")
        hlns.setObjectName("HST STIS Nsrf2")
        hlnq = hststis.addAction("Nqtz")
        hlnq.setObjectName("HST STIS Nqtz")
        hlcn = hststis.addAction("cn182")
        hlcn.setObjectName("HST STIS cn182")
        hlcn2 = hststis.addAction("cn270")
        hlcn2.setObjectName("HST STIS cn270")
        hlo = hststis.addAction("Oclear")
        hlo.setObjectName("HST STIS Oclear")
        hloc = hststis.addAction("Oclear-lp")
        hloc.setObjectName("HST STIS Oclear-lp")
        hlo2 = hststis.addAction("[O II]")
        hlo2.setObjectName("HST STIS [O II]")
        hlo3 = hststis.addAction("[O III]")
        hlo3.setObjectName("HST STIS [O III]")

        # 2mass
        twomass = rootmenu.addMenu("2MASS")
        tmj = twomass.addAction("J")
        tmj.setObjectName("2MASS J")
        tmh = twomass.addAction("H")
        tmh.setObjectName("2MASS H")
        tmjks = twomass.addAction("Ks")
        tmjks.setObjectName("2MASS Ks")

        # gaia
        gaia = rootmenu.addMenu("Gaia")
        gg2006 = gaia.addAction("G (2006)")
        gg2006.setObjectName("Gaia G (2006)")
        gg2010 = gaia.addAction("G (2010)")
        gg2010.setObjectName("Gaia G (2010)")
        ggbp = gaia.addAction("Gbp")
        ggbp.setObjectName("Gaia Gbp")
        ggrp = gaia.addAction("Grp")
        ggrp.setObjectName("Gaia Grp")
        ggrvs = gaia.addAction("Grvs")
        ggrvs.setObjectName("Gaia Grvs")

        seperator = rootmenu.addSeparator()
        # single menu bands
        hipparchos = rootmenu.addAction("Hipparchos Hp")
        hipparchos.setObjectName("Hipparchos Hp")
        kepler = rootmenu.addAction("KEPLER")
        kepler.setObjectName("KEPLER")
        swasp = rootmenu.addAction("SWASP")
        swasp.setObjectName("SWASP")
        most = rootmenu.addAction("MOST")
        most.setObjectName("MOST")
        triplet = rootmenu.addAction("Ca II triplet")
        triplet.setObjectName("Ca II triplet")
        wire = rootmenu.addAction("WIRE V+R")
        wire.setObjectName("WIRE V+R")
        lut = rootmenu.addAction("Lunar Ultraviolet Telescope")
        lut.setObjectName("Lunar Ultraviolet Telescope")

        return rootmenu

    def repick(self):
        dialog = QtGui.QFileDialog(self)
        dialog.setAcceptMode(0)
        returnCode = dialog.exec_()
        filePath = (dialog.selectedFiles())[0]
        if filePath != "" and returnCode != 0:
            self.datawidget.clear()
            self.populateFromFile(filePath)

    def populateFromFile(self, filePath):
        curve = classes.Curve(filePath)
        if curve.hasError:
            self.hasError = True
            msg = QtGui.QMessageBox()
            msg.setText(curve.error)
            msg.setWindowTitle("PyWD - Error")
            msg.exec_()
        else:
            self.filepath_label.setText(filePath)
            self.filepath_label.setToolTip(filePath)
            self.datawidget.clear()
            for x in curve.lines:
                a = QtGui.QTreeWidgetItem(self.datawidget, x)

    def populateFromObject(self, CurveProperties):
        curve = classes.Curve(CurveProperties.FilePath)
        if curve.hasError:
            self.hasError = True
            msg = QtGui.QMessageBox()
            msg.setText(curve.error)
            msg.setWindowTitle("PyWD - Error")
            msg.exec_()
        else:
            self.filepath_label.setText(CurveProperties.FilePath)
            self.filepath_label.setToolTip(CurveProperties.FilePath)
            self.band_box.setValue(int(CurveProperties.band))
            self.ksd_box.setValue(int(CurveProperties.ksd))
            self.l1_ipt.setText(CurveProperties.l1)
            self.l2_ipt.setText(CurveProperties.l2)
            self.x1_ipt.setText(CurveProperties.x1)
            self.x2_ipt.setText(CurveProperties.x2)
            self.y1_ipt.setText(CurveProperties.y1)
            self.y2_ipt.setText(CurveProperties.y2)
            self.e1_ipt.setText(CurveProperties.e1)
            self.e2_ipt.setText(CurveProperties.e2)
            self.e3_ipt.setText(CurveProperties.e3)
            self.e4_ipt.setText(CurveProperties.e4)
            self.wla_ipt.setText(CurveProperties.wla)
            self.opsf_ipt.setText(CurveProperties.opsf)
            self.sigma_ipt.setText(CurveProperties.sigma)
            self.datawidget.clear()
            for x in curve.lines:
                a = QtGui.QTreeWidgetItem(self.datawidget, x)
            if self.type == "lc":
                self.noise_combobox.setCurrentIndex(int(CurveProperties.noise))
                self.el3a_ipt.setText(CurveProperties.el3a)
                self.aextinc_ipt.setText(CurveProperties.aextinc)
                self.xunit_ipt.setText(CurveProperties.xunit)
                self.calib_ipt.setText(CurveProperties.calib)


class SpotConfigureWidget(QtGui.QWidget, spotconfigurewidget.Ui_SpotConfigureWidget):
    def __init__(self):  # constructor
        super(SpotConfigureWidget, self).__init__()
        self.setupUi(self)  # setup ui from spotconfigurewidget.py
        self.setWindowIcon(QtGui.QIcon("resources/pywd.ico"))  # set app icon
        # variables
        self.star1RowCount = 0
        self.star2RowCount = 0
        self.star1ElementList = []
        # [[label], [radioA], [radioB], [lat_input], [lon_input], [radsp_input], [temsp_input],
        # [tstart], [tmax1], [tmax2], [tend], [remove_button]]
        self.star2ElementList = []
        # [[label], [radioA], [radioB], [lat_input], [lon_input], [radsp_input], [temsp_input],
        # [tstart], [tmax1], [tmax2], [tend], [remove_button]]]
        self.radioButtonGroupA = QtGui.QButtonGroup()
        self.radioButtonGroupB = QtGui.QButtonGroup()
        self.connectSignals()  # connect signals

    def connectSignals(self):
        self.addspot1_btn.clicked.connect(partial(methods.addSpotRow, self, 1))
        self.addspot2_btn.clicked.connect(partial(methods.addSpotRow, self, 2))
        self.spotconfigsave_btn.clicked.connect(self.saveSpotConfigDialog)
        self.spotconfigload_btn.clicked.connect(self.loadSpotConfigDialog)
        self.whatsthis_btn.clicked.connect(QtGui.QWhatsThis.enterWhatsThisMode)

    def saveSpotConfigDialog(self):
        dialog = QtGui.QFileDialog(self)
        dialog.setDefaultSuffix("spotconfig")
        dialog.setNameFilter("Spot Configuration File (*.spotconfig)")
        dialog.setAcceptMode(1)
        returnCode = dialog.exec_()
        filePath = str((dialog.selectedFiles())[0])
        if filePath != "" and returnCode != 0:
            try:
                parser = methods.SaveSpotConfiguration(self)
                with open(filePath, 'w') as f:
                    parser.write(f)
            except:
                msg = QtGui.QMessageBox()
                msg.setText("An error has ocurred: \n" + str(sys.exc_info()[1]))
                msg.exec_()

    def loadSpotConfigDialog(self):
        dialog = QtGui.QFileDialog(self)
        dialog.setAcceptMode(0)
        dialog.setDefaultSuffix("spotconfig")
        dialog.setNameFilter("Spot Configuration File (*.spotconfig)")
        returnCode = dialog.exec_()
        filePath = (dialog.selectedFiles())[0]
        if filePath != "" and returnCode != 0:
            try:
                parser = ConfigParser.SafeConfigParser()
                with open(filePath, 'r') as f:
                    parser.readfp(f)
                methods.LoadSpotConfiguration(self, parser)
            except:
                msg = QtGui.QMessageBox()
                msg.setText("An error has ocurred: \n" + str(sys.exc_info()[1]))
                msg.exec_()
                methods.clearSpotConfigureWidget(self)


class DCWidget(QtGui.QWidget, dcwidget.Ui_DCWidget):
    def __init__(self):
        super(DCWidget, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon("resources/pywd.ico"))
        # variables
        self.dcpath = None
        self.dcinpath = None
        self.dcoutpath = None
        self.MainWindow = None  # mainwindow sets itself here
        self.PlotResultsWidget = PlotResultsWidget()
        self.DcinView = OutputView()
        self.DcoutView = OutputView()
        self.iterator = None
        self.parameterDict = {
            "1": "Spot 1 Latitude",
            "2": "Spot 1 Longitude",
            "3": "Spot 1 Ang. Rad.",
            "4": "Spot 1 Temp. Factor",
            "5": "Spot 2 Latitude",
            "6": "Spot 2 Longitude",
            "7": "Spot 2 Ang. Rad.",
            "8": "Spot 2 Temp. Factor",
            "9": "a",
            "10": "e",
            "11": "Omega",
            "12": "F1",
            "13": "F2",
            "14": "Phase Shift",
            "15": "V Gamma",
            "16": "i",
            "17": "g1",
            "18": "g2",
            "19": "T1",
            "20": "T2",
            "21": "Alb1",
            "22": "Alb2",
            "23": "Pot1",
            "24": "Pot2",
            "25": "Q(M2/M1)",
            "26": "Ephemeris",
            "27": "Period",
            "28": "dP/dt",
            "29": "d(Omega)/dt",
            "30": "a (3B)",
            "31": "Period (3B)",
            "32": "i (3B)",
            "33": "e (3B)",
            "34": "Omega (3B)",
            "35": "Ephemeris (3B)",
            "41": "Log(d)",
            "42": "Desig. Ext.",
            "43": "Spot 1 Tstart",
            "44": "Spot 1 Tmax1",
            "45": "Spot 1 Tmax2",
            "46": "Spot 1 Tend",
            "47": "Spot 2 Tstart",
            "48": "Spot 2 Tmax1",
            "49": "Spot 2 Tmax2",
            "50": "Spot 2 Tend",
            "56": "L1",
            "57": "L2",
            "58": "X1",
            "59": "X2",
            "60": "L3"
        }
        self.bandpassDict = {
            "1": "Stromgren u",
            "2": "Stromgren v",
            "3": "Stromgren b",
            "4": "Stromgren y",
            "5": "Johnson U",
            "6": "Johnson B",
            "7": "Johnson V",
            "8": "Johnson R",
            "9": "Johnson I",
            "10": "Johnson J",
            "11": "Johnson K",
            "12": "Johnson L",
            "13": "Johnson M",
            "14": "Johnson N",
            "15": "Cousins Rc",
            "16": "Cousins Ic",
            "17": "Bessel UX",
            "18": "Bessel BX",
            "19": "Bessel B",
            "20": "Bessel V",
            "21": "Bessel R",
            "22": "Bessel I",
            "23": "Tycho Bt",
            "24": "Tycho Vt",
            "25": "Hipparchos Hp",
            "26": "KEPLER",
            "27": "COROT SIS",
            "28": "COROT EXO",
            "29": "Geneva U",
            "30": "Geneva B",
            "31": "Geneva B1",
            "32": "Geneva B2",
            "33": "Geneva V",
            "34": "Geneva V1",
            "35": "Geneva G",
            "36": "Vilnius U",
            "37": "Vilnius P",
            "38": "Vilnius X",
            "39": "Vilnius Y",
            "40": "Vilnius Z",
            "41": "Vilnius V",
            "42": "Vilnius S",
            "43": "Milone iz",
            "44": "Milone iJ",
            "45": "Milone iH",
            "46": "Milone iK",
            "47": "YMS94 iz",
            "48": "YMS94 iJ",
            "49": "YMS94 iH",
            "50": "YMS94 iK",
            "51": "YMS94 iL",
            "52": "YMS94 iL'",
            "53": "YMS94 iM",
            "54": "YMS94 in",
            "55": "YMS94 iN",
            "56": "Sloan DDS u'",
            "57": "Sloan DDS g'",
            "58": "Sloan DDS r'",
            "59": "Sloan DDS i'",
            "60": "Sloan DDS z'",
            "61": "HST STIS Ly alpha",
            "62": "HST STIS Fclear",
            "63": "HST STIS Fsrf2",
            "64": "HST STIS Fqtz",
            "65": "HST STIS C III",
            "66": "HST STIS Mg II",
            "67": "HST STIS Nclear",
            "68": "HST STIS Nsrf2",
            "69": "HST STIS Nqtz",
            "70": "HST STIS cn182",
            "71": "HST STIS cn270",
            "72": "HST STIS Oclear",
            "73": "HST STIS Oclear-lp",
            "74": "HST STIS [O II]",
            "75": "HST STIS [O III]",
            "76": "2MASS J",
            "77": "2MASS H",
            "78": "2MASS Ks",
            "79": "SWASP",
            "80": "MOST",
            "81": "Gaia G (2006)",
            "82": "Gaia G (2010)",
            "83": "Gaia Gbp",
            "84": "Gaia Grp",
            "85": "Gaia Grvs",
            "86": "Milone 230",
            "87": "Milone 250",
            "88": "Milone 270",
            "89": "Milone 290",
            "90": "Milone 310",
            "91": "Milone 330",
            "92": "Ca II triplet",
            "93": "WIRE V+R",
            "94": "Lunar Ultraviolet Telescope",

        }
        self.lastBaseSet = None
        self.lastSubSets = None
        self.lastiteration = 0
        self.connectSignals()

    def connectSignals(self):
        self.rundc2015_btn.clicked.connect(self.runDc)
        self.setdeldefaults_btn.clicked.connect(self.setDelDefaults)
        self.clearbaseset_btn.clicked.connect(self.clearKeeps)
        self.updateinputs_btn.clicked.connect(self.updateInputFromOutput)
        self.viewlastdcin_btn.clicked.connect(self.showDcin)
        self.viewlaastdcout_btn.clicked.connect(self.showDcout)
        self.plotdcresults_btn.clicked.connect(self.PlotResultsWidget.show)

    def closeEvent(self, *args, **kwargs):
        try:
            self.iterator.exit()
        except:
            pass

        self.DcinView.close()
        self.DcoutView.close()
        self.PlotResultsWidget.close()

    def showDcin(self):
        self.DcinView.setWindowTitle("PyWD - " + self.dcinpath)
        self.DcinView.fill(self.dcinpath)
        self.DcinView.show()

    def showDcout(self):
        self.DcoutView.setWindowTitle("PyWD - " + self.dcoutpath)
        self.DcoutView.fill(self.dcoutpath)
        self.DcoutView.show()

    def setDelDefaults(self):
        self.del_s1lat_ipt.setText("0.02")
        self.del_s1lng_ipt.setText("0.02")
        self.del_s1agrad_ipt.setText("0.001")
        self.del_s1tmpf_ipt.setText("0.02")
        self.del_s2lat_ipt.setText("0.02")
        self.del_s2lng_ipt.setText("0.001")
        self.del_s2agrad_ipt.setText("0.0001")
        self.del_s2tmpf_ipt.setText("0.02")
        self.del_a_ipt.setText("0.05")
        self.del_e_ipt.setText("0.001")
        self.del_f1_ipt.setText("0.01")
        self.del_f2_ipt.setText("0.01")
        self.del_pshift_ipt.setText("0.002")
        self.del_perr0_ipt.setText("0.01")
        self.del_i_ipt.setText("0.2")
        self.del_q_ipt.setText("0.003")
        self.del_g1_ipt.setText("0.01")
        self.del_g2_ipt.setText("0.01")
        self.del_t1_ipt.setText("0.02")
        self.del_t2_ipt.setText("0.02")
        self.del_alb1_ipt.setText("0.05")
        self.del_alb2_ipt.setText("0.05")
        self.del_pot1_ipt.setText("0.02")
        self.del_pot2_ipt.setText("0.02")
        self.del_x1_ipt.setText("0.01")
        self.del_x2_ipt.setText("0.01")
        self.del_l1_ipt.setText("0.01")
        self.del_l2_ipt.setText("0.01")

    def clearKeeps(self):
        self.jd0_chk.setChecked(False)
        self.p0_chk.setChecked(False)
        self.dpdt_chk.setChecked(False)
        self.dperdt_chk.setChecked(False)
        self.a_chk.setChecked(False)
        self.e_chk.setChecked(False)
        self.perr0_chk.setChecked(False)
        self.f1_chk.setChecked(False)
        self.f2_chk.setChecked(False)
        self.pshift_chk.setChecked(False)
        self.vgam_chk.setChecked(False)
        self.incl_chk.setChecked(False)
        self.t1_chk.setChecked(False)
        self.t2_chk.setChecked(False)
        self.g1_chk.setChecked(False)
        self.g2_chk.setChecked(False)
        self.alb1_chk.setChecked(False)
        self.alb2_chk.setChecked(False)
        self.pot1_chk.setChecked(False)
        self.pot2_chk.setChecked(False)
        self.q_chk.setChecked(False)
        self.s1lat_chk.setChecked(False)
        self.s1long_chk.setChecked(False)
        self.s1rad_chk.setChecked(False)
        self.s1temp_chk.setChecked(False)
        self.s2lat_chk.setChecked(False)
        self.s2long_chk.setChecked(False)
        self.s2rad_chk.setChecked(False)
        self.s2temp_chk.setChecked(False)
        self.a3b_chk.setChecked(False)
        self.p3b_chk.setChecked(False)
        self.xinc3b_chk.setChecked(False)
        self.e3b_chk.setChecked(False)
        self.tc3b_chk.setChecked(False)
        self.perr3b_chk.setChecked(False)
        self.logd_chk.setChecked(False)
        self.desextinc_chk.setChecked(False)
        self.l1_chk.setChecked(False)
        self.l2_chk.setChecked(False)
        self.x1_chk.setChecked(False)
        self.x2_chk.setChecked(False)
        self.el3_chk.setChecked(False)
        self.s1tstart_chk.setChecked(False)
        self.s1tmax1_chk.setChecked(False)
        self.s1tmax2_chk.setChecked(False)
        self.s1tend_chk.setChecked(False)
        self.s2tstart_chk.setChecked(False)
        self.s2tmax1_chk.setChecked(False)
        self.s2tmax2_chk.setChecked(False)
        self.s2tend_chk.setChecked(False)

    def runDc(self):
        dcin = classes.dcin(self.MainWindow)  # only used to check warnings/errors
        msg = QtGui.QMessageBox(self)
        if dcin.hasError:
            msg.setWindowTitle("PyWD - Fatal Error")
            msg.setText("There were errors while parsing inputs:\n" + dcin.error + "\n")
            if dcin.hasWarning:
                msg.setText(msg.text() + "\nPlus, warnings were encountered: \n" + dcin.warning)
            msg.exec_()
        else:
            answer = 0
            if dcin.hasWarning:
                title = "PyWD - Warning"
                text = "Warnings are encountered while parsing inputs: \n" + dcin.warning + \
                       "\nDo you still want to run the DC Program?"
                answer = QtGui.QMessageBox.question(msg, title, text, QtGui.QMessageBox.Yes,
                                                    QtGui.QMessageBox.No)
            if answer == QtGui.QMessageBox.Yes or dcin.hasWarning is False:
                self.runIteration()

    def disableUi(self):
        self.updateinputs_btn.setDisabled(True)
        self.exportresults_btn.setDisabled(True)
        self.viewlaastdcout_btn.setDisabled(True)
        # self.viewlastdcin_btn.setDisabled(True)
        self.rundc2015_btn.clicked.disconnect()
        self.rundc2015_btn.clicked.connect(self.abort)
        self.result_treewidget.setDisabled(True)
        self.curvestat_treewidget.setDisabled(True)
        self.DcinView.fill(self.dcinpath)
        self.DcoutView.hide()
        self.MainWindow.LoadObservationWidget.setDisabled(True)
        self.MainWindow.SpotConfigureWidget.setDisabled(True)
        self.MainWindow.EclipseWidget.setDisabled(True)
        self.MainWindow.setDisabled(True)
        self.tabWidget_2.setDisabled(True)

    def enableUi(self):
        self.updateinputs_btn.setDisabled(False)
        self.exportresults_btn.setDisabled(False)
        self.viewlaastdcout_btn.setDisabled(False)
        # self.viewlastdcin_btn.setDisabled(False)
        self.rundc2015_btn.setText("Run DC")
        self.rundc2015_btn.clicked.disconnect()
        self.rundc2015_btn.clicked.connect(self.runDc)
        self.result_treewidget.setDisabled(False)
        self.curvestat_treewidget.setDisabled(False)
        self.MainWindow.LoadObservationWidget.setDisabled(False)
        self.MainWindow.SpotConfigureWidget.setDisabled(False)
        self.MainWindow.EclipseWidget.setDisabled(False)
        self.MainWindow.setDisabled(False)
        self.tabWidget_2.setDisabled(False)

    def updateInputFromOutput(self):
        paramdict = {
            9: self.MainWindow.a_ipt,
            10: self.MainWindow.e_ipt,
            11: self.MainWindow.perr0_ipt,
            12: self.MainWindow.f1_ipt,
            13: self.MainWindow.f2_ipt,
            14: self.MainWindow.pshift_ipt,
            15: self.MainWindow.vgam_ipt,
            16: self.MainWindow.xincl_ipt,
            17: self.MainWindow.gr1_spinbox,
            18: self.MainWindow.gr2_spinbox,
            19: self.MainWindow.tavh_ipt,
            20: self.MainWindow.tavc_ipt,
            21: self.MainWindow.alb1_spinbox,
            22: self.MainWindow.alb2_spinbox,
            23: self.MainWindow.phsv_ipt,
            24: self.MainWindow.pcsv_ipt,
            25: self.MainWindow.rm_ipt,
            26: self.MainWindow.jd0_ipt,
            27: self.MainWindow.p0_ipt,
            28: self.MainWindow.dpdt_ipt,
            29: self.MainWindow.dperdt_ipt,
            30: self.MainWindow.a3b_ipt,
            31: self.MainWindow.p3b_ipt,
            32: self.MainWindow.xinc3b_ipt,
            33: self.MainWindow.e3b_ipt,
            34: self.MainWindow.perr3b_ipt,
            35: self.MainWindow.tc3b_ipt,
            41: self.MainWindow.dpclog_ipt,
            42: self.MainWindow.desextinc_ipt
        }
        spotparamdict = {
            1: 3,
            2: 4,
            3: 5,
            4: 6,
            5: 3,
            6: 4,
            7: 5,
            8: 6,
            43: 7,
            44: 8,
            45: 9,
            46: 10,
            47: 7,
            48: 8,
            49: 9,
            50: 10,
        }
        # add conditions here
        spota = (1, 2, 3, 4, 43, 44, 45, 46)
        spotb = (5, 6, 7, 8, 47, 48, 49, 50)
        valueparams = (17, 18, 21, 22)

        for result in self.lastBaseSet:
            index = int(result[0])
            if result[1] != "0":
                curveindex = int(result[1]) - 1
                if result[0] == "56":
                    self.MainWindow.LoadObservationWidget.lcPropertiesList[curveindex].l1 = result[4]
                if result[0] == "57":
                    self.MainWindow.LoadObservationWidget.lcPropertiesList[curveindex].l2 = result[4]
                if result[0] == "58":
                    self.MainWindow.LoadObservationWidget.lcPropertiesList[curveindex].x1 = result[4]
                if result[0] == "59":
                    self.MainWindow.LoadObservationWidget.lcPropertiesList[curveindex].x2 = result[4]
                if result[0] == "60":
                    self.MainWindow.LoadObservationWidget.lcPropertiesList[curveindex].el3a = result[4]
            else:
                if index in (spota + spotb):
                    star1spots = self.MainWindow.SpotConfigureWidget.star1ElementList
                    star2spots = self.MainWindow.SpotConfigureWidget.star2ElementList
                    radioindex = ""
                    if index in spota:
                        radioindex = 1
                    if index in spotb:
                        radioindex = 2
                    for spot in star1spots:
                        if spot[radioindex].isChecked():
                            spot[spotparamdict[index]].setText(result[4])
                    for spot in star2spots:
                        if spot[radioindex].isChecked():
                            spot[spotparamdict[index]].setText(result[4])
                else:
                    if index in (19, 20):
                        paramdict[index].setText(str(float(result[4]) * 10000.0))
                    else:
                        if index is 15:
                            paramdict[index].setText(str(float(result[4]) * float(self.MainWindow.vunit_ipt.text())))
                        else:
                            if index in valueparams:  # input is spinbox
                                paramdict[index].setValue(float(result[4]))
                            else:  # just slap output into input
                                paramdict[index].setText(result[4])

    def updateResultTree(self, resultTable):
        def _populateItem(itm, rslt):
            frmt = "{:11.8f}"  # TODO add this as a user setting
            id = int(rslt[0])
            input = rslt[2]
            corr = rslt[3]
            output = rslt[4]
            stderr = rslt[5]
            if id in (19, 20):  # T's are in K/10000 format
                input = str(float(input) * 10000.0)
                corr = str(float(corr) * 10000.0)
                output = str(float(output) * 10000.0)
                stderr = str(float(stderr) * 10000.0)
            if id == 15:  # vgamma is in V/Vunit format
                input = str(float(input) * float(self.MainWindow.vunit_ipt.text()))
                corr = str(float(corr) * float(self.MainWindow.vunit_ipt.text()))
                output = str(float(output) * float(self.MainWindow.vunit_ipt.text()))
                stderr = str(float(stderr) * float(self.MainWindow.vunit_ipt.text()))
            itm.setText(0, self.parameterDict[rslt[0]])
            itm.setText(1, frmt.format(float(input)))
            itm.setText(2, frmt.format(float(corr)))
            itm.setText(3, frmt.format(float(output)))
            itm.setText(4, frmt.format(float(stderr)))
            if np.absolute(float(stderr)) > np.absolute(float(corr)):
                #itm.setBackground(0, QtGui.QBrush(QtGui.QColor("green")))
                #itm.setBackground(1, QtGui.QBrush(QtGui.QColor("green")))
                #itm.setBackground(2, QtGui.QBrush(QtGui.QColor("green")))
                itm.setBackground(3, QtGui.QBrush(QtGui.QColor("green")))
                #itm.setBackground(4, QtGui.QBrush(QtGui.QColor("green")))
            return itm
        self.result_treewidget.clear()
        root = self.result_treewidget.invisibleRootItem()
        curvelist = self.MainWindow.LoadObservationWidget.lcPropertiesList
        for result in resultTable:
            if result[1] != "0":
                name = str(result[1]) + ": " + self.bandpassDict[curvelist[int(result[1])-1].band]
                if curvelist[int(result[1])-1].type == "vc":
                    name = name + " (VC #{0})".format(curvelist[int(result[1])-1].star)
                isParent = False
                for i in range(root.childCount()):
                    parent = root.child(i)
                    if parent.text(0) == name:
                        isParent = True
                        item = _populateItem(QtGui.QTreeWidgetItem(parent), result)
                        parent.addChild(item)
                        self.result_treewidget.addTopLevelItem(item)
                if isParent is False:
                    parent = QtGui.QTreeWidgetItem(self.result_treewidget)
                    parent.setText(0, name)
                    item = _populateItem(QtGui.QTreeWidgetItem(parent), result)
                    parent.addChild(item)
                    parent.addChild(item)
                    self.result_treewidget.addTopLevelItem(item)
            else:
                item = _populateItem(QtGui.QTreeWidgetItem(self.result_treewidget), result)
                self.result_treewidget.addTopLevelItem(item)
        self.result_treewidget.expandAll()

    def updateCurveInfoTree(self, curveinfoTable):
        self.curvestat_treewidget.clear()
        frmt = "{:g}"  # TODO add this as a user setting
        curve = 0
        curvelist = self.MainWindow.LoadObservationWidget.Curves()
        for result in curveinfoTable:
            i = 0
            item = QtGui.QTreeWidgetItem(self.curvestat_treewidget)
            for value in result:
                if i is 0:
                    label = "//"
                    try:
                        label = self.bandpassDict[curvelist[curve].band]
                        if curvelist[curve].type == "vc":
                            label = label + " (VC #{0})".format(curvelist[curve].star)
                    except:
                         label = "Eclipse Timings"
                    item.setText(0, label)
                else:
                    item.setText(i, frmt.format(float(value.replace("D", "E"))))
                i = i + 1
            self.curvestat_treewidget.addTopLevelItem(item)
            curve = curve + 1

    def abort(self):
        self.iterator.stop()
        self.iterator = None
        self.enableUi()
        self.lastiteration = 0

    def iteratorException(self, *args):  # unused
        msg = QtGui.QMessageBox(self)
        msg.setText("Iterator thread has caught an exception:\n" + args[0])
        msg.setWindowTitle("PyWD - Thread Error")
        msg.exec_()
        self.enableUi()

    def runIteration(self):
        dcin = classes.dcin(self.MainWindow)  # we dont care about warnings/errors if we are already here
        self.rundc2015_btn.setText("Abort (Iteration {0} of {1})".format(self.lastiteration + 1,
                                                                         int(self.iteration_spinbox.value())))
        try:
            with open(self.dcinpath, "w") as f:
                f.write(dcin.output)
            thread = classes.IteratorThread(self.dcpath)
            self.iterator = thread
            self.connect(thread, QtCore.SIGNAL("finished()"), self.afterIteration)
            # self.connect(thread, thread.exception, self.iteratorException)
            self.disableUi()
            thread.start()
        except IOError as ex:
            msg = QtGui.QMessageBox(self)
            msg.setWindowTitle("PyWD - IO Error")
            msg.setText("An IO error has been caught:\n" + ex.message)
            msg.exec_()
        except:
            msg = QtGui.QMessageBox(self)
            msg.setWindowTitle("PyWD - Unknown Exception")
            msg.setText("Unknown exception has ben caught: " + str(sys.exc_info()))
            msg.exec_()

    def afterIteration(self):
        try:
            # self.disconnect(self.iterator, QtCore.SIGNAL("finished()"), _afterIteration)
            # self.disconnect(self.iterator, self.iterator.exception, self.iteratorException)
            # self.iterator.deleteLater()  # dispose iterator
            self.iterator = None
            self.lastBaseSet = methods.getTableFromOutput(self.dcoutpath, "Input-Output in F Format")
            self.updateResultTree(self.lastBaseSet)
            self.updateCurveInfoTree(methods.getTableFromOutput(self.dcoutpath,
                "Standard Deviations for Computation of Curve-dependent Weights")
            )
            self.enableUi()
            sanity = self.checkSanity()
            if sanity is True:
                self.continueIterating()
            else:
                niter = int(self.lastiteration)
                self.lastiteration = 0
                raise ValueError("Iteration #{0} resulted in NaN for one "
                                 "or multiple solutions.".format(niter + 1))
        except IOError as ex:
            msg = QtGui.QMessageBox(self)
            msg.setWindowTitle("PyWD - IO Error")
            msg.setText("An IO error has been caught:\n" + ex.message + str(sys.exc_info()))
            msg.exec_()
            self.enableUi()
        except ValueError as ex:
            msg = QtGui.QMessageBox(self)
            msg.setWindowTitle("PyWD - Value Error")
            msg.setText("A value error has been caught:\n" + ex.message)
            msg.exec_()
            self.enableUi()
        except:
            msg = QtGui.QMessageBox(self)
            msg.setWindowTitle("PyWD - Unknown Exception")
            msg.setText("Unknown exception has ben caught: " + str(sys.exc_info()))
            msg.exec_()
            self.enableUi()

    def checkSanity(self):
        sanity = True
        for result in self.lastBaseSet:
            for cell in result:
                if cell == "NaN" or cell == "nan":
                    sanity = False
                    break
        return sanity

    def continueIterating(self):
        self.lastiteration = self.lastiteration + 1
        if self.lastiteration < int(self.iteration_spinbox.value()):
            self.updateinputs_btn.click()
            self.runIteration()
        else:
            self.lastiteration = 0


class OutputView(QtGui.QWidget, outputview.Ui_OutputView):
    def __init__(self):  # constructor
        super(OutputView, self).__init__()
        self.setupUi(self)
        db = QtGui.QFontDatabase()
        db.addApplicationFont(os.path.join(os.getcwd(), "resources", "PTM55FT.ttf"))
        ptmono = QtGui.QFont(QtCore.QString("PT Mono"), pointSize=11)
        self.output_textedit.setFont(ptmono)

    def fill(self, filepath):
        text = ""
        with open(filepath, "r") as f:
            for line in f:
                text = text + line
        self.output_textedit.setPlainText(text)


class PlotResultsWidget(QtGui.QWidget, plotresultswidget.Ui_PlotResultsWidget):
    def __init__(self):
        super(PlotResultsWidget, self).__init__()
        self.setupUi(self)
        self.connectSignals()

    def connectSignals(self):
        pass

    def updateCurveComboBox(self):
        pass


if __name__ == "__main__":
    pass

