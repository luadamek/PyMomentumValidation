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

from SagittaBiasUtils import eta_edges_ID, eta_edges_else, phi_edges, convert_df_to_data, put_data_back_in_df, inject_bias, add_pair_mass, get_histogram_function, merge_results, find_bindex

def get_cov_matrices(df, detector_location, debug = False):
    #get rid of overflow
    if debug: print("Before overflow correction {}".format(len(df)))
    df = df.query("(pos_bindex >= 0) and (neg_bindex >= 0)")
    if debug: print("After overflow correction {}".format(len(df)))

    n_corr_bins = global_binning_pos.get_global_nbins()#number of bins in which to apply the correction

    e_vector = np.zeros((n_corr_bins, len(df)))
    weights = df.eval("TotalWeight").values

    if debug: print("Printing the weights")
    if debug: print("weights", weights)
    if debug: print("min weight", np.min(weights))
    if debug: print("max weight", np.max(weights))

    #calculate the e vector
    e_vector[df["pos_bindex"].values, np.arange(0, len(df))] += df.eval("(Pair_{}_Mass ** 2) * Pos_{}_Pt".format(detector_location, detector_location)).values
    e_vector[df["neg_bindex"].values, np.arange(0, len(df))] -= df.eval("(Pair_{}_Mass ** 2) * Neg_{}_Pt".format(detector_location, detector_location)).values

    if debug: print("calculating the covariance")
    #calculate the covariance matrix
    cov = utils_cov(e_vector, aweights=weights)
    if debug: print("Done!")

    #equal_to = np.zeros((n_corr_bins))
    masses = df.eval("(Pair_{}_Mass ** 2)".format(detector_location)).values
    masses = masses.reshape(masses.shape[0],-1)
    mean_mass = np.average(masses, axis = 0, weights=weights)

    e_vector_trans = e_vector.transpose()
    mean_e_vector = np.average(e_vector_trans, axis=0, weights=weights)

    equal_to = (1.0/np.sum(weights)) * np.sum( weights.reshape(weights.shape[0],-1) * ((masses - mean_mass) * (e_vector_trans - mean_e_vector)), axis=0)

    return cov, equal_to, np.sum(weights)

def get_deltas_from_job(outfile_location, update_cache = False, final_only=False):
    import glob
    import os
    import pickle as pkl
    import ROOT

    matrices = glob.glob(os.path.join(outfile_location, "*.pkl"))
    matrices = [m for m in matrices if "CACHE" not in os.path.split(m)[-1] and "BOOTSTRAP" not in os.path.split(m)[-1]]

    cache_file = os.path.join(outfile_location, "CACHE.pkl")
    failed = True
    results = None
    corrections = None
    try:
        print("Trying to open {}".format(cache_file))
        import pickle as pkl
        with open(cache_file, "rb") as f:
            stuff = pkl.load(f)
            if type(stuff) == tuple: delta_hist,  var_dict, detector_location, corrections = stuff
            else: results = stuff
        print("Successfully opened {}".format(cache_file))
        failed = False

    except Exception as e: pass

    if update_cache:
        if len(matrices) == 0: raise ValueError("Couldn't create the cache because there were no files to read...")
        print("Failed to open cache. Opening each pkl file instead")
        opened = []
        for m in matrices:
            with open(m, "rb") as f:
                print("opening {}".format(m))
                opened.append(pkl.load(f))

        covs = merge_results(opened, "cov")
        bs = merge_results(opened, "b")

        if not type(covs) == list:
           cov, b = covs, bs
           import numpy as np
           deltas = np.linalg.solve(cov, b)

           binning = opened[0]["pos_binning"]
           detector_location = opened[0]["detector_location"]

           from SagittaBiasUtils import place_deltas_into_histogram
           delta_hist, var_dict = place_deltas_into_histogram(deltas, binning, detector_location)
           corrections = None
           if "corrections" in opened[0] and opened[0]["corrections"] != "":
               corrections = opened[0]["corrections"]

           import pickle as pkl
           with open(cache_file, "wb") as f:
               pkl.dump((delta_hist,  var_dict, detector_location, corrections), f)

           del opened
           print("Done opening")

        else:
           results = []
           for cov, b in zip(covs, bs):
               import numpy as np
               deltas = np.linalg.solve(cov, b)

               binning = opened[0]["pos_binning"]
               detector_location = opened[0]["detector_location"]

               from SagittaBiasUtils import place_deltas_into_histogram
               delta_hist, var_dict = place_deltas_into_histogram(deltas, binning, detector_location)
               corrections = None
               if "corrections" in opened[0] and opened[0]["corrections"] != "":
                   corrections = opened[0]["corrections"]
               results.append((delta_hist,  var_dict, detector_location, corrections))

           import pickle as pkl
           with open(cache_file, "wb") as f:
               pkl.dump(results, f)

           #for el in matrices:
           #    import os
           #    os.system("rm {}".format(m))

           del opened
           print("Done opening")

    if failed and not update_cache:
        raise ValueError("Call this function with update_cache True if there is no cache file already")

    if corrections is not None and not final_only:
        for c in corrections.split(","):
            delta_hist.Add(get_deltas_from_job(c)[0], 1.0)

    if results is None: return delta_hist,  var_dict, detector_location
    else: return results

if __name__ == "__main__":
    from SagittaBiasUtils import get_parser

    parser = get_parser()
    parser.add_argument('--filename', type=str, dest='filename')
    parser.add_argument('--start', type=int, dest='start')
    parser.add_argument('--stop', type=int, dest='stop')
    parser.add_argument('--bootstraps', type=str, dest="bootstraps", required=False, default="")
    args = parser.parse_args()
    args.method = "matrix"

    df, eta_edges, phi_edges = get_df_for_job(args)

    if len(df) != 0: 
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

       if not args.bootstraps:
           cov, equal_to, nentries = get_cov_matrices(df, args.detector_location)
       else:
           cov = []
           equal_to = []
           nentries = []
           for bootstrap_fname in args.bootstraps.split(","):
               with open(bootstrap_fname, "rb") as f:
                   import pickle as pkl
                   bootstraps = pkl.load(f)
                   #print(bootstraps)
               keep = bootstraps[np.in1d(bootstraps,df.index.values)] #only keep those values  that passed the selection for the dataframe
               #print(bootstraps)
               #print(df["read_index"].values)
               #print(df)
               #print(keep)
               this_df = df.loc[keep]
               #print(this_df)
               #print(len(this_df))
               this_cov, this_equal_to, this_nentries = get_cov_matrices(this_df, args.detector_location)
               cov.append(this_cov)
               equal_to.append(this_equal_to)
               nentries.append(this_nentries)

       if not os.path.exists(os.path.split(args.output_filename)[0]):
           os.makedirs(os.path.split(args.output_filename)[0])

       with open(args.output_filename, "wb") as f:
           import pickle as pkl
           pkl.dump({"cov":cov, "b":equal_to, "nentries":nentries, "pos_binning": global_binning_pos, "neg_binning": global_binning_neg, "detector_location":args.detector_location, "corrections":args.corrections}, f)
    print("__FINISHED__")

