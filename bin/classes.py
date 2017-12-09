from itertools import izip

class LightCurveProperties:
    def __init__(self, EditLightCurveDialog):
        self.FilePath = str(EditLightCurveDialog.filepath_label.text())
        self.band = str(EditLightCurveDialog.band_box.text())
        self.ksd = str(EditLightCurveDialog.ksd_box.text())
        self.l1 = str(EditLightCurveDialog.l1_ipt.text())
        self.l2 = str(EditLightCurveDialog.l2_ipt.text())
        self.x1 = str(EditLightCurveDialog.x1_ipt.text())
        self.x2 = str(EditLightCurveDialog.x2_ipt.text())
        self.y1 = str(EditLightCurveDialog.y1_ipt.text())
        self.y2 = str(EditLightCurveDialog.y2_ipt.text())
        self.e1 = str(EditLightCurveDialog.e1_ipt.text())
        self.e2 = str(EditLightCurveDialog.e2_ipt.text())
        self.e3 = str(EditLightCurveDialog.e3_ipt.text())
        self.e4 = str(EditLightCurveDialog.e4_ipt.text())
        self.el3a = str(EditLightCurveDialog.el3a_ipt.text())
        self.opsf = str(EditLightCurveDialog.opsf_ipt.text())
        self.sigma = str(EditLightCurveDialog.sigma_ipt.text())
        noiseDict = {
            "None": "0",
            "Square Root": "1",
            "Linear": "2"
        }
        self.noise = noiseDict[str(EditLightCurveDialog.noise_combobox.currentText())]
        self.wla = str(EditLightCurveDialog.wla_ipt.text())
        self.aextinc = str(EditLightCurveDialog.aextinc_ipt.text())
        self.xunit = str(EditLightCurveDialog.xunit_ipt.text())
        self.calib = str(EditLightCurveDialog.calib_ipt.text())


class VelocityCurveProperties:
    def __init__(self, EditVelocityCurveDialog):
        self.FilePath = str(EditVelocityCurveDialog.filepath_label.text())
        self.band = str(EditVelocityCurveDialog.band_box.text())
        self.ksd = str(EditVelocityCurveDialog.ksd_box.text())
        self.l1 = str(EditVelocityCurveDialog.l1_ipt.text())
        self.l2 = str(EditVelocityCurveDialog.l2_ipt.text())
        self.x1 = str(EditVelocityCurveDialog.x1_ipt.text())
        self.x2 = str(EditVelocityCurveDialog.x2_ipt.text())
        self.y1 = str(EditVelocityCurveDialog.y1_ipt.text())
        self.y2 = str(EditVelocityCurveDialog.y2_ipt.text())
        self.e1 = str(EditVelocityCurveDialog.e1_ipt.text())
        self.e2 = str(EditVelocityCurveDialog.e2_ipt.text())
        self.e3 = str(EditVelocityCurveDialog.e3_ipt.text())
        self.e4 = str(EditVelocityCurveDialog.e4_ipt.text())
        self.wla = str(EditVelocityCurveDialog.wla_ipt.text())
        self.opsf = str(EditVelocityCurveDialog.opsf_ipt.text())
        self.sigma = str(EditVelocityCurveDialog.sigma_ipt.text())


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
