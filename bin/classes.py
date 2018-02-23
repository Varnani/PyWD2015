import itertools
import subprocess
import os
import sys
import numpy as np
from PyQt4 import QtCore


class CurveProperties:
    def __init__(self, type):
        self.type = type
        self.FilePath = ""
        self.band = ""
        self.ksd = ""
        self.l1 = ""
        self.l2 = ""
        self.x1 = ""
        self.x2 = ""
        self.y1 = ""
        self.y2 = ""
        self.e1 = ""
        self.e2 = ""
        self.e3 = ""
        self.e4 = ""
        self.wla = ""
        self.opsf = ""
        self.sigma = ""
        if type == "lc":
            self.noiseDict = {
                "None": "0",
                "Square Root": "1",
                "Linear": "2"
            }
            self.noise = ""
            self.el3a = ""
            self.aextinc = ""
            self.xunit = ""
            self.calib = ""
        if type == "vc":
            self.star = 0

    def populateFromInterface(self, CurvePropertiesDialog):
        self.FilePath = str(CurvePropertiesDialog.filepath_label.text())
        self.band = str(CurvePropertiesDialog.band_box.value())
        self.ksd = str(CurvePropertiesDialog.ksd_box.value())
        self.l1 = str(CurvePropertiesDialog.l1_ipt.text())
        self.l2 = str(CurvePropertiesDialog.l2_ipt.text())
        self.x1 = str(CurvePropertiesDialog.x1_ipt.text())
        self.x2 = str(CurvePropertiesDialog.x2_ipt.text())
        self.y1 = str(CurvePropertiesDialog.y1_ipt.text())
        self.y2 = str(CurvePropertiesDialog.y2_ipt.text())
        self.e1 = str(CurvePropertiesDialog.e1_ipt.text())
        self.e2 = str(CurvePropertiesDialog.e2_ipt.text())
        self.e3 = str(CurvePropertiesDialog.e3_ipt.text())
        self.e4 = str(CurvePropertiesDialog.e4_ipt.text())
        self.wla = str(CurvePropertiesDialog.wla_ipt.text())
        self.opsf = str(CurvePropertiesDialog.opsf_ipt.text())
        self.sigma = str(CurvePropertiesDialog.sigma_ipt.text())
        if CurvePropertiesDialog.type == "lc":
            self.type = "lc"
            self.noise = self.noiseDict[str(CurvePropertiesDialog.noise_combobox.currentText())]
            self.el3a = str(CurvePropertiesDialog.el3a_ipt.text())
            self.aextinc = str(CurvePropertiesDialog.aextinc_ipt.text())
            self.xunit = str(CurvePropertiesDialog.xunit_ipt.text())
            self.calib = str(CurvePropertiesDialog.calib_ipt.text())
        if CurvePropertiesDialog.type == "vc":
            self.type = "vc"

    def populateFromParserSection(self, parser, section):
        self.FilePath = parser.get(section, "filepath")
        self.band = parser.get(section, "band")
        self.ksd = parser.get(section, "ksd")
        self.l1 = parser.get(section, "l1")
        self.l2 = parser.get(section, "l2")
        self.x1 = parser.get(section, "x1")
        self.x2 = parser.get(section, "x2")
        self.y1 = parser.get(section, "y1")
        self.y2 = parser.get(section, "y2")
        self.e1 = parser.get(section, "e1")
        self.e2 = parser.get(section, "e2")
        self.e3 = parser.get(section, "e3")
        self.e4 = parser.get(section, "e4")
        self.wla = parser.get(section, "wla")
        self.opsf = parser.get(section, "opsf")
        self.sigma = parser.get(section, "sigma")
        if self.type == "lc":
            self.noise = parser.get(section, "noise")
            self.el3a = parser.get(section, "el3a")
            self.aextinc = parser.get(section, "aextinc")
            self.xunit = parser.get(section, "xunit")
            self.calib = parser.get(section, "calib")
        if self.type == "vc":
            self.star = parser.getint(section, "star")


class WDInput:
    def __init__(self):
        pass

    def formatEcc(self, ipt):
        f_ipt = float(ipt)
        if f_ipt > 1 or f_ipt < 0:
            raise ValueError("Invalid eccentricity value: " + ipt)
        else:
            output = "{:6.5f}".format(f_ipt)
            return output[1:]

    def formatInput(self, ipt, width, precision, exponent, isDeg=False):
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

    def evalCheckBox(self, checkBox):
        if checkBox.isChecked():
            return "1"
        else:
            return "0"


class dcin(WDInput):
    def __init__(self, MainWindow):
        WDInput.__init__(self)
        self.output = ""  # ready-to-write dcin.active file
        self.warning = ""  # stored warnings
        self.error = ""  # caught error
        self.hasWarning = False
        self.hasError = False
        self.fill(MainWindow)

    def addWarning(self, warning):
        self.warning = self.warning + "\n" + warning + "\n"
        self.hasWarning = True

    def addError(self, error):
        self.error = self.error + "\n" + error + "\n"
        self.hasError = True
        self.output = ""
    
    def formatDel(self, ipt):  # only used in dcin.active
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

    def formatKeep(self, keep):  # only used in dcin.active
        if keep.isChecked():
            return "0"
        else:
            return "1"

    def fill(self, MainWindow):
        try:
            vunit = float(MainWindow.vunit_ipt.text())
            if vunit != float(1):
                warning = "VUnit parameter is different than 1:" + \
                          "\nVGamma, velocity curve sigmas and all velocity observations " + \
                          "will be divided by VUnit, as it is required by DC program.\n" + \
                          "Make sure you provide these parameters normally, not in [Parameter/VUnit] format."
                self.addWarning(warning)
            
            if float(MainWindow.tavh_ipt.text()) < float(1000) or float(MainWindow.tavc_ipt.text()) < float(1000):
                warning = "Entered surface temperature value is lower than 1000 Kelvin:" + \
                          "\nKeep in mind that surface temperature parameters will be " + \
                          "divided by 10,000 before writing into dcin.active file, as it is required by DC program." + \
                          "\nMake sure you provide surface temperatures normally, not in [T/10,000] format."
                self.addWarning(warning)

            line1 = " {0} {1} {2} {3} {4} {5} {6} {7}\n".format(
                self.formatDel(MainWindow.DCWidget.del_s1lat_ipt.text()),
                self.formatDel(MainWindow.DCWidget.del_s1lng_ipt.text()),
                self.formatDel(MainWindow.DCWidget.del_s1agrad_ipt.text()),
                self.formatDel(MainWindow.DCWidget.del_s1tmpf_ipt.text()),
                self.formatDel(MainWindow.DCWidget.del_s2lat_ipt.text()),
                self.formatDel(MainWindow.DCWidget.del_s2lng_ipt.text()),
                self.formatDel(MainWindow.DCWidget.del_s2agrad_ipt.text()),
                self.formatDel(MainWindow.DCWidget.del_s2tmpf_ipt.text())
            )
            line2 = " {0} {1} {2} {3} {4} {5} {6} {7} {8} {9} {10}\n".format(
                self.formatDel(MainWindow.DCWidget.del_a_ipt.text()),
                self.formatDel(MainWindow.DCWidget.del_e_ipt.text()),
                self.formatDel(MainWindow.DCWidget.del_perr0_ipt.text()),
                self.formatDel(MainWindow.DCWidget.del_f1_ipt.text()),
                self.formatDel(MainWindow.DCWidget.del_f2_ipt.text()),
                self.formatDel(MainWindow.DCWidget.del_pshift_ipt.text()),
                self.formatDel(MainWindow.DCWidget.del_i_ipt.text()),
                self.formatDel(MainWindow.DCWidget.del_g1_ipt.text()),
                self.formatDel(MainWindow.DCWidget.del_g2_ipt.text()),
                self.formatDel(MainWindow.DCWidget.del_t1_ipt.text()),
                self.formatDel(MainWindow.DCWidget.del_t2_ipt.text())
            )
            line3 = " {0} {1} {2} {3} {4} {5} {6} {7} {8}\n".format(
                self.formatDel(MainWindow.DCWidget.del_alb1_ipt.text()),
                self.formatDel(MainWindow.DCWidget.del_alb2_ipt.text()),
                self.formatDel(MainWindow.DCWidget.del_pot1_ipt.text()),
                self.formatDel(MainWindow.DCWidget.del_pot2_ipt.text()),
                self.formatDel(MainWindow.DCWidget.del_q_ipt.text()),
                self.formatDel(MainWindow.DCWidget.del_l1_ipt.text()),
                self.formatDel(MainWindow.DCWidget.del_l2_ipt.text()),
                self.formatDel(MainWindow.DCWidget.del_x1_ipt.text()),
                self.formatDel(MainWindow.DCWidget.del_x2_ipt.text())
            )
            block1 = "{0}{1}{2}{3}".format(
                self.formatKeep(MainWindow.DCWidget.s1lat_chk),
                self.formatKeep(MainWindow.DCWidget.s1long_chk),
                self.formatKeep(MainWindow.DCWidget.s1rad_chk),
                self.formatKeep(MainWindow.DCWidget.s1temp_chk),
            )
            block2 = "{0}{1}{2}{3}".format(
                self.formatKeep(MainWindow.DCWidget.s2lat_chk),
                self.formatKeep(MainWindow.DCWidget.s2long_chk),
                self.formatKeep(MainWindow.DCWidget.s2rad_chk),
                self.formatKeep(MainWindow.DCWidget.s2temp_chk)
            )
            block3 = "{0}{1}{2}{3}{4}{5}{6}".format(
                self.formatKeep(MainWindow.DCWidget.a_chk),
                self.formatKeep(MainWindow.DCWidget.e_chk),
                self.formatKeep(MainWindow.DCWidget.perr0_chk),
                self.formatKeep(MainWindow.DCWidget.f1_chk),
                self.formatKeep(MainWindow.DCWidget.f2_chk),
                self.formatKeep(MainWindow.DCWidget.pshift_chk),
                self.formatKeep(MainWindow.DCWidget.vgam_chk)
            )
            block4 = "{0}{1}{2}{3}{4}".format(
                self.formatKeep(MainWindow.DCWidget.incl_chk),
                self.formatKeep(MainWindow.DCWidget.g1_chk),
                self.formatKeep(MainWindow.DCWidget.g2_chk),
                self.formatKeep(MainWindow.DCWidget.t1_chk),
                self.formatKeep(MainWindow.DCWidget.t2_chk)
            )
            block5 = "{0}{1}{2}{3}{4}".format(
                self.formatKeep(MainWindow.DCWidget.alb1_chk),
                self.formatKeep(MainWindow.DCWidget.alb2_chk),
                self.formatKeep(MainWindow.DCWidget.pot1_chk),
                self.formatKeep(MainWindow.DCWidget.pot2_chk),
                self.formatKeep(MainWindow.DCWidget.q_chk)
            )
            block6 = "{0}{1}{2}{3}{4}".format(
                self.formatKeep(MainWindow.DCWidget.jd0_chk),
                self.formatKeep(MainWindow.DCWidget.p0_chk),
                self.formatKeep(MainWindow.DCWidget.dpdt_chk),
                self.formatKeep(MainWindow.DCWidget.dperdt_chk),
                self.formatKeep(MainWindow.DCWidget.a3b_chk),
            )
            block7 = "{0}{1}{2}{3}{4}".format(
                self.formatKeep(MainWindow.DCWidget.p3b_chk),
                self.formatKeep(MainWindow.DCWidget.xinc3b_chk),
                self.formatKeep(MainWindow.DCWidget.e3b_chk),
                self.formatKeep(MainWindow.DCWidget.perr3b_chk),
                self.formatKeep(MainWindow.DCWidget.tc3b_chk),
            )
            block8 = "11111"  # unused block
            block9 = "{0}{1}{2}{3}{4}".format(
                self.formatKeep(MainWindow.DCWidget.logd_chk),
                self.formatKeep(MainWindow.DCWidget.desextinc_chk),
                self.formatKeep(MainWindow.DCWidget.s1tstart_chk),
                self.formatKeep(MainWindow.DCWidget.s1tmax1_chk),
                self.formatKeep(MainWindow.DCWidget.s1tmax2_chk),
            )
            block10 = "{0}{1}{2}{3}{4}".format(
                self.formatKeep(MainWindow.DCWidget.s1tend_chk),
                self.formatKeep(MainWindow.DCWidget.s2tstart_chk),
                self.formatKeep(MainWindow.DCWidget.s2tmax1_chk),
                self.formatKeep(MainWindow.DCWidget.s2tmax2_chk),
                self.formatKeep(MainWindow.DCWidget.s2tend_chk)
            )
            block11 = "11111"  # unused block
            block12 = "{0}{1}{2}{3}{4}".format(
                self.formatKeep(MainWindow.DCWidget.l1_chk),
                self.formatKeep(MainWindow.DCWidget.l2_chk),
                self.formatKeep(MainWindow.DCWidget.x1_chk),
                self.formatKeep(MainWindow.DCWidget.x2_chk),
                self.formatKeep(MainWindow.DCWidget.el3_chk)
            )
            marqmul = ("0" * (2 - len(str(MainWindow.DCWidget.marqmul_spinbox.value())))) + str(
                MainWindow.DCWidget.marqmul_spinbox.value())
            line4 = " " + block1 + " " + block2 + " " + block3 + " " + block4 + " " + block5 + \
                    " " + block6 + " " + block7 + " " + block8 + " " + block9 + " " + block10 + \
                    " " + block11 + " " + block12 + " 01 1.000d-" + marqmul + \
                    self.formatInput(MainWindow.DCWidget.vlr_spinbox.value(), 6, 3, "F") + "\n"
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
                    + " " + self.evalCheckBox(MainWindow.EclipseWidget.iftime_chk) + " 2" + " 0" + " " + \
                    isymDict[str(MainWindow.isym_combobox.currentText())] + " 1" + " " + \
                    self.evalCheckBox(MainWindow.DCWidget.ifder_chk) + " " + "1" \
                    + " " + self.evalCheckBox(MainWindow.DCWidget.ifoc_chk) + "\n"
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
            line7 = str(MainWindow.nref_spinbox.value()) + " " + self.evalCheckBox(MainWindow.mref_chk) + " " \
                    + self.evalCheckBox(MainWindow.SpotConfigureWidget.ifsmv1_chk) + " " \
                    + self.evalCheckBox(MainWindow.SpotConfigureWidget.ifsmv2_chk) + " " \
                    + self.evalCheckBox(MainWindow.icor1_chk) + " " + self.evalCheckBox(MainWindow.icor2_chk) + " " \
                    + self.evalCheckBox(MainWindow.if3b_chk) \
                    + " " + ld1 + " " + ld2 + " " \
                    + self.evalCheckBox(MainWindow.SpotConfigureWidget.kspev_chk) + " " \
                    + self.evalCheckBox(MainWindow.SpotConfigureWidget.kspot_chk) + " " \
                    + nomaxDict[str(MainWindow.SpotConfigureWidget.nomax_combobox.currentText())] + " " \
                    + self.evalCheckBox(MainWindow.ifcgs_chk) + " " \
                    + magliteDict[str(MainWindow.maglite_combobox.currentText())] + " " \
                    + str(MainWindow.linkext_spinbox.value()) + " " \
                    + self.formatInput(MainWindow.desextinc_ipt.text(), 7, 4, "F") + "\n"

            jdDict = {
                "Time": "1",
                "Phase": "2"
            }

            nga = " " * (3 - len(str(MainWindow.nga_spinbox.value()))) + str(MainWindow.nga_spinbox.value())

            line8 = jdDict[str(MainWindow.jdphs_combobox.currentText())] + \
                    self.formatInput(MainWindow.jd0_ipt.text(), 15, 6, "F") + \
                    self.formatInput(MainWindow.p0_ipt.text(), 17, 10, "D") + \
                    self.formatInput(MainWindow.dpdt_ipt.text(), 14, 6, "D") + \
                    self.formatInput(MainWindow.pshift_ipt.text(), 10, 5, "F") + \
                    self.formatInput(MainWindow.delph_ipt.text(), 8, 5, "F") + nga + "\n"

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

            line9 = modeDict[str(MainWindow.mode_combobox.currentText())] + " " + \
                    self.evalCheckBox(MainWindow.ipb_chk) + \
                    ifatDict[str(MainWindow.ifat1_combobox.currentText())] + \
                    ifatDict[str(MainWindow.ifat2_combobox.currentText())] + n1 + n2 + n1l + n2l + \
                    self.formatInput(MainWindow.perr0_ipt.text(), 13, 6, "F", isDeg=True) + \
                    self.formatInput(MainWindow.dperdt_ipt.text(), 13, 5, "D") + \
                    self.formatInput(MainWindow.the_ipt.text(), 8, 5, "F") + \
                    self.formatInput(MainWindow.vunit_ipt.text(), 9, 3, "F") + "\n"

            line10 = self.formatEcc(MainWindow.e_ipt.text()) + self.formatInput(MainWindow.a_ipt.text(), 13, 6, "D") + \
                     self.formatInput(MainWindow.f1_ipt.text(), 10, 4, "F") + \
                     self.formatInput(MainWindow.f2_ipt.text(), 10, 4, "F") + \
                     self.formatInput((float(MainWindow.vgam_ipt.text()) / vunit), 10, 4, "F") + \
                     self.formatInput(MainWindow.xincl_ipt.text(), 9, 3, "F") + \
                     self.formatInput(MainWindow.gr1_spinbox.value(), 7, 3, "F") + \
                     self.formatInput(MainWindow.gr2_spinbox.value(), 7, 3, "F") + \
                     self.formatInput(MainWindow.abunin_ipt.text(), 7, 2, "F") + \
                     self.formatInput(MainWindow.SpotConfigureWidget.fspot1_ipt.text(), 10, 4, "F") + \
                     self.formatInput(MainWindow.SpotConfigureWidget.fspot2_ipt.text(), 10, 4, "F") + "\n"

            line11 = self.formatInput(float(MainWindow.tavh_ipt.text()) / 10000.0, 7, 4, "F") + \
                     self.formatInput(float(MainWindow.tavc_ipt.text()) / 10000.0, 8, 4, "F") + \
                     self.formatInput(MainWindow.alb1_spinbox.value(), 7, 3, "F") + \
                     self.formatInput(MainWindow.alb2_spinbox.value(), 7, 3, "F") + \
                     self.formatInput(MainWindow.phsv_ipt.text(), 13, 6, "D") + \
                     self.formatInput(MainWindow.pcsv_ipt.text(), 13, 6, "D") + \
                     self.formatInput(MainWindow.rm_ipt.text(), 13, 6, "D") + \
                     self.formatInput(MainWindow.xbol1_ipt.text(), 7, 3, "F") + \
                     self.formatInput(MainWindow.xbol2_ipt.text(), 7, 3, "F") + \
                     self.formatInput(MainWindow.ybol1_ipt.text(), 7, 3, "F") + \
                     self.formatInput(MainWindow.ybol2_ipt.text(), 7, 3, "F") + \
                     self.formatInput(MainWindow.dpclog_ipt.text(), 9, 5, "F") + "\n"

            line12 = self.formatInput(MainWindow.a3b_ipt.text(), 12, 6, "D") + \
                     self.formatInput(MainWindow.p3b_ipt.text(), 14, 7, "D") + \
                     self.formatInput(MainWindow.xinc3b_ipt.text(), 11, 5, "F") + \
                     self.formatInput(MainWindow.e3b_ipt.text(), 9, 6, "F") + \
                     self.formatInput(MainWindow.perr3b_ipt.text(), 10, 7, "F", isDeg=True) + \
                     self.formatInput(MainWindow.tc3b_ipt.text(), 17, 8, "F") + "\n"

            vclines = ""
            vcList = []
            if ifvc1 == "1":
                vcList.append(MainWindow.LoadWidget.vcPropertiesList[0])
            if ifvc2 == "1":
                vcList.append(MainWindow.LoadWidget.vcPropertiesList[1])
            if len(vcList) != 0:
                for vcprop in vcList:
                    iband = (" " * (3 - len(vcprop.band))) + vcprop.band
                    vclines = vclines + iband + self.formatInput(vcprop.l1, 13, 6, "D") \
                              + self.formatInput(vcprop.l2, 13, 6, "D") \
                              + self.formatInput(vcprop.x1, 7, 3, "F") \
                              + self.formatInput(vcprop.x2, 7, 3, "F") \
                              + self.formatInput(vcprop.y1, 7, 3, "F") \
                              + self.formatInput(vcprop.y2, 7, 3, "F") \
                              + self.formatInput(vcprop.opsf, 10, 3, "D") \
                              + self.formatInput(float(vcprop.sigma) / vunit, 12, 5, "D") \
                              + self.formatInput(vcprop.e1, 8, 5, "F") \
                              + self.formatInput(vcprop.e2, 8, 5, "F") \
                              + self.formatInput(vcprop.e3, 8, 5, "F") \
                              + self.formatInput(vcprop.e4, 8, 5, "F") \
                              + self.formatInput(vcprop.wla, 10, 6, "F") + " " + vcprop.ksd + "\n"

            lclines = ""
            lcextralines = ""
            if len(MainWindow.LoadWidget.lcPropertiesList) != 0:
                lcparamsList = []
                lcextraparamsList = []
                for lcprop in MainWindow.LoadWidget.lcPropertiesList:
                    iband = (" " * (3 - len(lcprop.band))) + lcprop.band
                    lcparams = iband + self.formatInput(lcprop.l1, 13, 6, "F") + \
                               self.formatInput(lcprop.l2, 13, 6, "F") + \
                               self.formatInput(lcprop.x1, 7, 3, "F") + \
                               self.formatInput(lcprop.x2, 7, 3, "F") + \
                               self.formatInput(lcprop.y1, 7, 3, "F") + \
                               self.formatInput(lcprop.y2, 7, 3, "F") + \
                               self.formatInput(lcprop.el3a, 12, 4, "D") + self.formatInput(lcprop.opsf, 10, 3, "D") + " " + \
                               lcprop.noise + self.formatInput(lcprop.sigma, 12, 5, "D") + \
                               self.formatInput(lcprop.e1, 8, 5, "F") + \
                               self.formatInput(lcprop.e2, 8, 5, "F") + \
                               self.formatInput(lcprop.e3, 8, 5, "F") + \
                               self.formatInput(lcprop.e4, 8, 5, "F") + " " + lcprop.ksd + "\n"
                    lcextraparams = self.formatInput(lcprop.wla, 9, 6, "F") + \
                                    self.formatInput(lcprop.aextinc, 8, 4, "F") + \
                                    self.formatInput(lcprop.xunit, 11, 4, "D") + \
                                    self.formatInput(lcprop.calib, 12, 5, "D") + "\n"
                    lcparamsList.append(lcparams)
                    lcextraparamsList.append(lcextraparams)
                for lcparams in lcparamsList:
                    lclines = lclines + lcparams
                for lcextraparams in lcextraparamsList:
                    lcextralines = lcextralines + lcextraparams
            eclipseline = ""
            if MainWindow.EclipseWidget.iftime_chk.isChecked():
                eclipseline = (" " * 82) + \
                              self.formatInput(MainWindow.EclipseWidget.sigma_ipt.text(), 11, 5, "D") + \
                              (" " * 32) + \
                              " " + str(MainWindow.EclipseWidget.ksd_box.value()) + "\n"

            star1spotline = ""
            star2spotline = ""
            if MainWindow.SpotConfigureWidget.star1RowCount != 0:
                star1spotparams = MainWindow.SpotConfigureWidget.star1ElementList
                for spot in star1spotparams:
                    star1spotline = star1spotline + \
                                    self.formatInput(spot[3].text(), 9, 5, "F") + \
                                    self.formatInput(spot[4].text(), 9, 5, "F") + \
                                    self.formatInput(spot[5].text(), 9, 5, "F") + \
                                    self.formatInput(spot[6].text(), 9, 5, "F") + \
                                    self.formatInput(spot[7].text(), 14, 5, "F") + \
                                    self.formatInput(spot[8].text(), 14, 5, "F") + \
                                    self.formatInput(spot[9].text(), 14, 5, "F") + \
                                    self.formatInput(spot[10].text(), 14, 5, "F") + "\n"

            if MainWindow.SpotConfigureWidget.star2RowCount != 0:
                star2spotparams = MainWindow.SpotConfigureWidget.star2ElementList
                for spot in star2spotparams:
                    star2spotline = star2spotline + \
                                    self.formatInput(spot[3].text(), 9, 5, "F") + \
                                    self.formatInput(spot[4].text(), 9, 5, "F") + \
                                    self.formatInput(spot[5].text(), 9, 5, "F") + \
                                    self.formatInput(spot[6].text(), 9, 5, "F") + \
                                    self.formatInput(spot[7].text(), 14, 5, "F") + \
                                    self.formatInput(spot[8].text(), 14, 5, "F") + \
                                    self.formatInput(spot[9].text(), 14, 5, "F") + \
                                    self.formatInput(spot[10].text(), 14, 5, "F") + "\n"
            vc1dataline = ""
            if ifvc1 == "1":
                vc1prop = Curve(MainWindow.LoadWidget.vcPropertiesList[0].FilePath)
                if vc1prop.hasError:
                    self.addError(vc1prop.error)
                else:
                    for time, observation, weight in itertools.izip(vc1prop.timeList,
                                                                    vc1prop.observationList,
                                                                    vc1prop.weightList):
                        vc1dataline = vc1dataline + \
                                      self.formatInput(time, 14, 5, "F") + \
                                      self.formatInput((float(observation) / vunit), 11, 6, "F") + \
                                      self.formatInput(weight, 8, 3, "F") + "\n"
                vc1dataline = vc1dataline + "  -10001.00000\n"
            vc2dataline = ""
            if ifvc2 == "1":
                vc2prop = Curve(MainWindow.LoadWidget.vcPropertiesList[1].FilePath)
                if vc2prop.hasError:
                    self.addError(vc2prop.error)
                else:
                    for time, observation, weight in itertools.izip(vc2prop.timeList,
                                                                    vc2prop.observationList,
                                                                    vc2prop.weightList):
                        vc2dataline = vc2dataline + \
                                      self.formatInput(time, 14, 5, "F") + \
                                      self.formatInput((float(observation) / vunit), 11, 6, "F") + \
                                      self.formatInput(weight, 8, 3, "F") + "\n"
                vc2dataline = vc2dataline + "  -10001.00000\n"

            lcdataline = ""
            if len(MainWindow.LoadWidget.lcPropertiesList) != 0:
                for lcprop in MainWindow.LoadWidget.lcPropertiesList:
                    curve = Curve(lcprop.FilePath)
                    if curve.hasError:
                        self.addError(curve.error)
                    else:
                        for time, observation, weight in itertools.izip(curve.timeList,
                                                                        curve.observationList,
                                                                        curve.weightList):
                            lcdataline = lcdataline + self.formatInput(time, 14, 5, "F") + \
                                         self.formatInput(observation, 11, 6, "F") + \
                                         self.formatInput(weight, 8, 3, "F") + "\n"
                    lcdataline = lcdataline + "  -10001.00000\n"

            ecdataline = ""
            if MainWindow.EclipseWidget.filepath_label.text() != "None" \
                    and MainWindow.EclipseWidget.iftime_chk.isChecked():
                curve = Curve(MainWindow.EclipseWidget.filepath_label.text())
                if curve.hasError:
                    self.addError(curve.error)
                else:
                    for time, mintype, weight in itertools.izip(curve.timeList,
                                                                curve.observationList,
                                                                curve.weightList):
                        ecdataline = ecdataline + \
                                     self.formatInput(time, 14, 5, "F") + (" " * 5 + mintype) + \
                                     self.formatInput(weight, 13, 3, "F") + "\n"
                ecdataline = ecdataline + "  -10001.00000\n"

            self.output = line1 + line2 + line3 + line4 + line5 + line6 + line7 + line8 + line9 + line10 + line11 + line12 \
                          + vclines + lclines + eclipseline + lcextralines + \
                          star1spotline + "300.00000\n" + star2spotline + "300.00000\n" + \
                          "150.\n" + vc1dataline + vc2dataline + lcdataline + \
                          ecdataline + " 2\n"
            if vc1dataline == "" and vc2dataline == "":
                self.addWarning("There aren't any velocity curves loaded.")
            if lcdataline == "":
                self.addWarning("There aren't any light curves loaded.")
            if MainWindow.EclipseWidget.iftime_chk.isChecked() and ecdataline == "":
                self.addWarning("IFTIME is checked, but eclipse timings are not provided.")

        except ValueError as ex:
            self.addError("Value Error - Can't cast input into a numeric value: \n" + ex.message)
        except IndexError as ex:
            self.addError("Wrong Input: \n" + ex.message)
        except:
            self.addError("Unknown exception has been caught. This is most likely a programming error: \n" +
                          str(sys.exc_info()))


class Curve:
    def __init__(self, filePath):
        self.timeList = []
        self.observationList = []
        self.weightList = []
        self.lines = []
        self.filepath = filePath
        self.hasError = False
        self.error = ""
        self.parseFile(filePath)

    def validateData(self):
        try:
            for time, observation, weight in itertools.izip(self.timeList, self.observationList, self.weightList):
                float(time)
                float(observation)
                float(weight)
        except ValueError as ex:
            self.hasError = True
            self.error = "File has data that can't be parsed into a numerical value:\n" + \
                         self.filepath + "\n" + ex.message

    def parseFile(self, filePath):
        try:
            with open(filePath) as data:
                for line in data:
                    i = line.split()
                    if len(i) is not 0:
                        self.lines.append(i)
            self.timeList = [x[0] for x in self.lines]
            self.observationList = [x[1] for x in self.lines]
            self.weightList = [x[2] for x in self.lines]
            self.validateData()
        except IndexError:
            self.hasError = True
            self.error = "File is not a valid data source:\n" + filePath
        except IOError as ex:
            self.hasError = True
            self.error = "An IO error has been caught:\n" + ex.strerror + " " + filePath


class IteratorThread(QtCore.QThread):
    exception = QtCore.pyqtSignal(str, name="exception")

    def __init__(self, binarypath):
        QtCore.QThread.__init__(self)
        self.binarypath = binarypath
        self.cwd = os.path.dirname(binarypath)
        self.iteration = None
        self.connect(self, QtCore.SIGNAL("terminated()"), self.stop)

    def exit(self, returnCode=0):  # should not be called manually
        self.stop()
        QtCore.QThread.exit(self, returnCode=returnCode)

    def stop(self):
        self.blockSignals(True)
        try:
            self.iteration.kill()
        except:
            pass

    def run(self):
        try:
            if os.path.isfile(self.binarypath) is not True:
                raise RuntimeError("Binary does not exists in path: " + self.binarypath)
            self.iteration = subprocess.Popen(self.binarypath, cwd=self.cwd)
            self.iteration.wait()
        except RuntimeError as ex:
            self.exception.emit(ex.message)
            self.blockSignals(True)
        except:
            self.exception.emit(str(sys.exc_info()))
            self.blockSignals(True)


# class bidict(dict):
# this could be useful in the future
#     def __init__(self):
#         dict.__init__(self)
#         self.reverse = dict()
#
#     def __setitem__(self, key, value):
#         self.reverse[value] = key
#         dict.__setitem__(self, key, value)
#
#     def __delitem__(self, key):
#         self.reverse.__delitem__(key)
#         dict.__delitem__(self, key)


if __name__ == "__main__":
    pass
