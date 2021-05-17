from variables import recalc_id_mass, recalc_me_mass, calc_recalc_id_mass, calc_recalc_me_mass, calc_recalc_cb_mass, recalc_cb_mass
import numpy as np

def stat_comb(vec1, mat1, vec2, mat2):
    # vec1, vec2: shape = (N events, 5, )
    # mat1, mat2: shape = (N events, 5, 5)
    inv_mat1 = np.linalg.inv(mat1)
    inv_mat2 = np.linalg.inv(mat2)
    res_mat = np.linalg.inv(inv_mat1 + inv_mat2)
    first_dot = np.einsum("...i,...ij", vec1, inv_mat1)#np.dot(vec1,inv_mat1)
    second_dot = np.einsum("...i,...ij", vec2, inv_mat2)#np.dot(vec2,inv_mat2)
    res_vec = np.einsum("...i,...ij", first_dot + second_dot, res_mat)#np.dot(first_dot + second_dot, res_mat)
    return res_vec, res_mat

def get_calib_pt(data, charge="", uncorr=False, do_full_matrix = False):

    id_pt_string = "{}_ID_Pt".format(charge)
    id_eta_string = "{}_ID_Eta".format(charge)
    id_phi_string = "{}_ID_Phi".format(charge)
    id_charge_string = "{}_ID_Charge".format(charge)

    me_pt_string = "{}_ME_Pt".format(charge)
    me_eta_string = "{}_ME_Eta".format(charge)
    me_phi_string = "{}_ME_Phi".format(charge)
    me_charge_string = "{}_ME_Charge".format(charge)

    if uncorr:
        id_pt_string += "_UNCORR"
        me_pt_string += "_UNCORR"

    id_cov_string = "{}_ID_TrackCovMatrix".format(charge)
    me_cov_string = "{}_ME_TrackCovMatrix".format(charge)

    id_track_pars = "{}_ID_TrackPars".format(charge)
    me_track_pars = "{}_ME_TrackPars".format(charge)

    safe = (data[me_pt_string] > 0) & ( data[id_pt_string] > 0)

    if not do_full_matrix:

        over_p_id = 1.0/(data[id_pt_string] * np.cosh(data[id_eta_string]))
        res_id = data[id_cov_string][:,-1, -1] * 1000.0 * 1000.0

        over_p_me = 1.0/(data[me_pt_string] * np.cosh(data[me_eta_string]))
        res_me = data[me_cov_string][:,-1, -1] * 1000.0 * 1000.0

        w = (res_me)/( (res_me) + (res_id) )

        over_p_cb = (w * over_p_id) + ( (1.0 - w) * over_p_me)


        pts = np.ones(len(data["Pos_CB_Pt"]))

        pts[safe] = ((1.0 / over_p_cb[safe]) / np.cosh(data[id_eta_string][safe]))

        pts[np.logical_not(safe)] = data["{}_CB_Pt".format(charge)][np.logical_not(safe)] #if there is no ID or ME track, default to the CB track
        return pts, data["{}_CB_Eta".format(charge)], data["{}_CB_Phi".format(charge)]

    else:

        nevents = len(data["{}_CB_Charge".format(charge)])

        original_charge = np.sign(data["{}_CB_Charge".format(charge)])
        track_pars_id = data[id_track_pars][safe] # N x 5 array (N events x 5 track pars)
        track_pars_me = data[me_track_pars][safe]

        #put the corrected pt params into the track pars matrix
        id_qop = data[id_charge_string][safe] / (data[id_pt_string][safe] * np.cosh(data[id_eta_string][safe])  * 1000.0) #convert to 1/MeV
        me_qop = data[me_charge_string][safe] / (data[me_pt_string][safe] * np.cosh(data[me_eta_string][safe])  * 1000.0)
        #insert the corrected variables into the track params vector
        track_pars_id[:,-1] = id_qop
        track_pars_me[:,-1] = me_qop

        cov_mat_id = data[id_cov_string][safe] # N x 5 x 5 array (N events x 5 track pars x 5 track pars)
        cov_mat_me = data[me_cov_string][safe]

        stacco_pars = stat_comb(track_pars_id, cov_mat_id, track_pars_me, cov_mat_me)
        track_pars = stacco_pars[0]

        qop = track_pars[:, 4]
        theta = track_pars[:, 3]
        phi = track_pars[:, 2]
        z0 = track_pars[:, 1]
        d0 = track_pars[:, 0]

        p = np.abs((1.0/qop))
        eta = -1.0 * np.log(np.tan(theta/2.0))
        pt = (p/np.cosh(eta)) / 1000.0 #convert to GeV
        this_charge = np.sign(qop)

        if np.any(np.isnan(eta)): print("Nan etas! {} of {}".format(np.sum(1.0 * np.isnan(eta)), nevents))
        if np.any(pt < 0.0): print("Negative pt!")
        if np.any(original_charge[safe] != this_charge): print("Some have flipped charge w.r.t. CB")

        print("The max eta after combination was ", np.max(eta[np.logical_not(np.isnan(eta))]))

        new_safe = (original_charge[safe] == this_charge) & (pt > 0.0) & (np.logical_not(np.isnan(eta)))

        safe[safe] = safe[safe] & new_safe # do not allow charge flipping and nan etas

        to_return_pt = np.zeros(nevents)
        to_return_eta = np.zeros(nevents)
        to_return_phi = np.zeros(nevents)
        to_return_charge = np.zeros(nevents)

        to_return_pt[:] = data["{}_CB_Pt".format(charge)]
        to_return_eta[:] = data["{}_CB_Eta".format(charge)]
        to_return_phi[:] = data["{}_CB_Phi".format(charge)]
        to_return_charge[:] = data["{}_CB_Charge".format(charge)]

        #0.02 % of tracks have their charges flipped. Keep the original charge

        to_return_pt[safe] = pt[new_safe]
        to_return_eta[safe] = eta[new_safe]
        to_return_phi[safe] = phi[new_safe]

        return to_return_pt, to_return_eta, to_return_phi

class WeightedCBCorrectionCov:

    #the histogram is a segitta bias correction map for delta s
    def __init__(self, do_percent_corr=False, do_full_matrix = False):
        self.branches = self.get_branches()
        self.do_percent_corr=do_percent_corr
        self.do_full_matrix = do_full_matrix

    def get_branches(self):
        branches = []
        for region in ["ID", "ME", "CB"]:
            for uncalib, matrix in zip(["Pos_{}_Pt", "Neg_{}_Pt", "Pos_{}_TrackPars", "Pos_{}_Charge"],  ["Pos_{}_TrackCovMatrix", "Neg_{}_TrackCovMatrix", "Neg_{}_TrackPars", "Neg_{}_Charge"]):
                branches.append(uncalib.format(region))
                branches.append(matrix.format(region))
                branches+=calc_recalc_id_mass.branches
                branches+=calc_recalc_me_mass.branches
                branches+=calc_recalc_cb_mass.branches
                branches = list(set(branches))
        return branches

    def calibrate(self, data):
        print("Track Combination")

        pos_pts_corr, pos_etas_corr, pos_phis_corr = get_calib_pt(data, charge="Pos", uncorr=False, do_full_matrix = self.do_full_matrix)
        neg_pts_corr, neg_etas_corr, neg_phis_corr = get_calib_pt(data, charge="Neg", uncorr=False, do_full_matrix = self.do_full_matrix)

        if self.do_percent_corr and "Pos_ID_Pt_UNCORR" in data:
            print("Doing percent change correction")
            pos_pts_uncorr, pos_etas_uncorr = get_calib_pt(data, charge="Pos", uncorr=True, do_full_matrix = self.do_full_matrix)
            neg_pts_uncorr, neg_etas_uncorr = get_calib_pt(data, charge="Neg", uncorr=True, do_full_matrix = self.do_full_matrix)

            cbpt_pos = "Pos_CB_Pt"
            cbpt_neg = "Neg_CB_Pt"

            cbeta_pos = "Pos_CB_Eta"
            cbeta_neg = "Neg_CB_Eta"

            cbphi_pos = "Pos_CB_Phi"
            cbphi_neg = "Neg_CB_Phi"

            if "Pos_CB_Pt_UNCORR" in data:
                cbpt_pos += "_UNCORR"
                cbpt_neg += "_UNCORR"

                cbeta_pos += "_UNCORR"
                cbeta_neg += "_UNCORR"

                cbphi_pos += "_UNCORR"
                cbphi_neg += "_UNCORR"

            data["Pos_CB_Pt"] = (1.0 + ((pos_pts_corr - pos_pts_uncorr)/pos_pts_uncorr)) * data[cbpt_pos]
            data["Neg_CB_Pt"] = (1.0 + ((neg_pts_corr - neg_pts_uncorr)/neg_pts_uncorr)) * data[cbpt_neg]

            data["Pos_CB_Eta"] = (1.0 + ((pos_etas_corr - pos_etas_uncorr)/pos_etas_uncorr)) * data[cbeta_pos]
            data["Neg_CB_Eta"] = (1.0 + ((neg_etas_corr - neg_etas_uncorr)/neg_etas_uncorr)) * data[cbeta_neg]

            data["Pos_CB_Phi"] = (1.0 + ((pos_phis_corr - pos_phis_uncorr)/pos_phis_uncorr)) * data[cbphi_pos]
            data["Neg_CB_Phi"] = (1.0 + ((neg_phis_corr - neg_phis_uncorr)/neg_phis_uncorr)) * data[cbphi_neg]

        elif not self.do_percent_corr:
            data["Pos_CB_Pt"] = pos_pts_corr
            data["Neg_CB_Pt"] = neg_pts_corr

            data["Pos_CB_Eta"] = pos_etas_corr
            data["Neg_CB_Eta"] = neg_etas_corr

            data["Pos_CB_Phi"] = pos_phis_corr
            data["Neg_CB_Phi"] = neg_phis_corr

        if hasattr(data, "dtype"): keys =  data.dtype.names
        else: keys = list(data.keys())

        data["Pair_{}_Mass".format("CB")] = recalc_cb_mass(data)
        return data

