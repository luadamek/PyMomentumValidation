#first define the binning to be used for the sagitta bias correction

from binnings import Binning
import math
import numpy as np
import os
from utils import cov as utils_cov
import uproot as ur

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
from SagittaBiasUtils import 

eta_edges_ID = np.linspace(-2.5, +2.5 , 25)
#eta_edges_ID[0] = -2.65
#eta_edges_ID[-1] = 2.65

eta_edges_else = np.linspace(-2.7, +2.7 , 27)
#eta_edges_else[0] = -2.85
#eta_edges_else[-1] = 2.85

phi_edges = np.linspace(-1.0 * math.pi, +1.0 * math.pi, 25)

def get_dataframe(root_file, start, stop,  variables, selection):
    #calculate what bin events belong in

    df = ur.open(root_file)["MuonMomentumCalibrationTree"].pandas.df(branches = variables, entrystart = start, entrystop = stop)
    if selection: df = df.query(selection) #apply the selection
    return df

def get_qm_m(df, detector_location, phi_binning_pos, phi_binning_neg, eta_binning_pos, eta_binning_neg, leading_only = False):
    df["pos_bindex_phi"] = phi_binning_pos.get_global_bindex(df)
    df["neg_bindex_phi"] = phi_binning_neg.get_global_bindex(df)
    df["pos_bindex_eta"] = eta_binning_pos.get_global_bindex(df)
    df["neg_bindex_eta"] = eta_binning_neg.get_global_bindex(df)
    #get rid of overflow
    print("Before overflow correction {}".format(len(df)))
    df = df.query("(pos_bindex_phi >= 0) and (neg_bindex_phi >= 0) and (pos_bindex_eta >= 0) and (neg_bindex_eta >= 0)")
    print("After overflow correction {}".format(len(df)))

    qm_means = np.zeros((eta_binning_pos.get_global_nbins(), phi_binning_pos.get_global_nbins()))
    q_means = np.zeros((eta_binning_pos.get_global_nbins(), phi_binning_pos.get_global_nbins()))

    for i in range(eta_binning_pos.get_global_nbins()):
        for j in range(phi_binning_pos.get_global_nbins()):

            if leading_only:
                pos_leading_selection = "(Pos_{loc}_Pt > Neg_{loc}_Pt)".format(loc=detector_location)
                neg_leading_selection = "(Neg_{loc}_Pt >= Pos_{loc}_Pt)".format(loc=detector_location)

                selection = "(({charge}_bindex_phi == {value_phi}) and ({charge}_bindex_eta == {value_eta}))"
                selection_pos = selection.format(charge == "pos", value_eta = i, value_phi = j)
                selection_neg = selection.format(charge == "neg", value_eta = i, value_phi = j)

                selection_pos = "({}) and ({})".format(pos_leading_selection, selection_pos)
                selection_neg = "({}) and ({})".format(neg_leading_selection, selection_neg)
            else:
                selection = "({charge}_bindex_phi == {value_phi}) and ({charge}_bindex_eta == {value_eta})"
                selection_pos = selection.format(charge == "pos", value_eta = i, value_phi = j)
                selection_neg = selection.format(charge == "neg", value_eta = i, value_phi = j)

            qm_average = 0.0

            df_pos = df.query(selection_pos)
            val_pos = np.sum(df_pos["Pair_{}_Mass".format(detector_location)].values * df_pos["TotalWeight"].values)
            qm_average += val_pos

            df_neg = df.query(selection_neg)
            val_neg = np.sum(df_neg["Pair_{}_Mass".format(detector_location)].values * df_neg["TotalWeight"].values)
            qm_average -= val_neg

            qm_means[i, j] = qm_average / (np.sum(df_pos["TotalWeight"].values) + np.sum(df_neg["TotalWeight"].values))

            pos_sum = np.sum(df_pos["TotalWeight"].values)
            neg_sum = np.sum(df_neg["TotalWeight"].values)
            q_means[i, j] = (pos_sum - neg_sum) / (pos_sum + neg_sum)

    mean = np.average(df["Pair_{}_Mass".format(detector_location).values, weights = df["TotalWeight"].values)
    nentries = np.sum(df["TotalWeight"].values)
    return qm_means, mean, q_mean, nentries

def merge_covariances(list_of_covs,key ):
    total = sum([el["nentries"] for el in list_of_covs])
    total_cov = sum([el["nentries"] * el[key] for el in list_of_covs])
    return total_cov/total

def get_deltas_from_job(outfile_location):
    import glob
    import os
    import pickle as pkl
    import ROOT

    matrices = glob.glob(os.path.join(outfile_location, "*.pkl"))

    opened = []
    for m in matrices:
        with open(m, "rb") as f:
            print("opening {}".format(m))
            opened.append(pkl.load(f))

    mean_mass = merge_covariances(opened, "mean_m")
    mean_qmass = merge_covariances(opened, "mean_qm")
    mean_q = merge_covariances(opened, "mean_q")

    deltas = (mean_qmass / mean_mass) - (mean_q)

    binning_phi = opened[0]["phi_binning_pos"]
    binning_eta = opened[0]["eta_binning_pos"]
    detector_location = opened[0]["detector_location"]

    x_bins = binning_eta.bin_edges
    y_bins = binning_phi.bin_edges

    from array import array
    delta_hist = ROOT.TH2D("delta", "delta", len(x_bins) - 1, array('d',x_bins), len(y_bins) - 1, array('d',y_bins))

    #put the deltas back into a histogram
    n_xbins = len(xbins) - 1
    n_ybins = len(ybins) - 1
    for i in range(1, n_xbins + 1):
        for j in range(1, n_ybins + 1):
            edges_dict = {}
            edges_dict[y_var] = edges[1]
            edges_dict[x_var] = edges[0]
            delta_hist.GetXaxis().SetTitle(x_var)
            delta_hist.GetYaxis().SetTitle(y_var)
            delta_hist.SetBinContent(i, j, deltas[i-1, j-1])

    return delta_hist, {"x_var":x_var, "y_var":y_var}, detector_location


def get_histogram_function(inject):
    from BiasInjection import injection_histogram_local, injection_histogram_global, injection_histogram_globalpluslocal, injection_histogram_null, injection_histogram_data
    if inject == "Global": injection_function = injection_histogram_global
    if inject == "GlobalPlusLocal": injection_function = injection_histogram_globalpluslocal
    if inject == "Local": injection_function = injection_histogram_local
    if inject == "Null": injection_function = injection_histogram_null
    if inject == "Data": injection_function = injection_histogram_data
    return injection_function

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Calculate the covariance matrices and vectors needed to compute the sagitta bias.')
    parser.add_argument('--filename', type=str, dest='filename')
    parser.add_argument('--start', type=int, dest='start')
    parser.add_argument('--stop', type=int, dest='stop')
    parser.add_argument('--detector_location', type=str, dest='detector_location')
    parser.add_argument('--output_filename', type=str, dest='output_filename')
    parser.add_argument('--inject', '-i', type=str, dest="inject", default = "", required=False)
    parser.add_argument('--leading_only', '-lo', action="store_true")
    parser.add_argument('--load_corrections', '-lc', type=str, dest="load_injections", default = "", required = False)
    parser.add_argument('--load_subtractions', '-ls', type=str, dest="load_subtractions", default = "", required=False)

    args = parser.parse_args()
    df, eta_edges, phi_edges= SagittaBiasUtils.get_df_for_job(args) #don't need the global binning, just the edges

    phi_binning_pos = Binning("Pos_{}_Phi".format(args.detector_location), phi_edges, None, repr_override=None)
    phi_binning_neg = Binning("Neg_{}_Phi".format(args.detector_location), phi_edges, None, repr_override=None)
    eta_binning_pos = Binning("Pos_{}_Eta".format(args.detector_location), eta_edges, None, repr_override=None)
    eta_binning_neg = Binning("Neg_{}_Eta".format(args.detector_location), eta_edges, None, repr_override=None)

    mean_qm, mean_m, mean_q, nentries = get_qm_m(df, args.detector_location, phi_binning_pos, phi_binning_neg, eta_binning_pos, eta_binning_neg, leading_only = args.leading_only)

    if not os.path.exists(os.path.split(args.output_filename)[0]):
        os.makedirs(os.path.split(args.output_filename)[0])

    with open(args.output_filename, "wb") as f:
        import pickle as pkl
        pkl.dump({"mean_qm":mean_qm, "mean_m":mean_m, "mean_q": mean, "nentries":nentries, "phi_binning_pos": phi_binning_pos, "phi_binning_neg": phi_binning_neg, "eta_binning_pos": eta_binning_pos, "eta_binning_neg": eta_binning_neg, "detector_location":args.detector_location}, f)
    print("__FINISHED__")

