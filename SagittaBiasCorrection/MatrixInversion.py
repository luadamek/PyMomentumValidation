#first define the binning to be used for the sagitta bias correction

from binnings import Binning
import math
import numpy as np
import os
from utils import cov as utils_cov
import uproot as ur

from SagittaBiasUtils import get_df_for_job

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

from SagittaBiasUtils import eta_edges_ID, eta_edges_else, phi_edges, convert_df_to_data, put_data_back_in_df, inject_bias, add_pair_mass, get_histogram_function

from utils import get_dataframe

def get_cov_matrices(df, global_binning_pos, global_binning_neg, detector_location):
    df["pos_bindex"] = global_binning_pos.get_global_bindex(df)
    df["neg_bindex"] = global_binning_neg.get_global_bindex(df)
    #get rid of overflow
    print("Before overflow correction {}".format(len(df)))
    df = df.query("(pos_bindex >= 0) and (neg_bindex >= 0)")
    print("After overflow correction {}".format(len(df)))

    n_corr_bins = global_binning_pos.get_global_nbins()#number of bins in which to apply the correction
    e_vector = np.zeros((n_corr_bins, len(df)))

    weights = df.eval("TotalWeight").values
    print(weights)
    #calculate the e vector
    e_vector[df["pos_bindex"].values, np.arange(0, len(df))] += df.eval("(Pair_{}_Mass ** 2) * Pos_{}_Pt".format(detector_location, detector_location)).values
    e_vector[df["neg_bindex"].values, np.arange(0, len(df))] -= df.eval("(Pair_{}_Mass ** 2) * Neg_{}_Pt".format(detector_location, detector_location)).values

    print("calculating the covariance")
    #calculate the covariance matrix
    cov = utils_cov(e_vector, aweights=weights)
    print("Done!")

    #equal_to = np.zeros((n_corr_bins))
    masses = df.eval("(Pair_{}_Mass ** 2)".format(detector_location)).values
    masses = masses.reshape(masses.shape[0],-1)
    mean_mass = np.average(masses, axis = 0, weights=weights)

    e_vector_trans = e_vector.transpose()
    mean_e_vector = np.average(e_vector_trans, axis=0, weights=weights)

    equal_to = (1.0/np.sum(weights)) * np.sum( weights.reshape(weights.shape[0],-1) * ((masses - mean_mass) * (e_vector_trans - mean_e_vector)), axis=0)

    print(cov)
    print(equal_to)
    return cov, equal_to, np.sum(weights)

from SagittaBiasUtils import merge_results

def find_bindex(edges_of_bin, all_edges):
    bindex = 1
    found=False
    for bin_low, bin_high in zip(all_edges[:-1], all_edges[1:]):
        if bin_low == edges_of_bin[0] and bin_high == edges_of_bin[1]:
            return bindex
        bindex += 1
    assert False


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

    cov = merge_results(opened, "cov")
    b = merge_results(opened, "b")

    import numpy as np
    delta = np.linalg.solve(cov, b)

    #ok now load everything into a histogram
    binning = opened[0]["pos_binning"]
    detector_location = opened[0]["detector_location"]

    x_bins = binning.bin_edges
    y_bins = binning.subbins[0].bin_edges

    x_var = binning.variable.replace("Pos_", "").replace("Neg_", "")
    y_var = binning.subbins[0].variable.replace("Pos_", "").replace("Neg_", "")

    #delta_hist = ROOT.TH2D("delta", "delta", len(x_bins)-1, min(x_bins), max(x_bins), len(y_bins)-1, min(y_bins), max(y_bins))
    from array import array
    delta_hist = ROOT.TH2D("delta", "delta", len(x_bins) - 1, array('d',x_bins), len(y_bins) - 1, array('d',y_bins))

    for i in range(0, len(delta)):
        edges = binning.edges_global(i)
        bindex = binning.edges_global
        edges_dict = {}
        edges_dict[y_var] = edges[1]
        edges_dict[x_var] = edges[0]
        x_bindex = find_bindex(edges_dict[x_var], x_bins)
        y_bindex = find_bindex(edges_dict[y_var], y_bins)
        delta_hist.GetXaxis().SetTitle(x_var)
        delta_hist.GetYaxis().SetTitle(y_var)
        delta_hist.SetBinContent(x_bindex, y_bindex, delta[i])

    return delta_hist, {"x_var":x_var, "y_var":y_var}, detector_location

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Calculate the covariance matrices and vectors needed to compute the sagitta bias.')
    parser.add_argument('--filename', type=str, dest='filename')
    parser.add_argument('--start', type=int, dest='start')
    parser.add_argument('--stop', type=int, dest='stop')
    parser.add_argument('--detector_location', type=str, dest='detector_location')
    parser.add_argument('--output_filename', type=str, dest='output_filename')
    parser.add_argument('--inject', '-i', type=str, dest="inject", default = "", required=False)
    parser.add_argument('--resonance', '-r', type=str, dest="resonance", default="Z", required=False)
    parser.add_argument('--selection', '-s', type=str, dest="selection", default="", required=False)
    parser.add_argument('--range', '-rg', type=float, dest="range", default=10.0, required=False)
    parser.add_argument('--pt_threshold', '-pth', type=float, dest="pt_threshold", default=-1.0, required=False)
    args = parser.parse_args()

    df, eta_edges, phi_edges = get_df_for_job(args)

    #create a phi binning:
    phi_binning_pos = Binning("Pos_{}_Phi".format(args.detector_location), phi_edges, None, repr_override=None)
    phi_binning_neg = Binning("Neg_{}_Phi".format(args.detector_location), phi_edges, None, repr_override=None)

    pos_eta_subbins = []
    neg_eta_subbins = []
    for i in range(0, len(eta_edges) - 1):
        pos_eta_subbins.append(phi_binning_pos)
        neg_eta_subbins.append(phi_binning_neg)

    #create a global binning scheme
    global_binning_pos = Binning("Pos_{}_Eta".format(args.detector_location), eta_edges, pos_eta_subbins)
    global_binning_pos.recursively_include_overflow(False)
    global_binning_neg = Binning("Neg_{}_Eta".format(args.detector_location), eta_edges, neg_eta_subbins)
    global_binning_neg.recursively_include_overflow(False)

    cov, equal_to, nentries = get_cov_matrices(df, global_binning_pos, global_binning_neg, args.detector_location)

    if not os.path.exists(os.path.split(args.output_filename)[0]):
        os.makedirs(os.path.split(args.output_filename)[0])

    with open(args.output_filename, "wb") as f:
        import pickle as pkl
        pkl.dump({"cov":cov, "b":equal_to, "nentries":nentries, "pos_binning": global_binning_pos, "neg_binning": global_binning_neg, "detector_location":args.detector_location}, f)
    print("__FINISHED__")

