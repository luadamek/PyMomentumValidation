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
from SagittaBiasUtils import merge_results, get_histogram_function, merge_results



def get_qm_m(df, detector_location, phi_binning_pos, phi_binning_neg, eta_binning_pos, eta_binning_neg, leading_only = True):
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
                selection_pos = selection.format(charge = "pos", value_eta = i, value_phi = j)
                selection_neg = selection.format(charge = "neg", value_eta = i, value_phi = j)

                selection_pos = "({}) and ({})".format(pos_leading_selection, selection_pos)
                selection_neg = "({}) and ({})".format(neg_leading_selection, selection_neg)
            else:
                selection = "({charge}_bindex_phi == {value_phi}) and ({charge}_bindex_eta == {value_eta})"
                selection_pos = selection.format(charge = "pos", value_eta = i, value_phi = j)
                selection_neg = selection.format(charge = "neg", value_eta = i, value_phi = j)

            qm_average = 0.0

            df_pos = df.query(selection_pos)
            df_neg = df.query(selection_neg)

            pos_sum = np.sum(df_pos["TotalWeight"].values)
            neg_sum = np.sum(df_neg["TotalWeight"].values)

            val_pos = np.sum(df_pos["Pair_{}_Mass".format(detector_location)].values * df_pos["TotalWeight"].values)
            qm_average += val_pos

            val_neg = np.sum(df_neg["Pair_{}_Mass".format(detector_location)].values * df_neg["TotalWeight"].values)
            qm_average -= val_neg

            if (pos_sum + neg_sum) > 0.0:
                qm_means[i, j] = qm_average / (pos_sum + neg_sum)
                q_means[i, j] = (pos_sum - neg_sum) / (pos_sum + neg_sum)
            else:
                qm_means[i, j] = 0.0
                q_means[i, j] = 0.0

    nentries = np.sum(df["TotalWeight"].values)
    if nentries > 0.0: mean = np.average(df["Pair_{}_Mass".format(detector_location)].values, weights = df["TotalWeight"].values)
    else: mean = 0.0
    return qm_means, mean, q_means, nentries

def get_deltas_from_job(outfile_location, update_cache = False):
    import glob
    import os
    import pickle as pkl
    import ROOT

    output_statistics = glob.glob(os.path.join(outfile_location, "*.pkl"))
    output_statistics = [m for m in output_statistics if "CACHE" not in os.path.split(m)[-1]]

    cache_file = os.path.join(outfile_location, "CACHE.pkl")
    failed = True
    try:
        print("Trying to open {}".format(cache_file))
        import pickle as pkl
        with open(cache_file, "rb") as f:
            delta_hist,  var_dict, detector_location, corrections = pkl.load(f)
        print("Successfully opened {}".format(cache_file))
        failed = False
    except Exception as e: pass

    if update_cache:
        if len(output_statistics) == 0: raise ValueError("Couldn't create the cache because there were no files to read...")
        print("You want to update the cache. I am doing that. Opening each pkl file instead")
        opened = []
        for m in output_statistics:
            with open(m, "rb") as f:
                print("opening {}".format(m))
                opened.append(pkl.load(f))
                opened[-1]["mean_q"][np.isnan(opened[-1]["mean_q"])] = 0.0
                if np.isnan(opened[-1]["mean_m"]): opened[-1]["mean_m"] = 0.0
                opened[-1]["mean_qm"][np.isnan(opened[-1]["mean_qm"])] = 0.0

        mean_mass = merge_results(opened, "mean_m")
        mean_qmass = merge_results(opened, "mean_qm")
        mean_q = merge_results(opened, "mean_q")

        delta_s = ((mean_qmass / mean_mass) - (mean_q))
        deltas = 4 * delta_s/mean_mass

        binning_phi = opened[0]["phi_binning_pos"]
        binning_eta = opened[0]["eta_binning_pos"]
        detector_location = opened[0]["detector_location"]

        from SagittaBiasUtils import place_deltas_into_histogram
        delta_hist, var_dict = place_deltas_into_histogram(deltas, (binning_eta, binning_phi), detector_location)

        corrections = None
        if "corrections" in opened[0] and opened[0]["corrections"] != "":
            corrections = opened[0]["corrections"]

        import pickle as pkl
        with open(cache_file, "wb") as f:
            pkl.dump((delta_hist,  var_dict, detector_location, corrections), f)

        del opened
        print("Done opening")

    if failed and not update_cache:
        raise ValueError("Call this function with update_cache True if there is no cache file already")

    if corrections is not None:
        for c in corrections.split(","):
            delta_hist.Add(get_deltas_from_job(c)[0], 1.0)

    return delta_hist, var_dict, detector_location

if __name__ == "__main__":
    from SagittaBiasUtils import get_parser, get_df_for_job
    parser = get_parser()
    parser.add_argument('--use_both_lead_and_sublead', '-lo', action="store_true", dest="use_both_lead_and_sublead")
    parser.add_argument('--filename', type=str, dest='filename')
    parser.add_argument('--start', type=int, dest='start')
    parser.add_argument('--stop', type=int, dest='stop')

    args = parser.parse_args()
    args.method = "delta_qm"
    df, eta_edges, phi_edges= get_df_for_job(args) #don't need the global binning, just the edges

    phi_binning_pos = Binning("Pos_{}_Phi".format(args.detector_location), phi_edges, None, repr_override=None)
    phi_binning_pos.recursively_include_overflow(False)
    phi_binning_neg = Binning("Neg_{}_Phi".format(args.detector_location), phi_edges, None, repr_override=None)
    phi_binning_neg.recursively_include_overflow(False)
    eta_binning_pos = Binning("Pos_{}_Eta".format(args.detector_location), eta_edges, None, repr_override=None)
    eta_binning_pos.recursively_include_overflow(False)
    eta_binning_neg = Binning("Neg_{}_Eta".format(args.detector_location), eta_edges, None, repr_override=None)
    eta_binning_neg.recursively_include_overflow(False)

    mean_qm, mean_m, mean_q, nentries = get_qm_m(df, args.detector_location, phi_binning_pos, phi_binning_neg, eta_binning_pos, eta_binning_neg, leading_only = not args.use_both_lead_and_sublead)

    if not os.path.exists(os.path.split(args.output_filename)[0]):
        os.makedirs(os.path.split(args.output_filename)[0])

    with open(args.output_filename, "wb") as f:
        import pickle as pkl
        pkl.dump({"mean_qm":mean_qm, "mean_m":mean_m, "mean_q": mean_q, "nentries":nentries, "phi_binning_pos": phi_binning_pos, "phi_binning_neg": phi_binning_neg, "eta_binning_pos": eta_binning_pos, "eta_binning_neg": eta_binning_neg, "detector_location":args.detector_location, "corrections":args.corrections}, f)
        print("DUMPED TO ", args.output_filename)
    print("__FINISHED__")

