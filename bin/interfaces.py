from PyQt4 import QtGui
from gui import mainwindow, loadwidget, spotconfigurewidget, \
    editlightcurvedialog, editvelocitycurvedialog, eclipsewidget
from functools import partial
from bin import methods, classes
import sys


class MainWindow(QtGui.QMainWindow, mainwindow.Ui_MainWindow):  # main window class
    def __init__(self):  # constructor
        super(MainWindow, self).__init__()
        self.setupUi(self)  # setup ui from mainwindow.py
        self.setWindowIcon(QtGui.QIcon("resources/pywd.ico"))  # set app icon
        self.LoadWidget = LoadWidget()  # get loadwidget
        self.SpotConfigureWidget = SpotConfigureWidget()  # get spotconfigurewidget
        self.EclipseWidget = EclipseWiget()
        self.populateStyles()  # populate theme combobox
        self.setKeepDefaults()  # set keeps to their defaults
        self.connectSignals()  # connect events with methods

    def connectSignals(self):
        self.whatsthis_btn.clicked.connect(QtGui.QWhatsThis.enterWhatsThisMode)  # enters what's this mode
        self.loadwidget_btn.clicked.connect(self.LoadWidget.show)  # opens loadwidget
        self.spotconfigure_btn.clicked.connect(self.SpotConfigureWidget.show)  # opens spotconfigurewidget
        self.export_btn.clicked.connect(partial(methods.runDc, self))
        self.theme_combobox.currentIndexChanged.connect(self.changeStyle)
        self.setdeldefaults_btn.clicked.connect(self.setDelDefaults)
        self.clearkeeps_btn.clicked.connect(self.clearKeeps)
        self.setkeepdefaults_btn.clicked.connect(self.setKeepDefaults)
        self.eclipsewidget_btn.clicked.connect(self.EclipseWidget.show)
        self.saveproject_btn.clicked.connect(self.saveProjectDialog)

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
                methods.saveProject(self, filePath)
            except:
                msg = QtGui.QMessageBox()
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
        def _evalkeeps(keep):  # eval keeps for clearing
            if keep.isChecked():
                keep.toggle()

        _evalkeeps(self.jd0_chk)
        _evalkeeps(self.p0_chk)
        _evalkeeps(self.dpdt_chk)
        _evalkeeps(self.dperdt_chk)
        _evalkeeps(self.a_chk)
        _evalkeeps(self.e_chk)
        _evalkeeps(self.perr0_chk)
        _evalkeeps(self.f1_chk)
        _evalkeeps(self.f2_chk)
        _evalkeeps(self.pshift_chk)
        _evalkeeps(self.vgam_chk)
        _evalkeeps(self.incl_chk)
        _evalkeeps(self.t1_chk)
        _evalkeeps(self.t2_chk)
        _evalkeeps(self.g1_chk)
        _evalkeeps(self.g2_chk)
        _evalkeeps(self.alb1_chk)
        _evalkeeps(self.alb2_chk)
        _evalkeeps(self.pot1_chk)
        _evalkeeps(self.pot2_chk)
        _evalkeeps(self.q_chk)
        _evalkeeps(self.s1lat_chk)
        _evalkeeps(self.s1long_chk)
        _evalkeeps(self.s1rad_chk)
        _evalkeeps(self.s1temp_chk)
        _evalkeeps(self.s2lat_chk)
        _evalkeeps(self.s2long_chk)
        _evalkeeps(self.s2rad_chk)
        _evalkeeps(self.s2temp_chk)
        _evalkeeps(self.a3b_chk)
        _evalkeeps(self.p3b_chk)
        _evalkeeps(self.xinc3b_chk)
        _evalkeeps(self.e3b_chk)
        _evalkeeps(self.tc3b_chk)
        _evalkeeps(self.perr3b_chk)
        _evalkeeps(self.logd_chk)
        _evalkeeps(self.desextinc_chk)
        _evalkeeps(self.l1_chk)
        _evalkeeps(self.l2_chk)
        _evalkeeps(self.x1_chk)
        _evalkeeps(self.x2_chk)
        _evalkeeps(self.el3_chk)

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
        self.EditLightCurveDialog = EditLightCurveDialog()  # get light curve edit widget
        self.EditVelocityCurveDialog = EditVelocityCurveDialog()  # get velocity curve edit widget
        self.connectSignals()  # connect signals

    def connectSignals(self):
        self.lcadd_btn.clicked.connect(partial(methods.addLightCurve, self))
        self.vc1load_btn.clicked.connect(partial(methods.loadVelocityCurve, 1, self))
        self.vc2load_btn.clicked.connect(partial(methods.loadVelocityCurve, 2, self))
        self.vc1edit_btn.clicked.connect(partial(methods.editVelocityCurve, 1, self))
        self.vc2edit_btn.clicked.connect(partial(methods.editVelocityCurve, 2, self))

    def closeEvent(self, *args, **kwargs):  # overriding QWidget's closeEvent
        self.EditLightCurveDialog.close()  # close curve edit widget if we exit
        self.EditVelocityCurveDialog.close()  # close curve edit widget if we exit


class EditLightCurveDialog(QtGui.QDialog, editlightcurvedialog.Ui_EditLightCurveDialog):
    def __init__(self):  # consturctor
        super(EditLightCurveDialog, self).__init__()
        self.setupUi(self)  # setup ui from editcurvewidget.py
        self.setWindowIcon(QtGui.QIcon("resources/pywd.ico"))  # set app icon
        self.timeList = []
        self.observationList = []
        self.weightList = []
        self.lines = []
        self.connectSignals()  # connect signals

    def connectSignals(self):
        self.accept_btn.clicked.connect(self.acceptChanges)
        self.discard_btn.clicked.connect(self.discardChanges)
        self.whatsthis_btn.clicked.connect(QtGui.QWhatsThis.enterWhatsThisMode)

    def populate(self, LightCurveProperties):  # populate ui from a lcprop obj
        self.filepath_label.setText(LightCurveProperties.FilePath)
        curve = classes.Curve(LightCurveProperties.FilePath)
        self.filepath_label.setToolTip(LightCurveProperties.FilePath)
        self.band_box.setValue(int(LightCurveProperties.band))
        self.ksd_box.setValue(int(LightCurveProperties.ksd))
        self.l1_ipt.setText(LightCurveProperties.l1)
        self.l2_ipt.setText(LightCurveProperties.l2)
        self.x1_ipt.setText(LightCurveProperties.x1)
        self.x2_ipt.setText(LightCurveProperties.x2)
        self.y1_ipt.setText(LightCurveProperties.y1)
        self.y2_ipt.setText(LightCurveProperties.y2)
        self.e1_ipt.setText(LightCurveProperties.e1)
        self.e2_ipt.setText(LightCurveProperties.e2)
        self.e3_ipt.setText(LightCurveProperties.e3)
        self.e4_ipt.setText(LightCurveProperties.e4)
        self.el3a_ipt.setText(LightCurveProperties.el3a)
        self.opsf_ipt.setText(LightCurveProperties.opsf)
        self.sigma_ipt.setText(LightCurveProperties.sigma)
        self.noise_combobox.setCurrentIndex(int(LightCurveProperties.noise))
        self.wla_ipt.setText(LightCurveProperties.wla)
        self.aextinc_ipt.setText(LightCurveProperties.aextinc)
        self.xunit_ipt.setText(LightCurveProperties.xunit)
        self.calib_ipt.setText(LightCurveProperties.calib)
        self.datawidget.clear()
        for x in curve.lines:
            a = QtGui.QTreeWidgetItem(self.datawidget, x)

    def load(self, filePath, curve):  # populate ui from a file
        self.filepath_label.setText(filePath)
        self.filepath_label.setToolTip(filePath)
        self.band_box.setValue(7)
        self.ksd_box.setValue(1)
        self.l1_ipt.setText("0")
        self.l2_ipt.setText("0")
        self.x1_ipt.setText("0")
        self.x2_ipt.setText("0")
        self.y1_ipt.setText("0")
        self.y2_ipt.setText("0")
        self.e1_ipt.setText("0")
        self.e2_ipt.setText("0")
        self.e3_ipt.setText("0")
        self.e4_ipt.setText("0")
        self.el3a_ipt.setText("0")
        self.opsf_ipt.setText("0")
        self.sigma_ipt.setText("0")
        self.noise_combobox.setCurrentIndex(1)
        self.wla_ipt.setText("0")
        self.aextinc_ipt.setText("0")
        self.xunit_ipt.setText("1.0000")
        self.calib_ipt.setText("0")
        self.datawidget.clear()
        for x in curve.lines:
            a = QtGui.QTreeWidgetItem(self.datawidget, x)

    def acceptChanges(self):
        self.done(1)

    def discardChanges(self):
        self.done(0)


class EditVelocityCurveDialog(QtGui.QDialog, editvelocitycurvedialog.Ui_EditVelocityCurveDialog):
    def __init__(self):
        super(EditVelocityCurveDialog, self).__init__()
        self.setupUi(self)  # setup ui from editcurvewidget.py
        self.timeList = []
        self.observationList = []
        self.weightList = []
        self.lines = []
        self.setWindowIcon(QtGui.QIcon("resources/pywd.ico"))  # set app icon
        self.connectSignals()

    def connectSignals(self):
        self.accept_btn.clicked.connect(self.acceptChanges)
        self.discard_btn.clicked.connect(self.discardChanges)
        self.whatsthis_btn.clicked.connect(QtGui.QWhatsThis.enterWhatsThisMode)

    def populate(self, VelocityCurveProperties):  # populate ui from a lcprop obj
        self.filepath_label.setText(VelocityCurveProperties.FilePath)
        curve = classes.Curve(VelocityCurveProperties.FilePath)
        self.filepath_label.setToolTip(VelocityCurveProperties.FilePath)
        self.band_box.setValue(int(VelocityCurveProperties.band))
        self.ksd_box.setValue(int(VelocityCurveProperties.ksd))
        self.l1_ipt.setText(VelocityCurveProperties.l1)
        self.l2_ipt.setText(VelocityCurveProperties.l2)
        self.x1_ipt.setText(VelocityCurveProperties.x1)
        self.x2_ipt.setText(VelocityCurveProperties.x2)
        self.y1_ipt.setText(VelocityCurveProperties.y1)
        self.y2_ipt.setText(VelocityCurveProperties.y2)
        self.e1_ipt.setText(VelocityCurveProperties.e1)
        self.e2_ipt.setText(VelocityCurveProperties.e2)
        self.e3_ipt.setText(VelocityCurveProperties.e3)
        self.e4_ipt.setText(VelocityCurveProperties.e4)
        self.wla_ipt.setText(VelocityCurveProperties.wla)
        self.opsf_ipt.setText(VelocityCurveProperties.opsf)
        self.sigma_ipt.setText(VelocityCurveProperties.sigma)
        self.datawidget.clear()
        for x in curve.lines:
            a = QtGui.QTreeWidgetItem(self.datawidget, x)

    def load(self, filePath, curve):
        self.filepath_label.setText(filePath)
        self.filepath_label.setToolTip(filePath)
        self.band_box.setValue(7)
        self.ksd_box.setValue(1)
        self.l1_ipt.setText("0")
        self.l2_ipt.setText("0")
        self.x1_ipt.setText("0")
        self.x2_ipt.setText("0")
        self.y1_ipt.setText("0")
        self.y2_ipt.setText("0")
        self.e1_ipt.setText("0")
        self.e2_ipt.setText("0")
        self.e3_ipt.setText("0")
        self.e4_ipt.setText("0")
        self.wla_ipt.setText("0")
        self.opsf_ipt.setText("0")
        self.sigma_ipt.setText("0")
        self.datawidget.clear()
        for x in curve.lines:
            a = QtGui.QTreeWidgetItem(self.datawidget, x)

    def acceptChanges(self):
        self.done(1)

    def discardChanges(self):
        self.done(0)


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
                methods.SaveSpotConfiguration(self, filePath)
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
                methods.LoadSpotConfiguration(self, filePath)
            except:
                msg = QtGui.QMessageBox()
                msg.setText("An error has ocurred: \n" + str(sys.exc_info()[1]))
                msg.exec_()
                methods.clearSpotConfigureWidget(self)

if __name__ == "__main__":
    pass
