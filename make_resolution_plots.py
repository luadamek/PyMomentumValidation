import ROOT
#Apr2_v05_matrix
input_files = [\
#"/project/def-psavard/ladamek/momentumvalidationoutput/Apr2_v05_nocalib/Output.root",\
#"/project/def-psavard/ladamek/momentumvalidationoutput/Apr2_v05_matrix/Output.root",\
#Apr2_defaultcorr_v05_standardvars_nocalib
#"/project/def-psavard/ladamek/momentumvalidationoutput/Apr2_defaultcorr_v05_standardvars_nocalib/Output.root",\
("/project/def-psavard/ladamek/momentumvalidationoutput/May24_defaultcorr_simplecbcomb_latest_mc_v05_standardvars_matrix/Output.root", "SimpleComb"),\
("/project/def-psavard/ladamek/momentumvalidationoutput/May24_defaultcorr_covcbcomb_latest_mc_v05_standardvars_matrix/Output.root", "QOPComb"),\
("/project/def-psavard/ladamek/momentumvalidationoutput/May24_defaultcorr_fullcovcbcomb_latest_mc_v05_standardvars_matrix/Output.root", "Stacco"),\
("/project/def-psavard/ladamek/momentumvalidationoutput/May24_defaultcorr_covcbcombpercent_latest_mc_v05_standardvars_matrix/Output.root", "QOPCombPercentCorr"),\
("/project/def-psavard/ladamek/momentumvalidationoutput/May24_defaultcorr_nocbcomb_latest_mc_v05_standardvars_matrix/Output.root", "Default_SagittaCorr"),\
#("/project/def-psavard/ladamek/momentumvalidationoutput/May16_nocbcomb_latest_mc_v05_standardvars_matrix/Output.root", "Default"),\
("/project/def-psavard/ladamek/momentumvalidationoutput/May24_defaultcorr_bdtcbcomb_latest_mc_v05_standardvars_matrix/Output.root", "BDTComb"),\
]


from BiasCorrection import extract_binning_from_histogram
def convert_to_rms_profile_histogram(histogram_2d):
    axes = extract_binning_from_histogram(histogram_2d)
    from array import array
    hist = ROOT.TH1D(histogram_2d.GetName() + "RMS", histogram_2d.GetName() + "RMS", len(axes["x"]) -1, array("d", axes["x"]))
    hist.Sumw2()
    for i in range(1, hist.GetNbinsX() + 1):
        hist.SetBinContent(i, histogram_2d.ProjectionY(histogram_2d.GetName() + "projection_{}".format(i), i, i).GetRMS())
        hist.SetBinError(i, histogram_2d.ProjectionY(histogram_2d.GetName() + "projection_{}".format(i), i, i).GetRMSError())
    return hist


def convert_3d_to_rms_profile_histogram(histogram_3d):
    axes = extract_binning_from_histogram(histogram_3d)
    from array import array
    hist = ROOT.TH2D(histogram_3d.GetName() + "RMS", histogram_3d.GetName() + "RMS", len(axes["x"]) -1, array("d", axes["x"]), len(axes["y"]) -1, array("d", axes["y"]))
    hist.Sumw2()
    for i in range(1, hist.GetNbinsX() + 1):
        for j in range(1, hist.GetNbinsY() + 1):
            hist.SetBinContent(i, histogram_3d.ProjectionZ(histogram_3d.GetName() + "projection_{}_{}".format(i,j), i, i, j, j).GetRMS())
            hist.SetBinError(i, histogram_3d.ProjectionZ(histogram_3d.GetName() + "projection_{}_{}".format(i,j), i, i, j, j).GetRMSError())
            if "MC" in histogram_3d.GetName():
                for k in range(1, histogram_3d.GetNbinsZ()):
                    print(histogram_3d.GetBinContent(i, j, k))
                input()
    return hist

from histogram_manager import HistogramManager
import os
from plotting_utils import draw_histograms, draw_2d_histogram


histograms = {}

for input_file, combination in input_files:
     ROOT.gStyle.SetErrorX(1.0)
     hm = HistogramManager(input_file)
     output_file_location = input_file.split("/")[-2] + "output_files"
     output_folder = os.path.join(os.getenv("MomentumValidationDir"), "ResolutionPlots", input_file.split("/")[-2].split("_")[0], output_file_location)
     if not os.path.exists(output_folder): os.makedirs(output_folder)
     histograms[combination] = {}

     for detector_location in ["CB"]:#["ID", "ME", "CB"]:
          histogram_name = "MeanMassProfile_{}".format(detector_location)
          histograms[combination][detector_location] = {}
          for histogram_name in ["MeanMassProfile_{}".format(detector_location), "MassVsEta2D_{}".format(detector_location)]:
              if detector_location == "ID" and "2D" in histogram_name: histogram_name += "_{identified}"
              ROOT.gStyle.SetErrorX(1.0)
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

                  systematic_histograms = {}
                  if "MC{}_scale_up".format(period) in hists and "MC{}_scale_down".format(period) in hists:
                      if "MC{}".format(period) not in systematic_histograms: systematic_histograms["MC{}".format(period)] = {}
                      systematic_histograms["MC{}".format(period)]["scale"] = {"up": hists["MC{}_scale_up".format(period)], "down": hists["MC{}_scale_down".format(period)]}
                  if "MC{}_res_up".format(period) in hists and "MC{}_res_down".format(period) in hists:
                      if "MC{}".format(period) not in systematic_histograms: systematic_histograms["MC{}".format(period)] = {}
                      systematic_histograms["MC{}".format(period)]["res"] = {"up": hists["MC{}_res_up".format(period)], "down": hists["MC{}_res_down".format(period)]}

                  draw_histograms(these_hists,  colours = colors, styles = styles, legend_labels = legend_labels, legend_coordinates = (0.5, 0.7, 0.8, 0.9), logy=False, to_return = False, ftype = ".pdf", plot_dir = output_folder, x_axis_label = "#eta_{Lead}^{"+detector_location+"}", y_axis_label = y_axis_label,         extra_descr="#splitline:#sqrt{s} = 13 TeV, " + integrated_lumi + " fb^{-1}", savename="{}_{}_{}_{}".format(data_channel, mc_channel, histogram_name, detector_location), systematic_histograms=systematic_histograms)

          #start here for the second loop to make the RMS maps
          for histogram_name in ["3DEtaPtVsPtOverTruth_{detloc}_{charge}".format(detloc=detector_location, charge="{}"), "3DEtaPtVsPtOverTruth_{detloc}_{charge}_WIDER".format(detloc=detector_location, charge="{}")]:
              ROOT.gStyle.SetErrorX(1.0)
              hists_pos = hm.get_histograms(histogram_name.format("Pos"))
              hists_neg = hm.get_histograms(histogram_name.format("Neg"))

              hists = {}
              for key in hists_pos:
                  hists[key] = hists_pos[key]
                  hists[key].Add(hists_neg[key])

              hists = {key:convert_3d_to_rms_profile_histogram(hists[key]) for key in hists}

              for period in ["1516", "17", "18"]:
                  mc_channel = "MC{}".format(period)

                  if mc_channel == "MC":
                      integrated_lumi = "mc16ade"
                  elif mc_channel == "MC1516":
                      integrated_lumi = "mc16a"
                  elif mc_channel == "MC17":
                      integrated_lumi = "mc16d"
                  elif mc_channel == "MC18":
                      integrated_lumi = "mc16e"
                  legend_labels = {data_channel: data_channel, mc_channel: "PP8 Z#rightarrow#mu#mu"}#, mc_channel_sherpa: "Sherpa Z#rightarrow#mu#mu"}
                  styles = {data_channel: 24, mc_channel:26}
                  colors = {data_channel: ROOT.kBlack, mc_channel: ROOT.kBlue}
                  z_axis_label = "RMS(P_T^{Truth}/P_T^{Reco}) [GeV]"

                  draw_2d_histogram(hists[mc_channel], description = integrated_lumi + ", " + combination, normalize = True, output_location=output_folder, palette_override = None, ftype = "png", fix_axes = True)


allcolors = [ROOT.kBlack, ROOT.kGreen + 2, ROOT.kBlue, ROOT.kRed, ROOT.kMagenta, ROOT.kOrange, ROOT.kGray]
allstyles = [22, 24, 26, 28, 30, 32, 34]
output_file_location = "CombinationComparisons"
output_folder = os.path.join(os.getenv("MomentumValidationDir"), "ResolutionPlots", input_file.split("/")[-2].split("_")[0], output_file_location)
if not os.path.exists(output_folder): os.makedirs(output_folder)
for gen in ["Data", "MC"]:
    for period in ["1516", "17", "18"]:
        if period == "1516":
            integrated_lumi = "36.2"
        elif period == "17":
            integrated_lumi = "44.3"
        elif period == "18":
            integrated_lumi = "58.5"
        if gen == "Data": extra_descr = "#splitline:#sqrt{s} = 13 TeV, " + integrated_lumi + " fb^{-1}"
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

        #make the ratio plot w.r.t. the default
        divisor = "Default"
        new_histograms = {}
        for el in to_plot:
            if el == divisor: continue
            new_histograms[el] = to_plot[el].Clone(to_plot[el].GetName() + "Ratio")
            new_histograms[el].Divide(to_plot[divisor])

        draw_histograms(new_histograms,  colours = colors, styles = styles, legend_labels = legend_labels, legend_coordinates = (0.5, 0.7, 0.8, 0.9), logy=False, to_return = False, ftype = ".pdf", plot_dir = output_folder, x_axis_label = "#eta_{Lead}^{"+detector_location+"}", y_axis_label = "X/Default", extra_descr=extra_descr, savename="{}_{}_{}_{}".format(gen, period, "all_combinations_ratio", "CB"))


