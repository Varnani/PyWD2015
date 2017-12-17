from itertools import izip


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


class dcin:
    def __init__(self):
        self.output = ""  # ready-to-write dcin.active file
        self.warning = ""  # stored warnings
        self.error = ""  # caught error
        self.hasWarning = False
        self.hasError = False

    def addWarning(self, warning):
        self.warning = self.warning + "\n" + warning + "\n"
        self.hasWarning = True

    def addError(self, error):
        self.error = self.error + "\n" + error + "\n"
        self.hasError = True
        self.output = ""


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
            for time, observation, weight in izip(self.timeList, self.observationList, self.weightList):
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


if __name__ == "__main__":
    pass
