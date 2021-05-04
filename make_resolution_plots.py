import ROOT
#Apr2_v05_matrix
input_files = [\
#"/project/def-psavard/ladamek/momentumvalidationoutput/Apr2_v05_nocalib/Output.root",\
#"/project/def-psavard/ladamek/momentumvalidationoutput/Apr2_v05_matrix/Output.root",\
#Apr2_defaultcorr_v05_standardvars_nocalib
#"/project/def-psavard/ladamek/momentumvalidationoutput/Apr2_defaultcorr_v05_standardvars_nocalib/Output.root",\
("/project/def-psavard/ladamek/momentumvalidationoutput/May2_defaultcorr_simplecbcomb_latest_mc_v05_standardvars_matrix/Output.root", "SimpleComb"),\
("/project/def-psavard/ladamek/momentumvalidationoutput/May2_defaultcorr_covcbcomb_latest_mc_v05_standardvars_matrix/Output.root", "CovComb"),\
("/project/def-psavard/ladamek/momentumvalidationoutput/May2_defaultcorr_nocbcomb_latest_mc_v05_standardvars_matrix/Output.root", "Default"),\
#("/project/def-psavard/ladamek/momentumvalidationoutput/May2_defaultcorr_bdtcbcomb_latest_mc_v05_standardvars_matrix/Output.root", "BDTComb"),\
]


from BiasCorrection import extract_binning_from_histogram
def convert_to_rms_profile_histogram(histogram_2d):
    axes = extract_binning_from_histogram(histogram_2d)
    from array import array
    hist = ROOT.TH1D(histogram_2d.GetName(), histogram_2d.GetName(), len(axes["x"]) -1, array("d", axes["x"]))
    hist.Sumw2()
    for i in range(1, hist.GetNbinsX() + 1):
        hist.SetBinContent(i, histogram_2d.ProjectionY(histogram_2d.GetName() + "projection_{}".format(i), i, i).GetRMS())
        hist.SetBinError(i, histogram_2d.ProjectionY(histogram_2d.GetName() + "projection_{}".format(i), i, i).GetRMSError())
    return hist

from histogram_manager import HistogramManager
import os
from plotting_utils import draw_histograms

histograms = {}

for input_file, combination in input_files:
     hm = HistogramManager(input_file)
     output_file_location = input_file.split("/")[-2] + "output_files"
     output_folder = os.path.join(os.getenv("MomentumValidationDir"), "ResolutionPlots", output_file_location)
     if not os.path.exists(output_folder): os.makedirs(output_folder)
     histograms[combination] = {}

     for detector_location in ["ID", "ME", "CB"]:
          histogram_name = "MeanMassProfile_{}".format(detector_location)
          histograms[combination][detector_location] = {}
          for histogram_name in ["MeanMassProfile_{}".format(detector_location), "MassVsEta2D_{}".format(detector_location)]:
              if detector_location == "ID" and "2D" in histogram_name: histogram_name += "_{identified}"
              hists = hm.get_histograms(histogram_name)

              if "2D" in histogram_name:
                  hists = {key:convert_to_rms_profile_histogram(hists[key]) for key in hists}

              histograms[combination][detector_location][histogram_name] = {}

              for period in ["1516", "17", "18"]:

                  these_hists = {}
                  data_channel = "Data{}".format(period)
                  mc_channel = "MC{}".format(period)
                  these_hists["MC{}".format(period)] = hists["MC{}".format(period)]
                  these_hists["Data{}".format(period)] = hists["Data{}".format(period)]
                  histograms[combination][detector_location][histogram_name][period] = these_hists

                  if data_channel == "Data":
                      integrated_lumi = "139"
                  elif data_channel == "Data1516":
                      integrated_lumi = "36.2"
                  elif data_channel == "Data17":
                      integrated_lumi = "44.3"
                  elif data_channel == "Data18":
                      integrated_lumi = "58.5"
                  legend_labels = {data_channel: data_channel, mc_channel: "PP8 Z#rightarrow#mu#mu"}#, mc_channel_sherpa: "Sherpa Z#rightarrow#mu#mu"}
                  styles = {data_channel: 24, mc_channel:26}
                  colors = {data_channel: ROOT.kBlack, mc_channel: ROOT.kBlue}
                  y_axis_label = "<M_{#mu#mu}> [GeV]"
                  if "2D" in histogram_name: y_axis_label = "RMS(M_{#mu#mu}) [GeV]"

                  draw_histograms(these_hists,  colours = colors, styles = styles, legend_labels = legend_labels, legend_coordinates = (0.5, 0.7, 0.8, 0.9), logy=False, to_return = False, ftype = ".pdf", plot_dir = output_folder, x_axis_label = "#eta_{Lead}^{"+detector_location+"}", y_axis_label = y_axis_label,         extra_descr="#splitline:#sqrt{s} = 13 TeV, " + integrated_lumi + " fb^{-1}", savename="{}_{}_{}_{}".format(data_channel, mc_channel, histogram_name, detector_location))

allcolors = [ROOT.kBlack, ROOT.kGreen, ROOT.kBlue, ROOT.kRed]
allstyles = [22, 24, 26, 28]
output_file_location = "CombinationComparisons"
output_folder = os.path.join(os.getenv("MomentumValidationDir"), "ResolutionPlots", output_file_location)
if not os.path.exists(output_folder): os.makedirs(output_folder)
for gen in ["Data", "MC"]:
    if gen == "Data": extra_descr = "#splitline:#sqrt{s} = 13 TeV, " + integrated_lumi + " fb^{-1}"
    for period in ["1516", "17", "18"]:
        if gen == "MC" and period == "1516": extra_descr = "#splitline:#sqrt{s} = 13 TeV, " + "mc16a"
        if gen == "MC" and period == "17": extra_descr = "#splitline:#sqrt{s} = 13 TeV, " + "mc16d"
        if gen == "MC" and period == "18": extra_descr = "#splitline:#sqrt{s} = 13 TeV, " + "mc16e"
        to_plot = {} 
        stypes = {}
        colors = {}
        legend_labels = {}
        for i, combination in enumerate(list(histograms.keys())):
            to_plot[combination] = histograms[combination]["CB"]["MassVsEta2D_{}".format("CB")][period]["{}{}".format(gen, period)]
            styles[combination] = allstyles[i]
            colors[combination] = allcolors[i]
            legend_labels[combination] = combination
        draw_histograms(to_plot,  colours = colors, styles = styles, legend_labels = legend_labels, legend_coordinates = (0.5, 0.7, 0.8, 0.9), logy=False, to_return = False, ftype = ".pdf", plot_dir = output_folder, x_axis_label = "#eta_{Lead}^{"+detector_location+"}", y_axis_label = y_axis_label,         extra_descr=extra_descr, savename="{}_{}_{}_{}".format(gen, period, "all_combinations", "CB"))

