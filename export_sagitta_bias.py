DATE = "Mar10"
import os
import ROOT
base_directory = "/project/def-psavard/ladamek//sagittabias_matrices/Injection_" + DATE + "_{file_type}_inject_{inject}_method_{method}_region_{detector_location}_{end_string}_{syst_var}_round_{round}/OutputFiles/"
#methods = ["delta_qm", "matrix"]
methods = ["matrix"]

import ROOT as r
from BiasCorrection import extract_binning_from_histogram
matrix_round = 5
delta_qm_round = 21
release = "v03_p2"
for mc_ftype, data_ftype in zip(["MC1516", "MC17", "MC18"], ["Data1516", "Data17", "Data18"]):
    for method in methods:
        if "matrix" == method:
            from MatrixInversion import get_deltas_from_job
            global get_deltas_from_job
            roun = matrix_round
            descriptor = "varmin_{}".format(data_ftype)

        elif "delta_qm" == method:
            from DeltaQMIterativeMethod import get_deltas_from_job
            global get_deltas_from_job
            roun = delta_qm_round
            descriptor = "delta_qm_{}".format(data_ftype)

        output_filename = "{}.root".format(descriptor)
        f = r.TFile(output_filename, "RECREATE")

        for detector_location in ["ID", "ME", "CB"]:
            nom_dir = base_directory.format(file_type=data_ftype, inject="None", method=method, detector_location=detector_location, end_string="loose_preselection_tight_select_after_correction", syst_var = "nom", round = roun)
            sub_dir = base_directory.format(file_type=mc_ftype, inject="None", method=method, detector_location=detector_location, end_string="loose_preselection_tight_select_after_correction", syst_var = "nom", round = roun)

            nom_dir = nom_dir.format(detector_location = detector_location, round = roun)
            sub_dir = sub_dir.format(detector_location = detector_location, round = roun)

            nom_hist = get_deltas_from_job(nom_dir)[0]
            sub_hist = get_deltas_from_job(sub_dir)[0]

            nom_hist.SetName("deltas_GeV_WARNING_UNCORRECTED_WARNING_{}_{}".format(descriptor, detector_location))
            nom_hist.Write()

            nom_hist.Add(sub_hist, -1.0)
            nom_hist.SetName("deltas_GeV_{}_{}".format(descriptor, detector_location))

            nom_hist.Write()

        #export the biases in gaetano's format
        basedir = os.path.join(release, data_ftype)
        for detector_location in ["ID", "ME", "CB"]:
            lasthist = None
            for ftype in ["data", "mc_nocorr", "mc"]:
                if not os.path.exists(basedir): os.makedirs(basedir)
                if ftype == "data":
                    dir = base_directory.format(file_type=data_ftype, inject="None", method=method, detector_location=detector_location, end_string="loose_preselection_tight_select_after_correction", syst_var = "nom", round = roun)
                    fname = os.path.join(basedir, "{}_data.root".format(detector_location))
                    hist = get_deltas_from_job(dir)[0]

                if ftype == "mc_nocorr": 
                    dir = base_directory.format(file_type=mc_ftype, inject="None", method=method, detector_location=detector_location, end_string="loose_preselection_tight_select_after_correction", syst_var = "nom", round = roun)
                    fname = os.path.join(basedir, "{}_mc_NoCorr.root".format(detector_location))
                    hist = get_deltas_from_job(dir)[0]

                if ftype == "mc": 
                    fname = os.path.join(basedir, "{}_mc.root".format(detector_location))
                    hist = lasthist
                    for i in range(1, hist.GetNbinsX() + 1):
                        for j in range(1, hist.GetNbinsY() + 1):
                            hist.SetBinContent(i, j, 0.0)
                            hist.SetBinError(i, j, 0.0)

                hist.SetName("p{}_0_hist".format(detector_location))
                bins = extract_binning_from_histogram(hist)
                from array import array
                x_bins = bins["x"]
                y_bins = bins["y"]
                delta_hist = ROOT.TProfile2D("p{}_0".format(detector_location), "p{}_0".format(detector_location), len(x_bins) - 1, array('d',x_bins), len(y_bins) - 1, array('d',y_bins))
                for i in range(0, int(delta_hist.GetNumberOfBins())+3):
                    delta_hist.SetBinEntries(i, 1.0)

                for i in range(1, hist.GetNbinsX() + 1):
                    for j in range(1, hist.GetNbinsY() + 1):
                        delta_hist.SetBinContent(i, j, hist.GetBinContent(i, j))
                        print(delta_hist.GetBinContent(i, j))
                        assert delta_hist.GetBinContent(i, j) != 0 or ftype == "mc"
                rf = ROOT.TFile(fname, "RECREATE")
                delta_hist.Write()
                rf.Close()
                lasthist = hist.Clone()


        f.Close()

