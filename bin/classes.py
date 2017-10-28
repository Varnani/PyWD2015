class LightCurveProperties:
    def __init__(self, EditLightCurveDialog):
        self.FilePath = EditLightCurveDialog.filepath_label.text()
        self.band = EditLightCurveDialog.band_box.text()
        self.ksd = EditLightCurveDialog.ksd_box.text()
        self.l1 = EditLightCurveDialog.l1_ipt.text()
        self.l2 = EditLightCurveDialog.l2_ipt.text()
        self.x1 = EditLightCurveDialog.x1_ipt.text()
        self.x2 = EditLightCurveDialog.x2_ipt.text()
        self.y1 = EditLightCurveDialog.y1_ipt.text()
        self.y2 = EditLightCurveDialog.y2_ipt.text()
        self.e1 = EditLightCurveDialog.e1_ipt.text()
        self.e2 = EditLightCurveDialog.e2_ipt.text()
        self.e3 = EditLightCurveDialog.e3_ipt.text()
        self.e4 = EditLightCurveDialog.e4_ipt.text()
        self.el3a = EditLightCurveDialog.el3a_ipt.text()
        self.opsf = EditLightCurveDialog.opsf_ipt.text()
        self.sigma = EditLightCurveDialog.sigma_ipt.text()
        self.timeList = EditLightCurveDialog.timeList
        self.observationList = EditLightCurveDialog.observationList
        self.weightList = EditLightCurveDialog.weightList
        self.lines = EditLightCurveDialog.lines


class VelocityCurveProperties:
    def __init__(self, EditVelocityCurveDialog):
        self.FilePath = EditVelocityCurveDialog.filepath_label.text()
        self.band = EditVelocityCurveDialog.band_box.text()
        self.ksd = EditVelocityCurveDialog.ksd_box.text()
        self.l1 = EditVelocityCurveDialog.l1_ipt.text()
        self.l2 = EditVelocityCurveDialog.l2_ipt.text()
        self.x1 = EditVelocityCurveDialog.x1_ipt.text()
        self.x2 = EditVelocityCurveDialog.x2_ipt.text()
        self.y1 = EditVelocityCurveDialog.y1_ipt.text()
        self.y2 = EditVelocityCurveDialog.y2_ipt.text()
        self.e1 = EditVelocityCurveDialog.e1_ipt.text()
        self.e2 = EditVelocityCurveDialog.e2_ipt.text()
        self.e3 = EditVelocityCurveDialog.e3_ipt.text()
        self.e4 = EditVelocityCurveDialog.e4_ipt.text()
        self.wla = EditVelocityCurveDialog.wla_ipt.text()
        self.opsf = EditVelocityCurveDialog.opsf_ipt.text()
        self.sigma = EditVelocityCurveDialog.sigma_ipt.text()
        self.timeList = EditVelocityCurveDialog.timeList
        self.observationList = EditVelocityCurveDialog.observationList
        self.weightList = EditVelocityCurveDialog.weightList
        self.lines = EditVelocityCurveDialog.lines


if __name__ == "__main__":
    pass
