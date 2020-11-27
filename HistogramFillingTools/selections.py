from calculation import Calculation
import numpy as np

def range_selection_function(event, variable, range_low, range_hi):
    if not isinstance(variable, Calculation): return (event[variable] < range_hi) & (range_low < event[variable])
    else: 
        vals = variable.eval(event)
        return (vals < range_hi) & (range_low < vals)

def pos_leading_id(event):
    return event["Pos_ID_Pt"] > event["Neg_ID_Pt"]
branches = ["Pos_ID_Pt", "Neg_ID_Pt"]
sel_pos_leading_id = Calculation(pos_leading_id, branches)

def neg_leading_id(event):
    return np.logical_not(pos_leading_id(event))
branches = ["Pos_ID_Pt", "Neg_ID_Pt"]
sel_neg_leading_id = Calculation(neg_leading_id, branches)

def check_safe_event(event, charge, region):
     string = "{}_{}_Eta".format(charge, region)
     return (event[string] < 5.0) & (event[string] > -5.0)
