from variables import recalc_id_mass, recalc_me_mass, calc_recalc_id_mass, calc_recalc_me_mass, calc_recalc_cb_mass, recalc_cb_mass

class DefaultCorrection:

    #the histogram is a segitta bias correction map for delta s
    def __init__(self):
        self.branches = self.get_branches()

    def get_branches(self):
        branches = []
        for region in ["ID", "ME", "CB"]:
            for uncalib, calib in zip(["Pos_{}_Pt", "Neg_{}_Pt"],  ["Pos_{}_CalibPt", "Neg_{}_CalibPt"]):
                branches.append(uncalib.format(region))
                branches.append(calib.format(region))
                branches+=calc_recalc_id_mass.branches
                branches+=calc_recalc_me_mass.branches
                branches+=calc_recalc_cb_mass.branches
        return branches

    def calibrate(self, data, region=None):
        print("Applying the deafult correction")
        if region is not None: regions = [region]
        else: regions = ["ID", "ME", "CB"]
        for region in regions:
            for uncalib, calib in zip(["Pos_{}_Pt", "Neg_{}_Pt"],  ["Pos_{}_CalibPt", "Neg_{}_CalibPt"]):
                pt = uncalib.format(region)
                pt_calib = calib.format(region)
                print("pre-correction")
                print("Uncalib ", data[pt])
                print("Calib ",data[pt_calib])
                data[pt] = data[pt_calib]
                print("post-correction")
                print("Uncalib ", data[pt])
                print("Calib ", data[pt_calib])

        if hasattr(data, "dtype"): keys =  data.dtype.names
        else: keys = list(data.keys())

        for region in regions:
            variable_name = "Pair_{}_Mass".format(region)
            if region == "ID":
                data[variable_name] = recalc_id_mass(data)
            if region == "ME":
                data[variable_name] = recalc_me_mass(data)
            if region == "CB":
                data[variable_name] = recalc_cb_mass(data)
        return data

