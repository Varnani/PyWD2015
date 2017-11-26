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
        self.timeList = EditLightCurveDialog.timeList
        self.observationList = EditLightCurveDialog.observationList
        self.weightList = EditLightCurveDialog.weightList
        self.lines = EditLightCurveDialog.lines


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
        self.timeList = EditVelocityCurveDialog.timeList
        self.observationList = EditVelocityCurveDialog.observationList
        self.weightList = EditVelocityCurveDialog.weightList
        self.lines = EditVelocityCurveDialog.lines


if __name__ == "__main__":
    pass
