from PyQt4 import QtGui, QtCore
from gui import mainwindow, loadwidget, spotconfigurewidget, eclipsewidget, curvepropertiesdialog, dcwidget
from functools import partial
from bin import methods, classes
import sys
import ConfigParser


class MainWindow(QtGui.QMainWindow, mainwindow.Ui_MainWindow):  # main window class
    def __init__(self):  # constructor
        super(MainWindow, self).__init__()
        self.setupUi(self)  # setup ui from mainwindow.py
        self.setWindowIcon(QtGui.QIcon("resources/pywd.ico"))  # set app icon
        self.LoadWidget = LoadWidget()  # get loadwidget
        self.SpotConfigureWidget = SpotConfigureWidget()  # get spotconfigurewidget
        self.EclipseWidget = EclipseWiget()
        self.DCWidget = DCWidget()
        self.DCWidget.MainWindow = self
        self.populateStyles()  # populate theme combobox
        self.setKeepDefaults()  # set keeps to their defaults
        self.connectSignals()  # connect events with methods

    def connectSignals(self):
        self.whatsthis_btn.clicked.connect(QtGui.QWhatsThis.enterWhatsThisMode)  # enters what's this mode
        self.loadwidget_btn.clicked.connect(self.LoadWidget.show)  # opens loadwidget
        self.spotconfigure_btn.clicked.connect(self.SpotConfigureWidget.show)  # opens spotconfigurewidget
        self.dc_rundc_btn.clicked.connect(partial(self.DCWidget.show))
        self.theme_combobox.currentIndexChanged.connect(self.changeStyle)
        self.setdeldefaults_btn.clicked.connect(self.setDelDefaults)
        self.clearkeeps_btn.clicked.connect(self.clearKeeps)
        self.setkeepdefaults_btn.clicked.connect(self.setKeepDefaults)
        self.eclipsewidget_btn.clicked.connect(self.EclipseWidget.show)
        self.saveproject_btn.clicked.connect(self.saveProjectDialog)
        self.loadproject_btn.clicked.connect(self.loadProjectDialog)

    def closeEvent(self, *args, **kwargs):  # overriding QMainWindow's closeEvent
        self.LoadWidget.close()  # close loadwidget if we exit
        self.SpotConfigureWidget.close()  # close spotconfigurewidget if we exit
        self.EclipseWidget.close()

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
            text = "Loading a project file will erase all unsaved changes. Do you want to load \"" + \
                   fi.fileName() + "\" ?"
            answer = QtGui.QMessageBox.question(self, title, text, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if answer == QtGui.QMessageBox.Yes:
                try:
                    parser = ConfigParser.SafeConfigParser()
                    with open(filePath, "r") as f:
                        parser.readfp(f)
                    methods.loadProject(self, parser)
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
        def _clearKeep(keep):  # eval keeps for clearing
            if keep.isChecked():
                keep.toggle()

        _clearKeep(self.jd0_chk)
        _clearKeep(self.p0_chk)
        _clearKeep(self.dpdt_chk)
        _clearKeep(self.dperdt_chk)
        _clearKeep(self.a_chk)
        _clearKeep(self.e_chk)
        _clearKeep(self.perr0_chk)
        _clearKeep(self.f1_chk)
        _clearKeep(self.f2_chk)
        _clearKeep(self.pshift_chk)
        _clearKeep(self.vgam_chk)
        _clearKeep(self.incl_chk)
        _clearKeep(self.t1_chk)
        _clearKeep(self.t2_chk)
        _clearKeep(self.g1_chk)
        _clearKeep(self.g2_chk)
        _clearKeep(self.alb1_chk)
        _clearKeep(self.alb2_chk)
        _clearKeep(self.pot1_chk)
        _clearKeep(self.pot2_chk)
        _clearKeep(self.q_chk)
        _clearKeep(self.s1lat_chk)
        _clearKeep(self.s1long_chk)
        _clearKeep(self.s1rad_chk)
        _clearKeep(self.s1temp_chk)
        _clearKeep(self.s2lat_chk)
        _clearKeep(self.s2long_chk)
        _clearKeep(self.s2rad_chk)
        _clearKeep(self.s2temp_chk)
        _clearKeep(self.a3b_chk)
        _clearKeep(self.p3b_chk)
        _clearKeep(self.xinc3b_chk)
        _clearKeep(self.e3b_chk)
        _clearKeep(self.tc3b_chk)
        _clearKeep(self.perr3b_chk)
        _clearKeep(self.logd_chk)
        _clearKeep(self.desextinc_chk)
        _clearKeep(self.l1_chk)
        _clearKeep(self.l2_chk)
        _clearKeep(self.x1_chk)
        _clearKeep(self.x2_chk)
        _clearKeep(self.el3_chk)
        _clearKeep(self.s1tstart_chk)
        _clearKeep(self.s1tmax1_chk)
        _clearKeep(self.s1tmax2_chk)
        _clearKeep(self.s1tend_chk)
        _clearKeep(self.s2tstart_chk)
        _clearKeep(self.s2tmax1_chk)
        _clearKeep(self.s2tmax2_chk)
        _clearKeep(self.s2tend_chk)

    def setKeepDefaults(self):
        self.clearKeeps()
        self.p0_chk.toggle()
        self.vgam_chk.toggle()
        self.pot1_chk.toggle()
        self.pot2_chk.toggle()
        self.q_chk.toggle()
        self.l1_chk.toggle()
        self.el3_chk.toggle()

    def populateStyles(self):
        styleFactory = QtGui.QStyleFactory()
        styleKeys = styleFactory.keys()
        for style in styleKeys:
            self.theme_combobox.addItem(str(style))

    def changeStyle(self):
        styleFactory = QtGui.QStyleFactory()
        style = styleFactory.create(self.theme_combobox.currentText())
        self.app.setStyle(style)


class EclipseWiget(QtGui.QWidget, eclipsewidget.Ui_EclipseWidget):
    def __init__(self):
        super(EclipseWiget, self).__init__()
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
        # self.EditLightCurveDialog = EditLightCurveDialog()  # get light curve edit widget
        # self.EditVelocityCurveDialog = EditVelocityCurveDialog()  # get velocity curve edit widget
        self.connectSignals()  # connect signals

    def connectSignals(self):
        self.lcadd_btn.clicked.connect(partial(self.loadCurveDialog, "lc", -1))
        self.vc1load_btn.clicked.connect(partial(self.loadCurveDialog, "vc", 1))
        self.vc2load_btn.clicked.connect(partial(self.loadCurveDialog, "vc", 2))
        self.vc1edit_btn.clicked.connect(partial(methods.editVelocityCurve, 1, self))
        self.vc2edit_btn.clicked.connect(partial(methods.editVelocityCurve, 2, self))

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
        # [[label], [radioA], [radioB], [lat_input], [lon_input], [radsp_input], [temsp_input], [remove_button]]
        self.star2ElementList = []
        # [[label], [radioA], [radioB], [lat_input], [lon_input], [radsp_input], [temsp_input], [remove_button]]
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
        self.MainWindow = None
        self.connectSignals()

    def connectSignals(self):
        self.rundc2015_btn.clicked.connect(self.runDc)

    def runDc(self):  # TODO refactor this after implementing methods.runDc()
        methods.runDc(self.MainWindow)


if __name__ == "__main__":
    pass
