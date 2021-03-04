class DefaultCorrection:

    #the histogram is a segitta bias correction map for delta s
    def __init__(self):
        pass

    def get_branches(self):
        branches = []
        for uncalib, calib in zip(["Pos_{}_Pt", "Neg_{}_Pt"],  ["Pos_{}_CalibPt", "Neg_{}_CalibPt"]):
            branches.append(uncalib.format(region))
            branches.append(calib.format(region))
        return branches

    def calibrate(self, data):
        for region in ["ID", "ME"]:
            for uncalib, calib in zip(["Pos_{}_Pt", "Neg_{}_Pt"],  ["Pos_{}_CalibPt", "Neg_{}_CalibPt"]):
                pt = uncalib.format(region)
                pt_calib = calib.format(region)
                data[pt] = data[pt_calib]
        return data

