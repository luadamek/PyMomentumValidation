from variables import recalc_id_mass, recalc_me_mass, calc_recalc_id_mass, calc_recalc_me_mass, calc_recalc_cb_mass, recalc_cb_mass

class DefaultCombination:

    #the histogram is a segitta bias correction map for delta s
    def __init__(self):
        self.branches = self.get_branches()

    def get_branches(self):
        branches = []
        for region in ["ID", "ME", "CB"]:
            for calib in ["Pos_{}_Pt", "Neg_{}_Pt"]:

                branches.append(calib.format(region))
                branches+=calc_recalc_id_mass.branches
                branches+=calc_recalc_me_mass.branches
                branches+=calc_recalc_cb_mass.branches
        return branches

    def calibrate(self, data, region=None):
        print("Applying the default combination")

        region = "CB"
        variable_name = "Pair_{}_Mass".format(region)

        if "Pos_ID_Pt_UNCORR" in data and "Pos_ME_Pt_UNCORR" in data:
            print("Found uncorrected branches. Running combination")
            frac_pos = (data["Pos_CB_Pt"] - data["Pos_ME_Pt_UNCORR"])/(data["Pos_ID_Pt_UNCORR"] + data["Pos_ME_Pt_UNCORR"])
            data["Pos_CB_Pt"] = frac_pos * data["Pos_ID_Pt_UNCORR"] + (1.0 - frac_pos) * data["Pos_ME_Pt_UNCORR"]
            data[variable_name] = recalc_cb_mass(data)
            print("Done pos")


        if  "Neg_ID_Pt_UNCORR" in data and "Neg_ME_Pt_UNCORR" in data:
            print("Found uncorrected branches. Running combination")
            frac_neg = (data["Neg_CB_Pt"] - data["Neg_ME_Pt_UNCORR"])/(data["Neg_ID_Pt_UNCORR"] + data["Neg_ME_Pt_UNCORR"])
            data["Neg_CB_Pt"] = frac_neg * data["Neg_ID_Pt_UNCORR"] + (1.0 - frac_neg) * data["Neg_ME_Pt_UNCORR"]
            data[variable_name] = recalc_cb_mass(data)
            print("Done neg")

        return data

