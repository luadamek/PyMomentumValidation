
from histogram_manager import HistogramManager
import atlasplots
import ROOT
from binnings import global_pt_binning, global_pt_binning_zipped
from plotting_utils import draw_2d_histogram, draw_histograms
from utils import draw_text
from atlasplots import set_atlas_style, atlas_label
from MatrixInversion import get_deltas_from_job
import os


input_files = [\
"/project/def-psavard/ladamek/momentumvalidationoutput/Mar4_v03_v2_nocalib/Output.root",\
"/project/def-psavard/ladamek/momentumvalidationoutput/Mar4_v03_v2_deltaqm_calib_21/Output.root",\
"/project/def-psavard/ladamek/momentumvalidationoutput/Mar4_v03_v2_matrix_calib_7/Output.root"\
]

#Mar4_nocalib_inject_${inject}_correct

output_locations = [os.path.join(os.getenv("PWD"), "PosNegRatio" + el.split("/")[-2]) for el in input_files]


histnames = \
[\
"PT_Leading_{location}_{identified}", "PT_Subleading_{location}_{identified}",\
"Eta_Leading_{location}_{identified}", "Eta_Subleading_{location}_{identified}",\
"Phi_Leading_{location}_{identified}", "Phi_Subleading_{location}_{identified}",\
"MassSpectrum_{location}_{identified}", "CosThetaStar_{location}_{identified}", \
]


for input_file, output_location in zip(input_files, output_locations):
    set_atlas_style()
    hist_manager = HistogramManager(input_file)
    hist_manager.list_histograms("Mass")
    hist_manager.merge_channels("MC", ["MC1516", "MC17", "MC18"])
    hist_manager.merge_channels("Data", ["Data1516", "Data17", "Data18"])

    for data, mc, mc_sherpa, mc_corr, mc_sherpa_corr, integrated_lumi in zip(["Data", "Data1516", "Data17", "Data18"], ["MC", "MC1516", "MC17", "MC18"], ["MCSherpa", "MCSherpa1516", "MCSherpa17", "MCSherpa18"], ["MCCorr", "MC1516Corr", "MC17Corr", "MC18Corr"], ["MCSherpaCorr", "MCSherpa1516Corr", "MCSherpa17Corr", "MCSherpa18Corr"], ["139", "36.2", "44.3", "58.5"]):


       colors = {data: ROOT.kBlack, mc: ROOT.kBlue, mc_sherpa: ROOT.kGreen, mc_corr: ROOT.kMagenta, mc_sherpa_corr: ROOT.kViolet}
       styles = {data: 24, mc:26, mc_sherpa:28, mc_corr:29, mc_sherpa_corr:30}
       legend_labels = {data: "Data", mc: "PP8 Z#rightarrow#mu#mu", mc_sherpa: "Sherpa Z#rightarrow#mu#mu", mc_corr: "PP8 Calibrated", mc_sherpa_corr: "Sherpa Calibrated"}

       for histogram_name_base in histnames: #["MassSpectrum_{location}_{identified}", "CosThetaStar_{location}_{identified}"]:
           for location in ["ID", "ME"]:
               #make a plot of the ratio of the mass distribution for +'ve and ='ve tracks
               sets_of_histograms = {}
               for name in ["poslead", "neglead"]:
                  #make invariant mass histograms for ID tracks
                  hist_name = histogram_name_base.format(location=location, identified=name)
                  histograms = hist_manager.get_histograms(hist_name)
                  sets_of_histograms[name] = histograms
                  to_plot = [data, mc, mc_sherpa]
                  new_histograms = {key:histograms[key] for key in to_plot}
                  if "CosTheta" in histogram_name_base:
                       x_axis_label = "cos#theta*_{"+location+"}"
                       x_range=(-0.9, 0.9)
                       mins_maxes=None
                  elif "Mass" in histogram_name_base:
                       x_axis_label = "M_{#mu#mu}^{"+location+"}[GeV]"
                       x_range=None
                       mins_maxes=None
                  elif "PT" in histogram_name_base:
                       x_axis_label = None
                       if "Lead" in histogram_name_base: x_range = (30.0, 100.0)
                       else: x_range = (30.0, 70.0)
                       mins_maxes=None
                  else:
                       x_axis_label = None
                       x_range=None
                       mins_maxes=None

                  draw_histograms(new_histograms,  colours = colors, styles = styles, legend_labels = legend_labels, legend_coordinates = (0.5, 0.7, 0.8, 0.9), logy=False, extra_descr="#splitline:#sqrt{s} = 13 TeV, " + integrated_lumi + " fb^{-1}", to_return = False, ftype = ".pdf", plot_dir = output_location, x_axis_label = x_axis_label, x_range=x_range, mins_maxes=mins_maxes)

               divided_histograms = {}
               pos_histograms = sets_of_histograms["poslead"]
               neg_histograms = sets_of_histograms["neglead"]
               for key in pos_histograms:
                   if key != data and key != mc and key != mc_sherpa: continue
                   divided_histograms[key] = pos_histograms[key].Clone( pos_histograms[key].GetName() + "_OVER_" + neg_histograms[key].GetName() )
                   divided_histograms[key].Divide(neg_histograms[key])
                   divided_histograms[key].GetXaxis().SetTitle(pos_histograms[key].GetXaxis().GetTitle())

               #ok now draw the divided histograms
               if "CosTheta" in histogram_name_base:
                    x_axis_label = "cos#theta*_{"+location+"}"
                    x_range=(-0.9, 0.9)
                    mins_maxes=(0.5, 1.5)
               elif "Mass" in histogram_name_base:
                    x_axis_label = "M_{#mu#mu}^{"+location+"}[GeV]"
                    x_range=None
                    mins_maxes=None
               elif "PT" in histogram_name_base:
                    x_axis_label = None
                    if "Lead" in histogram_name_base:
                        x_range = (30.0, 100.0)
                    else: x_range = (30.0, 70.0)
                    mins_maxes=None
               else:
                    x_axis_label = None
                    x_range=None
                    mins_maxes=None
               draw_histograms(divided_histograms,  colours = colors, styles = styles, legend_labels = legend_labels, legend_coordinates = (0.5, 0.7, 0.8, 0.9), y_axis_label="N(+ leading)/N(- leading)", logy=False, extra_descr="#splitline:#sqrt{s} = 13 TeV, " + integrated_lumi + " fb^{-1}", to_return = False, ftype = ".pdf", plot_dir = output_location, x_axis_label = x_axis_label, x_range=x_range, mins_maxes=mins_maxes)

mc_noinjection = "/project/def-psavard/ladamek/momentumvalidationoutput/Mar4_nocalib/Output.root"
basename = "/project/def-psavard/ladamek/momentumvalidationoutput/Mar4_nocalib_inject_{inject}_correct/Output.root"
compare_against = ["Local", "GlobalPlusLocal", "Global", "Random"]
for injection in compare_against:

       colors = {"RAW": ROOT.kBlack, "INJECTED": ROOT.kBlue}
       styles = {"RAW": 24, "INJECTED": 26}
       legend_labels = {"RAW": "PP8 Z#rightarrow#mu#mu", "INJECTED": "PP8 Z#rightarrow#mu#mu, {} injection".format(injection)}

       injected_file = basename.format(inject = injection)
       raw_file = mc_noinjection

       set_atlas_style()
       hist_manager_injected = HistogramManager(injected_file)
       hist_manager_raw = HistogramManager(raw_file)

       output_location = "/project/def-psavard/ladamek/pymomentumvalidation/Mar4_nocalib_inject_{inject}_correct_plots/".format(inject = injection)

       for histogram_name_base in ["MassSpectrum_{location}_{identified}", "CosThetaStar_{location}_{identified}"]:

           for location in ["ID", "ME"]:
               if "CosTheta" in histogram_name_base:
                   x_axis_label = "cos#theta*_{"+location+"}"
                   x_range=(-0.9, 0.9)
                   mins_maxes=None
               else:
                   x_axis_label = "M_{#mu#mu}^{"+location+"}[GeV]"
                   x_range=None
                   mins_maxes=None
               ratio_hists = None
               #make a plot of the ratio of the mass distribution for +'ve and ='ve tracks
               sets_of_histograms = {}
               for name in ["poslead", "neglead"]:
                    #make invariant mass histograms for ID tracks
                    hist_name = histogram_name_base.format(location=location, identified=name)
                    histogram_injected = hist_manager_injected.get_histograms(hist_name)["MC"]
                    histogram_raw = hist_manager_raw.get_histograms(hist_name)["MC"]

                    histograms = {}
                    histograms["RAW"] = histogram_raw
                    histograms["INJECTED"] = histogram_injected
                    draw_histograms(histograms,  colours = colors, styles = styles, legend_labels = legend_labels, legend_coordinates = (0.45, 0.7, 0.8, 0.9), logy=False, extra_descr="", to_return = False, ftype = ".pdf", plot_dir = output_location, x_axis_label = x_axis_label, x_range=x_range, mins_maxes=mins_maxes)

                    if ratio_hists is None:
                        ratio_hists = histograms
                        for key in ratio_hists:
                             ratio_hists[key].SetName(ratio_hists[key].GetName() + "_OVER_" + name)
                    else: {key:ratio_hists[key].Divide(histograms[key]) for key in histograms}

               draw_histograms(ratio_hists,  colours = colors, styles = styles, legend_labels = legend_labels, legend_coordinates = (0.45, 0.7, 0.8, 0.9), logy=False, extra_descr="", to_return = False, ftype = ".pdf", plot_dir = output_location, x_axis_label = x_axis_label, x_range=x_range, mins_maxes=mins_maxes, y_axis_label="N(+ leading)/N(- leading)")

