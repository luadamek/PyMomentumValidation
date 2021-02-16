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

def neg_leading_id(event):
    return get_leading(event, "ID", "Neg")

branches = ["Neg_ID_Pt", "Neg_ID_Pt"]
sel_neg_leading_id = Calculation(neg_leading_id, branches)

def pos_leading_me(event):
    return get_leading(event, "ME", "Pos")

branches = ["Pos_ME_Pt", "Neg_ME_Pt"]
sel_pos_leading_me = Calculation(pos_leading_me, branches)

def neg_leading_me(event):
    return get_leading(event, "ME", "Neg")

branches = ["Neg_ME_Pt", "Neg_ME_Pt"]
sel_neg_leading_me = Calculation(neg_leading_me, branches)

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

def nom_delta_selection_me(event):
    return nom_delta_selection(event, "ME")

sel_nom_delta_selection_id = Calculation(nom_delta_selection_id, ["Pos_ID_Pt", "Neg_ID_Pt", "Pair_ID_Mass"])
sel_nom_delta_selection_me = Calculation(nom_delta_selection_me, ["Pos_ME_Pt", "Neg_ME_Pt", "Pair_ME_Mass"])

def nom_delta_preselection(event, region):
     mass_window = np.abs(event["Pair_{}_Mass".format(region)] - 91.2) < 40.0
     pt_sel = (event["Pos_{}_Pt".format(region)] < 500.0) & (event["Neg_{}_Pt".format(region)] < 500.0) & (event["Pos_{}_Pt".format(region)] > 0.0) & (event["Neg_{}_Pt".format(region)] > 0.0)
     return mass_window & pt_sel

def nom_delta_preselection_id(event):
    return nom_delta_preselection(event, "ID")

def nom_delta_preselection_ms(event):
    return nom_delta_preselection(event, "MS")

def nom_delta_preselection_me(event):
    return nom_delta_preselection(event, "ME")

sel_nom_delta_preselection_id = Calculation(nom_delta_preselection_id, ["Pos_ID_Pt", "Neg_ID_Pt", "Pair_ID_Mass"])
sel_nom_delta_preselection_me = Calculation(nom_delta_preselection_me, ["Pos_ME_Pt", "Neg_ME_Pt", "Pair_ME_Mass"])
sel_nom_delta_preselection_ms = Calculation(nom_delta_preselection_ms, ["Pos_MS_Pt", "Neg_MS_Pt", "Pair_MS_Mass"])


