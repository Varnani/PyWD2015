from PyQt4 import QtGui, QtCore
import numpy
from scipy.optimize import fsolve
from matplotlib import pyplot, gridspec
from matplotlib.lines import Line2D
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from gui import mainwindow, spotconfigurewidget, eclipsewidget, curvepropertiesdialog, \
    dcwidget, lcdcpickerdialog, outputview, loadobservationwidget, plotresultswidget, syntheticcurvewidget
from functools import partial
from bin import methods, classes
from itertools import izip
import subprocess
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
        self.SyntheticCurveWidget = SyntheticCurveWidget()
        self.SyntheticCurveWidget.MainWindow = self
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
        self.fill_btn.clicked.connect(self.fillLcHJDMenu)
        self.lc_lightcurve_btn.clicked.connect(self.SyntheticCurveWidget.show)

    def closeEvent(self, *args, **kwargs):  # overriding QMainWindow's closeEvent
        self.LoadObservationWidget.close()
        self.SpotConfigureWidget.close()
        self.EclipseWidget.close()
        self.DCWidget.close()
        self.SyntheticCurveWidget.close()

    def setPaths(self, lcpath, dcpath):
        self.lcpath = lcpath
        self.lcinpath = os.path.join(os.path.dirname(lcpath), "lcin.active")
        self.lcoutpath = os.path.join(os.path.dirname(lcpath), "lcout.active")
        self.DCWidget.dcpath = dcpath
        self.DCWidget.dcinpath = os.path.join(os.path.dirname(dcpath), "dcin.active")
        self.DCWidget.dcoutpath = os.path.join(os.path.dirname(dcpath), "dcout.active")

    def clearWidgets(self):
        # TODO add proper cleaning here (plots, trees, widgets which depend on current project)
        self.DCWidget.data_combobox.clear()
        self.DCWidget.plot_observationAxis.clear()
        self.DCWidget.plot_residualAxis.clear()

        self.SyntheticCurveWidget.plot_observationAxis.clear()
        self.SyntheticCurveWidget.plot_residualAxis.clear()
        self.SyntheticCurveWidget.plot_starposAxis.clear()

        self.DCWidget.obs_x = []
        self.DCWidget.obs_y = []
        self.DCWidget.model_x = []
        self.DCWidget.model_y = []
        self.DCWidget.resd_x = []
        self.DCWidget.resd_y = []
        self.DCWidget.obslabel = ""
        self.DCWidget.timelabel = ""

        yticks_resd = self.DCWidget.plot_residualAxis.yaxis.get_major_ticks()
        yticks_resd[-1].label1.set_visible(False)
        yticks_star = self.SyntheticCurveWidget.plot_starposAxis.yaxis.get_major_ticks()
        yticks_star[0].label1.set_visible(False)
        yticks_star[-1].label1.set_visible(False)

        self.DCWidget.plot_canvas.draw()
        self.SyntheticCurveWidget.plot_canvas.draw()

        pyplot.cla()

        self.DCWidget.result_treewidget.clear()
        self.DCWidget.component_treewidget.clear()
        self.DCWidget.residual_treewidget.clear()
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

    def fillLcHJDMenu(self):
        curves = self.LoadObservationWidget.Curves()
        if len(curves) >= 1:
            menu = QtGui.QMenu()
            for index, curve in enumerate(curves):
                a = menu.addAction(os.path.basename(curve.FilePath))
                a.idx = index
            selection = menu.exec_(QtGui.QCursor.pos())
            if selection is not None:
                curve = classes.Curve(self.LoadObservationWidget.Curves()[selection.idx].FilePath)
                start = min(curve.timeList)
                stop = max(curve.timeList)
                if self.jdphs_combobox.currentText() == "Time":
                    self.jdstart_ipt.setText(start)
                    self.jdstop_ipt.setText(stop)
                    self.jdincrement_ipt.setText(str(float(self.p0_ipt.text()) / 100.0))
                if self.jdphs_combobox.currentText() == "Phase":
                    self.phasestart_ipt.setText(start)
                    self.phasestop_ipt.setText(stop)
                    self.phaseincrement_ipt.setText("0.001")

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

    def numberOfVelocityCurves(self):
        i = 0
        for curve in self.vcPropertiesList:
            if curve is not 0:
                i = i + 1
        return i

    def loadCurveDialog(self, type, vcNumber):
        dialog = QtGui.QFileDialog(self)
        dialog.setAcceptMode(0)
        returnCode = dialog.exec_()
        filePath = (dialog.selectedFiles())[0]
        if filePath != "" and returnCode != 0:
            try:
                curvedialog = CurvePropertiesDialog.createCurveDialog(type)
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
                curvedialog = CurvePropertiesDialog.createCurveDialog("vc")
                curvedialog.populateFromObject(self.vcPropertiesList[0])
            if item.text(1) == "Velocity Curve (#2)":
                curvedialog = CurvePropertiesDialog.createCurveDialog("vc")
                curvedialog.populateFromObject(self.vcPropertiesList[1])
            if item.text(1) == "Light Curve":
                curvedialog = CurvePropertiesDialog.createCurveDialog("lc")
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
        self.MainWindow.SyntheticCurveWidget.loaded_treewidget.clear()
        self.MainWindow.SyntheticCurveWidget.loaded_treewidget.model().dataChanged.disconnect(
            self.MainWindow.SyntheticCurveWidget.updateObservations
        )
        self.MainWindow.clearWidgets()
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
        self.curve_treewidget.header().setResizeMode(3)
        self.MainWindow.SyntheticCurveWidget.populateSyntheticCurveWidget()
        self.MainWindow.SyntheticCurveWidget.appendSynthetics()
        self.MainWindow.SyntheticCurveWidget.loaded_treewidget.model().dataChanged.connect(
            self.MainWindow.SyntheticCurveWidget.updateObservations
        )


class CurvePropertiesDialog(QtGui.QDialog, curvepropertiesdialog.Ui_CurvePropertiesDialog):
    def __init__(self):
        super(CurvePropertiesDialog, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon("resources/pywd.ico"))
        self.type = ""
        self.synthetic = False
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
        self.reverseBandpassDict = {self.bandpassdict[key]: key for key in self.bandpassdict.keys()}
        self.bandpassContextMenu = self.createBandpassContextMenu()
        self.datawidget.header().setResizeMode(3)
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
        if CurveProperties.synthetic is not True:
            curve = classes.Curve(CurveProperties.FilePath)
            if curve.hasError:
                self.hasError = True
                msg = QtGui.QMessageBox()
                msg.setText(curve.error)
                msg.setWindowTitle("PyWD - Error")
                msg.exec_()
            for x in curve.lines:
                a = QtGui.QTreeWidgetItem(self.datawidget, x)
        if self.type == "lc":
            if CurveProperties.synthetic is not True:
                self.noise_combobox.setCurrentIndex(int(CurveProperties.noise))
            else:
                self.noise_combobox.addItem("N/A")
                self.noise_combobox.setCurrentIndex(3)
            self.el3a_ipt.setText(CurveProperties.el3a)
            self.aextinc_ipt.setText(CurveProperties.aextinc)
            self.xunit_ipt.setText(CurveProperties.xunit)
            self.calib_ipt.setText(CurveProperties.calib)
        if CurveProperties.synthetic:
            self.filepath_label.setText("N/A")
            self.filepath_label.setToolTip("N/A")
            self.e1_ipt.setText("N/A")
            self.e2_ipt.setText("N/A")
            self.e3_ipt.setText("N/A")
            self.e4_ipt.setText("N/A")
            self.label_11.setText("ZERO")
            self.sigma_ipt.setText(CurveProperties.zero)
            self.xunit_ipt.setText(CurveProperties.factor)
            self.label_21.setText("FACTOR")

    @staticmethod
    def createCurveDialog(type, synthetic=False):
        curvedialog = CurvePropertiesDialog()
        curvedialog.type = type
        if type == "lc":
            curvedialog.label_53.setText("Load or edit a light curve")
            curvedialog.type = "lc"
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
        if synthetic:
            if type == "lc":
                curvedialog.label_53.setText("Load or edit a synthetic light curve")
            if type == "vc":
                curvedialog.label_53.setText("Load or edit a synthetic velocity curve")
                curvedialog.aextinc_ipt.setText("0")
                curvedialog.calib_ipt.setText("0")
                curvedialog.el3a_ipt.setDisabled(True)
                curvedialog.el3a_ipt.setText("0")
            curvedialog.ksd_box.setDisabled(True)
            curvedialog.datawidget.setDisabled(True)
            curvedialog.filepath_label.setText("N/A")
            curvedialog.e1_ipt.setDisabled(True)
            curvedialog.e1_ipt.setText("N/A")
            curvedialog.e2_ipt.setDisabled(True)
            curvedialog.e2_ipt.setText("N/A")
            curvedialog.e3_ipt.setDisabled(True)
            curvedialog.e3_ipt.setText("N/A")
            curvedialog.e4_ipt.setDisabled(True)
            curvedialog.e4_ipt.setText("N/A")
            curvedialog.label_11.setText("ZERO")
            curvedialog.label_11.setToolTip("A reference magnitude that can shift "
                                            "a magnitude light curve (LC output) vertically")
            curvedialog.sigma_ipt.setText("8")
            curvedialog.label_21.setText("FACTOR")
            curvedialog.label_21.setToolTip("A scaling factor for LC output curves in flux (not magnitude)")
            curvedialog.xunit_ipt.setText("1")
            curvedialog.xunit_ipt.setDisabled(False)
            curvedialog.noise_combobox.setDisabled(True)
            curvedialog.noise_combobox.addItem("N/A")
            curvedialog.noise_combobox.setCurrentIndex(3)
            curvedialog.repick_btn.setDisabled(True)
            curvedialog.synthetic = True
        return curvedialog


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
        self.result_treewidget.header().setResizeMode(3)
        self.residual_treewidget.header().setResizeMode(3)
        self.component_treewidget.header().setResizeMode(3)
        self.curvestat_treewidget.header().setResizeMode(3)
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
        # variables for plot
        self.obs_x = []
        self.obs_y = []
        self.model_x = []
        self.model_y = []
        self.resd_x = []
        self.resd_y = []
        self.obslabel = ""
        self.timelabel = ""
        # canvas for main
        self.plot_figure = Figure()
        self.plot_canvas = FigureCanvas(self.plot_figure)
        self.plot_toolbar = NavigationToolbar(self.plot_canvas, self.plotwidget)
        plot_layout = QtGui.QVBoxLayout()
        plot_layout.addWidget(self.plot_toolbar)
        plot_layout.addWidget(self.plot_canvas)
        self.plotwidget.setLayout(plot_layout)
        grid = gridspec.GridSpec(2, 1, height_ratios=[1.5, 1])
        self.plot_observationAxis = self.plot_figure.add_subplot(grid[0])
        self.plot_residualAxis = self.plot_figure.add_subplot(grid[1], sharex=self.plot_observationAxis)
        self.plot_observationAxis.get_xaxis().set_visible(False)
        yticks = self.plot_residualAxis.yaxis.get_major_ticks()
        yticks[-1].label1.set_visible(False)
        self.plot_figure.tight_layout()
        self.plot_figure.subplots_adjust(top=0.95, bottom=0.1, left=0.1, right=0.95, hspace=0, wspace=0)
        self.plot_canvas.draw()
        # signal connection
        self.connectSignals()

    def connectSignals(self):
        self.rundc2015_btn.clicked.connect(self.runDc)
        self.setdeldefaults_btn.clicked.connect(self.setDelDefaults)
        self.clearbaseset_btn.clicked.connect(self.clearKeeps)
        self.updateinputs_btn.clicked.connect(self.updateInputFromOutput)
        self.viewlastdcin_btn.clicked.connect(self.showDcin)
        self.viewlaastdcout_btn.clicked.connect(self.showDcout)
        # self.plotdcresults_btn.clicked.connect(self.PlotResultsWidget.show)
        self.plot_btn.clicked.connect(self.plotData)
        self.popmain_btn.clicked.connect(self.popPlotWindow)

    def closeEvent(self, *args, **kwargs):
        try:
            self.iterator.exit()
        except:
            pass

        self.DcinView.close()
        self.DcoutView.close()
        self.PlotResultsWidget.close()

    def getXYfromFile(self, filepath):
        curve = classes.Curve(filepath)
        offset = 0.0
        if str(self.MainWindow.jdphs_combobox.currentText()) == "Phase":
            offset = float(curve.timeList[0])
        x = [float(x) - offset for x in curve.timeList]
        y = [float(y) for y in curve.observationList]
        return x, y

    def populatePlotCombobox(self):
        lastindex = self.data_combobox.currentIndex()
        self.data_combobox.clear()
        for curve in self.MainWindow.LoadObservationWidget.Curves():
            self.data_combobox.addItem(os.path.basename(curve.FilePath))
        try:
            self.data_combobox.setCurrentIndex(lastindex)
        except:
            self.data_combobox.setCurrentIndex(0)
            self.autoupdate_chk.setChecked(False)

    def plotData(self):
        # TODO this is becoming messy. clean up before doing anything else.
        if str(self.data_combobox.currentText()) != "":
            index = self.data_combobox.currentIndex()

            ocTable = methods.getTableFromOutput(self.dcoutpath, "Unweighted Observational Equations")
            curvestatTable = methods.getTableFromOutput(
                self.dcoutpath,
                "Standard Deviations for Computation of Curve-dependent Weights"
            )
            columnLimit = 20
            baseColumns = 4
            if self.MainWindow.jdphs_combobox.currentText() == "Time":
                columnLimit = 23
                baseColumns = 5
            currentColumns = len(methods.getTableFromOutput(self.dcoutpath, "Input-Output in F Format")) + baseColumns
            if currentColumns > columnLimit:
                currentIndex = 0
                tempList = []
                step = 2
                if currentColumns > columnLimit * 2:
                    step = 3
                if currentColumns > columnLimit * 3:
                    step = 4
                while currentIndex < len(ocTable):
                    tempList.append(ocTable[currentIndex] + ocTable[currentIndex + 1])
                    currentIndex = currentIndex + step
                ocTable = tempList

            nobsStart = 0
            i = int(index)
            t = 0
            while i != 0:
                nobsStart = nobsStart + int(curvestatTable[t][1])
                i = i - 1
                t = t + 1
            nobsEnd = nobsStart + int(curvestatTable[index][1])
            ocTable = ocTable[nobsStart:nobsEnd]
            obsIndex = 1
            timeIndex = 0
            xlabel = self.time_combobox.currentText()
            ylabel = self.MainWindow.maglite_combobox.currentText()
            if ylabel == "Flux":
                ylabel = "Norm. Flux"
            if self.MainWindow.LoadObservationWidget.Curves()[self.data_combobox.currentIndex()].type == "vc":
                ylabel = "Radial Velocity (km s$^{-1}$)"
            if self.MainWindow.jdphs_combobox.currentText() == "Time":  # wd outputs are in HJD
                obsIndex = 2
            if self.time_combobox.currentText() == "Phase" and self.MainWindow.jdphs_combobox.currentText() == "Time":
                timeIndex = 1
            x_axis = [float(x[timeIndex]) for x in ocTable]
            obs = [float(x[obsIndex]) for x in ocTable]
            resd = [float(x[-1]) for x in ocTable]

            lc_x = []
            lc_y = []

            if self.uselc_chk.isChecked():
                # get model
                curveProp = self.MainWindow.LoadObservationWidget.Curves()[self.data_combobox.currentIndex()].getSynthetic()
                curveProp.zero = "8"
                curveProp.factor = "1"
                curve = classes.Curve(curveProp.FilePath)
                line3 = []
                if self.MainWindow.jdphs_combobox.currentText() == "Time" and self.time_combobox.currentText() == "HJD":
                    line3 = [min(curve.timeList), max(curve.timeList), float(self.MainWindow.p0_ipt.text()) / 100,
                             0, 1, 0.001, 0.25, 0.75, 1, float(self.MainWindow.tavh_ipt.text()) / 10000]
                else:
                    line3 = [self.MainWindow.jd0_ipt.text(), float(self.MainWindow.jd0_ipt.text()) + 1, 0.1,
                             0, 1, 0.001, 0.25, 0.75, 1, float(self.MainWindow.tavh_ipt.text()) / 10000]
                model = classes.lcin(self.MainWindow)
                mpage = 1
                if curveProp.type == "vc":
                    mpage = 2
                jdphs = "2"
                if self.time_combobox.currentText() == "HJD" and self.MainWindow.jdphs_combobox.currentText() == "Time":
                    jdphs = "1"
                model.syntheticCurve(curveProp, mpage, line3=line3, jdphs=jdphs)
                with open(self.MainWindow.lcinpath, "w") as f:
                    f.write(model.output)
                # exec model
                process = subprocess.Popen(self.MainWindow.lcpath, cwd=os.path.dirname(self.MainWindow.lcpath))
                process.wait()
                # get data
                lcoutTable = methods.getTableFromOutput(self.MainWindow.lcoutpath, "grid1/4", offset=6)
                lc_y_index = 4
                lc_x_index = 1
                if self.MainWindow.jdphs_combobox.currentText() == "Time" and self.time_combobox.currentText() == "HJD":
                    lc_x_index = 0
                if curveProp.type == "vc":
                    lc_y_index = 6 + self.data_combobox.currentIndex()

                lc_x = [float(x[lc_x_index].replace("D", "E")) for x in lcoutTable]
                lc_y = [float(y[lc_y_index].replace("D", "E")) for y in lcoutTable]

                if curveProp.type == "vc":
                    t = [x * float(str(self.MainWindow.vunit_ipt.text())) for x in lc_y]
                    lc_y = t
                    t = [x * float(str(self.MainWindow.vunit_ipt.text())) for x in obs]
                    obs = t
            else:
                lc_x = x_axis
                idx = 2
                if self.MainWindow.jdphs_combobox.currentText() == "Time":
                    idx = 3
                lc_y = [float(x[idx]) for x in ocTable]

            self.plot_observationAxis.clear()
            self.plot_residualAxis.clear()
            self.plot_observationAxis.plot(x_axis, obs, linestyle="", marker="o", markersize=4, color="#4286f4")
            if self.uselc_chk.isChecked():
                self.plot_observationAxis.plot(lc_x, lc_y, color="red")
            else:
                self.plot_observationAxis.plot(lc_x, lc_y, linestyle="", marker="o", markersize=4, color="red")
            self.plot_residualAxis.plot(x_axis, resd, linestyle="", marker="o", markersize=4, color="#4286f4")
            self.plot_residualAxis.axhline(c="r")
            self.plot_toolbar.update()
            # yticks = self.plot_residualAxis.yaxis.get_major_ticks()
            # yticks[-1].label1.set_visible(False)
            self.plot_residualAxis.set_xlabel(xlabel)
            self.plot_residualAxis.set_ylabel("Residuals")
            self.plot_observationAxis.set_ylabel(ylabel)
            self.plot_canvas.draw()
            # store plot data
            self.obs_x = x_axis
            self.obs_y = obs
            self.model_x = lc_x
            self.model_y = lc_y
            self.resd_x = x_axis
            self.resd_y = resd
            self.obslabel = ylabel
            self.timelabel = xlabel

    def popPlotWindow(self):
        if self.data_combobox.currentText() != "":
            self.plot_btn.click()
            pyplot.cla()
            grid = gridspec.GridSpec(2, 1, height_ratios=[1.5, 1])
            obs = pyplot.subplot(grid[0])
            resd = pyplot.subplot(grid[1], sharex=obs)
            pyplot.subplots_adjust(top=0.95, bottom=0.1, left=0.1, right=0.95, hspace=0, wspace=0)
            yticks = resd.yaxis.get_major_ticks()
            yticks[-1].label1.set_visible(False)

            obs.plot(self.obs_x, self.obs_y, linestyle="", marker="o", markersize=4, color="#4286f4")
            resd.plot(self.resd_x, self.resd_y, linestyle="", marker="o", markersize=4, color="#4286f4")
            if self.uselc_chk.isChecked():
                obs.plot(self.model_x, self.model_y, color="red")
            else:
                obs.plot(self.model_x, self.model_y, linestyle="", marker="o", markersize=4, color="red")
            title = "Matplotlib - " + os.path.basename(str(self.MainWindow.LoadObservationWidget.Curves()[self.data_combobox.currentIndex()].FilePath))
            resd.axhline(c="r")
            pyplot.get_current_fig_manager().set_window_title(title)
            obs.set_ylabel(self.obslabel)
            resd.set_ylabel("Residuals")
            resd.set_xlabel(self.timelabel)
            pyplot.show()

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
        self.DcinView.fill(self.dcinpath)
        self.DcoutView.hide()
        self.MainWindow.LoadObservationWidget.setDisabled(True)
        self.MainWindow.SpotConfigureWidget.setDisabled(True)
        self.MainWindow.EclipseWidget.setDisabled(True)
        self.MainWindow.setDisabled(True)
        self.tabWidget_2.setDisabled(True)
        self.plot_btn.setDisabled(True)
        self.autoupdate_chk.setDisabled(True)
        self.popmain_btn.setDisabled(True)

    def enableUi(self):
        self.updateinputs_btn.setDisabled(False)
        self.exportresults_btn.setDisabled(False)
        self.viewlaastdcout_btn.setDisabled(False)
        # self.viewlastdcin_btn.setDisabled(False)
        self.rundc2015_btn.setText("Run DC")
        self.rundc2015_btn.clicked.disconnect()
        self.rundc2015_btn.clicked.connect(self.runDc)
        self.MainWindow.LoadObservationWidget.setDisabled(False)
        self.MainWindow.SpotConfigureWidget.setDisabled(False)
        self.MainWindow.EclipseWidget.setDisabled(False)
        self.MainWindow.setDisabled(False)
        self.tabWidget_2.setDisabled(False)
        self.plot_btn.setDisabled(False)
        self.autoupdate_chk.setDisabled(False)
        self.popmain_btn.setDisabled(False)

    def updateInputFromOutput(self):
        if self.lastBaseSet is not None:
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
            self.MainWindow.SyntheticCurveWidget.loaded_treewidget.model().dataChanged.disconnect(
                self.MainWindow.SyntheticCurveWidget.updateObservations
            )
            self.MainWindow.SyntheticCurveWidget.loaded_treewidget.clear()
            self.MainWindow.SyntheticCurveWidget.populateSyntheticCurveWidget()
            self.MainWindow.SyntheticCurveWidget.appendSynthetics()
            self.MainWindow.SyntheticCurveWidget.loaded_treewidget.model().dataChanged.connect(
                self.MainWindow.SyntheticCurveWidget.updateObservations
            )

    def updateResultTree(self, resultTable):
        frmt = "{:11.8f}"

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
            input = str(frmt.format(float(input)).rstrip("0"))
            if input[-1] == ".":
                input = input + "0"
            corr = str(frmt.format(float(corr)).rstrip("0"))
            if corr[-1] == ".":
                corr = corr + "0"
            output = str(frmt.format(float(output)).rstrip("0"))
            if output[-1] == ".":
                output = output + "0"
            stderr = str(frmt.format(float(stderr)).rstrip("0"))
            if stderr[-1] == ".":
                stderr = stderr + "0"
            itm.setText(0, self.parameterDict[rslt[0]])
            itm.setText(1, input)
            itm.setText(2, corr)
            itm.setText(3, output)
            itm.setText(4, stderr)
            if numpy.absolute(float(stderr)) > numpy.absolute(float(corr)):
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

    def updateResidualTree(self, residualData):
        self.residual_treewidget.clear()
        item = QtGui.QTreeWidgetItem(self.residual_treewidget)
        item.setText(0, residualData[0].replace("D", "E"))
        item.setText(1, residualData[1].replace("D", "E"))
        item.setText(2, residualData[2].replace("D", "E"))

    def updateComponentTree(self, first, second):
        self.component_treewidget.clear()
        star1ParentItem = QtGui.QTreeWidgetItem(self.component_treewidget)
        star1ParentItem.setText(0, "Star 1")
        for component in first:
            item = QtGui.QTreeWidgetItem(star1ParentItem)
            item.setText(0, component[1].title())
            item.setText(1, component[2])
            item.setText(2, component[5])
            star1ParentItem.addChild(item)

        star2ParentItem = QtGui.QTreeWidgetItem(self.component_treewidget)
        star2ParentItem.setText(0, "Star 2")
        for component in second:
            item = QtGui.QTreeWidgetItem(star2ParentItem)
            item.setText(0, component[1].title())
            item.setText(1, component[2])
            item.setText(2, component[5])
            star2ParentItem.addChild(item)

        self.component_treewidget.expandAll()

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
            residualTable = methods.getTableFromOutput(self.dcoutpath, "Mean residual for input values", offset=1)[0]
            firstComponentTable = methods.getTableFromOutput(self.dcoutpath, "  1   pole", offset=0)
            secondComponentTable = methods.getTableFromOutput(self.dcoutpath, "  2   pole", offset=0)
            self.updateResultTree(self.lastBaseSet)
            self.updateComponentTree(firstComponentTable, secondComponentTable)
            self.updateResidualTree(residualTable)
            self.updateCurveInfoTree(methods.getTableFromOutput(self.dcoutpath,
                "Standard Deviations for Computation of Curve-dependent Weights")
            )
            self.enableUi()
            sanity = self.checkSanity()
            if sanity is True:
                self.populatePlotCombobox()
                if self.autoupdate_chk.isChecked():
                    self.plot_btn.click()
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


class SyntheticCurveWidget(QtGui.QWidget, syntheticcurvewidget.Ui_SyntheticCurveWidget):
    def __init__(self):
        super(SyntheticCurveWidget, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon("resources/pywd.ico"))  # set app icon
        # variables
        self.MainWindow = None
        self.lastEditedIndex = None
        self.lastEditedColumn = None
        # set up canvas
        self.plot_figure = Figure()
        self.plot_canvas = FigureCanvas(self.plot_figure)
        self.plot_toolbar = NavigationToolbar(self.plot_canvas, self.plot_widget)
        plot_layout = QtGui.QVBoxLayout()
        plot_layout.addWidget(self.plot_toolbar)
        plot_layout.addWidget(self.plot_canvas)
        self.plot_widget.setLayout(plot_layout)
        self.dual_grid = gridspec.GridSpec(2, 1, height_ratios=[1.5, 1])
        self.triple_grid = gridspec.GridSpec(2, 2, height_ratios=[1.5, 1], width_ratios=[2, 1], wspace=0.1)
        self.plot_observationAxis = self.plot_figure.add_subplot(self.dual_grid[0])
        self.plot_residualAxis = self.plot_figure.add_subplot(self.dual_grid[1], sharex=self.plot_observationAxis)
        self.plot_starposAxis = self.plot_figure.add_subplot(self.triple_grid[0:, -1])
        self.plot_starposAxis.axis("equal")
        self.plot_starposAxis.set_visible(False)
        self.plot_observationAxis.get_xaxis().set_visible(False)
        # self.plot_figure.tight_layout()
        self.plot_figure.subplots_adjust(top=0.95, bottom=0.1, left=0.1, right=0.95, hspace=0, wspace=0)
        self.plot_canvas.draw()
        # add synthetic curves
        self.appendSynthetics()
        self.loaded_treewidget.setEditTriggers(self.loaded_treewidget.NoEditTriggers)
        self.loaded_treewidget.header().setResizeMode(3)
        # signal connection
        self.connectSignals()

    def connectSignals(self):
        self.roche_chk.stateChanged.connect(self.rocheChanged)
        self.loaded_treewidget.model().dataChanged.connect(self.updateObservations)
        self.loaded_treewidget.itemDoubleClicked.connect(self.checkEditable)
        self.plot_btn.clicked.connect(self.plotSelected)

    def selectedItem(self):
        selecteditem = self.loaded_treewidget.selectedItems()
        if len(selecteditem) > 0:
            return selecteditem[0]
        else:
            return None

    def plotSelected(self):
        if self.selectedItem() is not None:
            self.plot_observationAxis.clear()
            self.plot_residualAxis.clear()
            self.plot_starposAxis.clear()
            self.plot_observationAxis.set_position(self.dual_grid[0].get_position(self.plot_figure))
            self.plot_residualAxis.set_position(self.dual_grid[1].get_position(self.plot_figure))
            self.plot_starposAxis.set_visible(False)
            item = self.selectedItem()
            ylabel = None
            type = ""
            if str(item.text(1)) in ("Velocity Curve", "Velocity Curve #1", "Velocity Curve #2"):
                type = "vc"
                ylabel = "Radial Velocity (km s$^{-1}$)"
            else:
                type = "lc"
                ylabel = str(self.MainWindow.maglite_combobox.currentText())
                if ylabel == "Flux":
                    ylabel = "Norm. Flux"
            xlabel = None
            if str(self.time_combobox.currentText()) == "Phase":
                xlabel = "Phase"
            if str(self.time_combobox.currentText()) == "HJD" and str(self.MainWindow.jdphs_combobox.currentText()) == "Time":
                xlabel = "HJD"
            self.plot_observationAxis.set_ylabel(ylabel)
            self.plot_residualAxis.set_xlabel(xlabel)
            syntheticCurve = classes.CurveProperties(type, synthetic=True)
            curveProps = CurvePropertiesDialog()
            if str(item.text(0)) == "[Synthetic]" and str(item.text(1)) == "Velocity Curve":
                syntheticCurve.band = "7"
                syntheticCurve.l1 = "1"
                syntheticCurve.l2 = "1"
                syntheticCurve.x1 = "1"
                syntheticCurve.x2 = "1"
                syntheticCurve.y1 = "1"
                syntheticCurve.y2 = "1"
                syntheticCurve.el3a = "1"
                syntheticCurve.opsf = "1"
                syntheticCurve.zero = "8"
                syntheticCurve.factor = "1"
                syntheticCurve.wla = "0.55"
                syntheticCurve.aextinc = "0"
                syntheticCurve.calib = "0"
            elif str(item.text(0)) == "[Synthetic]" and str(item.text(1)) == "Light Curve":
                button = self.loaded_treewidget.itemWidget(item, 2)
                syntheticCurve.band = curveProps.bandpassdict[str(button.text())]
                syntheticCurve.l1 = item.text(3)
                syntheticCurve.l2 = item.text(4)
                syntheticCurve.x1 = item.text(6)
                syntheticCurve.x2 = item.text(7)
                syntheticCurve.y1 = item.text(8)
                syntheticCurve.y2 = item.text(9)
                syntheticCurve.el3a = item.text(5)
                syntheticCurve.opsf = item.text(10)
                syntheticCurve.zero = "8"
                syntheticCurve.factor = "1"
                syntheticCurve.wla = "0.55"
                syntheticCurve.aextinc = item.text(11)
                syntheticCurve.calib = item.text(12)
            else:
                index = self.loaded_treewidget.invisibleRootItem().indexOfChild(item)
                curve = self.MainWindow.LoadObservationWidget.Curves()[index]
                syntheticCurve = curve.getSynthetic()
                syntheticCurve.zero = "8"
                syntheticCurve.factor = "1"
            if self.plotobs_chk.isChecked():
                if str(item.text(0)) != "[Synthetic]":
                    index = self.loaded_treewidget.invisibleRootItem().indexOfChild(item)
                    curve = classes.Curve(self.MainWindow.LoadObservationWidget.Curves()[index].FilePath)
                    curveProperties = self.MainWindow.LoadObservationWidget.Curves()[index]
                    x_obs = [float(x) for x in curve.timeList]
                    y_obs = [float(y) for y in curve.observationList]
                    print curveProps.type
                    if curveProperties.type == "vc":
                        idxDict = {
                            1: 1,
                            2: 0
                        }
                        idx = idxDict[curveProperties.star]
                        vc2curveProperties = self.MainWindow.LoadObservationWidget.vcPropertiesList[idx]
                        if vc2curveProperties != 0:
                            curve2 = classes.Curve(vc2curveProperties.FilePath)
                            x2_obs = [float(x) for x in curve2.timeList]
                            y2_obs = [float(y) for y in curve2.observationList]
                    if self.time_combobox.currentText() == "Phase" and self.MainWindow.jdphs_combobox.currentText() == "Time":
                        t0 = float(self.MainWindow.jd0_ipt.text())
                        p = float(self.MainWindow.p0_ipt.text())
                        x2 = []
                        for t in x_obs:
                            obs = ((t - t0) / p) - int((t - t0) / p)
                            while obs < 0.0:
                                obs = obs + 1.0
                            x2.append(obs)
                        x_obs = x2
                        if curveProperties.type == "vc":
                            x2_2 = []
                            for t in x2_obs:
                                obs2 = ((t - t0) / p) - int((t - t0) / p)
                                while obs2 < 0.0:
                                    obs2 = obs2 + 1.0
                                x2_2.append(obs2)
                            x2_obs = x2_2

                    self.plot_observationAxis.plot(x_obs, y_obs, linestyle="", marker="o", markersize=4, color="#4286f4")
                    if curveProperties.type == "vc":
                        self.plot_observationAxis.plot(x2_obs, y2_obs, linestyle="", marker="o", markersize=4,
                                                       color="#f73131")
                    curveProps = self.MainWindow.LoadObservationWidget.Curves()[index]

            if self.plotmodel_chk.isChecked():
                lcin = classes.lcin(self.MainWindow)
                mpage = 1
                if syntheticCurve.type == "vc":
                    mpage = 2
                jdphs = None
                if str(self.time_combobox.currentText()) == "HJD":
                    jdphs = "1"
                else:
                    jdphs = "2"
                lcin.syntheticCurve(syntheticCurve, mpage, jdphs=jdphs)
                with open(self.MainWindow.lcinpath, "w") as f:
                    f.write(lcin.output)
                process = subprocess.Popen(self.MainWindow.lcpath, cwd=os.path.dirname(self.MainWindow.lcpath))
                process.wait()
                table = methods.getTableFromOutput(self.MainWindow.lcoutpath, "grid1/4", offset=6)
                # set data indexes
                x_index = None
                y_index = None
                y2_index = None
                if syntheticCurve.type == "vc":
                    y_index = 6
                    y2_index = 7
                if syntheticCurve.type == "lc":
                    y_index = 4
                if self.time_combobox.currentText() == "HJD":
                    x_index = 0
                else:
                    x_index = 1
                # get data from table
                x_model = [float(line[x_index].replace("D", "E")) for line in table]
                y_model = [float(line[y_index].replace("D", "E")) for line in table]
                y2_model = []
                if syntheticCurve.type == "vc":
                    vunit = float(str(self.MainWindow.vunit_ipt.text()))
                    y1 = [y * vunit for y in y_model]
                    y_model = y1
                    y2_model = [float(line[y2_index].replace("D", "E")) * vunit for line in table]
                # plot data
                if syntheticCurve.type == "lc":
                    self.plot_observationAxis.plot(x_model, y_model, color="red")
                if syntheticCurve.type == "vc":
                    self.plot_observationAxis.plot(x_model, y_model, color="red")
                    self.plot_observationAxis.plot(x_model, y2_model, color="#f48942")
                if self.plotobs_chk.isChecked() and str(item.text(0)) != "[Synthetic]":
                    if syntheticCurve.type == "vc":
                        if syntheticCurve.star == 2:
                            a = y_model
                            y_model = y2_model
                            y2_model = a
                        interpolated_y2_model = numpy.interp(x2_obs, x_model, y2_model)
                        y2_residuals = []
                        for o, c in izip(y2_obs, interpolated_y2_model):
                            y2_residuals.append(o - c)
                        self.plot_residualAxis.plot(x_obs, y2_residuals, linestyle="", marker="o", markersize=4,
                                                    color="#f73131")
                    interpolated_y_model = numpy.interp(x_obs, x_model, y_model)
                    y_residuals = []
                    for o, c in izip(y_obs, interpolated_y_model):
                        y_residuals.append(o - c)
                    self.plot_residualAxis.plot(x_obs, y_residuals, linestyle="", marker="o", markersize=4, color="#4286f4")
                self.plot_residualAxis.set_ylabel("Residuals")
                    
            if self.drawstars_chk.isChecked() or self.roche_chk.isChecked():
                center_of_mass = 1 - (1 / (1 + float(self.MainWindow.rm_ipt.text())))
                self.plot_observationAxis.set_position(self.triple_grid[0, :-1].get_position(self.plot_figure))
                self.plot_residualAxis.set_position(self.triple_grid[1, :-1].get_position(self.plot_figure))
                self.plot_starposAxis.set_visible(True)
                if self.drawstars_chk.isChecked():
                    if self.roche_chk.isChecked():
                        stored_inclination = str(self.MainWindow.xincl_ipt.text())
                        self.MainWindow.xincl_ipt.setText("90")
                    lcin = classes.lcin(self.MainWindow)
                    phase = self.phase_spinbox.value()
                    lcin.starPositions(line3=[self.MainWindow.jd0_ipt.text(), float(self.MainWindow.jd0_ipt.text()) + 1, 0.1,
                                 phase, phase, 0.1, 0.25, 0.75, 1, float(self.MainWindow.tavh_ipt.text()) / 10000], jdphs="2")
                    with open(self.MainWindow.lcinpath, "w") as f:
                        f.write(lcin.output)
                    process = subprocess.Popen(self.MainWindow.lcpath, cwd=os.path.dirname(self.MainWindow.lcpath))
                    process.wait()
                    table = methods.getTableFromOutput(self.MainWindow.lcoutpath, "grid1/4", offset=9)
                    x = [float(x[0].replace("D", "E")) + center_of_mass for x in table]
                    y = [float(y[1].replace("D", "E")) for y in table]
                    self.plot_starposAxis.plot(x, y, 'ko', markersize=0.2, label="Surface Grids")
                    self.plot_starposAxis.plot([center_of_mass], [0], linestyle="", marker="+", markersize=5, color="#ff3a3a")
                    if self.roche_chk.isChecked():
                        self.MainWindow.xincl_ipt.setText(stored_inclination)
                if self.roche_chk.isChecked():

                    # This snippet is only for e = 0 and f = 1, for now
                    # For in-depth discussion about calculating Roche potentials, refer to:
                    # Eclipsing Binary Stars: Modeling and Analysis (Kallrath & Milone, 2009, Springer)

                    w = float(self.MainWindow.perr0_ipt.text())
                    # e = float(self.MainWindow.e_ipt.text())
                    e = 0.0
                    phase = float(self.phase_spinbox.value())
                    phase_shift = float(self.MainWindow.pshift_ipt.text())

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
                    print "Separation at phase {0}: {1}".format(phase, separation_at_phase)
                    q = float(self.MainWindow.rm_ipt.text())
                    qIsInverse = False
                    if q > 1.0:
                        q = 1 / q
                        qIsInverse = True
                    f = 1.0
                    f_critical = lambda x: (-1 / x ** 2) - \
                                                 (q * ((x - separation_at_phase) / pow(numpy.absolute(separation_at_phase - x), 3))) + \
                                                 (x * f ** 2 * (q + 1)) - (q / separation_at_phase ** 2)  # Appendix E.12.4
                    inner_critical_x = fsolve(f_critical, separation_at_phase / 2.0)
                    inner_potential = (1 / inner_critical_x) + (q * ((1 / numpy.absolute(separation_at_phase - inner_critical_x)) - (inner_critical_x / (separation_at_phase ** 2)))) + (
                            ((q + 1) / 2) * (f ** 2) * (inner_critical_x ** 2))  # Appendix E.12.8
                    print "Inner critical potential: {0}".format(inner_potential)
                    mu = (1.0 / 3.0) * q / (1.0 + q)
                    outer_critical_estimation = 1.0 + mu ** (1.0 / 3.0) + (1.0 / 3.0) * mu ** (2.0 / 3.0) + (1.0 / 9.0) * mu ** (3.0 / 3.0)
                    outer_critical_x = fsolve(f_critical, outer_critical_estimation)
                    outer_potential = (1.0 / outer_critical_x) + (q * ((1.0 / numpy.absolute(separation_at_phase - outer_critical_x)) - (outer_critical_x / (separation_at_phase ** 2)))) + (
                            ((q + 1.0) / 2.0) * (f ** 2) * (outer_critical_x ** 2))  # Appendix E.12.8
                    print "Outer critical potential: {0}".format(outer_potential)
                    f_outer_critical = lambda x: 1.0/(numpy.sqrt(x**2)) + q*(1.0 / (numpy.sqrt(separation_at_phase**2-2.0*x*separation_at_phase+x**2)) - x/separation_at_phase**2) + f**2*((q+1.0)/2.0)*(x**2) - outer_potential
                    left_limit = fsolve(f_outer_critical, -1.0 * (separation_at_phase / 2.0))
                    right_limit = outer_critical_x
                    x_axis = numpy.linspace(left_limit, right_limit, 2000)
                    z_axis = numpy.linspace(-1, 2, 2000)
                    (X, Z) = numpy.meshgrid(x_axis, z_axis)
                    all_pots = ((1 / numpy.sqrt(X ** 2 + Z ** 2)) + (q * (
                            (1 / numpy.sqrt((separation_at_phase ** 2) - (2 * X * separation_at_phase) + (numpy.sqrt(X ** 2 + Z ** 2) ** 2))) - (
                            X / (separation_at_phase ** 2)))) + (0.5 * (f ** 2) * (q + 1) * (X ** 2)))
                    if qIsInverse:
                        self.plot_starposAxis.contour(-1.0 * X + 1.0, Z, all_pots, inner_potential, colors="red")
                        self.plot_starposAxis.contour(-1.0 * X + 1.0, Z, all_pots, outer_potential, colors="blue")
                    else:
                        self.plot_starposAxis.contour(X, Z, all_pots, inner_potential, colors="red")
                        self.plot_starposAxis.contour(X, Z, all_pots, outer_potential, colors="blue")
                    self.plot_starposAxis.plot([0, separation_at_phase, center_of_mass], [0, 0, 0], linestyle="", marker="+", markersize=10, color="#ff3a3a")
                self.plot_starposAxis.set_xlim(-1, 2)
                self.plot_starposAxis.set_ylim(-1, 1)
                self.plot_starposAxis.set_xlabel('x')
                self.plot_starposAxis.set_ylabel('y')
            self.plot_toolbar.update()
            yticks_resd = self.plot_residualAxis.yaxis.get_major_ticks()
            yticks_resd[-1].label1.set_visible(False)
            self.plot_residualAxis.axhline(0, color="red")
            self.plot_canvas.draw()

    def updateObservations(self):
        item = self.loaded_treewidget.invisibleRootItem().child(self.lastEditedIndex)
        if item.text(0) != "[Synthetic]":
            curve = self.MainWindow.LoadObservationWidget.Curves()[self.lastEditedIndex]
            if self.lastEditedColumn == 2:
                curveProp = CurvePropertiesDialog()
                button = self.loaded_treewidget.itemWidget(item, 2)
                curve.band = curveProp.bandpassdict[str(button.text())]
                item2 = self.MainWindow.LoadObservationWidget.curve_treewidget.invisibleRootItem().child(self.lastEditedIndex)
                item2.setText(2, button.text())
            elif self.lastEditedColumn == 3:
                curve.l1 = str(item.text(self.lastEditedColumn))
            elif self.lastEditedColumn == 4:
                curve.l2 = str(item.text(self.lastEditedColumn))
            elif self.lastEditedColumn == 5:
                curve.el3a = str(item.text(self.lastEditedColumn))
            elif self.lastEditedColumn == 6:
                curve.x1 = str(item.text(self.lastEditedColumn))
            elif self.lastEditedColumn == 7:
                curve.x2 = str(item.text(self.lastEditedColumn))
            elif self.lastEditedColumn == 8:
                curve.y1 = str(item.text(self.lastEditedColumn))
            elif self.lastEditedColumn == 9:
                curve.y2 = str(item.text(self.lastEditedColumn))
            elif self.lastEditedColumn == 10:
                curve.opsf = str(item.text(self.lastEditedColumn))
            elif self.lastEditedColumn == 11:
                curve.aextinc = str(item.text(self.lastEditedColumn))
            elif self.lastEditedColumn == 12:
                curve.calib = str(item.text(self.lastEditedColumn))
            self.MainWindow.LoadObservationWidget.lcPropertiesList[
                self.lastEditedIndex - self.MainWindow.LoadObservationWidget.numberOfVelocityCurves()
            ] = curve

    def checkEditable(self, item, column):  # item and column are the clicked hex's properties
        if column not in (0, 1):
            if str(item.text(1)) not in ("Velocity Curve", "Velocity Curve #1", "Velocity Curve #2"):
                self.lastEditedIndex = self.loaded_treewidget.invisibleRootItem().indexOfChild(item)
                self.lastEditedColumn = column
                self.loaded_treewidget.editItem(item, column)

    def appendSynthetics(self):
        item = QtGui.QTreeWidgetItem(self.loaded_treewidget)
        item.setText(0, "[Synthetic]")
        item.setText(1, "Velocity Curve")
        item.setText(2, "-")
        item.setText(3, "-")
        item.setText(4, "-")
        item.setText(5, "-")
        item.setText(6, "-")
        item.setText(7, "-")
        item.setText(8, "-")
        item.setText(9, "-")
        item.setText(10, "-")
        item.setText(11, "-")
        item.setText(12, "-")
        item = QtGui.QTreeWidgetItem(self.loaded_treewidget)
        item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
        item.setText(0, "[Synthetic]")
        item.setText(1, "Light Curve")
        curveProps = CurvePropertiesDialog()
        button = QtGui.QPushButton(self)
        button.setText("Select a filter")
        button.setMaximumHeight(20)
        button.clicked.connect(partial(self.selectBand, button, item))
        self.loaded_treewidget.setItemWidget(item, 2, button)
        item.setText(3, "0")
        item.setText(4, "0")
        item.setText(5, "0")
        item.setText(6, "0")
        item.setText(7, "0")
        item.setText(8, "0")
        item.setText(9, "0")
        item.setText(10, "0")
        item.setText(11, "0")
        item.setText(12, "0")

    def populateSyntheticCurveWidget(self):
        for curve in self.MainWindow.LoadObservationWidget.Curves():
            item = QtGui.QTreeWidgetItem(self.loaded_treewidget)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
            if curve.type == "vc":
                item.setText(0, os.path.basename(curve.FilePath))
                item.setText(1, "Velocity Curve #{0}".format(curve.star))
                item.setText(2, "-")
                item.setText(3, "-")
                item.setText(4, "-")
                item.setText(5, "-")
                item.setText(6, "-")
                item.setText(7, "-")
                item.setText(8, "-")
                item.setText(9, "-")
                item.setText(10, "-")
                item.setText(11, "-")
                item.setText(12, "-")
            if curve.type == "lc":
                curveProps = CurvePropertiesDialog()
                item.setText(0, os.path.basename(curve.FilePath))
                item.setText(1, "Light Curve")
                button = QtGui.QPushButton(self)
                button.setText(curveProps.reverseBandpassDict[curve.band])
                button.setMaximumHeight(20)
                button.clicked.connect(partial(self.selectBand, button, item))
                self.loaded_treewidget.setItemWidget(item, 2, button)
                item.setText(3, curve.l1)
                item.setText(4, curve.l2)
                item.setText(5, curve.el3a)
                item.setText(6, curve.x1)
                item.setText(7, curve.x2)
                item.setText(8, curve.y1)
                item.setText(9, curve.y2)
                item.setText(10, curve.opsf)
                item.setText(11, curve.aextinc)
                item.setText(12, curve.calib)
        self.loaded_treewidget.header().setResizeMode(3)

    def selectBand(self, button, item):
        curve = CurvePropertiesDialog()
        menu = curve.bandpassContextMenu
        band = menu.exec_(QtGui.QCursor.pos())
        if band is not None:
            button.setText(band.objectName())
            self.lastEditedIndex = self.loaded_treewidget.invisibleRootItem().indexOfChild(item)
            self.lastEditedColumn = 2
            self.loaded_treewidget.model().dataChanged.emit(QtCore.QModelIndex(), QtCore.QModelIndex())

    def rocheChanged(self):
        if self.roche_chk.isChecked():
            self.phase_spinbox.setDisabled(True)
            self.phase_spinbox.setValue(float(0.25))
        else:
            self.phase_spinbox.setDisabled(False)


if __name__ == "__main__":
    pass

