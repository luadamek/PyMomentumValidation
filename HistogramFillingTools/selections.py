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

def get_subleading(event,  location, charge):
    charge_leading = get_leading(event, charge, location)
    return np.logical_not(charge_leading)


def check_safe_event(event, charge, region):
     string = "{}_{}_Eta".format(charge, region)
     return (event[string] < 5.0) & (event[string] > -5.0)
