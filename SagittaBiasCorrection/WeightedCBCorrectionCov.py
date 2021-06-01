from variables import recalc_id_mass, recalc_me_mass, calc_recalc_id_mass, calc_recalc_me_mass, calc_recalc_cb_mass, recalc_cb_mass
import numpy as np

def vec_stat_comb(vec1, mat1, vec2, mat2):
    # vec1, vec2: shape = (5, )
    # mat1, mat2: shape = (5, 5)
    inv_mat1 = np.linalg.pinv(mat1)
    inv_mat2 = np.linalg.pinv(mat2)
    res_mat = np.linalg.pinv(inv_mat1 + inv_mat2)
    res_vec = res_mat.dot(inv_mat1.dot(vec1) + inv_mat2.dot(vec2))
    return res_vec, res_mat

def stat_comb(vec1, mat1, vec2, mat2):
    # vec1, vec2: shape = (N events, 5, )
    # mat1, mat2: shape = (N events, 5, 5)
    mat1 = mat1 * (1000.0**4)
    mat2 = mat2 * (1000.0**4)
    vec1 = vec1 * (1000.0**2)
    vec2 = vec2 * (1000.0**2)
    inv_mat1 = np.linalg.inv(mat1)
    inv_mat2 = np.linalg.inv(mat2)
    res_mat = np.linalg.inv(inv_mat1 + inv_mat2)
    first_dot = np.einsum("...i,...ij", vec1, inv_mat1)#np.dot(vec1,inv_mat1)
    second_dot = np.einsum("...i,...ij", vec2, inv_mat2)#np.dot(vec2,inv_mat2)
    res_vec = np.einsum("...i,...ij", first_dot + second_dot, res_mat)#np.dot(first_dot + second_dot, res_mat)

    res_vec /= (1000.0**2)
    res_mat /= (1000.0*4)

    #for i in range(0, 100):
     #   vec1_i = vec1[i]
    #    vec2_i = vec2[i]
    #    mat1_i = mat1[i]
    #    mat2_i = mat2[i]
    #    vec, _ = vec_stat_comb(vec1_i, mat1_i, vec2_i, mat2_i)
    #    print(vec, res_vec[i])

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
        res_id = data[id_cov_string][:,-1, -1]

        over_p_me = 1.0/(data[me_pt_string] * np.cosh(data[me_eta_string]))
        res_me = data[me_cov_string][:,-1, -1]

        w = (res_me)/( (res_me) + (res_id) )

        over_p_cb = (w * over_p_id) + ( (1.0 - w) * over_p_me)

        pts = np.ones(len(data["Pos_CB_Pt"]))

        pts[safe] = ((1.0 / over_p_cb[safe]) / np.cosh(data["{}_CB_Eta".format(charge)][safe]))

        pts[np.logical_not(safe)] = data["{}_CB_Pt".format(charge)][np.logical_not(safe)] #if there is no ID or ME track, default to the CB track
        return pts, data["{}_CB_Eta".format(charge)], data["{}_CB_Phi".format(charge)]

    else:

        #print("Original_CB ", data["{}_CB_Pt".format(charge)])
        #print("Original_CB eta ", data["{}_CB_Eta".format(charge)])
        #print("Original_CB phi ", data["{}_CB_Phi".format(charge)])

        nevents = len(data["{}_CB_Charge".format(charge)])

        original_charge = np.sign(data["{}_CB_Charge".format(charge)])

        #put the corrected pt params into the track pars matrix

        safe_data = {key:data[key][safe] for key in data}
        id_qop = safe_data[id_charge_string]/ (safe_data[id_pt_string]* np.cosh(safe_data[id_eta_string])) /1000.0
        me_qop = safe_data[me_charge_string]/ (safe_data[me_pt_string]* np.cosh(safe_data[me_eta_string])) /1000.0
        track_pars_id = safe_data[id_track_pars] # N x 5 array (N events x 5 track pars)
        track_pars_me = safe_data[me_track_pars]

        #insert the corrected variables into the track params vector
        #order = np.argsort(np.abs(track_pars_id[:,-1] - id_qop))[::-1]
        track_pars_id[:,-1] = id_qop
        track_pars_me[:,-1] = me_qop

        qop_o = track_pars_id[:, 4]
        theta_o = track_pars_id[:, 3]
        phi_o = track_pars_id[:, 2]
        z0_o = track_pars_id[:, 1]
        d0_o = track_pars_id[:, 0]

        print("qop id", qop_o)
        print("theta id", theta_o)
        print("phi id", phi_o)
        print("z0 id", z0_o)
        print("d0 id", d0_o)


        qop_o = track_pars_me[:, 4]
        theta_o = track_pars_me[:, 3]
        phi_o = track_pars_me[:, 2]
        z0_o = track_pars_me[:, 1]
        d0_o = track_pars_me[:, 0]

        print("qop me", qop_o)
        print("theta me", theta_o)
        print("phi me", phi_o)
        print("z0 me", z0_o)
        print("d0 me", d0_o)

        print("\n\n\n")

        cov_mat_id = safe_data[id_cov_string] # N x 5 x 5 array (N events x 5 track pars x 5 track pars)
        cov_mat_me = safe_data[me_cov_string]

        stacco_pars = stat_comb(track_pars_id, cov_mat_id, track_pars_me, cov_mat_me)
        track_pars = stacco_pars[0]

        qop = track_pars[:, 4]
        theta = track_pars[:, 3]
        phi = track_pars[:, 2]
        z0 = track_pars[:, 1]
        d0 = track_pars[:, 0]

        print("qop", qop)
        print("theta", theta)
        print("phi", phi)
        print("z0", z0)
        print("d0", d0)

        print("\n\n\n")

        p = np.abs((1.0/qop)) / 1000.0
        eta = -1.0 * np.log(np.tan(theta/2.0))  

        pt = (p/np.cosh(eta))  
        this_charge = np.sign(qop)

        if np.any(np.isnan(eta)): print("Nan etas! {} of {}".format(np.sum(1.0 * np.isnan(eta)), nevents))
        if np.any(pt < 0.0): print("Negative pt!")
        if np.any(original_charge[safe] != this_charge): print("Some have flipped charge w.r.t. CB")

        #print("The max eta after combination was ", np.max(eta[np.logical_not(np.isnan(eta))]))

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

        print("Printing std dev of reco/truth before and after correction")
        has_truth = data["{}_TruthPt".format(charge)] > 0.0
        print(to_return_pt[has_truth])
        ratio = (to_return_pt[has_truth]/data["{}_TruthPt".format(charge)][has_truth])
        order = np.argsort(ratio)[::-1]
        #print("pts ordered ", to_return_pt[has_truth][order])
        #print("determinants", np.linalg.det(data[me_cov_string] * (1000.0**4))[has_truth][order])
        print(ratio[order])
        print(np.std(ratio))

        print("Nevents and det is zero ", nevents, np.sum(1.0 * (np.linalg.det(data[me_cov_string] * (1000.0**4)) == 0)), np.sum(1.0 * (np.linalg.det(data[id_cov_string] * (1000.0**4)) == 0)))

        to_return_pt[safe] = pt[new_safe]
        to_return_eta[safe] = eta[new_safe]
        to_return_phi[safe] = phi[new_safe]

        #print("Final CB pt ", to_return_pt)
        #print("Final CB eta ", to_return_eta)
        #print("Final CB phi ", to_return_phi)

        print(to_return_pt[has_truth])
        ratio = (to_return_pt[has_truth]/data["{}_TruthPt".format(charge)][has_truth])
        order = np.argsort(ratio)[::-1]
        print("pts ordered ", to_return_pt[has_truth][order])
        print(ratio[order])
        print(np.std((ratio)))

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
        branches += ["Pos_TruthPt", "Neg_TruthPt"]
        return branches

    def calibrate(self, data):
        print("Track Combination")

        pos_pts_corr, pos_etas_corr, pos_phis_corr = get_calib_pt(data, charge="Pos", uncorr=False, do_full_matrix = self.do_full_matrix)
        neg_pts_corr, neg_etas_corr, neg_phis_corr = get_calib_pt(data, charge="Neg", uncorr=False, do_full_matrix = self.do_full_matrix)

        if self.do_percent_corr and "Pos_ID_Pt_UNCORR" in data:
            print("Doing percent change correction")
            pos_pts_uncorr, pos_etas_uncorr, pos_phis_uncorr = get_calib_pt(data, charge="Pos", uncorr=True, do_full_matrix = self.do_full_matrix)
            neg_pts_uncorr, neg_etas_uncorr, neg_phis_uncorr = get_calib_pt(data, charge="Neg", uncorr=True, do_full_matrix = self.do_full_matrix)

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

            #data["Pos_CB_Eta"] = (1.0 + ((pos_etas_corr - pos_etas_uncorr)/pos_etas_uncorr)) * data[cbeta_pos]
            #data["Neg_CB_Eta"] = (1.0 + ((neg_etas_corr - neg_etas_uncorr)/neg_etas_uncorr)) * data[cbeta_neg]

            #data["Pos_CB_Phi"] = (1.0 + ((pos_phis_corr - pos_phis_uncorr)/pos_phis_uncorr)) * data[cbphi_pos]
            #data["Neg_CB_Phi"] = (1.0 + ((neg_phis_corr - neg_phis_uncorr)/neg_phis_uncorr)) * data[cbphi_neg]

        elif not self.do_percent_corr:
            print("HERE")
            charge = "Pos"
            print("Original_CB ", data["{}_CB_Pt".format(charge)])
            #print("Original_CB eta ", data["{}_CB_Eta".format(charge)])
            #print("Original_CB phi ", data["{}_CB_Phi".format(charge)])
            data["Pos_CB_Pt"] = pos_pts_corr
            data["Neg_CB_Pt"] = neg_pts_corr

            data["Pos_CB_Eta"] = pos_etas_corr
            data["Neg_CB_Eta"] = neg_etas_corr

            data["Pos_CB_Phi"] = pos_phis_corr
            data["Neg_CB_Phi"] = neg_phis_corr
            charge = "Pos"
            print("Final_CB ", data["{}_CB_Pt".format(charge)])
            #print("Final_CB eta ", data["{}_CB_Eta".format(charge)])
            #print("Final_CB phi ", data["{}_CB_Phi".format(charge)])
            #print("OVER")

        if hasattr(data, "dtype"): keys =  data.dtype.names
        else: keys = list(data.keys())

        print("Original masses ", data["Pair_{}_Mass".format("CB")])
        print("CB ", np.std(data["Pair_{}_Mass".format("CB")][np.abs(data["Pair_{}_Mass".format("CB")] - 91.2) < 12]))
        print("ID ",np.std(data["Pair_{}_Mass".format("ID")][np.abs(data["Pair_{}_Mass".format("ID")] - 91.2) < 12]))
        print("ME ",np.std(data["Pair_{}_Mass".format("ME")][np.abs(data["Pair_{}_Mass".format("ME")] - 91.2) < 12]))
        data["Pair_{}_Mass".format("CB")] = recalc_cb_mass(data)
        print("Final masses ", data["Pair_{}_Mass".format("CB")])
        print("CB ", np.std(data["Pair_{}_Mass".format("CB")][np.abs(data["Pair_{}_Mass".format("CB")] - 91.2) < 12]))
        print("ID ",np.std(data["Pair_{}_Mass".format("ID")][np.abs(data["Pair_{}_Mass".format("ID")] - 91.2) < 12]))
        print("ME ",np.std(data["Pair_{}_Mass".format("ME")][np.abs(data["Pair_{}_Mass".format("ME")] - 91.2) < 12]))
        return data

