from PyQt4 import QtGui, QtCore
from gui import mainwindow, loadwidget, spotconfigurewidget, \
    eclipsewidget, curvepropertiesdialog, dcwidget, lcdcpickerdialog, outputview
from functools import partial
from bin import methods, classes
import numpy as np
import sys
import ConfigParser
import os


class MainWindow(QtGui.QMainWindow, mainwindow.Ui_MainWindow):  # main window class
    def __init__(self):  # constructor
        super(MainWindow, self).__init__()
        self.setupUi(self)  # setup ui from mainwindow.py
        self.setWindowIcon(QtGui.QIcon("resources/pywd.ico"))  # set app icon
        self.LoadWidget = LoadWidget()  # get loadwidget
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
        self.populateStyles()  # populate theme combobox
        self.connectSignals()  # connect events with method

    def connectSignals(self):
        self.whatsthis_btn.clicked.connect(QtGui.QWhatsThis.enterWhatsThisMode)  # enters what's this mode
        self.loadwidget_btn.clicked.connect(self.LoadWidget.show)  # opens loadwidget
        self.spotconfigure_btn.clicked.connect(self.SpotConfigureWidget.show)  # opens spotconfigurewidget
        self.dc_rundc_btn.clicked.connect(partial(self.DCWidget.show))
        self.theme_combobox.currentIndexChanged.connect(self.changeStyle)
        self.eclipsewidget_btn.clicked.connect(self.EclipseWidget.show)
        self.saveproject_btn.clicked.connect(self.saveProjectDialog)
        self.loadproject_btn.clicked.connect(self.loadProjectDialog)

    def closeEvent(self, *args, **kwargs):  # overriding QMainWindow's closeEvent
        self.LoadWidget.close()  # close loadwidget if we exit
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

    def saveProjectDialog(self):
        dialog = QtGui.QFileDialog(self)
        dialog.setDefaultSuffix("pywdproject")
        dialog.setNameFilter("PyWD2015 Project File (*pywdproject)")
        dialog.setAcceptMode(1)
        returnCode = dialog.exec_()
        filePath = str((dialog.selectedFiles())[0])
        if filePath != "" and returnCode != 0:
            try:
                project = methods.saveProject(self)
                with open(filePath, "w") as f:
                    f.write(project)
            except:
                msg = QtGui.QMessageBox()
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


class LoadWidget(QtGui.QWidget, loadwidget.Ui_LoadWidget):  # file load widget class
    def __init__(self):  # constructor
        super(LoadWidget, self).__init__()
        self.setupUi(self)  # setup ui from loadwidget.py
        self.setWindowIcon(QtGui.QIcon("resources/pywd.ico"))  # set app icon
        # setup variables
        self.lcCount = 0  # lc input count for widget restructure
        self.lcElementList = []  # a list of lists to store dynamically created elements
        # [[label], [filepath], [edit_button], [remove_button]]
        self.lcPropertiesList = []  # a list to hold lc property objects
        self.vcPropertiesList = [0, 0]  # a list to hold vc property objects
        self.connectSignals()  # connect signals

    def connectSignals(self):
        self.lcadd_btn.clicked.connect(partial(self.loadCurveDialog, "lc", -1))
        self.vc1load_btn.clicked.connect(partial(self.loadCurveDialog, "vc", 1))
        self.vc2load_btn.clicked.connect(partial(self.loadCurveDialog, "vc", 2))
        self.vc1edit_btn.clicked.connect(partial(methods.editVelocityCurve, 1, self))
        self.vc2edit_btn.clicked.connect(partial(methods.editVelocityCurve, 2, self))

    def getCurveProperties(self):
        curves = []
        for element in (self.vcPropertiesList + self.lcPropertiesList):
            if element != 0:
                curves.append(element)
        return curves

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
                            methods.addLightCurve(self)  # actually just adds a row to the ui
                        if type == "vc":
                            self.vcPropertiesList[vcNumber-1] = curveprop
                            methods.loadVelocityCurve(vcNumber, self)
            except:
                msg = QtGui.QMessageBox()
                msg.setText("An error has ocurred: \n" + str(sys.exc_info()[1]))
                msg.exec_()

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


class CurvePropertiesDialog(QtGui.QDialog, curvepropertiesdialog.Ui_CurvePropertiesDialog):
    def __init__(self):
        super(CurvePropertiesDialog, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon("resources/pywd.ico"))
        self.type = ""
        self.hasError = False
        self.connectSignals()

    def connectSignals(self):
        self.accept_btn.clicked.connect(partial(self.done, 1))
        self.discard_btn.clicked.connect(partial(self.done, 2))
        self.whatsthis_btn.clicked.connect(QtGui.QWhatsThis.enterWhatsThisMode)
        self.repick_btn.clicked.connect(self.repick)

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
        self.connectSignals()

    def connectSignals(self):
        self.rundc2015_btn.clicked.connect(self.runDc)
        self.setdeldefaults_btn.clicked.connect(self.setDelDefaults)
        self.clearbaseset_btn.clicked.connect(self.clearKeeps)
        self.updateinputs_btn.clicked.connect(self.updateInputFromOutput)
        self.viewlastdcin_btn.clicked.connect(self.showDcin)
        self.viewlaastdcout_btn.clicked.connect(self.showDcout)

    def closeEvent(self, *args, **kwargs):
        try:
            self.iterator.exit()
        except:
            pass

        self.DcinView.close()
        self.DcoutView.close()

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
                if int(self.iteration_spinbox.value()) == 1:
                    self.singleIteration()
                else:
                    self.singleIteration()
                    # self.multipleIteration()

    def disableUi(self):
        self.updateinputs_btn.setDisabled(True)
        self.exportresults_btn.setDisabled(True)
        self.viewlaastdcout_btn.setDisabled(True)
        # self.viewlastdcin_btn.setDisabled(True)
        self.rundc2015_btn.setText("Abort (Iteration 1 of {0})".format(int(self.iteration_spinbox.value())))
        self.rundc2015_btn.clicked.disconnect()
        self.rundc2015_btn.clicked.connect(self.abort)
        self.result_treewidget.setDisabled(True)
        self.curvestat_treewidget.setDisabled(True)
        self.DcinView.fill(self.dcinpath)
        self.DcoutView.hide()

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
        degreeparams = (11, 34)
        valueparams = (17, 18, 21, 22)

        for result in self.lastBaseSet:
            done = False
            index = int(result[0])
            if result[1] != "0":
                curveindex = int(result[1]) - 1
                if result[0] == "56":
                    self.MainWindow.LoadWidget.lcPropertiesList[curveindex].l1 = result[4]
                if result[0] == "57":
                    self.MainWindow.LoadWidget.lcPropertiesList[curveindex].l2 = result[4]
                if result[0] == "58":
                    self.MainWindow.LoadWidget.lcPropertiesList[curveindex].x1 = result[4]
                if result[0] == "59":
                    self.MainWindow.LoadWidget.lcPropertiesList[curveindex].x2 = result[4]
                if result[0] == "60":
                    self.MainWindow.LoadWidget.lcPropertiesList[curveindex].el3a = result[4]
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
                else:  # add rules here TODO move this to output formatting in result tree widget
                    if index in degreeparams:  # output is in radians
                        paramdict[index].setText(str(float(result[4]) * 180 / np.pi))
                        done = True
                    if index in valueparams:  # input is spinbox
                        paramdict[index].setValue(float(result[4]))
                        done = True
                    if index in (19, 20):  # output temp is in k/10000 format
                        paramdict[index].setText(str(float(result[4]) * 10000))
                        done = True
                    if index is 15:  # output is in v/vgam format
                        paramdict[index].setText(str(float(result[4]) * float(self.MainWindow.vunit_ipt.text())))
                        done = True
                    if done is False:  # just slap output into input
                        paramdict[index].setText(result[4])

    def updateResultTree(self, resultTable):
        def _populateItem(itm, rslt):
            frmt = "{:11.8f}"  # TODO add this as a user setting
            itm.setText(0, self.parameterDict[rslt[0]])
            itm.setText(1, frmt.format(float(rslt[2])))
            itm.setText(2, frmt.format(float(rslt[3])))
            itm.setText(3, frmt.format(float(rslt[4])))
            itm.setText(4, frmt.format(float(rslt[5])))
            return itm
        self.result_treewidget.clear()
        root = self.result_treewidget.invisibleRootItem()
        curvelist = self.MainWindow.LoadWidget.lcPropertiesList
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

    def updateCurveInfoTree(self, curveinfoTable):
        self.curvestat_treewidget.clear()
        frmt = "{:g}"  # TODO add this as a user setting
        curve = 0
        curvelist = self.MainWindow.LoadWidget.getCurveProperties()
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

    def iteratorException(self, *args):  # unused
        msg = QtGui.QMessageBox(self)
        msg.setText("Iterator thread has caught an exception:\n" + args[0])
        msg.setWindowTitle("PyWD - Thread Error")
        msg.exec_()
        self.enableUi()

    def singleIteration(self):
        def _afterIteration():
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
            except IOError as ex:
                msg = QtGui.QMessageBox(self)
                msg.setWindowTitle("PyWD - IO Error")
                msg.setText("An IO error has been caught:\n" + ex.message + str(sys.exc_info()))
                msg.exec_()
                self.enableUi()
            except:
                msg = QtGui.QMessageBox(self)
                msg.setWindowTitle("PyWD - Unknown Exception")
                msg.setText("Unknown exception has ben caught: " + str(sys.exc_info()))
                msg.exec_()
                self.enableUi()

        dcin = classes.dcin(self.MainWindow)  # we dont care about warnings/errors if we are already here
        try:
            with open(self.dcinpath, "w") as f:
                f.write(dcin.output)
            thread = classes.IteratorThread(self.dcpath)
            self.iterator = thread
            self.connect(thread, QtCore.SIGNAL("finished()"), _afterIteration)
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

    def multipleIteration(self):
        # TODO implement multiple iteration
        pass


class OutputView(QtGui.QWidget, outputview.Ui_OutputView):
    def __init__(self):  # constructor
        super(OutputView, self).__init__()
        self.setupUi(self)
        db = QtGui.QFontDatabase()
        db.addApplicationFont(os.path.join(os.getcwd(), "resources", "PTM55FT.ttf"))
        inconsolata = QtGui.QFont(QtCore.QString("PT Mono"), pointSize=11)
        self.output_textedit.setFont(inconsolata)

    def fill(self, filepath):
        text = ""
        with open(filepath, "r") as f:
            for line in f:
                text = text + line
        self.output_textedit.setPlainText(text)


if __name__ == "__main__":
    pass
