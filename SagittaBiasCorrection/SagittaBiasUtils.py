import numpy as np
from BiasCorrection import SagittaBiasCorrection
from BiasInjection import injection_histogram
import math

from variables import \
                      calc_pos_id_pt, calc_neg_id_pt,\
                      calc_pos_ms_pt, calc_neg_ms_pt,\
                      calc_pos_me_pt, calc_neg_me_pt,\
                      calc_pos_cb_pt, calc_neg_cb_pt,\
                      calc_pos_id_eta, calc_neg_id_eta,\
                      calc_pos_ms_eta, calc_neg_ms_eta,\
                      calc_pos_me_eta, calc_neg_me_eta,\
                      calc_pos_cb_eta, calc_neg_cb_eta,\
                      calc_pos_id_phi, calc_neg_id_phi,\
                      calc_pos_ms_phi, calc_neg_ms_phi,\
                      calc_pos_me_phi, calc_neg_me_phi,\
                      calc_pos_cb_phi, calc_neg_cb_phi

from BiasCorrection import SagittaBiasCorrection
import ROOT

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

def find_bindex(edges_of_bin, all_edges):
    bindex = 1
    found=False
    for bin_low, bin_high in zip(all_edges[:-1], all_edges[1:]):
        if bin_low == edges_of_bin[0] and bin_high == edges_of_bin[1]:
            return bindex
        bindex += 1
    assert False

def place_deltas_into_histogram(deltas, binning, detector_location):

    if type(binning) != tuple:

        x_bins = binning.bin_edges
        y_bins = binning.subbins[0].bin_edges

        x_var = binning.variable.replace("Pos_", "").replace("Neg_", "")
        y_var = binning.subbins[0].variable.replace("Pos_", "").replace("Neg_", "")

        from array import array
        delta_hist = ROOT.TH2D("delta", "delta", len(x_bins) - 1, array('d',x_bins), len(y_bins) - 1, array('d',y_bins))
        delta_hist.GetXaxis().SetTitle(x_var)
        delta_hist.GetYaxis().SetTitle(y_var)

        for i in range(0, len(deltas)):
            edges = binning.edges_global(i)
            bindex = binning.edges_global
            edges_dict = {}
            edges_dict[y_var] = edges[1]
            edges_dict[x_var] = edges[0]
            x_bindex = find_bindex(edges_dict[x_var], x_bins)
            y_bindex = find_bindex(edges_dict[y_var], y_bins)
            delta_hist.SetBinContent(x_bindex, y_bindex, deltas[i])

    else:
        x_bins = binning[0].bin_edges
        y_bins = binning[1].bin_edges

        x_var = binning[0].variable.replace("Pos_", "").replace("Neg_", "")
        y_var = binning[1].variable.replace("Pos_", "").replace("Neg_", "")

        from array import array
        delta_hist = ROOT.TH2D("delta", "delta", len(x_bins) - 1, array('d',x_bins), len(y_bins) - 1, array('d',y_bins))
        delta_hist.GetXaxis().SetTitle(x_var)
        delta_hist.GetYaxis().SetTitle(y_var)

        for x_bindex in range(1, len(x_bins)):
            for y_bindex in range(1, len(y_bins)):
                delta_hist.SetBinContent(x_bindex, y_bindex, deltas[x_bindex-1, y_bindex-1])


    return delta_hist, {"x_var":x_var, "y_var":y_var}

def merge_results(list_of_covs,key ):
    total = sum([el["nentries"] for el in list_of_covs])
    total_cov = sum([el["nentries"] * el[key] for el in list_of_covs])
    return total_cov/total

def get_variables(region):
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
    elif region == "ME":
        pos_varx = calc_pos_me_eta
        neg_varx = calc_neg_me_eta
        pos_vary = calc_pos_me_phi
        neg_vary = calc_neg_me_phi
    else: raise ValueError()
    return pos_varx, neg_varx, pos_vary, neg_vary

def inject_bias(df, region, injection_function):
    injection_histogram = injection_function(region)
    pos_varx, neg_varx, pos_vary, neg_vary = get_variables(region)
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
    from BiasInjection import injection_histogram_local, injection_histogram_global, injection_histogram_globalpluslocal, injection_histogram_null, injection_histogram_data, injection_histogram_random
    if inject == "Global": injection_function = injection_histogram_global
    if inject == "Random": injection_function = injection_histogram_random
    if inject == "GlobalPlusLocal": injection_function = injection_histogram_globalpluslocal
    if inject == "Local": injection_function = injection_histogram_local
    if inject == "Null": injection_function = injection_histogram_null
    if inject == "Data": injection_function = injection_histogram_data
    return injection_function

def get_parser():
    import argparse
    parser = argparse.ArgumentParser(description='a parser that handles options w.r.t. the sagitta bias correction')
    parser.add_argument('--detector_location', type=str, dest='detector_location')
    parser.add_argument('--output_filename', type=str, dest='output_filename')
    parser.add_argument('--inject', '-i', type=str, dest="inject", default = "", required=False)
    parser.add_argument('--pt_threshold', '-pth', type=float, dest="pt_threshold", default=-1.0, required=False)
    parser.add_argument('--preselection', '-presel', type=str, dest="preselection", default="", required=False)
    parser.add_argument('--select_before_corrections', '-sel_bf_corr', type=str, dest="select_before_corrections", default="", required=False)
    parser.add_argument('--select_after_corrections', '-sel_af_corr', type=str, dest="select_after_corrections", default="", required=False)
    parser.add_argument('--corrections', '-c', type=str, dest="corrections", default="", required=False)
    parser.add_argument("--qm_corrections", "-qmc", type=str, dest="qm_corrections", default="", required=False)
    parser.add_argument("--no_cleaning_selection", "-ncsel", action="store_false")
    parser.add_argument("--fold", "-f", type=str, default="None")
    return parser


def apply_selection(df, selection, args):
    selection = selection.format(*[args.detector_location for i in range(0, selection.count("{}"))])
    print("Applying selection {}".format(selection))
    df = df.query(selection)
    return df

def apply_cleaning_selection(df, args):
    base_selection = "(Pos_{loc}_Pt > 0.0) and (Neg_{loc}_Pt > 0.0)" #for some reason, some ME tracks have pT = -999 but a mass close to 91.2 GeV... I don't know why
    selection = base_selection.format(loc=args.detector_location)
    return df.query(selection)

from utils import get_dataframe
def get_df_for_job(args):

    if (args.inject != "") and (args.inject != None) and (args.inject != "None"):
        injection_histogram_function = get_histogram_function(args.inject)

    variables = ["Pos_{}_Eta", "Neg_{}_Eta", "Pos_{}_Phi", "Neg_{}_Phi", "Pos_{}_Pt", "Neg_{}_Pt", "Pair_{}_Mass", "TotalWeight"] #all of the variables needed

    variables = [v.format(args.detector_location) for v in variables]

    if args.detector_location == "ID": eta_edges = eta_edges_ID
    else: eta_edges = eta_edges_else

    do_add_pair_mass = False
    if "v03" in args.filename and "v2" in args.filename and "Pair_MS_Mass" in variables:
        variables.remove("Pair_MS_Mass")
        do_add_pair_mass = True

    if args.fold != "None":
        variables += ["EvtNumber"]
        variables = list(set(variables))


    df = get_dataframe(args.filename, args.start, args.stop, variables, "")

    if args.fold != "None":
        int_fold = None
        fold_divisor = 2 
        if args.fold == "one": int_fold = 0
        if args.fold == "two": int_fold = 1
        if int_fold is None: raise ValueError("Doesn't work!")

        fold_selection = "EvtNumber % fold_divisor == fold"
        print("Folding with {}".format(fold_selection))
        print("before folding: {} events".format(len(df)))
        fold_index = df["EvtNumber"].values
        passes = (fold_index % fold_divisor == int_fold)
        df = df.iloc[passes]
        print("after folding: {} events".format(len(df)))

    if "v03" in args.filename and "v2" in args.filename and do_add_pair_mass:
        df = add_pair_mass(df)
    df = apply_cleaning_selection(df, args)

    if args.preselection: df = apply_selection(df, args.preselection, args)

    if (args.inject != "") and (args.inject != None) and (args.inject != "None"):
        df = inject_bias(df, args.detector_location, injection_histogram_function)

    if args.select_before_corrections: df = apply_selection(df, args.select_before_corrections, args)

    #apply the corrections
    if args.corrections != "":
        for c in args.corrections.split(","):
            if args.method == "matrix": from MatrixInversion import get_deltas_from_job
            elif args.method == "delta_qm": from DeltaQMIterativeMethod import get_deltas_from_job
            correction_histogram, _, detector_location = get_deltas_from_job(c)
            assert args.detector_location == detector_location
            pos_varx, neg_varx, pos_vary, neg_vary = get_variables(detector_location)
            correction = SagittaBiasCorrection([correction_histogram],  pos_varx, neg_varx, pos_vary, neg_vary, pos_selections = [], neg_selections = [],flavour = detector_location)
            data = convert_df_to_data(df)
            data = correction.calibrate(data)
            df = put_data_back_in_df(data, df)
            del data

    if args.select_after_corrections: df = apply_selection(df, args.select_after_corrections, args)

    return df, eta_edges, phi_edges
