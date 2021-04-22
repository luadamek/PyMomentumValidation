from variables import recalc_id_mass, recalc_me_mass, calc_recalc_id_mass, calc_recalc_me_mass, calc_recalc_cb_mass, recalc_cb_mass
import numpy as np


class WeightedCBCorrectionCov:

    #the histogram is a segitta bias correction map for delta s
    def __init__(self):
        self.branches = self.get_branches()

    def get_branches(self):
        branches = []
        for region in ["ID", "ME", "CB"]:
            for uncalib, matrix in zip(["Pos_{}_Pt", "Neg_{}_Pt"],  ["Pos_{}_TrackCovMatrix", "Neg_{}_TrackCovMatrix"]):
                branches.append(uncalib.format(region))
                if region != "CB": branches.append(matrix.format(region))
                branches+=calc_recalc_id_mass.branches
                branches+=calc_recalc_me_mass.branches
                branches+=calc_recalc_cb_mass.branches
        return branches

    def calibrate(self, data):
        print("Track Combination")
        over_p_id_pos = 1.0/(data["Pos_ID_Pt"] * np.cosh(data["Pos_ID_Eta"]))
        over_p_id_neg = 1.0/(data["Neg_ID_Pt"] * np.cosh(data["Neg_ID_Eta"]))
        res_id_pos = data["Pos_ID_TrackCovMatrix"][:,0]
        res_id_neg = data["Neg_ID_TrackCovMatrix"][:,0]

        over_p_me_pos = 1.0/(data["Pos_ME_Pt"] * np.cosh(data["Pos_ME_Eta"]))
        over_p_me_neg = 1.0/(data["Neg_ME_Pt"] * np.cosh(data["Neg_ME_Eta"]))
        res_me_pos = data["Pos_ME_TrackCovMatrix"][:,0]
        res_me_neg = data["Neg_ME_TrackCovMatrix"][:,0]

        w_pos = (res_me_pos ** 2)/( (res_me_pos**2) + (res_id_pos**2) )
        w_neg = (res_me_neg ** 2)/( (res_me_neg**2) + (res_id_neg**2) )

        over_p_cb_pos = (w_pos * over_p_id_pos) + ( (1.0 - w_pos) * over_p_me_pos)
        over_p_cb_neg = (w_neg * over_p_id_neg) + ( (1.0 - w_neg) * over_p_me_neg)

        data["Pos_CB_Pt"] = (1.0 / over_p_cb_pos) / np.cosh(data["Pos_ID_Eta"])
        data["Neg_CB_Pt"] = (1.0 / over_p_cb_neg) / np.cosh(data["Neg_ID_Eta"])

        print("CB", data["Pos_CB_Pt"])
        print("ID", data["Pos_ID_Pt"])
        print("ME", data["Pos_ME_Pt"])

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

