from variables import recalc_id_mass, recalc_me_mass, calc_recalc_id_mass, calc_recalc_me_mass, calc_recalc_cb_mass, recalc_cb_mass
import numpy as np

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

  #      print("Correcting Pos")
   #     print(data["Pos_CB_Pt"])
        if "Pos_ID_Pt_UNCORR" in data and "Pos_ME_Pt_UNCORR" in data:
            print("Found uncorrected branches. Running combination")
            if "Pos_CB_Pt_UNCORR" in data: cbvar = "Pos_CB_Pt_UNCORR"
            else: cbvar = "Pos_CB_Pt"
            frac_pos = (data[cbvar] - data["Pos_ME_Pt_UNCORR"])/(data["Pos_ID_Pt_UNCORR"] - data["Pos_ME_Pt_UNCORR"])
            safe_pos = (data["Pos_ME_Pt"] > 0) & ( data["Pos_ID_Pt"] > 0)
            corr_pts = (frac_pos * data["Pos_ID_Pt"] + (1.0 - frac_pos) * data["Pos_ME_Pt"])
            corr_pts[np.logical_not(safe_pos)] = data["Pos_CB_Pt"][np.logical_not(safe_pos)]
            data["Pos_CB_Pt"] = corr_pts

            data[variable_name] = recalc_cb_mass(data)
            print("Done pos")
        print(data["Pos_CB_Pt"])


        print("Correcting Neg")
        if  "Neg_ID_Pt_UNCORR" in data and "Neg_ME_Pt_UNCORR" in data:
            print("Found uncorrected branches. Running combination")
            if "Neg_CB_Pt_UNCORR" in data: cbvar = "Neg_CB_Pt_UNCORR"
            else: cbvar = "Neg_CB_Pt"
            frac_neg = (data[cbvar] - data["Neg_ME_Pt_UNCORR"])/(data["Neg_ID_Pt_UNCORR"] - data["Neg_ME_Pt_UNCORR"])
            safe_neg = (data["Neg_ME_Pt"] > 0) & ( data["Neg_ID_Pt"] > 0)
            corr_pts = (frac_neg * data["Neg_ID_Pt"] + (1.0 - frac_neg) * data["Neg_ME_Pt"])
            corr_pts[np.logical_not(safe_neg)] = data["Neg_CB_Pt"][np.logical_not(safe_neg)]
            data["Neg_CB_Pt"] = corr_pts

            data[variable_name] = recalc_cb_mass(data)
            print("Done neg")
        print(data["Neg_CB_Pt"])

        return data

