from calculation import Calculation
import numpy as np

def range_selection_function(event, variable, range_low, range_hi):
    if not isinstance(variable, Calculation): return (event[variable] < range_hi) & (range_low < event[variable])
    else: 
        vals = variable.eval(event)
        return (vals < range_hi) & (range_low < vals)

def get_leading(event,  location, charge):
    pos_lead = event["Pos_{}_Pt".format(location)] > event["Neg_{}_Pt".format(location)]
    if charge == "Pos": return pos_lead
    if charge == "Neg": return np.logical_not(pos_lead)

def pos_leading_id(event):
    return get_leading(event, "ID", "Pos")
branches = ["Pos_ID_Pt", "Neg_ID_Pt"]
sel_pos_leading_id = Calculation(pos_leading_id, branches)

def nonzero_id_pts(event):
    return (event["Pos_ID_Pt"] > 0.0) & (event["Neg_ID_Pt"] > 0.0)
sel_nonzero_id_pts = Calculation(nonzero_id_pts, ["Pos_ID_Pt", "Neg_ID_Pt"])

def nonzero_me_pts(event):
    return (event["Pos_ME_Pt"] > 0.0) & (event["Neg_ME_Pt"] > 0.0)
sel_nonzero_me_pts = Calculation(nonzero_me_pts, ["Pos_ME_Pt", "Neg_ME_Pt"])

def nonzero_cb_pts(event):
    return (event["Pos_CB_Pt"] > 0.0) & (event["Neg_CB_Pt"] > 0.0)
sel_nonzero_cb_pts = Calculation(nonzero_cb_pts, ["Pos_CB_Pt", "Neg_CB_Pt"])

def min_fifteen_id_pts(event):
    return (event["Pos_ID_Pt"] > 15.0) & (event["Neg_ID_Pt"] > 15.0)
sel_min_fifteen_id_pts  = Calculation(min_fifteen_id_pts, ["Pos_ID_Pt", "Neg_ID_Pt"])

def min_fifteen_me_pts(event):
    return (event["Pos_ME_Pt"] > 15.0) & (event["Neg_ME_Pt"] > 15.0)
sel_min_fifteen_me_pts = Calculation(min_fifteen_me_pts, ["Pos_ME_Pt", "Neg_ME_Pt"])

def min_fifteen_cb_pts(event):
    return (event["Pos_CB_Pt"] > 15.0) & (event["Neg_CB_Pt"] > 15.0)
sel_min_fifteen_cb_pts = Calculation(min_fifteen_cb_pts, ["Pos_CB_Pt", "Neg_CB_Pt"])

def neg_leading_id(event):
    return get_leading(event, "ID", "Neg")
branches = ["Neg_ID_Pt", "Neg_ID_Pt"]
sel_neg_leading_id = Calculation(neg_leading_id, branches)

def pos_leading_me(event):
    return get_leading(event, "ME", "Pos")
branches = ["Pos_ME_Pt", "Neg_ME_Pt"]
sel_pos_leading_me = Calculation(pos_leading_me, branches)

def pos_leading_cb(event):
    return get_leading(event, "CB", "Pos")
branches = ["Pos_CB_Pt", "Neg_CB_Pt"]
sel_pos_leading_cb = Calculation(pos_leading_cb, branches)

def small_weight(event):
    return abs(event["TotalWeight"]) < 80.0
branches = ["TotalWeight"]
sel_small_weight = Calculation(small_weight, branches)

def neg_leading_me(event):
    return get_leading(event, "ME", "Neg")
branches = ["Neg_ME_Pt", "Neg_ME_Pt"]
sel_neg_leading_me = Calculation(neg_leading_me, branches)

def neg_leading_cb(event):
    return get_leading(event, "CB", "Neg")
branches = ["Neg_CB_Pt", "Neg_CB_Pt"]
sel_neg_leading_cb = Calculation(neg_leading_cb, branches)

def get_subleading(event,  location, charge):
    charge_leading = get_leading(event, location, charge)
    return np.logical_not(charge_leading)


def check_safe_event(event, charge, region):
     string = "{}_{}_Eta".format(charge, region)
     return (event[string] < 5.0) & (event[string] > -5.0)

def nom_delta_selection(event, region):
     mass_window = np.abs(event["Pair_{}_Mass".format(region)] - 91.2) < 12.0
     pt_sel = (event["Pos_{}_Pt".format(region)] < 100.0) & (event["Neg_{}_Pt".format(region)] < 100.0) & (event["Pos_{}_Pt".format(region)] > 0.0) & (event["Neg_{}_Pt".format(region)] > 0.0)
     return mass_window & pt_sel

def nom_delta_selection_id(event):
    return nom_delta_selection(event, "ID")

def nom_delta_selection_cb(event):
    return nom_delta_selection(event, "CB")

def nom_delta_selection_me(event):
    return nom_delta_selection(event, "ME")

sel_nom_delta_selection_id = Calculation(nom_delta_selection_id, ["Pos_ID_Pt", "Neg_ID_Pt", "Pair_ID_Mass"])
sel_nom_delta_selection_cb = Calculation(nom_delta_selection_cb, ["Pos_CB_Pt", "Neg_CB_Pt", "Pair_CB_Mass"])
sel_nom_delta_selection_me = Calculation(nom_delta_selection_me, ["Pos_ME_Pt", "Neg_ME_Pt", "Pair_ME_Mass"])

def nom_delta_preselection(event, region):
     mass_window = np.abs(event["Pair_{}_Mass".format(region)] - 91.2) < 40.0
     pt_sel = (event["Pos_{}_Pt".format(region)] < 500.0) & (event["Neg_{}_Pt".format(region)] < 500.0) & (event["Pos_{}_Pt".format(region)] > 0.0) & (event["Neg_{}_Pt".format(region)] > 0.0)
     return mass_window & pt_sel

def nom_delta_preselection_id(event):
    return nom_delta_preselection(event, "ID")

def nom_delta_preselection_cb(event):
    return nom_delta_preselection(event, "CB")

def nom_delta_preselection_ms(event):
    return nom_delta_preselection(event, "MS")

def nom_delta_preselection_me(event):
    return nom_delta_preselection(event, "ME")

sel_nom_delta_preselection_id = Calculation(nom_delta_preselection_id, ["Pos_ID_Pt", "Neg_ID_Pt", "Pair_ID_Mass"])
sel_nom_delta_preselection_cb = Calculation(nom_delta_preselection_cb, ["Pos_CB_Pt", "Neg_CB_Pt", "Pair_CB_Mass"])
sel_nom_delta_preselection_me = Calculation(nom_delta_preselection_me, ["Pos_ME_Pt", "Neg_ME_Pt", "Pair_ME_Mass"])
sel_nom_delta_preselection_ms = Calculation(nom_delta_preselection_ms, ["Pos_MS_Pt", "Neg_MS_Pt", "Pair_MS_Mass"])

def unprescaled_trigger(event):
    return (event["Pos_CB_Pt"] > 6.25) | (event["Neg_CB_Pt"] > 6.25)
sel_unprescaled_trigger = Calculation(unprescaled_trigger, ["Pos_CB_Pt", "Neg_CB_Pt"])

def opp_charge(event):
    return (event["Pair_IsOppCharge"] > 0.5)
sel_opp_charge = Calculation(opp_charge, ["Pair_IsOppCharge"])

def z_selection(event, detector_location = ""):
    pos_pt = event["Pos_{}_Pt".format(detector_location)]
    neg_pt = event["Neg_{}_Pt".format(detector_location)]

    quality_cut = (event["Pos_Quality".format(detector_location)] < 1) \
    & (event["Neg_Quality".format(detector_location)] < 1)

    leading_cut = np.maximum(pos_pt, neg_pt) > 27.0

    pass_opp_charge = opp_charge(event)

    author_cut = (event["Pos_Author".format(detector_location)] == 1) \
    & (event["Neg_Author".format(detector_location)] == 1)

    isolation_cut = (event["Pos_ptvarcone30_TightTTVA_pt1000"]/pos_pt < 0.06) & (event["Pos_ptvarcone30_TightTTVA_pt1000"]/neg_pt < 0.06)

    return leading_cut & pass_opp_charge & author_cut & quality_cut & isolation_cut

z_sel_branches = ["Pos_{}_Pt", "Neg_{}_Pt", "Pos_Quality", "Neg_Quality", "Pair_IsOppCharge", "Pos_Author", "Neg_Author", "Pos_ptvarcone30_TightTTVA_pt1000", "Pos_ptvarcone30_TightTTVA_pt1000"]

def z_selection_id(event):
    return z_selection(event, detector_location = "ID")
sel_z_selection_id = Calculation(z_selection_id, [el.format("ID") if "{}" in el else el for el in z_sel_branches])

def z_selection_me(event):
    return z_selection(event, detector_location = "ME")
sel_z_selection_me = Calculation(z_selection_me, [el.format("ME") if "{}" in el else el for el in z_sel_branches])

def z_selection_cb(event):
    return z_selection(event, detector_location = "CB")
sel_z_selection_cb = Calculation(z_selection_cb, [el.format("CB") if "{}" in el else el for el in z_sel_branches])


#φ segmentation of the correction parameters is needed in correspondence of the Large and Small MS sectors. We emphasize that the overlap area between Large and Small sectors is included in the Small sector definition because this improves the data-MC agreement after the application of the correction, as was observed in the studies conducted for the Run-1 muon performance paper [3]. In the barrel region, |η| < 1.05, the Large sector boundaries are:
#(−0.180+k×0.785<φ<0.180+k×0.785)∨(φ>2.960∧φ<−2.960),fork=−3...3, (6) and the Small sector boundaries are:
#0.180 + k × 0.785 < φ < 0.605 + k × 0.785, for k = −4 . . . 3. (7) In the Endcap/CSC region, 1.05 < |η| < 2.7, the Large sector boundaries are:
#(−0.131+k×0.784<φ<0.131+k×0.784)∨(φ>3.011∧φ<−3.011),fork=−3...3, (8) and the Small sector boundaries are:
#0.131 + k × 0.784 < φ < 0.655 + k × 0.784, for k = −4 . . . 3. (9)
def large_sector(event, muon=None, location=None):
    assert muon == "Pos" or muon == "Neg"
    sectors = []
    not_small = np.logical_not(small_sector(event, muon=muon, location=location))
    phi = event["{}_{}_Phi".format(muon, location)]
    eta = np.abs(event["{}_{}_Eta".format(muon, location)])

    for k in range(-3, 4):

        this_selection_barrel = \
        (\
            ((-0.180+k*0.785) < phi) \
            &\
            (phi < (0.180+k*0.785)) \
        ) \
        &\
        (eta < 1.05)

        this_selection_endcap =\
        (\
            (((-0.131+k*0.784)<phi) & (phi<(0.131+k*0.784)))\
            |\
            ( (phi>3.011) & (phi<-3.011)) \
        ) \
        &\
        ( \
            (eta < 2.7) \
            &\
            (1.05 < eta)\
        )

        sectors.append( (this_selection_barrel | this_selection_endcap) & not_small )

    return np.logical_or.reduce(sectors) #take the logical or of all sector selections

def small_sector(event, muon=None,location=None):
    assert muon == "Pos" or muon == "Neg"
    sectors = []
    phi = event["{}_{}_Phi".format(muon, location)]
    eta = np.abs(event["{}_{}_Eta".format(muon, location)])
    for k in range(-4, 4):


        this_selection_barrel =\
        ( \
            ( (0.180 + k * 0.785) < phi )\
            &\
            ( phi < (0.605 + k * 0.785) ) \
        )\
        &\
        (\
            (eta < 1.05)\
        )
        sectors.append(this_selection_barrel)

        this_selection_endcap =\
        (\
            ((0.131 + k * 0.784) < phi)\
            &\
            (phi < (0.655 + k * 0.784) )\
        ) \
        & \
        ( \
            (eta < 2.7) \
            &\
            (1.05 < eta) \
        )
        sectors.append(this_selection_endcap)

    return np.logical_or.reduce(sectors) #take the logical or of all sector selections

def large_sector_ID_Pos(event):
    return large_sector(event, muon="Pos", location="ID")
sel_large_sector_ID_Pos = Calculation(large_sector_ID_Pos, ["Pos_ID_Pt", "Pos_ID_Eta", "Pos_ID_Phi"])

def large_sector_ME_Pos(event):
    return large_sector(event, muon="Pos", location="ME")
sel_large_sector_ME_Pos = Calculation(large_sector_ME_Pos, ["Pos_ME_Pt", "Pos_ME_Eta", "Pos_ME_Phi"])

def large_sector_ID_Neg(event):
    return large_sector(event, muon="Neg", location="ID")
sel_large_sector_ID_Neg = Calculation(large_sector_ID_Neg, ["Neg_ID_Pt", "Neg_ID_Eta", "Neg_ID_Phi"])

def large_sector_ME_Neg(event):
    return large_sector(event, muon="Neg", location="ME")
sel_large_sector_ME_Neg = Calculation(large_sector_ME_Neg, ["Neg_ME_Pt", "Neg_ME_Eta", "Neg_ME_Phi"])

def small_sector_ID_Pos(event):
    return small_sector(event, muon="Pos", location="ID")
sel_small_sector_ID_Pos = Calculation(small_sector_ID_Pos, ["Pos_ID_Pt", "Pos_ID_Eta", "Pos_ID_Phi"])

def small_sector_ME_Pos(event):
    return small_sector(event, muon="Pos", location="ME")
sel_small_sector_ME_Pos = Calculation(small_sector_ME_Pos, ["Pos_ME_Pt", "Pos_ME_Eta", "Pos_ME_Phi"])

def small_sector_ID_Neg(event):
    return small_sector(event, muon="Neg", location="ID")
sel_small_sector_ID_Neg = Calculation(small_sector_ID_Neg, ["Neg_ID_Pt", "Neg_ID_Eta", "Neg_ID_Phi"])

def small_sector_ME_Neg(event):
    return small_sector(event, muon="Neg", location="ME")
sel_small_sector_ME_Neg = Calculation(small_sector_ME_Neg, ["Neg_ME_Pt", "Neg_ME_Eta", "Neg_ME_Phi"])

def define_eta_selection(event, range_low, range_high, detector_location, charge):
    branchname = "{}_{}_Eta".format(charge, detector_location)
    return (range_low <= event[branchname]) & (event[branchname] < range_high)


