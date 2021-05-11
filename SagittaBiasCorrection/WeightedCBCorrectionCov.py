from variables import recalc_id_mass, recalc_me_mass, calc_recalc_id_mass, calc_recalc_me_mass, calc_recalc_cb_mass, recalc_cb_mass
import numpy as np


def get_calib_pt(data, charge="", uncorr=False):
    id_pt_string = "{}_ID_Pt".format(charge)
    id_eta_string = "{}_ID_Eta".format(charge)
    id_phi_string = "{}_ID_Phi".format(charge)

    me_pt_string = "{}_ME_Pt".format(charge)
    me_eta_string = "{}_ME_Eta".format(charge)
    me_phi_string = "{}_ME_Phi".format(charge)

    if uncorr:
        id_pt_string += "_UNCORR"

        me_pt_string += "_UNCORR"

    id_cov_string = "{}_ID_TrackCovMatrix".format(charge)
    me_cov_string = "{}_ME_TrackCovMatrix".format(charge)

    over_p_id = 1.0/(data[id_pt_string] * np.cosh(data[id_eta_string]))
    res_id = data[id_cov_string][:,-1] * 1000.0 * 1000.0

    over_p_me = 1.0/(data[me_pt_string] * np.cosh(data[me_eta_string]))
    res_me = data[me_cov_string][:,-1] * 1000.0 * 1000.0

    w = (res_me ** 2)/( (res_me**2) + (res_id**2) )

    over_p_cb = (w * over_p_id) + ( (1.0 - w) * over_p_me)

    safe = (data[me_pt_string] > 0) & ( data[id_pt_string] > 0)

    pts = np.ones(len(data["Pos_CB_Pt"]))

    pts[safe] = ((1.0 / over_p_cb[safe]) / np.cosh(data[id_eta_string][safe]))

    # if not safe, take ID pt
    id_safe = np.logical_not(safe) & (data[id_pt_string] > 0)
    pts[id_safe] = data[id_pt_string][id_safe]

    #otherwise take the ME pt
    id_unsafe = np.logical_not(safe) & (data[me_pt_string] > 0)
    pts[id_unsafe] = data[me_pt_string][id_unsafe]

    return pts


class WeightedCBCorrectionCov:

    #the histogram is a segitta bias correction map for delta s
    def __init__(self, do_percent_corr=False):
        self.branches = self.get_branches()
        self.do_percent_corr=do_percent_corr

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

        pos_pts_corr = get_calib_pt(data, charge="Pos", uncorr=False)
        neg_pts_corr = get_calib_pt(data, charge="Neg", uncorr=False)

        if self.do_percent_corr and "Pos_ID_Pt_UNCORR" in data:
            print("Doing percent change correction")
            pos_pts_uncorr = get_calib_pt(data, charge="Pos", uncorr=True)
            neg_pts_uncorr = get_calib_pt(data, charge="Neg", uncorr=True)

            data["Pos_CB_Pt"] = (1.0 + ((pos_pts_corr - pos_pts_uncorr)/pos_pts_uncorr)) * data["Pos_CB_Pt"]
            data["Neg_CB_Pt"] = (1.0 + ((neg_pts_corr - neg_pts_uncorr)/neg_pts_uncorr)) * data["Neg_CB_Pt"]

        elif not self.do_percent_corr:
            data["Pos_CB_Pt"] = pos_pts_corr
            data["Neg_CB_Pt"] = neg_pts_corr

        if hasattr(data, "dtype"): keys =  data.dtype.names
        else: keys = list(data.keys())

        data["Pair_{}_Mass".format("CB")] = recalc_cb_mass(data)
        return data

