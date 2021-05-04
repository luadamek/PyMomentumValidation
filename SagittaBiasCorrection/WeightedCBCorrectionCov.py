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
        res_id_pos = data["Pos_ID_TrackCovMatrix"][:,-1] * 1000.0 * 1000.0
        res_id_neg = data["Neg_ID_TrackCovMatrix"][:,-1] * 1000.0 * 1000.0

        over_p_me_pos = 1.0/(data["Pos_ME_Pt"] * np.cosh(data["Pos_ME_Eta"]))
        over_p_me_neg = 1.0/(data["Neg_ME_Pt"] * np.cosh(data["Neg_ME_Eta"]))
        res_me_pos = data["Pos_ME_TrackCovMatrix"][:,-1] * 1000.0 * 1000.0
        res_me_neg = data["Neg_ME_TrackCovMatrix"][:,-1] * 1000.0 * 1000.0

        #print("ID Res {}, 1/p id {}".format(res_id_pos, over_p_id_pos))
        #print("ME Res {}, 1/p me {}".format(res_me_pos, over_p_me_pos))

        w_pos = (res_me_pos ** 2)/( (res_me_pos**2) + (res_id_pos**2) )
        w_neg = (res_me_neg ** 2)/( (res_me_neg**2) + (res_id_neg**2) )

        over_p_cb_pos = (w_pos * over_p_id_pos) + ( (1.0 - w_pos) * over_p_me_pos)
        over_p_cb_neg = (w_neg * over_p_id_neg) + ( (1.0 - w_neg) * over_p_me_neg)

        safe_pos = (data["Pos_ME_Pt"] > 0) & ( data["Pos_ID_Pt"] > 0)
        safe_neg = (data["Neg_ME_Pt"] > 0) & ( data["Neg_ID_Pt"] > 0)

        data["Pos_CB_Pt"][safe_pos] = ((1.0 / over_p_cb_pos) / np.cosh(data["Pos_ID_Eta"]))[safe_pos]
        data["Neg_CB_Pt"][safe_neg] = ((1.0 / over_p_cb_neg) / np.cosh(data["Neg_ID_Eta"]))[safe_neg]

        # if not safe, take ID pt
        id_safe_pos = np.logical_not(safe_pos) & (data["Pos_ID_Pt"] > 0)
        data["Pos_CB_Pt"][id_safe_pos] = data["Pos_ID_Pt"][id_safe_pos]

        #otherwise take the ME pt
        id_unsafe_pos = np.logical_not(safe_pos) & (data["Pos_ME_Pt"] > 0)
        data["Pos_CB_Pt"][id_unsafe_pos] = data["Pos_ME_Pt"][id_unsafe_pos]

        # if not safe, take ID pt
        id_safe_neg = np.logical_not(safe_neg) & (data["Neg_ID_Pt"] > 0)
        data["Neg_CB_Pt"][id_safe_neg] = data["Neg_ID_Pt"][id_safe_neg]

        #otherwise take the ME pt
        id_unsafe_neg = np.logical_not(safe_neg) & (data["Neg_ME_Pt"] > 0)
        data["Neg_CB_Pt"][id_unsafe_neg] = data["Neg_ME_Pt"][id_unsafe_neg]

        #print("ID weight {}".format(w_pos))
        #print("ME weight {}".format(1.0 - w_pos))
        #print("min ID weight {}".format(min(w_pos)))
        #print("min ID weight sorted {}".format(np.sort(w_pos[res_me_pos>0.0])))
        #for el in np.sort(w_pos[res_me_pos>0.0])[0:1000]:
        #    print(el)
        #print("CB", data["Pos_CB_Pt"])
        #print("ID", data["Pos_ID_Pt"])
        #print("ME", data["Pos_ME_Pt"])

        if hasattr(data, "dtype"): keys =  data.dtype.names
        else: keys = list(data.keys())

        data["Pair_{}_Mass".format("CB")] = recalc_cb_mass(data)
        return data

