from PyQt4 import QtGui, QtCore, QtOpenGL
import numpy
from matplotlib import pyplot, gridspec
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from gui import mainwindow, spotconfigurewidget, eclipsewidget, curvepropertiesdialog, \
    dcwidget, lcdcpickerdialog, outputview, loadobservationwidget, \
    syntheticcurvewidget, starpositionswidget, dimensionwidget, conjunctionwidget, \
    ocwidget, lineprofilewidget, historywidget
from functools import partial
from bin import methods, classes
from itertools import izip
import subprocess
import sys
import ConfigParser
import os
import time
import io

# globals
__cwd__ = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
__icon_path__ = os.path.join(__cwd__, "resources", "pywd.ico")
__font_path__ = os.path.join(__cwd__, "resources", "PTM55FT.ttf")


class MainWindow(QtGui.QMainWindow, mainwindow.Ui_MainWindow):  # main window class
    def __init__(self):  # constructor
        super(MainWindow, self).__init__()
        self.setupUi(self)  # setup ui from mainwindow.py
        self.setWindowIcon(QtGui.QIcon(__icon_path__))  # set app icon
        self.LoadObservationWidget = LoadObservationWidget()  # get loadwidget
        self.LoadObservationWidget.MainWindow = self
        self.SpotConfigureWidget = SpotConfigureWidget()  # get spotconfigurewidget
        self.EclipseWidget = EclipseWidget()
        self.DCWidget = DCWidget()
        self.DCWidget.MainWindow = self
        self.LCDCPickerWidget = LCDCPickerWidget()
        self.LCDCPickerWidget.MainWindow = self
        self.SyntheticCurveWidget = SyntheticCurveWidget()
        self.StarPositionWidget = StarPositionWidget()
        self.StarPositionWidget.MainWindow = self
        self.SyntheticCurveWidget.MainWindow = self
        self.DimensionWidget = DimensionWidget()
        self.DimensionWidget.MainWindow = self
        self.ConjunctionWidget = ConjunctionWidget()
        self.ConjunctionWidget.MainWindow = self
        self.OCWidget = OCWidget()
        self.OCWidget.MainWindow = self
        self.LineProfileWidget = LineProfileWidget()
        self.LineProfileWidget.MainWindow = self
        self.HistoryWidget = HistoryWidget()
        self.HistoryWidget.MainWindow = self
        # variables
        self.lcpath = None
        self.lcinpath = None
        self.lcoutpath = None
        self.lastProjectPath = None
        self.mode1Dictionary = {
            self.phsv_ipt: self.pcsv_ipt,
            self.tavh_ipt: self.tavc_ipt,
            self.gr1_spinbox: self.gr2_spinbox,
            self.alb1_spinbox: self.alb2_spinbox,
        }
        self.lcinview = None
        self.lcoutview = None
        #
        self.populateStyles()  # populate theme combobox
        self.connectSignals()  # connect events with method
        self.hideConjunctionGroup()
        self.applyConstraints()
        self.checkJdphs()

    def connectSignals(self):
        self.whatsthis_btn.clicked.connect(QtGui.QWhatsThis.enterWhatsThisMode)
        self.loadwidget_btn.clicked.connect(self.LoadObservationWidget.show)
        self.spotconfigure_btn.clicked.connect(self.SpotConfigureWidget.show)
        self.dc_rundc_btn.clicked.connect(partial(self.DCWidget.show))
        self.theme_combobox.currentIndexChanged.connect(self.changeStyle)
        self.eclipsewidget_btn.clicked.connect(self.EclipseWidget.show)
        self.saveproject_btn.clicked.connect(self.overwriteProject)
        self.loadproject_btn.clicked.connect(self.loadProjectDialog)
        self.saveas_btn.clicked.connect(self.saveProjectDialog)
        self.fill_btn.clicked.connect(self.fillLcHJDMenu)
        self.lc_lightcurve_btn.clicked.connect(self.SyntheticCurveWidget.show)
        self.lc_coordinates_btn.clicked.connect(self.StarPositionWidget.show)
        self.conj_btn.clicked.connect(self.showConjunctionGroup)
        self.compute_btn.clicked.connect(self.updateConjunctionPhases)
        self.inputtabwidget.currentChanged.connect(self.hideConjunctionGroup)
        self.maintabwidget.currentChanged.connect(self.hideConjunctionGroup)
        self.mode_combobox.currentIndexChanged.connect(self.applyConstraints)
        self.phsv_ipt.textChanged.connect(self.updateInputPairs)
        self.tavh_ipt.textChanged.connect(self.updateInputPairs)
        self.gr1_spinbox.valueChanged.connect(self.updateInputPairs)
        self.alb1_spinbox.valueChanged.connect(self.updateInputPairs)
        self.ipb_chk.stateChanged.connect(self.checkIPB)
        self.ld1_chk.stateChanged.connect(self.checkLD1LD2)
        self.ld2_chk.stateChanged.connect(self.checkLD1LD2)
        self.e_ipt.textChanged.connect(self.updatePotentials)
        self.rm_ipt.textChanged.connect(self.updatePotentials)
        self.jdphs_combobox.currentIndexChanged.connect(self.checkJdphs)
        self.lc_stardimphase_btn.clicked.connect(self.DimensionWidget.show)
        self.lc_conjunction_btn.clicked.connect(self.ConjunctionWidget.show)
        self.lc_oc_btn.clicked.connect(self.OCWidget.show)
        self.tool_radii_to_pot_btn.clicked.connect(self.computeOmega)
        self.tool_bv_calc_btn.clicked.connect(self.bvTempCalibration)
        self.tool_jhk_calc_btn.clicked.connect(self.jhkTempCalibration)
        self.tool_jd_convert_btn.clicked.connect(self.fromJDtoUTConvert)
        self.tool_month_spinbox.valueChanged.connect(self.checkMonthMaxLimit)
        self.tool_year_spinbox.valueChanged.connect(self.checkMonthMaxLimit)
        self.tool_date_convert_btn.clicked.connect(self.fromUTtoJDConvert)
        self.lc_speclineprof_btn.clicked.connect(self.LineProfileWidget.show)
        self.dchistory_btn.clicked.connect(self.HistoryWidget.show)

    def closeEvent(self, *args, **kwargs):  # overriding QMainWindow's closeEvent
        self.LoadObservationWidget.close()
        self.SpotConfigureWidget.close()
        self.EclipseWidget.close()
        self.DCWidget.close()
        self.SyntheticCurveWidget.close()
        self.StarPositionWidget.close()
        self.DimensionWidget.close()
        self.ConjunctionWidget.close()
        self.OCWidget.close()
        self.LineProfileWidget.close()
        self.HistoryWidget.close()

    def fromUTtoJDConvert(self):
        year = self.tool_year_spinbox.value()
        month = self.tool_month_spinbox.value()
        day = self.tool_day_spinbox.value()
        hour = self.tool_hour_spinbox.value()
        minute = self.tool_minute_spinbox.value()
        second = self.tool_second_spinbox.value()

        jd = 367.0 * year - int(7.0 * (year + int((month + 9.0) / 12.0)) / 4.0) + int(275.0 * month / 9.0) - \
             int(3.0 * ((year + (month - 9.0) / 7.0) / 100.0 + 1.0) / 4.0) + 1721028.5 + day + hour / 24.0 + \
             minute / 1440.0 + second / 86400.0

        self.tool_jd_output.setText(str(jd))

    def checkMonthMaxLimit(self):
        limit_dict = {
            1: 31,
            3: 31,
            4: 30,
            5: 31,
            6: 30,
            7: 31,
            8: 31,
            9: 30,
            10: 31,
            11: 30,
            12: 31
        }

        month = self.tool_month_spinbox.value()
        year = self.tool_year_spinbox.value()

        if month == 2:
            quotient, remainder = divmod(year, 4)
            if remainder == 0:
                self.tool_day_spinbox.setMaximum(29)

            quotient, remainder = divmod(year, 100)
            if remainder == 0:
                self.tool_day_spinbox.setMaximum(28)
                quotient, remainder = divmod(year, 400)
                if remainder == 0:
                    self.tool_day_spinbox.setMaximum(29)
        else:
            self.tool_day_spinbox.setMaximum(limit_dict[month])

    def computeOmega(self):
        self.tool_pot_output.setText(str(methods.computeOmegaPotential(self.tool_q_spinbox.value(),
                                                                       self.tool_fractradii_spinbox.value(),
                                                                       self.tool_f_spinbox.value(),
                                                                       self.tool_d_spinbox.value())))

    def bvTempCalibration(self):
        bv = self.tool_bv_spinbox.value()
        bv_err = self.tool_bv_err_spinbox.value()

        gray_calibrator = classes.ColorCalibrator("gray")
        flower_calibrator = classes.ColorCalibrator("flower")
        drilling_landold_calibrator = classes.ColorCalibrator("drilling_landolt")
        popper_calibrator = classes.ColorCalibrator("popper")

        gray, gray_err = gray_calibrator.calibrate(bv, bv_err)
        flower, flower_err = flower_calibrator.calibrate(bv, bv_err)
        d_l, d_l_err = drilling_landold_calibrator.calibrate(bv, bv_err)
        popper, popper_err = popper_calibrator.calibrate(bv, bv_err)

        self.tool_gray_output.setText(str(gray))
        self.tool_gray_err_output.setText(str(gray_err))

        self.tool_flower_output.setText(str(flower))
        self.tool_flower_err_output.setText(str(flower_err))

        self.tool_drilling_landolt_output.setText(str(d_l))
        self.tool_drilling_landolt_err_output.setText(str(d_l_err))

        self.tool_popper_output.setText(str(popper))
        self.tool_popper_err_output.setText(str(popper_err))

    def jhkTempCalibration(self):
        tokunaga_dict = {
            "V - K": "tokunaga_vk",
            "J - H": "tokunaga_jh",
            "H - K": "tokunaga_hk",
        }

        tokunaga_calibrator = classes.ColorCalibrator(tokunaga_dict[str(self.tool_jhk_combobox.currentText())])
        clr = self.tool_jhk_spinbox.value()
        err = self.tool_jhk_err_spinobx.value()
        tokunaga, tokunaga_err = tokunaga_calibrator.calibrate(clr, err)

        self.tool_tokunaga_output.setText(str(tokunaga))
        self.tool_tokunaga_err_output.setText(str(tokunaga_err))

    def fromJDtoUTConvert(self):
        year, month, day, hour, minute, second = methods.convertJDtoUT(self.tool_jd_spinbox.value(), dontAdd24=True)
        ut = "{2}/{1}/{0} - {3}:{4}:{5:4.2f}".format(year, month, day, hour, minute, second)
        self.tool_date_output.setText(ut)

    def checkJdphs(self):
        jdphs = str(self.jdphs_combobox.currentText())
        self.pshift_ipt.setDisabled(False)
        self.DCWidget.pshift_chk.setDisabled(False)
        self.DCWidget.jd0_chk.setDisabled(False)
        if jdphs == "Time":
            self.pshift_ipt.setDisabled(True)
            self.pshift_ipt.setText("0")
            self.DCWidget.pshift_chk.setDisabled(True)
            self.DCWidget.pshift_chk.setChecked(False)
        elif jdphs == "Phase":
            self.DCWidget.jd0_chk.setDisabled(True)
            self.DCWidget.jd0_chk.setChecked(False)

    def updateInputPairs(self):
        sender = self.sender()
        if str(self.mode_combobox.currentText()) == "Mode 1":
            if str(type(sender)) == "<class 'PyQt4.QtGui.QLineEdit'>":
                self.mode1Dictionary[sender].setText(sender.text())
            else:
                self.mode1Dictionary[sender].setValue(sender.value())

        if str(self.mode_combobox.currentText()) == "Mode 3":
            if str(sender.objectName()) == "phsv_ipt":
                self.pcsv_ipt.setText(self.phsv_ipt.text())

    def applyConstraints(self):
        self.clearConstraints()
        if str(self.mode_combobox.currentText()) == "Mode -1":
            self.pcsv_ipt.setDisabled(True)
            self.pcsv_ipt.setText(self.phsv_ipt.text())
            self.DCWidget.pot2_chk.setDisabled(True)
            self.DCWidget.pot2_chk.setChecked(False)

        if str(self.mode_combobox.currentText()) == "Mode 0":
            self.ipb_chk.setChecked(True)
            self.ipb_chk.setDisabled(True)

        if str(self.mode_combobox.currentText()) == "Mode 1":
            # Curve independent params
            self.pcsv_ipt.setText(self.phsv_ipt.text())
            self.tavc_ipt.setText(self.tavh_ipt.text())
            self.gr2_spinbox.setValue(self.gr1_spinbox.value())
            self.alb2_spinbox.setValue(self.alb1_spinbox.value())

            self.pcsv_ipt.setDisabled(True)
            self.DCWidget.pot2_chk.setDisabled(True)
            self.DCWidget.pot2_chk.setChecked(False)

            self.tavc_ipt.setDisabled(True)
            self.DCWidget.t2_chk.setDisabled(True)
            self.DCWidget.t2_chk.setChecked(False)

            self.gr2_spinbox.setDisabled(True)
            self.DCWidget.g2_chk.setDisabled(True)
            self.DCWidget.g2_chk.setChecked(False)

            self.alb2_spinbox.setDisabled(True)
            self.DCWidget.alb2_chk.setDisabled(True)
            self.DCWidget.alb2_chk.setChecked(False)

            # Curve dependent params
            if self.ipb_chk.isChecked() is not True:
                self.DCWidget.l2_chk.setDisabled(True)
                self.DCWidget.l2_chk.setChecked(False)
                if self.ld1_chk.isChecked() and self.ld2_chk.isChecked():
                    for curve in self.LoadObservationWidget.lcPropertiesList:
                        curve.x2 = curve.x1
                        curve.y2 = curve.y1
            self.DCWidget.x2_chk.setDisabled(True)
            self.DCWidget.x2_chk.setChecked(False)

        if str(self.mode_combobox.currentText()) == "Mode 3":
            self.pcsv_ipt.setText(self.phsv_ipt.text())
            self.pcsv_ipt.setDisabled(True)
            self.DCWidget.pot2_chk.setDisabled(True)
            self.DCWidget.pot2_chk.setChecked(False)

        if str(self.mode_combobox.currentText()) == "Mode 4":
            self.updatePotentials()
            self.phsv_ipt.setDisabled(True)
            self.DCWidget.pot1_chk.setDisabled(True)
            self.DCWidget.pot1_chk.setChecked(False)

        if str(self.mode_combobox.currentText()) == "Mode 5":
            self.updatePotentials()
            self.pcsv_ipt.setDisabled(True)
            self.DCWidget.pot2_chk.setDisabled(True)
            self.DCWidget.pot2_chk.setChecked(False)

        if str(self.mode_combobox.currentText()) == "Mode 6":
            self.updatePotentials()
            self.phsv_ipt.setDisabled(True)
            self.pcsv_ipt.setDisabled(True)
            self.DCWidget.pot1_chk.setDisabled(True)
            self.DCWidget.pot2_chk.setDisabled(True)
            self.DCWidget.pot1_chk.setChecked(False)
            self.DCWidget.pot2_chk.setChecked(False)

        self.checkLD1LD2()

    def clearConstraints(self):
        self.phsv_ipt.setDisabled(False)
        self.pcsv_ipt.setDisabled(False)
        self.DCWidget.pot1_chk.setDisabled(False)
        self.DCWidget.pot2_chk.setDisabled(False)

        self.tavc_ipt.setDisabled(False)
        self.DCWidget.t2_chk.setDisabled(False)

        self.gr2_spinbox.setDisabled(False)
        self.DCWidget.g2_chk.setDisabled(False)

        self.alb2_spinbox.setDisabled(False)
        self.DCWidget.alb2_chk.setDisabled(False)

        self.DCWidget.x1_chk.setDisabled(False)
        self.DCWidget.x2_chk.setDisabled(False)
        self.DCWidget.l2_chk.setDisabled(False)

        self.ipb_chk.setDisabled(False)

        self.checkIPB()

    def checkLD1LD2(self):
        self.DCWidget.x1_chk.setDisabled(False)
        self.DCWidget.x2_chk.setDisabled(False)

        if self.ld1_chk.isChecked() is not True:
            self.DCWidget.x1_chk.setDisabled(True)
            self.DCWidget.x1_chk.setChecked(False)

        if self.ld2_chk.isChecked() is not True:
            self.DCWidget.x2_chk.setDisabled(True)
            self.DCWidget.x2_chk.setChecked(False)

        if str(self.mode_combobox.currentText()) == "Mode 1":
            if self.ld1_chk.isChecked() and self.ld2_chk.isChecked():
                for curve in self.LoadObservationWidget.lcPropertiesList:
                    curve.x2 = curve.x1
                    curve.y2 = curve.y1
                self.DCWidget.x2_chk.setDisabled(True)

    def checkIPB(self):
        if self.ipb_chk.isChecked():
            self.DCWidget.l2_chk.setDisabled(False)
        else:
            self.DCWidget.l2_chk.setDisabled(True)
            self.DCWidget.l2_chk.setChecked(False)

    def updatePotentials(self):
        inner_potential = "N/A"
        hadError = False
        try:
            float(self.e_ipt.text())
            float(self.rm_ipt.text())
        except ValueError:
            hadError = True
        if hadError is not True and float(str(self.rm_ipt.text())) != 0.0 and float(str(self.e_ipt.text())) < 1.0:
            inner_potential, outer_potential = methods.computeRochePotentials(
                self,
                methods.computeConjunctionPhases(self)[4],
                None,
                getPotentials=True)
            inner_potential = str(float(inner_potential))

        if str(self.mode_combobox.currentText()) == "Mode 4":
            self.phsv_ipt.setText(inner_potential)
        if str(self.mode_combobox.currentText()) == "Mode 5":
            self.pcsv_ipt.setText(inner_potential)
        if str(self.mode_combobox.currentText()) == "Mode 6":
            self.phsv_ipt.setText(inner_potential)
            self.pcsv_ipt.setText(inner_potential)

    def showConjunctionGroup(self):
        self.conjunction_groupbox.show()
        self.setMaximumSize(1090, 345)
        self.setMinimumSize(1090, 345)
        self.whatsthis_btn.setGeometry(
            1040,
            self.whatsthis_btn.y(),
            self.whatsthis_btn.width(),
            self.whatsthis_btn.height())
        self.conj_btn.clicked.disconnect()
        self.conj_btn.clicked.connect(self.hideConjunctionGroup)

    def hideConjunctionGroup(self):
        self.conjunction_groupbox.hide()
        self.setMaximumSize(850, 345)
        self.setMinimumSize(850, 345)
        self.whatsthis_btn.setGeometry(
            800,
            self.whatsthis_btn.y(),
            self.whatsthis_btn.width(),
            self.whatsthis_btn.height())
        self.conj_btn.clicked.disconnect()
        self.conj_btn.clicked.connect(self.showConjunctionGroup)

    def updateConjunctionPhases(self):
        phase_of_primary_eclipse, \
        phase_of_first_quadrature, \
        phase_of_secondary_eclipse, \
        phase_of_second_quadrature, \
        phase_of_periastron, \
        phase_of_apastron = methods.computeConjunctionPhases(self)

        self.primaryeclipse_label.setText(": " + "{:0.4f}".format(phase_of_primary_eclipse))
        self.firstquadrature_label.setText(": " + "{:0.4f}".format(phase_of_first_quadrature))
        self.secondaryeclipse_label.setText(": " + "{:0.4f}".format(phase_of_secondary_eclipse))
        self.secondquadrature_label.setText(": " + "{:0.4f}".format(phase_of_second_quadrature))
        if float(self.e_ipt.text()) == 0.0:
            self.periastron_label.setText(": N/A")
            self.apastron_label.setText(": N/A")
        else:
            self.periastron_label.setText(": " + "{:0.4f}".format(phase_of_periastron))
            self.apastron_label.setText(": " + "{:0.4f}".format(phase_of_apastron))

    def setPaths(self, lcpath, dcpath):
        self.lcpath = lcpath
        self.lcinpath = os.path.join(os.path.dirname(lcpath), "lcin.active")
        self.lcoutpath = os.path.join(os.path.dirname(lcpath), "lcout.active")
        self.DCWidget.dcpath = dcpath
        self.DCWidget.dcinpath = os.path.join(os.path.dirname(dcpath), "dcin.active")
        self.DCWidget.dcoutpath = os.path.join(os.path.dirname(dcpath), "dcout.active")

        # setup outputviews
        self.lcinview = OutputView(self.lcinpath, self.lcin_btn)
        self.lcoutview = OutputView(self.lcoutpath, self.lcout_btn)
        self.DCWidget.DcinView = OutputView(self.DCWidget.dcinpath, self.DCWidget.viewlastdcin_btn)
        self.DCWidget.DcoutView = OutputView(self.DCWidget.dcoutpath, self.DCWidget.viewlaastdcout_btn)

    def clearWidgets(self):
        self.DCWidget.data_combobox.clear()
        self.DCWidget.plot_observationAxis.cla()
        self.DCWidget.plot_residualAxis.cla()

        self.SyntheticCurveWidget.plot_observationAxis.cla()
        self.SyntheticCurveWidget.plot_residualAxis.cla()
        self.SyntheticCurveWidget.plot_starposAxis.cla()

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
        self.DCWidget.residualTable = None
        self.DCWidget.firstComponentTable = None
        self.DCWidget.secondComponentTable = None
        self.DCWidget.curvestat_treewidget.clear()

        self.StarPositionWidget.plot_starPositionAxis.cla()
        self.StarPositionWidget.starRenderData = None
        self.StarPositionWidget.starsRendered = False

        self.updateConjunctionPhases()

        self.DimensionWidget.s1_plotAxis.cla()
        self.DimensionWidget.s2_plotAxis.cla()

        self.DimensionWidget.s1_pole = None
        self.DimensionWidget.s1_point = None
        self.DimensionWidget.s1_side = None
        self.DimensionWidget.s1_back = None
        self.DimensionWidget.s2_pole = None
        self.DimensionWidget.s2_point = None
        self.DimensionWidget.s2_side = None
        self.DimensionWidget.s2_back = None
        self.DimensionWidget.x = None

        self.DimensionWidget.s1_plot_canvas.draw()
        self.DimensionWidget.s1_plot_toolbar.update()
        self.DimensionWidget.s2_plot_canvas.draw()
        self.DimensionWidget.s2_plot_toolbar.update()

        self.ConjunctionWidget.data_treewidget.clear()
        self.ConjunctionWidget.data = None
        self.ConjunctionWidget.ut_data = []

        self.OCWidget.data_treewidget.clear()
        self.OCWidget.hjd = None
        self.OCWidget.linear = None
        self.OCWidget.dpdt = None
        self.OCWidget.plotAxis.clear()
        self.OCWidget.plotAxis.set_xlabel("HJD")
        self.OCWidget.plotAxis.set_ylabel("Day")
        self.OCWidget.plot_canvas.draw()
        self.OCWidget.plot_toolbar.update()

        self.LineProfileWidget.s1_data = None
        self.LineProfileWidget.s2_data = None
        self.LineProfileWidget.plotAxis.cla()
        self.LineProfileWidget.plotAxis.set_xlabel("Micron")
        self.LineProfileWidget.plotAxis.set_ylabel("Flux")
        self.LineProfileWidget.plot_canvas.draw()
        self.LineProfileWidget.plot_toolbar.update()

        self.HistoryWidget.clearHistory()

    def begin(self):  # check for wd.conf
        wdconf = os.path.join(__cwd__, "wd.conf")
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
                    self.jdincrement_ipt.setText(str(float(self.p0_ipt.text()) / 1000.0))
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
                    self.updatePotentials()
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
        font = self.font()
        styleFactory = QtGui.QStyleFactory()
        style = styleFactory.create(self.theme_combobox.currentText())
        self.app.setStyle(style)
        self.app.setFont(font)


class LCDCPickerWidget(QtGui.QDialog, lcdcpickerdialog.Ui_LCDCPickerDialog):
    def __init__(self):
        super(LCDCPickerWidget, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(__icon_path__))
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
        self.setWindowIcon(QtGui.QIcon(__icon_path__))
        self.connectSignals()

    def connectSignals(self):
        self.load_btn.clicked.connect(partial(methods.loadEclipseTimings, self))
        self.clear_btn.clicked.connect(partial(methods.removeEclipseTimings, self))


class LoadObservationWidget(QtGui.QWidget, loadobservationwidget.Ui_ObservationWidget):
    def __init__(self):
        super(LoadObservationWidget, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(__icon_path__))
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

    def loadCurveDialog(self, crv_type, vcNumber):
        dialog = QtGui.QFileDialog(self)
        dialog.setAcceptMode(0)
        returnCode = dialog.exec_()
        filePath = (dialog.selectedFiles())[0]
        if filePath != "" and returnCode != 0:
            try:
                curvedialog = CurvePropertiesDialog.createCurveDialog(crv_type, self.MainWindow)
                curvedialog.populateFromFile(filePath)
                if curvedialog.hasError:
                    pass
                else:
                    result = curvedialog.exec_()
                    if result == 1:
                        curveprop = classes.CurveProperties(crv_type)
                        curveprop.populateFromInterface(curvedialog)
                        if crv_type == "lc":
                            self.lcPropertiesList.append(curveprop)
                        if crv_type == "vc":
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
                curvedialog = CurvePropertiesDialog.createCurveDialog("vc", self.MainWindow)
                curvedialog.populateFromObject(self.vcPropertiesList[0])
            if item.text(1) == "Velocity Curve (#2)":
                curvedialog = CurvePropertiesDialog.createCurveDialog("vc", self.MainWindow)
                curvedialog.populateFromObject(self.vcPropertiesList[1])
            if item.text(1) == "Light Curve":
                curvedialog = CurvePropertiesDialog.createCurveDialog("lc", self.MainWindow)
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
            pyplot.plot(x, y, linestyle="", marker="o", markersize=4, color="#4286f4")
            pyplot.title(item.text(0))
            pyplot.get_current_fig_manager().set_window_title("Matplotlib - " + item.text(0))
            if str(self.MainWindow.maglite_combobox.currentText()) == "Magnitude" and str(item.text(1)) == "Light Curve":
                pyplot.gca().invert_yaxis()
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
    def __init__(self, MainWindow):
        super(CurvePropertiesDialog, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(__icon_path__))
        self.type = ""
        self.synthetic = False
        self.hasError = False
        self.MainWindow = MainWindow
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
            "Sloan DSS u'": "56",
            "Sloan DSS g'": "57",
            "Sloan DSS r'": "58",
            "Sloan DSS i'": "59",
            "Sloan DSS z'": "60",
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
        self.applyConstraints()

    def connectSignals(self):
        self.accept_btn.clicked.connect(partial(self.done, 1))
        self.discard_btn.clicked.connect(partial(self.done, 2))
        self.whatsthis_btn.clicked.connect(QtGui.QWhatsThis.enterWhatsThisMode)
        self.repick_btn.clicked.connect(self.repick)
        # this gets fired when we right click
        self.bandpasscontextlist_btn.customContextMenuRequested.connect(self.openBandpassContextMenu)
        self.bandpasscontextlist_btn.clicked.connect(self.openBandpassContextMenu)

    def applyConstraints(self):
        if self.MainWindow is not None:
            if self.MainWindow.ld1_chk.isChecked() is not True:
                self.x1_ipt.setDisabled(True)
                self.y1_ipt.setDisabled(True)
            if self.MainWindow.ld2_chk.isChecked() is not True:
                self.x2_ipt.setDisabled(True)
                self.y2_ipt.setDisabled(True)
            if self.MainWindow.ipb_chk.isChecked() is not True:
                self.l2_ipt.setDisabled(True)
            if str(self.MainWindow.mode_combobox.currentText()) == "Mode 1":
                if self.MainWindow.ld1_chk.isChecked() and self.MainWindow.ld2_chk.isChecked():
                    self.x2_ipt.setDisabled(True)
                    self.y2_ipt.setDisabled(True)

                    def _lockx2y2():
                        self.x2_ipt.setText(self.x1_ipt.text())
                        self.y2_ipt.setText(self.y1_ipt.text())

                    self.x1_ipt.textChanged.connect(_lockx2y2)
                    self.y1_ipt.textChanged.connect(_lockx2y2)

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
        sloandds = rootmenu.addMenu("Sloan DSS")
        sdu = sloandds.addAction("u'")
        sdu.setObjectName("Sloan DSS u'")
        sdg = sloandds.addAction("g'")
        sdg.setObjectName("Sloan DSS g'")
        sdr = sloandds.addAction("r'")
        sdr.setObjectName("Sloan DSS r'")
        sdi = sloandds.addAction("i'")
        sdi.setObjectName("Sloan DSS i'")
        sdz = sloandds.addAction("z'")
        sdz.setObjectName("Sloan DSS z'")

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
    def createCurveDialog(type, MainWindow, synthetic=False):
        curvedialog = CurvePropertiesDialog(MainWindow)
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
        self.setWindowIcon(QtGui.QIcon(__icon_path__))  # set app icon
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
        self.setWindowIcon(QtGui.QIcon(__icon_path__))
        self.result_treewidget.header().setResizeMode(3)
        self.residual_treewidget.header().setResizeMode(3)
        self.component_treewidget.header().setResizeMode(3)
        self.curvestat_treewidget.header().setResizeMode(3)
        # variables
        self.dcpath = None
        self.dcinpath = None
        self.dcoutpath = None
        self.MainWindow = None  # mainwindow sets itself here
        self.DcinView = None
        self.DcoutView = None
        self.iterator = None
        self.axisInverted = False
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
            "25": "q (M2/M1)",
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
        self.latexDict = {
            "1": "$Co-Latitude_{Spot1}$ $(^{\circ})$",
            "2": "$Longitude_{Spot1}$ $(^{\circ})$",
            "3": "$Radius_{Spot1}$ $(^{\circ})$",
            "4": "$Temperature~Factor_{Spot1}$",
            "5": "$Co-Latitude_{Spot2}$ $(^{\circ})$",
            "6": "$Longitude_{Spot2}$ $(^{\circ})$",
            "7": "$Radius_{Spot2}$ $(^{\circ})$",
            "8": "$Temperature~Factor_{Spot2}$",
            "9": "$a$~({\mbox{$R_{\odot}$}})",
            "10": "$e$",
            "11": "$\omega~(^{\circ})$",
            "12": "$F_{1}$",
            "13": "$F_{2}$",
            "14": "$Phase~Shift$",
            "15": "$V_{\gamma}$",
            "16": "$i~(^{\circ})$",
            "17": "$g_{1}$",
            "18": "$g_{2}$",
            "19": "$T_{1}(K)$",
            "20": "$T_{2}(K)$",
            "21": "$A_{{1}}$",
            "22": "$A_{{2}}$",
            "23": "$\Omega_{1}$",
            "24": "$\Omega_{2}$",
            "25": "$q~(=M{_2}/M{_1})$",
            "26": "$HJD_{Min1}$",
            "27": "$Period$",
            "28": "$dP/dt$",
            "29": "$d\omega/dt$",
            "30": "$a$ ({\mbox{$R_{\odot}$}}) (3B)$",
            "31": "$P~(3B)$",
            "32": "$i~(3B)~(^{\circ})$",
            "33": "$e~(3B)$",
            "34": "$\omega~(3B)$",
            "35": "$Ephemeris~(3B)$",
            "41": "$log(d)$",
            "42": "$Designated~Extinction$",
            "43": "nan",
            "44": "nan",
            "45": "nan",
            "46": "nan",
            "47": "nan",
            "48": "nan",
            "49": "nan",
            "50": "nan",
            "56": "$L_{{1}}$/$(L_{{1}}+L_{{2}})_{{{band}}}$",
            "57": "nan",
            "58": "$x{{_1}}_{{{band}}}$",
            "59": "$x{{_2}}_{{{band}}}$",
            "60": "$L_{{3}}$/$(L_{{1}}+L_{{2}}+L_{{3}})_{{{band}}}$"
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
            "56": "Sloan DSS u'",
            "57": "Sloan DSS g'",
            "58": "Sloan DSS r'",
            "59": "Sloan DSS i'",
            "60": "Sloan DSS z'",
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
        self.residualTable = None
        self.firstComponentTable = None
        self.secondComponentTable = None
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
        self.plot_btn.clicked.connect(self.plotData)
        self.popmain_btn.clicked.connect(self.popPlotWindow)
        self.exportresults_btn.clicked.connect(self.exportData)

    def closeEvent(self, *args, **kwargs):
        try:
            self.iterator.exit()
        except:
            pass

        self.DcinView.close()
        self.DcoutView.close()

    def exportData(self):
        if self.lastBaseSet is not None:
            menu = QtGui.QMenu(self)
            plaintext = menu.addAction("Plaintext")
            plaintext.setObjectName("plaintext")
            latex = menu.addAction("Latex")
            latex.setObjectName("latex")
            selection = menu.exec_(QtGui.QCursor.pos())

            if selection is not None:
                dialog = QtGui.QFileDialog(self)
                dialog.setDefaultSuffix("txt")
                dialog.setNameFilter("Plaintext File (*.txt)")
                dialog.setAcceptMode(1)
                returnCode = dialog.exec_()
                filePath = str((dialog.selectedFiles())[0])

                if filePath != "" and returnCode != 0:
                    msg = QtGui.QMessageBox()
                    fi = QtCore.QFileInfo(filePath)

                    try:
                        with open(filePath, "w") as f:
                            if selection.objectName() == "plaintext":
                                f.write("#Parameter                         #Value                             #Sigma\n")
                            if selection.objectName() == "latex":
                                f.write("\\begin{table}\n\\begin{center}\n\\begin{tabular}{c|c}\n")
                                f.write("Parameter & Value" + "\\" + "\\" + "\n")
                                f.write("\hline")

                            table = methods.getTableFromOutput(self.dcoutpath, "Input-Output in D Format", occurence=int(self.niter_spinbox.value()))

                            for result in table:

                                output = methods.convertFromScientificToGeneric(result[2].replace("D", "e"))
                                stderr = methods.convertFromScientificToGeneric(result[5].replace("D", "e"))

                                if result[0] in ("19", "20"):
                                    output = str(int(float(output) * 10000.0))
                                    stderr = str(int(float(stderr) * 10000.0))

                                if result[0] == "15":
                                    output = str(float(output) * float(str(self.MainWindow.vunit_ipt.text())))
                                    stderr = str(float(stderr) * float(str(self.MainWindow.vunit_ipt.text())))

                                if self.parameterDict[result[0]] == "L1":
                                    output = methods.convertFromScientificToGeneric(result[-2].replace("D", "e"))
                                    stderr = methods.convertFromScientificToGeneric(result[-1].replace("D", "e"))

                                if selection.objectName() == "plaintext":
                                    name = self.parameterDict[result[0]]
                                    if result[1] != "0":
                                        band = self.bandpassDict[self.MainWindow.LoadObservationWidget.lcPropertiesList[int(result[1]) - 1].band]
                                        name = name + " (" + band + ")"
                                    f.write(name + (" " * (35 - len(name))) + output + (" " * (35 - len(output))) + stderr + "\n")

                                if selection.objectName() == "latex":
                                    name = self.latexDict[result[0]]
                                    if name != "nan":
                                        if result[0] in ("1", "2", "3", "5", "6", "7", "11"):
                                            output = str(float(output) * 180.0 / numpy.pi)
                                            stderr = str(float(stderr) * 180.0 / numpy.pi)
                                        if result[1] != "0":
                                            band = self.bandpassDict[self.MainWindow.LoadObservationWidget.lcPropertiesList[int(result[1]) - 1].band]
                                            name = name.format(band=band.replace(" ", "~"))
                                        if result[0] == "23" and self.MainWindow.mode_combobox.currentText() in ("Mode 1", "Mode 3"):
                                            name = "$\Omega_{1}$ = $\Omega_{2}$"
                                        f.write(name + " & " + output + " $\pm$ " + stderr + " \\" + "\\" + "\n")

                            f.write("\n")
                            mean_radii = [1.0, 1.0]
                            mean_radii_err = [1.0, 1.0]
                            for i, component in enumerate((self.firstComponentTable, self.secondComponentTable)):
                                for result in component:
                                    if selection.objectName() == "plaintext":
                                        value = "r" + str(i + 1) + "_" + result[1]
                                        f.write(value + (" " * (12 - len(value))) + result[2] + "   " + result[5] + "\n")
                                    elif selection.objectName() == "latex":
                                        value = "$r_{" + str(i + 1) + "~" + result[1] + "}$"
                                        f.write(value + " & " + result[2] + " $\pm$ " + result[5] + " \\" + "\\" + "\n")
                                    mean_radii[i] = float(result[2]) * mean_radii[i]
                                    mean_radii_err[i] = float(result[5]) * mean_radii_err[i]

                            mean_radii[0] = numpy.power(mean_radii[0], 1.0 / len(self.firstComponentTable))
                            mean_radii[1] = numpy.power(mean_radii[1], 1.0 / len(self.secondComponentTable))
                            mean_radii_err[0] = numpy.power(mean_radii_err[0], 1.0 / len(self.firstComponentTable))
                            mean_radii_err[1] = numpy.power(mean_radii_err[1], 1.0 / len(self.secondComponentTable))

                            if selection.objectName() == "plaintext":
                                f.write("r1 mean" + (" " * (12 - len(str(mean_radii[0])))) + str(mean_radii[0]) + (" " * (12 - len(str(mean_radii_err[0])))) + str(mean_radii_err[0]) + "\n")
                                f.write("r2 mean" + (" " * (12 - len(str(mean_radii[1])))) + str(mean_radii[1]) + (" " * (12 - len(str(mean_radii_err[1])))) + str(mean_radii_err[1]) + "\n")

                                f.write("\n#Mean Residual for Input Values\n" + methods.convertFromScientificToGeneric(
                                    self.residualTable[0].replace("D", "e")))

                            elif selection.objectName() == "latex":
                                f.write("$r_{1~mean}$ & " + str(mean_radii[0]) + " $\pm$ " +
                                        methods.convertFromScientificToGeneric(str(mean_radii_err[0])) + "\\" + "\\" + "\n")
                                f.write("$r_{2~mean}$ & " + str(mean_radii[1]) + " $\pm$ " +
                                        methods.convertFromScientificToGeneric(str(mean_radii_err[1])) + "\\" + "\\" + "\n")

                                f.write("\n$Mean~residual~for~input~values$ & " + methods.convertFromScientificToGeneric(
                                    self.residualTable[0].replace("D", "e")) + "\\" + "\\" + "\n")
                                f.write("\\end{tabular}\n\\end{center}\n\\end{table}")

                        msg.setText("Result data file \"" + fi.fileName() + "\" saved.")
                        msg.setWindowTitle("PyWD - Data Saved")
                        msg.exec_()

                    except:
                        msg.setText("An error has ocurred: \n" + str(sys.exc_info()[1]))
                        msg.exec_()

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
        if self.MainWindow.LoadObservationWidget.vcPropertiesList[0] != 0 and self.MainWindow.LoadObservationWidget.vcPropertiesList[1] != 0:
            self.data_combobox.addItem("Vr1 + Vr2")
        if self.MainWindow.EclipseWidget.iftime_chk.isChecked() and os.path.isfile(str(self.MainWindow.EclipseWidget.filepath_label.text())):
            self.data_combobox.addItem("O - C")

    def plotData(self):
        # TODO this is becoming messy. clean up before doing anything else.
        magnitude = False
        if str(self.data_combobox.currentText()) == "Vr1 + Vr2":
            self.plot_observationAxis.cla()
            self.plot_residualAxis.cla()
            if self.plot_observationAxis.yaxis_inverted() == True:
                self.plot_observationAxis.invert_yaxis()
            if self.plot_residualAxis.yaxis_inverted() == True:
                self.plot_residualAxis.invert_yaxis()

            ocTable = methods.getTableFromOutput(self.dcoutpath, "Unweighted Observational Equations")
            curvestatTable = methods.getTableFromOutput(
                self.dcoutpath,
                "Standard Deviations for Computation of Curve-dependent Weights")
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
            obsIndex = 1
            if self.MainWindow.jdphs_combobox.currentText() == "Time":  # wd outputs are in HJD
                obsIndex = 2
            timeIndex = 0
            if self.time_combobox.currentText() == "Phase" and self.MainWindow.jdphs_combobox.currentText() == "Time":
                timeIndex = 1
            vr1_nobsStart = None
            vr1_nobsEnd = -1
            vr2_nobsStart = None
            vr2_nobsEnd = None
            vr1_table = None
            vr2_table = None
            if self.MainWindow.LoadObservationWidget.vcPropertiesList[0] != 0:
                vr1_nobsStart = 0
                vr1_nobsEnd = vr1_nobsStart + int(curvestatTable[0][1])
                vr1_table = ocTable[vr1_nobsStart:vr1_nobsEnd]
            if self.MainWindow.LoadObservationWidget.vcPropertiesList[1] != 0:
                vr2_nobsStart = vr1_nobsEnd
                vr2_nobsEnd = vr2_nobsStart + int(curvestatTable[1][1])
                vr2_table = ocTable[vr2_nobsStart:vr2_nobsEnd]

            if vr1_table is not None or vr2_table is not None:
                obs_vr1 = None
                obs_vr2 = None
                resd_vr1 = None
                resd_vr2 = None
                x_axis_vr1 = None
                x_axis_vr2 = None
                if vr1_table is not None:
                    obs_vr1 = [float(x[obsIndex]) * float(self.MainWindow.vunit_ipt.text()) for x in vr1_table]
                    resd_vr1 = [float(x[-1]) for x in vr1_table]
                    x_axis_vr1 = [float(x[timeIndex]) for x in vr1_table]
                if vr2_table is not None:
                    obs_vr2 = [float(x[obsIndex]) * float(self.MainWindow.vunit_ipt.text()) for x in vr2_table]
                    resd_vr2 = [float(x[-1]) for x in vr2_table]
                    x_axis_vr2 = [float(x[timeIndex]) for x in vr2_table]
                if self.uselc_chk.isChecked():
                    # get model
                    curveProp = self.MainWindow.LoadObservationWidget.Curves()[0].getSynthetic()
                    curveProp.zero = "8"
                    curveProp.factor = "1"
                    curve = classes.Curve(curveProp.FilePath)
                    line3 = []
                    if self.MainWindow.jdphs_combobox.currentText() == "Time" and self.time_combobox.currentText() == "HJD":
                        line3 = [min(curve.timeList), max(curve.timeList), float(self.MainWindow.p0_ipt.text()) / 100,
                                 0, 1, 0.001, 0.25, 0.75, 1, float(self.MainWindow.tavh_ipt.text()) / 10000]
                    else:
                        line3 = [float(self.MainWindow.jd0_ipt.text()), float(self.MainWindow.jd0_ipt.text()) + 1, 0.1,
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
                    lcoutTable = methods.getTableFromOutput(self.MainWindow.lcoutpath, "      JD      ", offset=1)
                    lc_x_index = 1
                    if self.MainWindow.jdphs_combobox.currentText() == "Time" and self.time_combobox.currentText() == "HJD":
                        lc_x_index = 0
                    lc_x = None
                    lc_y_vr1 = None
                    lc_y_vr2 = None
                    lc_x = [float(x[lc_x_index].replace("D", "E")) for x in lcoutTable]
                    if vr1_table is not None:
                        lc_y_vr1 = [float(y[6].replace("D", "E")) * float(self.MainWindow.vunit_ipt.text()) for y in
                                    lcoutTable]
                        self.plot_observationAxis.plot(lc_x, lc_y_vr1, color="#4286f4")
                    if vr2_table is not None:
                        lc_y_vr2 = [float(y[7].replace("D", "E")) * float(self.MainWindow.vunit_ipt.text()) for y in
                                    lcoutTable]
                        self.plot_observationAxis.plot(lc_x, lc_y_vr2, color="red")
                else:
                    idx = 2
                    if self.MainWindow.jdphs_combobox.currentText() == "Time":
                        idx = 3
                    if vr1_table is not None:
                        lc_x_vr1 = x_axis_vr1
                        lc_y_vr1 = [float(x[idx]) * float(self.MainWindow.vunit_ipt.text()) for x in vr1_table]
                        self.plot_observationAxis.plot(lc_x_vr1, lc_y_vr1, linestyle="", marker="o", markersize=4,
                                                       color="#4286f4")
                    if vr2_table is not None:
                        lc_x_vr2 = x_axis_vr2
                        lc_y_vr2 = [float(x[idx]) * float(self.MainWindow.vunit_ipt.text()) for x in vr2_table]
                        self.plot_observationAxis.plot(lc_x_vr2, lc_y_vr2, linestyle="", marker="o", markersize=4,
                                                       color="red")
                if vr1_table is not None:
                    self.plot_observationAxis.plot(x_axis_vr1, obs_vr1, linestyle="", marker="o", markersize=4, color="#4286f4")
                    self.plot_residualAxis.plot(x_axis_vr1, resd_vr1, linestyle="", marker="o", markersize=4, color="#4286f4")
                if vr2_table is not None:
                    self.plot_observationAxis.plot(x_axis_vr2, obs_vr2, linestyle="", marker="o", markersize=4, color="red")
                    self.plot_residualAxis.plot(x_axis_vr2, resd_vr2, linestyle="", marker="o", markersize=4, color="red")
            self.plot_residualAxis.axhline(c="r")
            self.plot_observationAxis.set_ylabel("Radial Velocity (km s$^{-1}$)")
            self.plot_residualAxis.set_ylabel("Residuals")
            if str(self.MainWindow.jdphs_combobox.currentText()) == "Time" and str(self.time_combobox.currentText()) == "HJD":
                self.plot_residualAxis.set_xlabel("HJD")
            else:
                self.plot_residualAxis.set_xlabel("Phase")
            self.plot_toolbar.update()
            self.plot_canvas.draw()
        elif str(self.data_combobox.currentText()) == "O - C":
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
            if os.path.isfile(str(self.MainWindow.EclipseWidget.filepath_label.text())):
                curve = classes.Curve(str(self.MainWindow.EclipseWidget.filepath_label.text()))
                if curve.hasError is False:
                    lenght = len(curve.timeList)
                    ocTable = ocTable[-1 * lenght:]
                    x = [float(x[0]) for x in ocTable]
                    y = [float(y[-1]) for y in ocTable]
                    self.plot_observationAxis.cla()
                    self.plot_residualAxis.cla()
                    self.plot_observationAxis.plot(x, y, linestyle="", marker="o", markersize=4, color="#4286f4")
                    self.plot_canvas.draw()
                    self.plot_toolbar.update()

        elif str(self.data_combobox.currentText()) != "":
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
            computedIndex = 2
            xlabel = self.time_combobox.currentText()
            ylabel = self.MainWindow.maglite_combobox.currentText()
            if ylabel == "Flux":
                ylabel = "Norm. Flux"
            if self.MainWindow.LoadObservationWidget.Curves()[self.data_combobox.currentIndex()].type == "vc":
                ylabel = "Radial Velocity (km s$^{-1}$)"
            if self.MainWindow.jdphs_combobox.currentText() == "Time":  # wd outputs are in HJD
                obsIndex = 2
                computedIndex = 3
            if self.time_combobox.currentText() == "Phase" and self.MainWindow.jdphs_combobox.currentText() == "Time":
                timeIndex = 1
            x_axis = [float(x[timeIndex]) for x in ocTable]
            obs = [float(x[obsIndex]) for x in ocTable]
            resd = [float(x[-1]) for x in ocTable]

            if str(self.MainWindow.maglite_combobox.currentText()) == "Magnitude" \
                and self.data_combobox.currentIndex() + 1 > len(self.MainWindow.LoadObservationWidget.vcPropertiesList):
                magnitude = True
                index = self.data_combobox.currentIndex() - len(self.MainWindow.LoadObservationWidget.vcPropertiesList)
                curve = classes.Curve(self.MainWindow.LoadObservationWidget.lcPropertiesList[index].FilePath)
                obs_mag = [float(x) for x in curve.observationList]
                computed = [float(x[computedIndex]) for x in ocTable]
                resd_mag = []
                for o, c in izip(obs, computed):
                    resd_mag.append(-2.5 * numpy.log10(o / c))
                resd = resd_mag
                obs = obs_mag
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
                    line3 = [min(curve.timeList), max(curve.timeList), float(self.MainWindow.p0_ipt.text()) / 1000,
                             0, 1, 0.001, 0.25, 0.75, 1, float(self.MainWindow.tavh_ipt.text()) / 10000]
                else:
                    line3 = [float(self.MainWindow.jd0_ipt.text()), float(self.MainWindow.jd0_ipt.text()) + 1, 0.1,
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
                lcoutTable = methods.getTableFromOutput(self.MainWindow.lcoutpath, "      JD      ", offset=1)
                lc_y_index = 4
                if magnitude:
                    lc_y_index = 8
                lc_x_index = 1
                if self.MainWindow.jdphs_combobox.currentText() == "Time" and self.time_combobox.currentText() == "HJD":
                    lc_x_index = 0
                if curveProp.type == "vc":
                    lc_y_index = 6 + curveProp.star - 1

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
                if magnitude:
                    lc_y_mag = [-2.5 * numpy.log10(x) for x in lc_y]
                    lc_y = lc_y_mag

            self.plot_observationAxis.cla()
            self.plot_residualAxis.cla()
            clr = "#4286f4"
            curveProp = self.MainWindow.LoadObservationWidget.Curves()[self.data_combobox.currentIndex()].getSynthetic()
            if curveProp.type == "vc" and curveProp.star == 2:
                clr = "red"
            self.plot_observationAxis.plot(x_axis, obs, linestyle="", marker="o", markersize=4, color=clr)
            if self.uselc_chk.isChecked():
                self.plot_observationAxis.plot(lc_x, lc_y, color="red")
            else:
                self.plot_observationAxis.plot(lc_x, lc_y, linestyle="", marker="o", markersize=4, color="red")
            self.plot_residualAxis.plot(x_axis, resd, linestyle="", marker="o", markersize=4, color=clr)
            self.plot_residualAxis.axhline(c="r")
            self.plot_toolbar.update()
            self.plot_observationAxis.tick_params(labeltop=False, labelbottom=False, bottom=True, top=True,
                                                  labelright=False, labelleft=True, labelsize=11)
            self.plot_residualAxis.set_xlabel(xlabel)
            self.plot_residualAxis.set_ylabel("Residuals")
            self.plot_observationAxis.set_ylabel(ylabel)
            if magnitude:
                if self.plot_observationAxis.yaxis_inverted() == False:
                    self.plot_observationAxis.invert_yaxis()
                if self.plot_residualAxis.yaxis_inverted() == False:
                    self.plot_residualAxis.invert_yaxis()
            else:
                if self.plot_observationAxis.yaxis_inverted() == True:
                    self.plot_observationAxis.invert_yaxis()
                if self.plot_residualAxis.yaxis_inverted() == True:
                    self.plot_residualAxis.invert_yaxis()
            self.plot_observationAxis.ticklabel_format(useOffset=False)
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
            obs.xaxis.get_major_ticks()
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
            obs.tick_params(labeltop=False, labelbottom=False, bottom=True, top=True,
                                                  labelright=False, labelleft=True, labelsize=11)

            if self.plot_observationAxis.yaxis_inverted() == True:
                obs.invert_yaxis()
                resd.invert_yaxis()
            pyplot.show()

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
        self.DcinView.fill()
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
                allChars = ""
                for val in result:
                    allChars = allChars + val

                if "*" not in allChars:
                    result[4] = result[4].replace("D", "e")
                    result[4] = methods.convertFromScientificToGeneric(result[4])
                    if len(result) >= 6:
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

        def _reformat(num):
            if -1.0e-5 < float(num) < 1.0e-5:
                return num
            else:
                return methods.convertFromScientificToGeneric(num)

        def _populateItem(itm, rslt):
            id = int(rslt[0])
            input = rslt[2].replace("D", "e")
            corr = rslt[3].replace("D", "e")
            output = rslt[4].replace("D", "e")
            stderr = rslt[5].replace("D", "e")

            if "*" not in input + corr + output + stderr:
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

                input = _reformat(input)
                corr = _reformat(corr)
                output = _reformat(output)
                stderr = _reformat(stderr)

                if numpy.absolute(float(stderr)) > numpy.absolute(float(corr)) or \
                        (numpy.absolute(float(stderr)) == 0.0 and numpy.absolute(float(corr)) == 0.0):
                    itm.setBackground(3, QtGui.QBrush(QtGui.QColor("green")))

            else:
                if "*" in input:
                    input = "***"
                    itm.setBackground(1, QtGui.QBrush(QtGui.QColor("red")))
                if "*" in corr:
                    corr = "***"
                    itm.setBackground(2, QtGui.QBrush(QtGui.QColor("red")))
                if "*" in output:
                    output = "***"
                    itm.setBackground(3, QtGui.QBrush(QtGui.QColor("red")))
                if "*" in stderr:
                    stderr = "***"
                    itm.setBackground(4, QtGui.QBrush(QtGui.QColor("red")))

            itm.setText(0, self.parameterDict[rslt[0]])
            itm.setText(1, input)
            itm.setText(2, corr)
            itm.setText(3, output)
            itm.setText(4, stderr)

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
        def _addComponentBlock(table, parentItem):
            for line in table:
                item = QtGui.QTreeWidgetItem(parentItem)
                item.setText(0, line[1].title())
                item.setText(1, line[2])
                item.setText(2, line[5])

                if "*" in line[2]:
                    item.setBackground(1, QtGui.QBrush(QtGui.QColor("red")))
                if "*" in line[5]:
                    item.setBackground(2, QtGui.QBrush(QtGui.QColor("red")))

                parentItem.addChild(item)

        self.component_treewidget.clear()
        star1ParentItem = QtGui.QTreeWidgetItem(self.component_treewidget)
        star1ParentItem.setText(0, "Star 1")
        _addComponentBlock(first, star1ParentItem)

        star2ParentItem = QtGui.QTreeWidgetItem(self.component_treewidget)
        star2ParentItem.setText(0, "Star 2")
        _addComponentBlock(second, star2ParentItem)

        emptyItem = QtGui.QTreeWidgetItem(self.component_treewidget)
        filloutItem = QtGui.QTreeWidgetItem(self.component_treewidget)

        filloutItem.setText(0, "Fillout")
        filloutItem.setText(1, methods.computeFillOutFactor(self.MainWindow))

        self.component_treewidget.expandAll()

    def updateCurveInfoTree(self, curveinfoTable):
        self.curvestat_treewidget.clear()
        frmt = "{:g}"
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
            self.lastBaseSet = methods.getTableFromOutput(self.dcoutpath, "Input-Output in D Format", splitmap=[5, 9, 28, 46, 65, 83], occurence=int(self.niter_spinbox.value()))
            self.residualTable = methods.getTableFromOutput(self.dcoutpath, "Mean residual for input values", offset=1, occurence=int(self.niter_spinbox.value()))[0]
            self.firstComponentTable = methods.getTableFromOutput(self.dcoutpath, "  1   pole", offset=0, splitmap=[3, 10, 24, 38, 52, 66], occurence=int(self.niter_spinbox.value()))
            self.secondComponentTable = methods.getTableFromOutput(self.dcoutpath, "  2   pole", offset=0, splitmap=[3, 10, 24, 38, 52, 66], occurence=int(self.niter_spinbox.value()))
            self.updateResultTree(self.lastBaseSet)
            self.updateComponentTree(self.firstComponentTable, self.secondComponentTable)
            self.updateResidualTree(self.residualTable)
            self.updateCurveInfoTree(methods.getTableFromOutput(self.dcoutpath,
                "Standard Deviations for Computation of Curve-dependent Weights"))
            self.enableUi()

            # check for output sanity
            sanity = True
            for result in self.lastBaseSet:
                for cell in result:
                    if cell == "NaN" or cell == "nan" or "*" in cell:
                        sanity = False
                        break

            if sanity is True:
                self.populatePlotCombobox()
                self.MainWindow.HistoryWidget.addIterationData(self.lastBaseSet)
                if self.autoupdate_chk.isChecked():
                    self.plot_btn.click()
                self.continueIterating()
            else:
                niter = int(self.lastiteration)
                self.lastiteration = 0
                self.lastBaseSet = None
                self.firstComponentTable = None
                self.secondComponentTable = None
                self.residualTable = None
                raise ValueError("Iteration #{0} resulted in NaN or *** for one "
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

    def continueIterating(self):
        self.lastiteration = self.lastiteration + 1
        if self.lastiteration < int(self.iteration_spinbox.value()):
            self.updateinputs_btn.click()
            self.runIteration()
        else:
            self.lastiteration = 0


class OutputView(QtGui.QWidget, outputview.Ui_OutputView):
    def __init__(self, path, button):  # constructor
        super(OutputView, self).__init__()
        self.setupUi(self)
        self.path = path
        button.clicked.connect(self.open)
        db = QtGui.QFontDatabase()
        db.addApplicationFont(__font_path__)
        ptmono = QtGui.QFont(QtCore.QString("PT Mono"), pointSize=11)
        self.output_textedit.setFont(ptmono)

    def fill(self):
        text = ""
        with open(self.path, "r") as f:
            for line in f:
                text = text + line
        self.output_textedit.setPlainText(text)

    def open(self):
        self.setWindowTitle("PyWD - " + self.path)
        self.fill()
        self.show()


class SyntheticCurveWidget(QtGui.QWidget, syntheticcurvewidget.Ui_SyntheticCurveWidget):
    def __init__(self):
        super(SyntheticCurveWidget, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(__icon_path__))  # set app icon
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
        self.plotIsInverted = False
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
        self.fillout_label.setText("Fillout = " + methods.computeFillOutFactor(self.MainWindow))
        if self.selectedItem() is not None:
            self.plot_observationAxis.cla()
            self.plot_residualAxis.cla()
            self.plot_starposAxis.cla()
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
            curveProps = CurvePropertiesDialog(self.MainWindow)
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
                syntheticCurve.zero = item.text(14)
                syntheticCurve.factor = item.text(13)
                syntheticCurve.wla = "0.55"
                syntheticCurve.aextinc = item.text(11)
                syntheticCurve.calib = item.text(12)
            else:
                index = self.loaded_treewidget.invisibleRootItem().indexOfChild(item)
                curve = self.MainWindow.LoadObservationWidget.Curves()[index]
                syntheticCurve = curve.getSynthetic()
                syntheticCurve.zero = item.text(14)
                syntheticCurve.factor = item.text(13)
                if syntheticCurve.type == "vc":
                    syntheticCurve.zero = "8"
                    syntheticCurve.factor = "1"
            if self.plotobs_chk.isChecked():
                if str(item.text(0)) != "[Synthetic]":
                    index = self.loaded_treewidget.invisibleRootItem().indexOfChild(item)
                    curve = classes.Curve(self.MainWindow.LoadObservationWidget.Curves()[index].FilePath)
                    curveProperties = self.MainWindow.LoadObservationWidget.Curves()[index]
                    x_obs = [float(x) for x in curve.timeList]
                    y_obs = [float(y) for y in curve.observationList]
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

                    if self.alias_chk.isChecked() and \
                            (self.MainWindow.jdphs_combobox.currentText() == "Phase" or
                             (self.time_combobox.currentText() == "Phase" and
                              self.MainWindow.jdphs_combobox.currentText() == "Time")):
                        x_obs, y_obs = methods.aliasObservations(x_obs, y_obs,
                                                                 float(str(self.MainWindow.phasestart_ipt.text())),
                                                                 float(str(self.MainWindow.phasestop_ipt.text())))
                        if curveProperties.type == "vc":
                            x2_obs, y2_obs = methods.aliasObservations(x2_obs, y2_obs,
                                                                     float(str(self.MainWindow.phasestart_ipt.text())),
                                                                     float(str(self.MainWindow.phasestop_ipt.text())))

                    self.plot_observationAxis.plot(x_obs, y_obs, linestyle="", marker="o", markersize=4, color="#4286f4")
                    if curveProperties.type == "vc":
                        self.plot_observationAxis.plot(x2_obs, y2_obs, linestyle="", marker="o", markersize=4,
                                                       color="#f73131")
                    curveProps = self.MainWindow.LoadObservationWidget.Curves()[index]
                    if str(self.MainWindow.maglite_combobox.currentText()) == "Magnitude" and curveProps.type == "lc":
                        if self.plot_observationAxis.yaxis_inverted() == False:
                            self.plot_observationAxis.invert_yaxis()
                        if self.plot_residualAxis.yaxis_inverted() == False:
                            self.plot_residualAxis.invert_yaxis()
                    else:
                        if self.plot_observationAxis.yaxis_inverted() == True:
                            self.plot_observationAxis.invert_yaxis()
                        if self.plot_residualAxis.yaxis_inverted() == True:
                            self.plot_residualAxis.invert_yaxis()

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
                table = methods.getTableFromOutput(self.MainWindow.lcoutpath, "      JD         ", offset=1)
                # set data indexes
                x_index = None
                y_index = None
                y2_index = None
                if syntheticCurve.type == "vc":
                    y_index = 6
                    y2_index = 7
                if syntheticCurve.type == "lc":
                    y_index = 4
                    if str(self.MainWindow.maglite_combobox.currentText()) == "Magnitude":
                        y_index = 8
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
                        self.plot_residualAxis.plot(x2_obs, y2_residuals, linestyle="", marker="o", markersize=4,
                                                    color="#f73131")
                    interpolated_y_model = numpy.interp(x_obs, x_model, y_model)
                    y_residuals = []
                    for o, c in izip(y_obs, interpolated_y_model):
                        y_residuals.append(o - c)
                    self.plot_residualAxis.plot(x_obs, y_residuals, linestyle="", marker="o", markersize=4, color="#4286f4")
                self.plot_residualAxis.set_ylabel("Residuals")
                if str(self.MainWindow.maglite_combobox.currentText()) == "Magnitude" and syntheticCurve.type == "lc":
                    if self.plot_observationAxis.yaxis_inverted() == False:
                        self.plot_observationAxis.invert_yaxis()
                    if self.plot_residualAxis.yaxis_inverted() == False:
                        self.plot_residualAxis.invert_yaxis()
                else:
                    if self.plot_observationAxis.yaxis_inverted() == True:
                        self.plot_observationAxis.invert_yaxis()
                    if self.plot_residualAxis.yaxis_inverted() == True:
                        self.plot_residualAxis.invert_yaxis()

            if self.drawstars_chk.isChecked():
                self.plot_observationAxis.set_position(self.triple_grid[0, :-1].get_position(self.plot_figure))
                self.plot_residualAxis.set_position(self.triple_grid[1, :-1].get_position(self.plot_figure))
                self.plot_starposAxis.set_visible(True)
                lcin = classes.lcin(self.MainWindow)
                phase = self.phase_spinbox.value()
                lcin.starPositions(line3=[self.MainWindow.jd0_ipt.text(), float(self.MainWindow.jd0_ipt.text()) + 1, 0.1,
                             phase, phase, 0.1, 0.25, 0.75, 1, float(self.MainWindow.tavh_ipt.text()) / 10000], jdphs="2")
                with open(self.MainWindow.lcinpath, "w") as f:
                    f.write(lcin.output)
                process = subprocess.Popen(self.MainWindow.lcpath, cwd=os.path.dirname(self.MainWindow.lcpath))
                process.wait()
                table = methods.getTableFromOutput(self.MainWindow.lcoutpath, "HJD =  ", offset=3)
                x = [float(x[0].replace("D", "E")) for x in table]
                y = [float(y[1].replace("D", "E")) for y in table]
                self.plot_starposAxis.plot(x, y, 'ko', markersize=0.2, label="Surface Grids")
                self.plot_starposAxis.plot([0], [0], linestyle="", marker="+", markersize=5, color="#ff3a3a")
            if self.roche_chk.isChecked():
                self.plot_observationAxis.set_position(self.triple_grid[0, :-1].get_position(self.plot_figure))
                self.plot_residualAxis.set_position(self.triple_grid[1, :-1].get_position(self.plot_figure))
                self.plot_starposAxis.set_visible(True)
                methods.computeRochePotentials(self.MainWindow, self.phase_spinbox.value(), self.plot_starposAxis)
                self.plot_starposAxis.set_xlim(-1, 2)
                self.plot_starposAxis.set_ylim(-1, 1)

            self.plot_toolbar.update()
            self.plot_starposAxis.set_xlabel('x')
            self.plot_starposAxis.set_ylabel('y')
            yticks_resd = self.plot_residualAxis.yaxis.get_major_ticks()
            yticks_resd[-1].label1.set_visible(False)
            self.plot_residualAxis.axhline(0, color="red")
            self.plot_canvas.draw()

    def updateObservations(self):
        item = self.loaded_treewidget.invisibleRootItem().child(self.lastEditedIndex)
        if item.text(0) != "[Synthetic]":
            curve = self.MainWindow.LoadObservationWidget.Curves()[self.lastEditedIndex]
            if self.lastEditedColumn == 2:
                curveProp = CurvePropertiesDialog(self.MainWindow)
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
        item.setText(13, "-")
        item.setText(14, "-")
        item = QtGui.QTreeWidgetItem(self.loaded_treewidget)
        item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
        item.setText(0, "[Synthetic]")
        item.setText(1, "Light Curve")
        curveProps = CurvePropertiesDialog(self.MainWindow)
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
        item.setText(13, "0")
        item.setText(14, "0")

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
                item.setText(13, "-")
                item.setText(14, "-")
            if curve.type == "lc":
                curveProps = CurvePropertiesDialog(self.MainWindow)
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
                item.setText(13, "1")
                item.setText(14, "8")
        self.loaded_treewidget.header().setResizeMode(3)

    def selectBand(self, button, item):
        curve = CurvePropertiesDialog(self.MainWindow)
        menu = curve.bandpassContextMenu
        band = menu.exec_(QtGui.QCursor.pos())
        if band is not None:
            button.setText(band.objectName())
            self.lastEditedIndex = self.loaded_treewidget.invisibleRootItem().indexOfChild(item)
            self.lastEditedColumn = 2
            self.loaded_treewidget.model().dataChanged.emit(QtCore.QModelIndex(), QtCore.QModelIndex())

    def rocheChanged(self):
        if self.roche_chk.isChecked():
            periastron = methods.computeConjunctionPhases(self.MainWindow)[4]
            self.phase_spinbox.setDisabled(True)
            self.phase_spinbox.setValue(periastron)
            self.drawstars_chk.setDisabled(True)
            self.drawstars_chk.setChecked(False)
        else:
            self.phase_spinbox.setDisabled(False)
            self.drawstars_chk.setDisabled(False)


class StarPositionWidget(QtGui.QWidget, starpositionswidget.Ui_StarPositionWidget):
    def __init__(self):
        super(StarPositionWidget, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(__icon_path__))
        self.start_btn.setIcon(QtGui.QIcon("resources/play.png"))
        self.skip_btn.setIcon(QtGui.QIcon("resources/jump.png"))
        self.backtostart_btn.setIcon(QtGui.QIcon("resources/start.png"))
        # variables
        self.MainWindow = None
        self.starRenderData = None
        self.starsRendered = False
        self.stopwatch = None
        self.lastFrameShown = 0
        self.iterator = None
        # animation variables
        self.framesPerSecond = 25.0  # 25 frames per second
        self.frameTime = 1.0 / self.framesPerSecond  # 0.04ms per frame (25fps)
        self.duration = 5.0  # duration of animation in seconds
        self.totalFrames = 5.0 * self.framesPerSecond  # 125 frames total
        self.phaseIncrement = 1.0 / self.totalFrames  # 0.008
        # set up canvas
        self.plot_figure = Figure()
        self.plot_canvas = FigureCanvas(self.plot_figure)
        self.plot_toolbar = NavigationToolbar(self.plot_canvas, self.plot_widget)
        plot_layout = QtGui.QVBoxLayout()
        plot_layout.addWidget(self.plot_toolbar)
        plot_layout.addWidget(self.plot_canvas)
        self.plot_widget.setLayout(plot_layout)
        self.plot_starPositionAxis = self.plot_figure.add_subplot(111)
        self.plot_starPositionAxis.set_xlabel("x")
        self.plot_starPositionAxis.set_ylabel("y")
        self.plot_starPositionAxis.set_xlim(-1, 1)
        self.plot_starPositionAxis.set_ylim(-1, 1)
        self.plot_starPositionAxis.axis("equal")
        self.plot_figure.tight_layout()
        # render area
        self.renderArea = self.RenderArea(self)
        render_layout = QtGui.QVBoxLayout()
        render_layout.addWidget(self.renderArea)
        self.render_widget.setLayout(render_layout)
        # signals
        self.connectSignals()

    class RenderArea(QtOpenGL.QGLWidget):
        def __init__(self, parent):
            QtOpenGL.QGLWidget.__init__(self)
            self.StarPositionWidget = parent
            self.imageToRender = None

        def paintEvent(self, QPaintEvent):
            QtOpenGL.QGLWidget.paintEvent(self, QPaintEvent)
            if self.imageToRender is not None:
                painter = QtGui.QPainter(self)
                painter.drawImage(0, 0, self.imageToRender, 0, 0, -1, -1)
                painter.setRenderHint(painter.SmoothPixmapTransform)
                painter.end()

        def showImage(self, image):
            self.imageToRender = image
            self.repaint()

    def playRender(self):
        for image in self.starRenderData:
            start = time.time()
            self.renderArea.showImage(image)
            wait = time.time() - start
            if wait < 0.0:
                wait = 0.0
            time.sleep(self.frameTime - wait)

    def closeEvent(self, QCloseEvent):
        try:
            self.iterator.stop()
        except:
            pass

    def connectSignals(self):
        self.single_chk.stateChanged.connect(self.checkSingle)
        self.render_btn.clicked.connect(self.renderStars)
        self.start_btn.clicked.connect(self.playRender)
        self.plot_btn.clicked.connect(self.plotSingle)
        self.roche_chk.stateChanged.connect(self.checkRoche)
        self.saveall_btn.clicked.connect(self.saveAll)

    def checkSingle(self):
        if self.single_chk.isChecked():
            self.render_phaseSpinbox.setDisabled(False)
        else:
            self.render_phaseSpinbox.setDisabled(True)

    def setPlotLimits(self):
        self.plot_starPositionAxis.set_xbound(lower=self.min_spinbox.value(), upper=self.max_spinbox.value())
        self.plot_starPositionAxis.set_ybound(lower=self.min_spinbox.value(), upper=self.max_spinbox.value())
        self.plot_canvas.draw()

    def checkRoche(self):
        if self.roche_chk.isChecked():
            periastron = methods.computeConjunctionPhases(self.MainWindow)[4]
            self.phase_spinbox.setValue(periastron)
            self.phase_spinbox.setDisabled(True)
        else:
            self.phase_spinbox.setDisabled(False)

    def plotSingle(self):
        self.plot_starPositionAxis.cla()
        if self.roche_chk.isChecked():
            methods.computeRochePotentials(self.MainWindow, self.phase_spinbox.value(), self.plot_starPositionAxis)
            inner, outer = methods.computeRochePotentials(self.MainWindow, self.phase_spinbox.value(), None, getPotentials=True)
            self.inner_crit_label.setText(str(inner[0]))
            self.outer_crit_label.setText(str(outer[0]))
        else:
            self.inner_crit_label.setText("N/A")
            self.outer_crit_label.setText("N/A")
            lcin = classes.lcin(self.MainWindow)
            phase = self.phase_spinbox.value()
            lcin.starPositions(line3=[self.MainWindow.jd0_ipt.text(), float(self.MainWindow.jd0_ipt.text()) + 1, 0.1,
                                      phase, phase, 0.1, 0.25, 0.75, 1, float(self.MainWindow.tavh_ipt.text()) / 10000],
                               jdphs="2")
            with open(self.MainWindow.lcinpath, "w") as f:
                f.write(lcin.output)
            process = subprocess.Popen(self.MainWindow.lcpath, cwd=os.path.dirname(self.MainWindow.lcpath))
            process.wait()
            table = methods.getTableFromOutput(self.MainWindow.lcoutpath, "HJD =  ", offset=3)
            x = [float(x[0].replace("D", "E")) for x in table]
            y = [float(y[1].replace("D", "E")) for y in table]
            self.plot_starPositionAxis.plot(x, y, 'ko', markersize=0.2)
        self.plot_starPositionAxis.plot([0], [0], linestyle="", marker="+", markersize=10, color="#ff3a3a")
        self.plot_starPositionAxis.set_xlabel("x")
        self.plot_starPositionAxis.set_ylabel("y")
        self.plot_toolbar.update()
        self.plot_canvas.draw()

    def renderFrame(self, x, y, phase):
        pyplot.cla()
        pyplot.axis("equal")
        pyplot.xlabel("x")
        pyplot.ylabel("y")
        pyplot.xlim(self.min_spinbox.value(), self.max_spinbox.value())
        pyplot.ylim(self.min_spinbox.value(), self.max_spinbox.value())
        pyplot.plot(x, y, 'ko', markersize=0.2, label="{:4.3f}".format(phase))
        pyplot.legend(loc="upper right")
        pyplot.plot([0], [0], linestyle="", marker="+", markersize=10, color="#ff3a3a")
        image = io.BytesIO()
        dpiDict = {
            "64dpi": 64,
            "128dpi": 128,
            "256dpi": 256
        }
        pyplot.savefig(image, dpi=dpiDict[str(self.dpi_combobox.currentText())], format="png")
        image.seek(0)
        qbyte = QtCore.QByteArray(image.getvalue())
        qimage = QtGui.QImage()
        qimage.loadFromData(qbyte)
        return qimage

    def saveAll(self):
        if self.starsRendered is True:
            dialog = QtGui.QFileDialog()
            dialog.setFileMode(2)
            dialog.exec_()
            path = str(dialog.selectedFiles()[0])
            i = 0
            saveOk = True
            for qimage in self.starRenderData:
                status = qimage.save(os.path.join(path, "{:0>4d}".format(i) + ".png"), "png", 100)
                i = i + 1
                if status is False:
                    saveOk = False
                    break
            msg = QtGui.QMessageBox()
            if saveOk is True:
                msg.setText("Frames are saved into " + path)
            else:
                msg.setText("An error has occured.")
            msg.exec_()

    def renderStars(self):
        if self.single_chk.isChecked():
            self.starRenderData = None
            self.starsRendered = False
            lcin = classes.lcin(self.MainWindow)
            phase = self.render_phaseSpinbox.value()
            lcin.starPositions(line3=[self.MainWindow.jd0_ipt.text(), float(self.MainWindow.jd0_ipt.text()) + 1, 0.1,
                                      phase, phase, 0.1, 0.25, 0.75, 1, float(self.MainWindow.tavh_ipt.text()) / 10000],
                               jdphs="2")
            with open(self.MainWindow.lcinpath, "w") as f:
                f.write(lcin.output)
            process = subprocess.Popen(self.MainWindow.lcpath, cwd=os.path.dirname(self.MainWindow.lcpath))
            process.wait()
            table = methods.getTableFromOutput(self.MainWindow.lcoutpath, "HJD =  ", offset=3)
            x = [float(x[0].replace("D", "E")) for x in table]
            y = [float(y[1].replace("D", "E")) for y in table]
            self.renderArea.showImage(self.renderFrame(x, y, float(str(self.render_phaseSpinbox.text()))))
        else:
            lcin = classes.lcin(self.MainWindow)
            lcin.starPositions(line3=[self.MainWindow.jd0_ipt.text(), float(self.MainWindow.jd0_ipt.text()) + 1, 0.1,
                                      0, 1, self.phaseIncrement, 0.25, 0.75, 1,
                                      float(self.MainWindow.tavh_ipt.text()) / 10000], jdphs="2")
            with open(self.MainWindow.lcinpath, "w") as f:
                f.write(lcin.output)
            self.iterator = classes.IteratorThread(self.MainWindow.lcpath)
            self.connect(self.iterator, QtCore.SIGNAL("finished()"), self.afterIteration)
            self.disableUi()
            self.message_label.setText("Running LC...")
            self.iterator.start()
            self.disableUi()

    def abortRender(self):
        self.iterator.stop()
        self.enableUi()

    def disableUi(self):
        self.render_btn.clicked.disconnect()
        self.render_btn.clicked.connect(self.abortRender)
        self.render_btn.setText("Abort")
        self.min_spinbox.setDisabled(True)
        self.max_spinbox.setDisabled(True)
        self.dpi_combobox.setDisabled(True)
        self.saveframe_btn.setDisabled(True)
        self.saveall_btn.setDisabled(True)
        self.start_btn.setDisabled(True)
        self.skip_btn.setDisabled(True)
        self.backtostart_btn.setDisabled(True)
        self.horizontalSlider.setDisabled(True)

    def enableUi(self):
        self.render_btn.clicked.disconnect()
        self.render_btn.clicked.connect(self.renderStars)
        self.render_btn.setText("Render")
        self.min_spinbox.setDisabled(False)
        self.max_spinbox.setDisabled(False)
        self.dpi_combobox.setDisabled(False)
        self.saveframe_btn.setDisabled(False)
        self.saveall_btn.setDisabled(False)
        self.start_btn.setDisabled(False)
        self.skip_btn.setDisabled(False)
        self.backtostart_btn.setDisabled(False)
        self.horizontalSlider.setDisabled(False)
        self.message_label.setText("Ready")

    def afterIteration(self):
        self.render_btn.setDisabled(True)
        self.message_label.setText("Rendering Plots...")
        data = methods.getAllTablesFromOutput(self.MainWindow.lcoutpath, "Y Sky Coordinate", "Z Sky Coordinate",
                                              offset=1)
        renderedFrames = []
        plotnumber = len(data)
        percentage = (1.0 / plotnumber) * 100
        currentPercentage = 0.0
        i = 0
        for line in data:
            lx = [float(x[0].replace("D", "E")) for x in line]
            ly = [float(x[1].replace("D", "E")) for x in line]
            frame = self.renderFrame(lx, ly, i * self.phaseIncrement)
            renderedFrames.append(frame)
            currentPercentage = percentage + currentPercentage
            self.progressBar.setValue(currentPercentage)
            self.progressBar.repaint()
            i = i + 1
        self.starRenderData = renderedFrames
        self.starsRendered = True
        self.enableUi()
        self.render_btn.setDisabled(False)


class DimensionWidget(QtGui.QWidget, dimensionwidget.Ui_DimensionWidget):
    def __init__(self):
        super(DimensionWidget, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(__icon_path__))
        self.MainWindow = None
        # set up plot widget for star 1
        self.s1_plot_figure = Figure()
        self.s1_plot_canvas = FigureCanvas(self.s1_plot_figure)
        self.s1_plot_toolbar = NavigationToolbar(self.s1_plot_canvas, self.s1_plot_widget)
        s1_plot_layout = QtGui.QVBoxLayout()
        s1_plot_layout.addWidget(self.s1_plot_toolbar)
        s1_plot_layout.addWidget(self.s1_plot_canvas)
        self.s1_plot_widget.setLayout(s1_plot_layout)
        self.s1_plotAxis = self.s1_plot_figure.add_subplot(111)
        # set up plot widget for star 2
        self.s2_plot_figure = Figure()
        self.s2_plot_canvas = FigureCanvas(self.s2_plot_figure)
        self.s2_plot_toolbar = NavigationToolbar(self.s2_plot_canvas, self.s2_plot_widget)
        s2_plot_layout = QtGui.QVBoxLayout()
        s2_plot_layout.addWidget(self.s2_plot_toolbar)
        s2_plot_layout.addWidget(self.s2_plot_canvas)
        self.s2_plot_widget.setLayout(s2_plot_layout)
        self.s2_plotAxis = self.s2_plot_figure.add_subplot(111)
        self.s1_plotAxis.set_xlabel("Phase")
        self.s1_plotAxis.set_ylabel("Fractional Radius")
        self.s2_plotAxis.set_xlabel("Phase")
        self.s2_plotAxis.set_ylabel("Fractional Radius")
        self.s1_plot_figure.tight_layout()
        self.s2_plot_figure.tight_layout()
        # variables to plot
        self.s1_pole = None
        self.s1_point = None
        self.s1_side = None
        self.s1_back = None
        self.s2_pole = None
        self.s2_point = None
        self.s2_side = None
        self.s2_back = None
        self.x = None
        # signal connection
        self.connectSignals()

    def connectSignals(self):
        self.plot_btn.clicked.connect(self.computeComponents)
        self.s1_pole_chk.stateChanged.connect(self.plotComponents)
        self.s1_point_chk.stateChanged.connect(self.plotComponents)
        self.s1_side_chk.stateChanged.connect(self.plotComponents)
        self.s1_back_chk.stateChanged.connect(self.plotComponents)
        self.s2_pole_chk.stateChanged.connect(self.plotComponents)
        self.s2_point_chk.stateChanged.connect(self.plotComponents)
        self.s2_side_chk.stateChanged.connect(self.plotComponents)
        self.s2_back_chk.stateChanged.connect(self.plotComponents)

    def plotComponents(self):
        self.s1_plotAxis.cla()
        self.s2_plotAxis.cla()

        if self.s1_pole_chk.isChecked() and self.s1_pole is not None:
            self.s1_plotAxis.plot(self.x, self.s1_pole, color="blue")
        if self.s1_point_chk.isChecked() and self.s1_point is not None:
            self.s1_plotAxis.plot(self.x, self.s1_point, color="black")
        if self.s1_side_chk.isChecked() and self.s1_side is not None:
            self.s1_plotAxis.plot(self.x, self.s1_side, color="red")
        if self.s1_back_chk.isChecked() and self.s1_back is not None:
            self.s1_plotAxis.plot(self.x, self.s1_back, color="green")

        if self.s2_pole_chk.isChecked() and self.s2_pole is not None:
            self.s2_plotAxis.plot(self.x, self.s2_pole, color="blue")
        if self.s2_point_chk.isChecked() and self.s2_point is not None:
            self.s2_plotAxis.plot(self.x, self.s2_point, color="black")
        if self.s2_side_chk.isChecked() and self.s2_side is not None:
            self.s2_plotAxis.plot(self.x, self.s2_side, color="red")
        if self.s2_back_chk.isChecked() and self.s2_back is not None:
            self.s2_plotAxis.plot(self.x, self.s2_back, color="green")

        self.s1_plotAxis.set_xlabel("Phase")
        self.s1_plotAxis.set_ylabel("Fractional Radius")

        self.s2_plotAxis.set_xlabel("Phase")
        self.s2_plotAxis.set_ylabel("Fractional Radius")

        self.s1_plotAxis.ticklabel_format(useOffset=False)
        self.s1_plot_canvas.draw()
        self.s1_plot_toolbar.update()

        self.s2_plotAxis.ticklabel_format(useOffset=False)
        self.s2_plot_canvas.draw()
        self.s2_plot_toolbar.update()
        self.s1_plot_figure.tight_layout()
        self.s2_plot_figure.tight_layout()

    def computeComponents(self):
        lcin = classes.lcin(self.MainWindow)
        lcin.starPositions(jdphs="2")
        lcin.output = "4" + lcin.output[1:]
        with open(self.MainWindow.lcinpath, "w") as f:
            f.write(lcin.output)
        process = subprocess.Popen(self.MainWindow.lcpath, cwd=os.path.dirname(self.MainWindow.lcpath))
        process.wait()
        table = methods.getTableFromOutput(self.MainWindow.lcoutpath, "      JD             Phase", offset=1)

        self.s1_pole = []
        self.s1_point = []
        self.s1_side = []
        self.s1_back = []
        self.s2_pole = []
        self.s2_point = []
        self.s2_side = []
        self.s2_back = []
        self.x = []

        for line in table:
            self.s1_pole.append(float(line[2]))
            self.s1_point.append(float(line[3]))
            self.s1_side.append(float(line[4]))
            self.s1_back.append(float(line[5]))
            self.s2_pole.append(float(line[6]))
            self.s2_point.append(float(line[7]))
            self.s2_side.append(float(line[8]))
            self.s2_back.append(float(line[9]))
            self.x.append(float(line[1]))

        self.plotComponents()


class ConjunctionWidget(QtGui.QWidget, conjunctionwidget.Ui_conjunctionwidget):
    def __init__(self):
        super(ConjunctionWidget, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(__icon_path__))
        self.MainWindow = None
        self.data_treewidget.header().setResizeMode(3)
        self.data = None
        self.ut_data = []
        self.outputHasDt = False
        # signal connection
        self.connectSignals()

    def connectSignals(self):
        self.compute_btn.clicked.connect(self.computeConjunction)
        self.export_btn.clicked.connect(self.exportData)
        self.dt_chk.stateChanged.connect(self.checkDt)

    def checkDt(self):
        self.radec_container.setEnabled(self.dt_chk.isChecked())

    def computeConjunction(self):
        self.outputHasDt = False
        self.data_treewidget.clear()
        self.ut_data = []
        lcin = classes.lcin(self.MainWindow)
        lcin.starPositions(jdphs="1")
        ktstep = str(self.kstep_spinbox.value())
        lcin.output = "6" + lcin.output[1:29] + " " + (" " * (5 - len(ktstep)) + ktstep) + lcin.output[29:]
        with open(self.MainWindow.lcinpath, "w") as f:
            f.write(lcin.output)
        process = subprocess.Popen(self.MainWindow.lcpath, cwd=os.path.dirname(self.MainWindow.lcpath))
        process.wait()
        table = methods.getTableFromOutput(self.MainWindow.lcoutpath, "    conj. time", 2)
        ut_table = []
        for row in table:
            item = QtGui.QTreeWidgetItem(self.data_treewidget)
            item.setText(0, row[0])
            item.setText(1, (" " * 9) + row[1])
            if self.ut_groupbox.isChecked():
                jd = row[0]
                if self.dt_chk.isChecked():
                    self.outputHasDt = True
                    jd = methods.convertHJDtoJD(float(jd), self.ra_h_spinbox.value(), self.ra_m_spinbox.value(), self.ra_s_spinbox.value(),
                                                self.dec_d_spinbox.value(), self.dec_m_spinbox.value(), self.dec_s_spinbox.value())
                year, month, day, hour, minute, second = methods.convertJDtoUT(jd)
                ut = "{2}/{1}/{0} - {3}:{4}:{5:4.2f}".format(year, month, day, hour, minute, second)
                item.setText(2, ut)
                ut_table.append(ut)
        self.ut_data = ut_table
        self.data = table

    def exportData(self):
        if self.data is not None:
            dialog = QtGui.QFileDialog(self)
            dialog.setDefaultSuffix("txt")
            dialog.setNameFilter("Plaintext File (*.txt)")
            dialog.setAcceptMode(1)
            returnCode = dialog.exec_()
            filePath = str((dialog.selectedFiles())[0])
            if filePath != "" and returnCode != 0:
                msg = QtGui.QMessageBox()
                fi = QtCore.QFileInfo(filePath)
                try:
                    with open(filePath, "w") as f:
                        if len(self.ut_data) > 0:
                            if self.outputHasDt is True:
                                f.write("#HJD" + (" " * (len(self.data[0][0]))) + "#Mintype" +
                                        "    #Date (D/M/Y) - Time (UTC, H:M:S) (dt EXCLUDED)" + "\n")
                            else:
                                f.write("#HJD" + (" " * (len(self.data[0][0]))) + "#Mintype" +
                                        "    #Date (D/M/Y) - Time (UTC, H:M:S)" + "\n")
                            for i, row in enumerate(self.data):
                                f.write(row[0] + "    " + row[1] + "           " + self.ut_data[i] + "\n")
                        else:
                            f.write("#HJD" + (" " * (len(self.data[0][0]))) + "#Mintype\n")
                            for row in self.data:
                                f.write(row[0] + "    " + row[1] + "\n")
                    msg.setText("Data file \"" + fi.fileName() + "\" saved.")
                    msg.setWindowTitle("PyWD - Data Saved")
                    msg.exec_()
                except:
                    msg.setText("An error has ocurred: \n" + str(sys.exc_info()[1]))
                    msg.exec_()


class OCWidget(QtGui.QWidget, ocwidget.Ui_OCWidget):
    def __init__(self):
        super(OCWidget, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(__icon_path__))
        self.MainWindow = None
        self.data_treewidget.header().setResizeMode(3)
        # set up plots
        self.plot_figure = Figure()
        self.plot_canvas = FigureCanvas(self.plot_figure)
        self.plot_toolbar = NavigationToolbar(self.plot_canvas, self.plot_widget)
        plot_layout = QtGui.QVBoxLayout()
        plot_layout.addWidget(self.plot_toolbar)
        plot_layout.addWidget(self.plot_canvas)
        self.plot_widget.setLayout(plot_layout)
        self.plotAxis = self.plot_figure.add_subplot(111)
        self.plotAxis.set_xlabel("HJD")
        self.plotAxis.set_ylabel("Day")
        self.plot_figure.tight_layout()
        # variables
        self.hjd = None
        self.linear = None
        self.dpdt = None
        # signal connection
        self.connectSignals()

    def connectSignals(self):
        self.compute_btn.clicked.connect(self.computeOC)
        self.linear_chk.stateChanged.connect(self.plotSelected)
        self.dpdt_chk.stateChanged.connect(self.plotSelected)
        self.export_btn.clicked.connect(self.exportData)

    def computeOC(self):
        if os.path.isfile(str(self.MainWindow.EclipseWidget.filepath_label.text())):
            self.data_treewidget.clear()
            lcin = classes.lcin(self.MainWindow)
            lcin.starPositions(jdphs="1")
            ktstep = "0"
            lcin.output = "6" + lcin.output[1:29] + " " + (" " * (5 - len(ktstep)) + ktstep) + lcin.output[29:]
            eclipseCurve = classes.Curve(str(self.MainWindow.EclipseWidget.filepath_label.text()))
            eclipse = []
            formatter = classes.WDInput()
            for jd, min in izip(eclipseCurve.timeList, eclipseCurve.observationList):
                eclipse.append(formatter.formatInput(jd, 14, 5, "F") + "     " + min)
            lcin.output = lcin.output.split("\n")
            lcin.output = lcin.output[:-1] + eclipse
            lcin.output.append("-10000.")
            lcin.output.append("9")
            output = ""
            for line in lcin.output:
                output = output + line + "\n"
            with open(self.MainWindow.lcinpath, "w") as f:
                f.write(output)
            process = subprocess.Popen(self.MainWindow.lcpath, cwd=os.path.dirname(self.MainWindow.lcpath))
            process.wait()
            table = methods.getTableFromOutput(self.MainWindow.lcoutpath, "eclipse timing   type", 2)

            self.hjd = []
            self.linear = []
            self.dpdt = []

            for row in table:
                item = QtGui.QTreeWidgetItem(self.data_treewidget)
                item.setText(0, row[0])
                self.hjd.append(float(row[0]))
                item.setText(1, row[3])
                self.linear.append(float(row[3]))
                item.setText(2, row[5])
                self.dpdt.append(float(row[5]))

            self.plotSelected()

        else:
            msg = QtGui.QMessageBox()
            msg.setWindowTitle("PyWD - Error")
            msg.setText("Please provide eclipse timings in the main menu before "
                        "attempting to calculate O - C residuals.")
            msg.exec_()

    def plotSelected(self):
        self.plotAxis.clear()

        if self.linear_chk.isChecked() and self.linear is not None:
            self.plotAxis.plot(self.hjd, self.linear, linestyle="", marker="o", markersize=4, color="#4286f4")

        if self.dpdt_chk.isChecked() and self.dpdt is not None:
            self.plotAxis.plot(self.hjd, self.dpdt, linestyle="", marker="o", markersize=4, color="#f73131")

        self.plotAxis.set_xlabel("HJD")
        self.plotAxis.set_ylabel("Day")
        self.plot_canvas.draw()
        self.plot_toolbar.update()

    def exportData(self):
        if self.hjd is not None and self.linear is not None and self.dpdt is not None:
            dialog = QtGui.QFileDialog(self)
            dialog.setDefaultSuffix("txt")
            dialog.setNameFilter("Plaintext File (*.txt)")
            dialog.setAcceptMode(1)
            returnCode = dialog.exec_()
            filePath = str((dialog.selectedFiles())[0])
            if filePath != "" and returnCode != 0:
                msg = QtGui.QMessageBox()
                fi = QtCore.QFileInfo(filePath)
                try:
                    with open(filePath, "w") as f:
                        f.write("#HJD            #Lin. Res. #with dP/dt\n")
                        for jd, ln, dt in izip(self.hjd, self.linear, self. dpdt):
                            f.write("{0:<13f}{1: >11f}{2: >11f}\n".format(jd, ln, dt))
                    msg.setText("Data file \"" + fi.fileName() + "\" saved.")
                    msg.setWindowTitle("PyWD - Data Saved")
                    msg.exec_()
                except:
                    msg.setText("An error has ocurred: \n" + str(sys.exc_info()[1]))
                    msg.exec_()


class LineProfileWidget(QtGui.QWidget, lineprofilewidget.Ui_LineProfileWidget):
    def __init__(self):
        super(LineProfileWidget, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(__icon_path__))
        self.MainWindow = None
        self.s1_data = None
        self.s2_data = None
        self.s1_treewidget.header().setResizeMode(3)
        self.s2_treewidget.header().setResizeMode(3)
        # set up plot
        self.plot_figure = Figure()
        self.plot_canvas = FigureCanvas(self.plot_figure)
        self.plot_toolbar = NavigationToolbar(self.plot_canvas, self.plot_widget)
        plot_layout = QtGui.QVBoxLayout()
        plot_layout.addWidget(self.plot_toolbar)
        plot_layout.addWidget(self.plot_canvas)
        self.plot_widget.setLayout(plot_layout)
        self.plotAxis = self.plot_figure.add_subplot(111)
        self.plotAxis.set_xlabel("Micron")
        self.plotAxis.set_ylabel("Flux")
        self.plot_figure.tight_layout()
        # signal connection
        self.connectSignals()

    def connectSignals(self):
        self.s1_add_btn.clicked.connect(partial(self.addWavelenghtToTree, self.s1_treewidget))
        self.s2_add_btn.clicked.connect(partial(self.addWavelenghtToTree, self.s2_treewidget))
        self.s1_remove_btn.clicked.connect(partial(self.removeWavelenghtFromTree, self.s1_treewidget))
        self.s2_remove_btn.clicked.connect(partial(self.removeWavelenghtFromTree, self.s2_treewidget))
        self.plot_btn.clicked.connect(self.plotData)
        self.export_btn.clicked.connect(self.exportData)

    def addWavelenghtToTree(self, treewidget):
        item = QtGui.QTreeWidgetItem(treewidget)
        item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
        item.setText(0, "0.656279")
        item.setText(1, "0.00001")
        item.setText(2, "0.5")
        item.setText(3, "0")

    def removeWavelenghtFromTree(self, treewidget):
        selectedItem = treewidget.selectedItems()
        if len(selectedItem) > 0:
            selectedItem = selectedItem[0]
            root = treewidget.invisibleRootItem()
            root.takeChild(root.indexOfChild(selectedItem))

    def plotData(self):
        lineprofile = ""
        lcin = classes.lcin(self.MainWindow)
        s1_root = self.s1_treewidget.invisibleRootItem()
        s2_root = self.s2_treewidget.invisibleRootItem()

        if self.s1_groupbox.isChecked() and s1_root.childCount() > 0:
            lineprofile = lineprofile + \
                          lcin.formatInput(self.s1_binwidth_spinbox.value(), 11, 5, "D") + \
                          lcin.formatInput(self.s1_contscale_spinbox.value(), 9, 4, "F") + \
                          lcin.formatInput(self.s1_contslope_spinbox.value(), 9, 2, "F") + \
                          (" " * (3 - len(str(self.s1_subgrid_spinbox.value()))) + str(self.s1_subgrid_spinbox.value())) + \
                          "\n"

            for i in range(s1_root.childCount()):
                item = s1_root.child(i)
                lineprofile = lineprofile + \
                              lcin.formatInput(item.text(0), 9, 6, "F") + \
                              lcin.formatInput(item.text(1), 12, 5, "D") + \
                              lcin.formatInput(item.text(2), 10, 5, "F") + \
                              (" " * (5 - len(item.text(3))) + item.text(3)) + \
                              "\n"
        else:
            # it wont matter what we print here if groupbox is not checked so we'll just use lcin.example default values
            lineprofile = lineprofile + "0.10000d-03 000.9900 -0005.00 03\n"

        lineprofile = lineprofile + "-1.\n"

        if self.s2_groupbox.isChecked() and s2_root.childCount() > 0:
            lineprofile = lineprofile + \
                          lcin.formatInput(self.s2_binwidth_spinbox.value(), 11, 5, "D") + \
                          lcin.formatInput(self.s2_contscale_spinbox.value(), 9, 4, "F") + \
                          lcin.formatInput(self.s2_contslope_spinbox.value(), 9, 2, "F") + \
                          (" " * (3 - len(str(self.s2_subgrid_spinbox.value()))) + str(self.s2_subgrid_spinbox.value())) + \
                          "\n"

            for i in range(s2_root.childCount()):
                item = s2_root.child(i)
                lineprofile = lineprofile + \
                              lcin.formatInput(item.text(0), 9, 6, "F") + \
                              lcin.formatInput(item.text(1), 12, 5, "D") + \
                              lcin.formatInput(item.text(2), 10, 5, "F") + \
                              (" " * (5 - len(item.text(3))) + item.text(3)) + \
                              "\n"
        else:
            lineprofile = lineprofile + "0.10000d-03 000.9900 -0005.00 03\n"

        lineprofile = lineprofile + "-1."

        if len(lineprofile.split("\n")) > 4:
            self.s1_data = None
            self.s2_data = None
            self.plotAxis.cla()
            # [jdstart, jdstop, jdincrement, phasestart, phasestop, phaseincrement, phasenorm, phobs, lsp, tobs]
            line3 = [50000, 51000, 0.001,
                     self.phase_spinbox.value(), self.phase_spinbox.value(), 0.1,
                     0.25,
                     self.MainWindow.phobs_ipt.text(), self.MainWindow.lsp_spinbox.value(), self.MainWindow.tavh_ipt.text()]
            lcin.starPositions(line3=line3, jdphs="2")
            lcin.output = "3" + lcin.output[1:]
            lcin.output = lcin.output.split("\n")
            lcin.output = lcin.output[:8] + list(lineprofile.split("\n")) + lcin.output[8:]
            output = ""
            for line in lcin.output:
                output = output + line + "\n"

            with open(self.MainWindow.lcinpath, "w") as f:
                f.write(output)
            process = subprocess.Popen(self.MainWindow.lcpath, cwd=os.path.dirname(self.MainWindow.lcpath))
            process.wait()

            if self.s1_groupbox.isChecked():

                s1_table = methods.getTableFromOutput(self.MainWindow.lcoutpath,
                                                      "                              star 1", offset=3)

                s1_x = [float(row[2]) for row in s1_table]
                s1_y = [float(row[3]) for row in s1_table]

                self.plotAxis.plot(s1_x, s1_y, color="#4286f4")

                self.s1_data = s1_x, s1_y

            if self.s2_groupbox.isChecked():
                s2_table = methods.getTableFromOutput(self.MainWindow.lcoutpath,
                                                      "                              star 2", offset=3)
                s2_x = [float(row[2]) for row in s2_table]
                s2_y = [float(row[3]) for row in s2_table]

                self.plotAxis.plot(s2_x, s2_y, color="#f73131")

                self.s2_data = s2_x, s2_y

            self.plotAxis.set_xlabel("Micron")
            self.plotAxis.set_ylabel("Flux")
            self.plot_canvas.draw()
            self.plot_toolbar.update()

    def exportData(self):
        def _tabulate(data, star):
            x = data[0]
            y = data[1]
            table = "#Wavelenght  #Flux --- #Star {0}\n".format(star)
            for wl, fx in izip(x, y):
                table = table + "{:0.7f}".format(wl) + "    " + "{:0.7f}".format(fx) + "\n"
            return table

        if self.s1_data is not None or self.s2_data is not None:
            dialog = QtGui.QFileDialog(self)
            dialog.setDefaultSuffix("txt")
            dialog.setNameFilter("Plaintext File (*.txt)")
            dialog.setAcceptMode(1)
            returnCode = dialog.exec_()
            filePath = str((dialog.selectedFiles())[0])
            if filePath != "" and returnCode != 0:
                msg = QtGui.QMessageBox()
                fi = QtCore.QFileInfo(filePath)
                try:
                    with open(filePath, "w") as f:
                        output = ""
                        if self.s1_data is not None:
                            output = output + _tabulate(self.s1_data, "1") + "\n"
                        if self.s2_data is not None:
                            output = output + _tabulate(self.s2_data, "2")
                        f.write(output)
                        msg.setText("Data file \"" + fi.fileName() + "\" saved.")
                        msg.setWindowTitle("PyWD - Data Saved")
                        msg.exec_()
                except:
                    msg.setText("An error has ocurred: \n" + str(sys.exc_info()[1]))
                    msg.exec_()


class HistoryWidget(QtGui.QWidget, historywidget.Ui_HistoryWidget):
    def __init__(self):
        super(HistoryWidget, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(__icon_path__))
        # variables
        self.MainWindow = None
        self.parameterList = []
        self.valueList = []
        self.stderrList = []
        self.history_treewidget.header().setResizeMode(3)
        # plot
        self.plot_figure = Figure()
        self.plot_canvas = FigureCanvas(self.plot_figure)
        self.plot_toolbar = NavigationToolbar(self.plot_canvas, self.plot_widget)
        plot_layout = QtGui.QVBoxLayout()
        plot_layout.addWidget(self.plot_toolbar)
        plot_layout.addWidget(self.plot_canvas)
        self.plot_widget.setLayout(plot_layout)
        self.plotAxis = self.plot_figure.add_subplot(111)
        self.plotAxis.set_xlabel("Iteration Number")
        self.plotAxis.set_ylabel("")
        self.plot_figure.tight_layout()
        # signal connection
        self.connectSignals()

    def connectSignals(self):
        self.clear_btn.clicked.connect(self.clearHistory)
        self.plot_btn.clicked.connect(self.plotSelected)

    def addIterationData(self, table):
        paramList = []
        valList = []
        errList = []

        for row in table:
            paramList.append(self.MainWindow.DCWidget.parameterDict[row[0]])
            valList.append(float(row[4].replace("D", "e")))
            errList.append(float(row[5].replace("D", "e")))

        if self.parameterList != paramList:
            self.clearHistory()
            self.parameterList = paramList
        else:
            pass

        self.valueList.append(valList)
        self.stderrList.append(errList)

        self.updateHistory()

        if self.auto_chk.isChecked():
            self.plot_btn.click()

    def updateHistory(self):
        idx = None
        selecteditems = self.history_treewidget.selectedItems()
        if len(selecteditems) > 0:
            selecteditem = selecteditems[0]
            idx = self.history_treewidget.invisibleRootItem().indexOfChild(selecteditem)

        self.history_treewidget.clear()
        header = QtGui.QTreeWidgetItem()
        header.setText(0, "Parameter")

        i = 1
        while i < len(self.valueList) + 1:
            header.setText(i, "Iteration {0}".format(i))
            i = i + 1

        for index, parameter in enumerate(self.parameterList):
            item = QtGui.QTreeWidgetItem(self.history_treewidget)
            item.setText(0, parameter)

            iteration = 1
            for value, error in izip(self.valueList, self.stderrList):
                item.setText(iteration, "{0} +/- {0}".format(value[index], error[index]))
                iteration = iteration + 1

            # t = 1
            # for value, error in izip(valueList, errorList):
            #     item.setText(t, "{0} +/- {1}".format(value, error))
            #     t = t + 1

        self.history_treewidget.setHeaderItem(header)

        if idx is not None:
            self.history_treewidget.invisibleRootItem().child(idx).setSelected(True)

    def clearHistory(self):
        header = QtGui.QTreeWidgetItem()
        header.setText(0, "Parameter")
        self.history_treewidget.setHeaderItem(header)

        self.parameterList = []
        self.valueList = []
        self.stderrList = []

        self.history_treewidget.clear()

        self.plotAxis.cla()
        self.plot_toolbar.update()
        self.plot_canvas.draw()

    def plotSelected(self):
        self.plotAxis.cla()

        selecteditems = self.history_treewidget.selectedItems()
        if len(selecteditems) > 0:
            selecteditem = selecteditems[0]
            index = self.history_treewidget.invisibleRootItem().indexOfChild(selecteditem)

            y = []
            y_err = []
            x = []
            i = 1
            for value, stderr in izip(self.valueList, self.stderrList):
                y.append(value[index])
                y_err.append(stderr[index])
                x.append(i)
                i = i + 1

            self.plotAxis.errorbar(x, y, yerr=y_err, linestyle="-", marker="o", markersize=4, color="#4286f4")
            self.plotAxis.set_xlabel("Iteration Number")
            self.plotAxis.set_ylabel("")
            self.plot_canvas.draw()
            self.plot_toolbar.update()


if __name__ == "__main__":
    pass
