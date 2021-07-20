DATE = "Mar10"
import os
import ROOT
base_directory = "/project/def-psavard/ladamek//sagittabias_matrices/Injection_" + DATE + "_{file_type}_inject_{inject}_method_{method}_region_{detector_location}_{end_string}_{syst_var}_round_{round}/OutputFiles/"
base_directory_Data_stat_err = {}
base_directory_Data_stat_err["ID"] = "/project/def-psavard/ladamek/sagittabias_matrices/Bootstraps_Mar17_{file_type}_inject_{inject}_method_{method}_region_{detector_location}_{end_string}_{syst_var}_round_0/OutputFiles/"
base_directory_Data_stat_err["ME"] = base_directory_Data_stat_err["ID"]
base_directory_Data_stat_err["CB"] = "/project/def-psavard/ladamek/sagittabias_matrices/Bootstrap_Apr7_{file_type}_inject_{inject}_method_{method}_region_{detector_location}_{end_string}_{syst_var}_round_0/OutputFiles/"
#nom_coarse_round
base_directory_MC_histograms = {}
base_directory_MC_histograms["ID"] = "/project/def-psavard/ladamek//sagittabias_matrices/Injection_" + DATE + "_{file_type}_inject_{inject}_method_{method}_region_{detector_location}_{end_string}_{syst_var}_coarse_round_{round}/OutputFiles/"
base_directory_MC_histograms["ME"] = "/project/def-psavard/ladamek//sagittabias_matrices/Injection_" + DATE + "_{file_type}_inject_{inject}_method_{method}_region_{detector_location}_{end_string}_{syst_var}_coarse_round_{round}/OutputFiles/"
base_directory_MC_histograms["CB"] = "/project/def-psavard/ladamek//sagittabias_matrices/Injection_" + DATE + "_{file_type}_inject_{inject}_method_{method}_region_{detector_location}_{end_string}_{syst_var}_coarse_round_{round}/OutputFiles/"

base_directory_MC_histograms_stat_err = {}
base_directory_MC_histograms_stat_err["ID"] = "/project/def-psavard/ladamek/sagittabias_matrices/Bootstrap_Apr7" + "_{file_type}_inject_{inject}_method_{method}_region_{detector_location}_{end_string}_{syst_var}_coarse_round_{round}/OutputFiles/"
base_directory_MC_histograms_stat_err["ME"] = base_directory_MC_histograms_stat_err["ID"]
base_directory_MC_histograms_stat_err["CB"] = base_directory_MC_histograms_stat_err["ME"]

#methods = ["delta_qm", "matrix"]
methods = ["matrix"]
generators = ["MCMadGraph", "MCSherpa", "MC"]
generator_round = 3
end_string = "loose_preselection_tight_select_after_correction"

import ROOT as r
from BiasCorrection import extract_binning_from_histogram
matrix_round = 5
delta_qm_round = 21
release = "v03_p3"
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

        basedir = os.path.join(release)
        if not os.path.exists(basedir): os.makedir(basedir)
        output_filename = os.path.join(basedir, "{}.root".format(descriptor))
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

            #write the statustical uncertainty histogram
            directory = base_directory_Data_stat_err[detector_location].format(file_type=data_ftype, inject="None", method=method, detector_location=detector_location, end_string="loose_preselection_tight_select_after_correction", syst_var = "nom")
            stat_hists = get_deltas_from_job(directory)
            stat_hists = [h[0] for h in stat_hists]
            from utils import get_stddev_histogram
            stat_hist = get_stddev_histogram(stat_hists)
            stat_hist.SetName("stddev_deltas_GeV_{}_{}".format(descriptor, detector_location))
            stat_hist.Write()


            #dump the histogram for each iteration
            last_hist_nom=None
            last_hist_sub=None
            for i in range(0, roun + 1):
                nom_dir = base_directory.format(file_type=data_ftype, inject="None", method=method, detector_location=detector_location, end_string="loose_preselection_tight_select_after_correction", syst_var = "nom", round = i)
                sub_dir = base_directory.format(file_type=mc_ftype, inject="None", method=method, detector_location=detector_location, end_string="loose_preselection_tight_select_after_correction", syst_var = "nom", round = i)

                nom_hist = get_deltas_from_job(nom_dir)[0]
                sub_hist = get_deltas_from_job(sub_dir)[0]

                nom_hist.SetName("deltas_GeV_DataUncorrected_{}_{}_round_{}".format(descriptor, detector_location, i))
                sub_hist.SetName("deltas_GeV_MCUncorrected_{}_{}_round_{}".format(descriptor, detector_location, i))

                if last_hist_nom is not None:
                    nom_hist.Add(last_hist_nom, -1.0)
                else:
                    last_hist_nom = nom_hist.Clone()

                if last_hist_sub is not None:
                    sub_hist.Add(last_hist_sub, -1.0)
                else:
                    last_hist_sub = sub_hist.Clone()

                nom_hist.Write()
                sub_hist.Write()

            for gen in generators:
               if detector_location == "CB": continue #these don't exist yet... making them!
               this_base_directory = base_directory_MC_histograms[detector_location].format(round=generator_round, \
               end_string=end_string, \
               syst_var="nom", \
               detector_location=detector_location,\
               file_type=gen,\
               inject="None",\
               method=method)
               histogram = get_deltas_from_job(this_base_directory)[0]
               histogram = histogram.ProjectionX(gen + detector_location)
               for i in range(1, histogram.GetNbinsX() + 1):
                   histogram.SetBinError(i, 0.0)

               if gen != "MC": 
                   this_stat_err_directory = base_directory_MC_histograms_stat_err[detector_location].format(round=0, \
                   end_string=end_string, \
                   syst_var="nom", \
                   detector_location=detector_location,\
                   file_type=gen,\
                   inject="None",\
                   method=method)

                   errors = [el[0] for el in get_deltas_from_job(this_stat_err_directory)]
                   errors = get_stddev_histogram(errors)

                   for i in range(1, histogram.GetNbinsX() + 1):
                       histogram.SetBinError(i, errors.GetBinContent(i))

               #write the histograms
               histogram.SetName("deltas_GeV_CoarseBinning_{}_{}".format(gen, descriptor))
               histogram.Write()




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

                    dir = base_directory.format(file_type=mc_ftype, inject="None", method=method, detector_location=detector_location, end_string="loose_preselection_tight_select_after_correction", syst_var = "nom", round = roun)
                    mc_hist = get_deltas_from_job(dir)[0]
                    hist.Add(mc_hist, -1.0)

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

