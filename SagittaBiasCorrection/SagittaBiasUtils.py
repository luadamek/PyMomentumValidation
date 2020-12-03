import numpy as np
from BiasCorrection import SagittaBiasCorrection
from BiasInjection import injection_histogram
import math

from variables import \
                      calc_pos_id_pt, calc_neg_id_pt,\
                      calc_pos_ms_pt, calc_neg_ms_pt,\
                      calc_pos_cb_pt, calc_neg_cb_pt,\
                      calc_pos_id_eta, calc_neg_id_eta,\
                      calc_pos_ms_eta, calc_neg_ms_eta,\
                      calc_pos_cb_eta, calc_neg_cb_eta,\
                      calc_pos_id_phi, calc_neg_id_phi,\
                      calc_pos_ms_phi, calc_neg_ms_phi,\
                      calc_pos_cb_phi, calc_neg_cb_phi

from BiasCorrection import SagittaBiasCorrection

eta_edges_ID = np.linspace(-2.5, +2.5 , 25)
#eta_edges_ID[0] = -2.65
#eta_edges_ID[-1] = 2.65

eta_edges_else = np.linspace(-2.7, +2.7 , 27)
#eta_edges_else[0] = -2.85
#eta_edges_else[-1] = 2.85

phi_edges = np.linspace(-1.0 * math.pi, +1.0 * math.pi, 25)
def convert_df_to_data(df):
    data = {}
    for c in df.columns:
        data[c] = df[c].values
    return data

def put_data_back_in_df(data, df):
    for c in data:
        print(c)
        df[c] = data[c]
    return df

def merge_results(list_of_covs,key ):
    total = sum([el["nentries"] for el in list_of_covs])
    total_cov = sum([el["nentries"] * el[key] for el in list_of_covs])
    return total_cov/total

def inject_bias(df, region, injection_function):
    injection_histogram = injection_function(region)
    if region == "ID":
        pos_varx = calc_pos_id_eta
        neg_varx = calc_neg_id_eta
        pos_vary = calc_pos_id_phi
        neg_vary = calc_neg_id_phi
    elif region == "MS":
        pos_varx = calc_pos_ms_eta
        neg_varx = calc_neg_ms_eta
        pos_vary = calc_pos_ms_phi
        neg_vary = calc_neg_ms_phi
    else: raise ValueError()
    correction = SagittaBiasCorrection([injection_histogram],  pos_varx, neg_varx, pos_vary, neg_vary, pos_selections = [], neg_selections = [],flavour = region)
    data = convert_df_to_data(df)
    data = correction.calibrate(data)
    df = put_data_back_in_df(data, df)
    return df

def add_pair_mass(df):
    from variables import calc_ms_mass
    data = convert_df_to_data(df)
    data["Pair_MS_Mass"] = calc_ms_mass.eval(data)
    df = put_data_back_in_df(data, df)
    print(df["Pair_MS_Mass"].values)
    return df

def get_histogram_function(inject):
    from BiasInjection import injection_histogram_local, injection_histogram_global, injection_histogram_globalpluslocal, injection_histogram_null, injection_histogram_data
    if inject == "Global": injection_function = injection_histogram_global
    if inject == "GlobalPlusLocal": injection_function = injection_histogram_globalpluslocal
    if inject == "Local": injection_function = injection_histogram_local
    if inject == "Null": injection_function = injection_histogram_null
    if inject == "Data": injection_function = injection_histogram_data
    return injection_function

def get_mass_selection(args):
    if args.resonance == "Z":
        mean_mass = 91.2 # GeV
        if args.detector_location == "MS": mean_mass = 86.0 # GeV
        selection = "abs(Pair_{}_Mass - {}) < 12.0".format(args.detector_location, mean_mass)
    elif args.resonance == "JPSI":
        mean_mass = 3.1 # GeV
        selection = "abs(Pair_{}_Mass - {}) < 0.3".format(args.detector_location, mean_mass)
    return selection

from utils import get_dataframe
def get_df_for_job(args):
    if (args.inject != "") and (args.inject != None) and (args.inject != "None"):
        injection_histogram_function = get_histogram_function(args.inject)

    variables = ["Pos_{}_Eta", "Neg_{}_Eta", "Pos_{}_Phi", "Neg_{}_Phi", "Pos_{}_Pt", "Neg_{}_Pt", "Pair_{}_Mass", "TotalWeight"] #all of the variables needed

    selection = get_mass_selection(args)

    variables = [v.format(args.detector_location) for v in variables]

    if args.detector_location == "ID": eta_edges = eta_edges_ID
    else: eta_edges = eta_edges_else

    do_add_pair_mass = False
    if "v03" in args.filename and "v2" in args.filename and "Pair_MS_Mass" in variables:
        variables.remove("Pair_MS_Mass")
        do_add_pair_mass = True

    df = get_dataframe(args.filename, args.start, args.stop, variables, "")
    if "v03" in args.filename and "v2" in args.filename and do_add_pair_mass:
        df = add_pair_mass(df)

    if (args.inject != "") and (args.inject != None) and (args.inject != "None"):
        df = inject_bias(df, args.detector_location, injection_histogram_function)

    if args.selection: df = df.query(args.selection)
    else: df = df.query(selection)

    return df, eta_edges, phi_edges
