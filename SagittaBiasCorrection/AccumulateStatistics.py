from SagittaBiasUtils import convert_df_to_data, put_data_back_in_df, get_df_for_job
import numpy as np

def calculate_rms(df, args):
    var = "Pair_{}_Mass".format(args.detector_location)
    xs = df[var].values
    weights = df["TotalWeight"].values
    rms = np.sqrt(np.average(xs**2, weights = weights) - np.average(xs, weights=weights)**2)
    return rms

def calculate_mean(df, args):
    var = "Pair_{}_Mass".format(args.detector_location)
    weights = df["TotalWeight"].values
    mean = np.average(df[var].values, weights=weights)
    return mean

def get_mins_maxs(df, args, eta_edges, phi_edges):
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

    df["pos_bindex"] = global_binning_pos.get_global_bindex(df)
    df["neg_bindex"] = global_binning_neg.get_global_bindex(df)
    df["pos_bindex_eta"] = global_binning_pos.get_local_bindex(df)
    df["neg_bindex_eta"] = global_binning_neg.get_local_bindex(df)
    df["pos_bindex_phi"] = phi_binning_pos.get_local_bindex(df)
    df["neg_bindex_phi"] = phi_binning_neg.get_local_bindex(df)

    mins = np.ones((global_binning_pos.get_local_nbins(), phi_binning_pos.get_local_nbins()))
    maxs = np.ones((global_binning_pos.get_local_nbins(), phi_binning_pos.get_local_nbins()))

    #create a histogram that contains the highest pT and lowest pT muon in each bin
    for i in range(0, global_binning_pos.get_global_nbins()):
        df_in_bin_pos = df.query("pos_bindex == {}".format(i))
        pos_pts = df_in_bin_pos["Pos_{}_Pt".format(args.detector_location)]

        df_in_bin_neg = df.query("neg_bindex == {}".format(i))
        neg_pts = df_in_bin_neg["Neg_{}_Pt".format(args.detector_location)]

        max_pos = max(pos_pts)
        max_neg = max(neg_pts)
        min_pos = min(pos_pts)
        min_neg = min(neg_pts)

        pos_bindex_eta = df_in_bin_pos["pos_bindex_eta"].values
        neg_bindex_eta = df_in_bin_neg["neg_bindex_eta"].values
        pos_bindex_phi = df_in_bin_pos["pos_bindex_phi"].values
        neg_bindex_phi = df_in_bin_neg["neg_bindex_phi"].values

        pos_bindex_eta_unique = np.unique(pos_bindex_eta)
        assert len(pos_bindex_eta_unique) == 1
        pos_bindex_eta_unique = pos_bindex_eta_unique[0]

        neg_bindex_eta_unique = np.unique(neg_bindex_eta)
        assert len(neg_bindex_eta_unique) == 1
        neg_bindex_eta_unique = neg_bindex_eta_unique[0]

        pos_bindex_phi_unique = np.unique(pos_bindex_phi)
        assert len(pos_bindex_phi_unique) == 1
        pos_bindex_phi_unique = pos_bindex_phi_unique[0]

        neg_bindex_phi_unique = np.unique(neg_bindex_phi)
        assert len(neg_bindex_phi_unique) == 1
        neg_bindex_phi_unique = neg_bindex_phi_unique[0]

        assert neg_bindex_phi_unique == pos_bindex_phi_unique
        assert neg_bindex_eta_unique == pos_bindex_eta_unique

        bindex_eta = neg_bindex_eta_unique
        bindex_phi = pos_bindex_phi_unique

        mins[bindex_eta, bindex_phi] = min(min_pos, min_neg)
        maxs[bindex_eta, bindex_phi] = max(max_pos, max_neg)

    return mins, maxs

from SagittaBiasUtils import get_mass_selection
from binnings import Binning
from MatrixInversion import find_bindex

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Calculate the statistics associated with the dataframe.')
    parser.add_argument('--filename', type=str, dest='filename')
    parser.add_argument('--start', type=int, dest='start')
    parser.add_argument('--stop', type=int, dest='stop')
    parser.add_argument('--detector_location', type=str, dest='detector_location')
    parser.add_argument('--output_filename', type=str, dest='output_filename')
    parser.add_argument('--inject', '-i', type=str, dest="inject", default = "", required=False)
    parser.add_argument('--correct', '-c', type=str, dest="correct", default = "", required=False)
    parser.add_argument('--resonance', '-r', type=str, dest="resonance", default="Z", required=False)
    parser.add_argument('--selection', '-s', type=str, dest="selection", default="", required=False)
    args = parser.parse_args()
    args.selection = ""
    print(args)

    df, eta_edges, phi_edges = get_df_for_job(args) #get a dataframe for the statistics calculations

    pre_mins, pre_maxs = get_mins_maxs(df, args, eta_edges, phi_edges)

    #calculate the pre correction statistics
    pre_rms = calculate_rms(df, args)
    pre_mean = calculate_mean(df, args)

    var = "Pair_{}_Mass".format(args.detector_location)
    pre_var = np.array(df[var].values)

    with open(args.correct, "rb") as f:
        import pickle as pkl
        correction = pkl.load(f)

    data = convert_df_to_data(df)
    data = correction.calibrate(data)
    df = put_data_back_in_df(data, df)

    post_rms = calculate_rms(df, args)
    post_mean = calculate_mean(df, args)

    df = df.query(get_mass_selection(args))
    post_rms_selection = calculate_rms(df, args)
    post_mean_selection = calculate_mean(df, args)
    post_mins, post_maxs = get_mins_maxs(df, args, eta_edges, phi_edges)

    print("Previously... min: {:.4f} max {:.4f}".format(min(pre_var), max(pre_var)))
    print("Afterwards... min: {:.4f} max {:.4f}".format(min(df[var].values), max(df[var].values)))
    print("Previously... std: {:.4f} mean {:.4f}".format(np.std(pre_var), np.average(pre_var)))
    print("Afterwards... std: {:.4f} mean {:.4f}".format(np.std(df[var].values), np.average(df[var].values)))
    print("Previously ...")
    print(pre_maxs)
    print("Afterwards ...")
    print(post_maxs)

    to_write = {"pre_rms":pre_rms, "post_rms":post_rms, "pos_rms_selection": post_rms_selection,  "pre_mean":pre_mean, "post_mean": post_mean, "args": args, "pos_mean_selection": post_mean_selection, "pre_mins":pre_mins, "pre_maxs":pre_maxs, "post_mins":post_mins, "post_maxs":post_maxs}

    with open(args.output_filename, "wb") as f:
        import pickle as pkl
        pkl.dump(to_write, f)
    print("__FINISHED__")
