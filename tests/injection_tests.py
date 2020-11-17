import uproot as ur
import utils
from binnings import Binning
from BiasInjection import injection_histogram_null, injection_histogram_global
from MatrixInversion import inject_bias, get_dataframe
import numpy as np
import math




import unittest
class PyMomentumTestSuite(unittest.TestCase):

     def __init__(self, *args):

        super().__init__(*args)
        detector_location = "ID"
        start = 0
        stop = 10000 #load 20,000 events

        variables = ["Pos_{}_Eta", "Neg_{}_Eta", "Pos_{}_Phi", "Neg_{}_Phi", "Pos_{}_Pt", "Neg_{}_Pt", "Pair_{}_Mass", "Pair_CB_Mass"] #all of the variables needed
        selection = "abs(Pair_{}_Mass - 91.2) < 20.0".format(detector_location)
        variables = [v.format(detector_location) for v in variables]
        variables = list(set(variables))

        eta_edges = np.linspace(-2.5, +2.5 , 10)
        phi_edges = np.linspace(-1.0 * math.pi, +1.0 * math.pi, 10)

        #create a phi binning:
        phi_binning_pos = Binning("Pos_{}_Phi".format(detector_location), phi_edges, None, repr_override=None)
        phi_binning_neg = Binning("Neg_{}_Phi".format(detector_location), phi_edges, None, repr_override=None)

        pos_eta_subbins = []
        neg_eta_subbins = []
        for i in range(0, len(eta_edges) - 1):
            pos_eta_subbins.append(phi_binning_pos)
            neg_eta_subbins.append(phi_binning_neg)

        #create a global binning scheme
        global_binning_pos = Binning("Pos_{}_Eta".format("ID"), eta_edges, pos_eta_subbins)
        global_binning_pos.recursively_include_overflow(False)
        global_binning_neg = Binning("Neg_{}_Eta".format("ID"), eta_edges, neg_eta_subbins)
        global_binning_neg.recursively_include_overflow(False)

        #inject a bias into the data

        filename = "/project/def-psavard/ladamek/ForLukas/muonptcalib_v03_combined/merged/Sig_Z_mc16d.root"
        df = get_dataframe(filename, start, stop, variables, selection)
        #cov, equal_to, nentries = get_cov_matrices(df, global_binning_pos, global_binning_neg, detector_location)

        self.df = df
        self.detector_location = detector_location

     def test_null_correction(self):
        #ok lets inject a null bias
        df = self.df
        original_masses = np.array(df["Pair_{}_Mass".format(self.detector_location)].values)
        df = inject_bias(df, self.detector_location, injection_histogram_null)
        new_masses = df["Pair_{}_Mass".format(self.detector_location)].values

        differences = np.sort(abs(original_masses-new_masses))
        diff_indices = np.argsort(abs(original_masses-new_masses))
        for el in differences[::-1][0:100]:
            print(el)
        print("new vs old masses, with null injection")
        print(original_masses[diff_indices][::-1], new_masses[diff_indices][::-1])
        print(df.iloc[diff_indices])
        self.assertTrue(np.allclose(original_masses, new_masses, atol = 0.2))

     def test_global_correction(self):
        #ok lets inject a null bias
        df = self.df
        original_masses = np.array(df["Pair_{}_Mass".format(self.detector_location)].values)
        df_new = inject_bias(df, self.detector_location, injection_histogram_global)
        new_masses = df_new["Pair_{}_Mass".format(self.detector_location)].values
        print("new vs old masses, with global injection")
        print(original_masses, new_masses)
        self.assertFalse(np.allclose(original_masses, new_masses))

if __name__ == "__main__":
    unittest.main()
