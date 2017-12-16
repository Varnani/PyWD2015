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
        self.el3a = ""
        self.opsf = ""
        self.sigma = ""
        if type == "lc":
            self.noiseDict = {
                "None": "0",
                "Square Root": "1",
                "Linear": "2"
            }
            self.noise = ""
            self.wla = ""
            self.aextinc = ""
            self.xunit = ""
            self.calib = ""

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
        self.el3a = str(CurvePropertiesDialog.el3a_ipt.text())
        self.opsf = str(CurvePropertiesDialog.opsf_ipt.text())
        self.sigma = str(CurvePropertiesDialog.sigma_ipt.text())
        if CurvePropertiesDialog.type == "lc":
            self.type = "lc"
            self.noise = self.noiseDict[str(CurvePropertiesDialog.noise_combobox.currentText())]
            self.wla = str(CurvePropertiesDialog.wla_ipt.text())
            self.aextinc = str(CurvePropertiesDialog.aextinc_ipt.text())
            self.xunit = str(CurvePropertiesDialog.xunit_ipt.text())
            self.calib = str(CurvePropertiesDialog.calib_ipt.text())
        else:
            self.type = "vc"

    def populateFromProjectFile(self, project):
        pass


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
            self.error = "An IO error has been caught:\n" + ex.strerror + filePath


if __name__ == "__main__":
    pass
