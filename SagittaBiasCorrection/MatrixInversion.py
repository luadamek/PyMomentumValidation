#first define the binning to be used for the sagitta bias correction

from binnings import Binning
import math
import numpy as np
import os

detector_location = "ID"

#these are the edges
eta_edges = np.linspace(-2.5, +2.5 , 27)
phi_edges = np.linspace(-1.0 * math.pi, +1.0 * math.pi, 25)

#create a phi binning:
phi_binning_pos = Binning("Pos_{}_Phi".format(detector_location), phi_edges, None, repr_override=None)
phi_binning_neg = Binning("Neg_{}_Phi".format(detector_location), phi_edges, None, repr_override=None)

pos_eta_subbins = []
neg_eta_subbins = []
for i in range(0, len(eta_edges) - 1):
    pos_eta_subbins.append(phi_binning_pos)
    neg_eta_subbins.append(phi_binning_neg)

#create a global binning scheme
global_binning_pos = Binning("Pos_{}_Eta".format(detector_location), eta_edges, pos_eta_subbins)
global_binning_pos.recursively_include_overflow(False)
global_binning_neg = Binning("Neg_{}_Eta".format(detector_location), eta_edges, neg_eta_subbins)
global_binning_neg.recursively_include_overflow(False)

#in order to do this, we a set of covarianve matrices, and their respective number of entries
covariance_matrices = []
equal_to_vectors = []

from utils import get_files

all_files = get_files("v03")
data_files = all_files["Data"]

from utils import get_entry_steps
import uproot as ur

def get_cov_matrices(root_file, start, stop, detector_location, global_binning_pos, global_binning_neg):
    #calculate what bin events belong in
    variables = ["Pos_{}_Eta", "Neg_{}_Eta", "Pos_{}_Phi", "Neg_{}_Phi", "Pos_{}_Pt", "Neg_{}_Pt", "Pair_{}_Mass"] #all of the variables needed
    selection = "abs(Pair_{}_Mass - 91.2) < 20.0".format(detector_location)
    variables = [v.format(detector_location) for v in variables]
    df = ur.open(root_file)["MuonMomentumCalibrationTree"].pandas.df(branches = variables, entrystart = start, entrystop = stop)
    df = df.query(selection) #apply the selection
    df["pos_bindex"] = global_binning_pos.get_global_bindex(df)
    df["neg_bindex"] = global_binning_neg.get_global_bindex(df)
    n_corr_bins = global_binning_pos.get_global_nbins()#number of bins in which to apply the correction
    e_vector = np.zeros((n_corr_bins, len(df)))

    #calculate the e vector
    e_vector[df["pos_bindex"].values, np.arange(0, len(df))] += df.eval("(Pair_{}_Mass ** 2) * Pos_{}_Pt".format(detector_location, detector_location)).values
    e_vector[df["neg_bindex"].values, np.arange(0, len(df))] -= df.eval("(Pair_{}_Mass ** 2) * Neg_{}_Pt".format(detector_location, detector_location)).values

    #calculate the covariance matrix
    cov = np.cov(e_vector)

    #equal_to = np.zeros((n_corr_bins))
    masses = df.eval("(Pair_{}_Mass ** 2)".format(detector_location)).values
    masses = masses.reshape(masses.shape[0],-1)
    mean_mass = np.average(masses, axis = 0)

    e_vector_trans = e_vector.transpose()
    mean_e_vector = np.average(e_vector_trans, axis=0)

    equal_to = (1.0/float(len(df))) * np.sum( (masses - mean_mass) * (e_vector_trans - mean_e_vector), axis=0)

    print(cov)
    print(equal_to)
    return cov, equal_to, len(df)


def get_deltas_from_job(outfile_location):
    import glob
    import os
    import pickle as pkl
    import ROOT

    matrices = glob.glob(os.path.join(outfile_location, "*.pkl"))
    print(matrices)

    opened = []
    for m in matrices:
        with open(m, "rb") as f:
            print("opening {}".format(m))
            opened.append(pkl.load(f))

    def merge_covariances(list_of_covs,key ):
        total = sum([el["nentries"] for el in list_of_covs])
        total_cov = sum([el["nentries"] * el[key] for el in list_of_covs])
        return total_cov/total

    def get_binning(binning):
         print(dir(binning))


    cov = merge_covariances(opened, "cov")
    b = merge_covariances(opened, "b")

    import numpy as np
    delta = np.linalg.solve(cov, b)

    print(delta)

    #ok now load everything into a histogram
    binning = opened[0]["pos_binning"]

    x_bins = binning.bin_edges
    y_bins = binning.subbins[0].bin_edges

    x_var = binning.variable.replace("Pos_", "").replace("Neg_", "")
    y_var = binning.subbins[0].variable.replace("Pos_", "").replace("Neg_", "")

    delta_hist = ROOT.TH2D("delta", "delta", len(x_bins)-1, min(x_bins), max(x_bins), len(y_bins)-1, min(y_bins), max(y_bins))

    def find_bindex(edges_of_bin, all_edges):
        bindex = 1
        found=False
        for bin_low, bin_high in zip(all_edges[:-1], all_edges[1:]):
            if bin_low == edges_of_bin[0] and bin_high == edges_of_bin[1]:
                return bindex
            bindex += 1
        assert False

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

    return delta_hist, {"xvar":x_var, "y_var":y_var}

#invert the matrix and solve the problem
#sagitta = np.linalg.solve(cov, equal_to_vector)
#print(sagitta)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Calculate the covariance matrices and vectors needed to compute the sagitta bias.')
    parser.add_argument('--filename', type=str, dest='filename')
    parser.add_argument('--start', type=int, dest='start')
    parser.add_argument('--stop', type=int, dest='stop')
    parser.add_argument('--detector_location', type=str, dest='detector_location')
    parser.add_argument('--output_filename', type=str, dest='output_filename')
    args = parser.parse_args()

    cov, equal_to, nentries = get_cov_matrices(args.filename, args.start, args.stop, args.detector_location, global_binning_pos, global_binning_neg)

    if not os.path.exists(os.path.split(args.output_filename)[0]):
        os.makedirs(os.path.split(args.output_filename)[0])

    with open(args.output_filename, "wb") as f:
        import pickle as pkl
        pkl.dump({"cov":cov, "b":equal_to, "nentries":nentries, "pos_binning": global_binning_pos, "neg_binning": global_binning_neg}, f)
    print("__FINISHED__")





