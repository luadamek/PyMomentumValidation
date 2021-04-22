
from histogram_manager import HistogramManager
import atlasplots
import ROOT
from binnings import global_pt_binning, global_pt_binning_zipped
from plotting_utils import draw_2d_histogram, draw_histograms
from utils import draw_text
from atlasplots import set_atlas_style, atlas_label
from MatrixInversion import get_deltas_from_job
import os

from plotting_utils import draw_syst, get_systematically_varied_histograms

#Mar22_NoTrigThreshold
input_files = [\
#"/project/def-psavard/ladamek/momentumvalidationoutput/Apr2_v05_nocalib/Output.root",\
#"/project/def-psavard/ladamek/momentumvalidationoutput/Apr2_v05_matrix/Output.root",\
"/project/def-psavard/ladamek/momentumvalidationoutput/Apr2_defaultcorr_v05_standardvars_nocalib/Output.root",\
"/project/def-psavard/ladamek/momentumvalidationoutput/Apr2_defaultcorr_v05_standardvars_matrix/Output.root",\
]

#Mar7_nocalib_inject_${inject}_correct

output_locations = [os.path.join(os.getenv("PWD"), "PosNegRatio" + el.split("/")[-2]) for el in input_files]


histnames = \
[\
"PT_Leading_{location}_{identified}", "PT_Subleading_{location}_{identified}",\
"Eta_Leading_{location}_{identified}", "Eta_Subleading_{location}_{identified}",\
"Phi_Leading_{location}_{identified}", "Phi_Subleading_{location}_{identified}",\
"MassSpectrum_{location}_{identified}", "CosThetaStar_{location}_{identified}", \
]

#OK Study the agreement between data and mc
systematics =      {"Sagitta_Stat": {"Up": "_stat_up", "Down":"_stat_down"}, "Sagitta_ResBias" : {"Up" : "_resbias_up", "Down" : "_resbias_down"}}
systematic_names = {"Sagitta_Stat": {"Up": " stat up", "Down":" stat down"}, "Sagitta_ResBias" : {"Up" : " resbias up", "Down" : " resbias down"}}

CB_color_cycle = [r'#377eb8', r'#ff7f00',r'#dede00', r'#4daf4a',\
                  r'#f781bf', r'#a65628', r'#e41a1c', r'#984ea3']

extra_colours = [ROOT.TColor.GetColor(c) for c in CB_color_cycle]


mc_sherpa = None
mc_sherpa_corr = None
do_systematics = False
for input_file, output_location in zip(input_files, output_locations):
    set_atlas_style()
    hist_manager = HistogramManager(input_file)
    hist_manager.list_histograms("Mass")
    hist_manager.merge_channels("MC", ["MC1516", "MC17", "MC18"])
    hist_manager.merge_channels("MC_stat_up", ["MC1516_stat_up", "MC17_stat_up", "MC18_stat_up"])
    hist_manager.merge_channels("MC_stat_down", ["MC1516_stat_down", "MC17_stat_down", "MC18_stat_down"])
    hist_manager.merge_channels("MC_resbias_up", ["MC1516_resbias_up", "MC17_resbias_up", "MC18_resbias_up"])
    hist_manager.merge_channels("MC_resbias_down", ["MC1516_resbias_down", "MC17_resbias_down", "MC18_resbias_down"])
   # hist_manager.merge_channels("MCCalib", ["MC1516Calib", "MC17Calib", "MC18Calib"])
    hist_manager.merge_channels("Data", ["Data1516", "Data17", "Data18"])

    #for data, mc, mc_sherpa, mc_corr, mc_sherpa_corr, integrated_lumi in zip(["Data", "Data1516", "Data17", "Data18"], ["MC", "MC1516", "MC17", "MC18"], ["MCSherpa", "MCSherpa1516", "MCSherpa17", "MCSherpa18"], ["MCCalib", "MC1516Calib", "MC17Calib", "MC18Calib"], ["MCSherpaCalib", "MCSherpa1516Calib", "MCSherpa17Calib", "MCSherpa18Calib"], ["139", "36.2", "44.3", "58.5"]):
    for data, mc, integrated_lumi in zip(["Data", "Data1516", "Data17", "Data18"], ["MC", "MC1516", "MC17", "MC18"], ["139", "36.2", "44.3", "58.5"]):

       colors = {data: ROOT.kBlack, mc: ROOT.kBlue, mc_sherpa: ROOT.kGreen}
       styles = {data: 24, mc:26, mc_sherpa:28}
       legend_labels = {data: "Data", mc: "PP8 Z#rightarrow#mu#mu", mc_sherpa: "Sherpa Z#rightarrow#mu#mu"}
       colour_counter = 0
       for syst in systematics:
           for key in systematics[syst]:
               if not do_systematics: continue
               colors[mc + systematics[syst][key]] = extra_colours[colour_counter]
               legend_labels[mc  + systematics[syst][key]] = legend_labels[mc] + systematic_names[syst][key]
               styles[mc + systematics[syst][key]] = styles[mc] + colour_counter
               colour_counter += 1


       for histogram_name_base in histnames: #["MassSpectrum_{location}_{identified}", "CosThetaStar_{location}_{identified}"]:
           for location in ["ID", "ME", "CB"]:

               #make a plot of the ratio of the mass distribution for +'ve and ='ve tracks
               sets_of_histograms = {}
               for name in ["poslead", "neglead"]:
                  #make invariant mass histograms for ID tracks
                  hist_name = histogram_name_base.format(location=location, identified=name)
                  histograms = hist_manager.get_histograms(hist_name)
                  sets_of_histograms[name] = histograms
                  #to_plot = [data, mc, mc_sherpa]
                  to_plot = [data, mc]
                  for syst in systematics:
                      for key in systematics[syst]:
                          if not do_systematics: continue
                          to_plot.append(mc + systematics[syst][key])

                  new_histograms = {key:histograms[key] for key in to_plot}
                  rebin = None
                  if "CosTheta" in histogram_name_base:
                       x_axis_label = "cos#theta*_{"+location+"}"
                       x_range=(-0.9, 0.9)
                       mins_maxes=None
                  elif "Mass" in histogram_name_base:
                       x_axis_label = "M_{#mu#mu}^{"+location+"}[GeV]"
                       x_range=None
                       mins_maxes=None
                       rebin = 4
                  elif "PT" in histogram_name_base:
                       x_axis_label = None
                       if "Lead" in histogram_name_base: x_range = (30.0, 100.0)
                       else: x_range = (30.0, 70.0)
                       mins_maxes=None
                       rebin = 2
                  else:
                       x_axis_label = None
                       x_range=None
                       mins_maxes=None

                  if rebin != None:
                      for h in histograms:
                          histograms[h].Rebin(rebin)

                  draw_histograms(new_histograms,  colours = colors, styles = styles, legend_labels = legend_labels, legend_coordinates = (0.5, 0.7, 0.8, 0.9), logy=False, extra_descr="#splitline:#sqrt{s} = 13 TeV, " + integrated_lumi + " fb^{-1}", to_return = False, ftype = ".pdf", plot_dir = output_location, x_axis_label = x_axis_label, x_range=x_range, mins_maxes=mins_maxes)

               divided_histograms = {}
               pos_histograms = sets_of_histograms["poslead"]
               neg_histograms = sets_of_histograms["neglead"]
               for key in pos_histograms:
                   if key != data and key != mc and key != mc_sherpa and key not in to_plot: continue
                   divided_histograms[key] = pos_histograms[key].Clone("Pos_OVER_Neg" + hist_name + key  + data)
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
               draw_histograms(divided_histograms,  colours = colors, styles = styles, legend_labels = legend_labels, legend_coordinates = (0.5, 0.7, 0.8, 0.9), y_axis_label="N(+ leading)/N(- leading)", logy=False, extra_descr="#splitline:#sqrt{s} = 13 TeV, " + integrated_lumi + " fb^{-1}", to_return = False, ftype = ".pdf", plot_dir = output_location, x_axis_label = x_axis_label, x_range=x_range, mins_maxes=mins_maxes, savename = "Pos_OVER_Neg" + hist_name + data + mc)
               if not do_systematics: continue

               syst_hists = get_systematically_varied_histograms(divided_histograms, data, mc, mc + "_stat_up", mc + "_stat_down")

               syst_legend_labels = {}
               syst_legend_labels[mc+ "_total_up"] = "Syst + Stat"
               syst_legend_labels[mc+ "_sagitta_stat_up"] = "Sagitta Syst"
               syst_legend_labels[mc+ "_stat_up"] = "MC Stat"
               syst_legend_labels[data] = "Data"

               draw_syst(syst_hists,  colours = None, styles = None, legend_labels = syst_legend_labels, legend_coordinates = (0.65, 0.7, 0.9, 0.9), x_axis_label = x_axis_label, y_axis_label="Data - MC", logy=False, extra_descr="#splitline:#sqrt{s} = 13 TeV, " + integrated_lumi + " fb^{-1}", to_return = False, ftype = ".png", plot_dir = output_location, x_range = x_range, mins_maxes = None, savename="{}_{}_{}_{}_Systematics".format(data, mc, input_file.split("/")[-2], location) + hist_name, data_key = data)

mc_noinjection = "/project/def-psavard/ladamek/momentumvalidationoutput/Mar7_nocalib/Output.root"
basename = "/project/def-psavard/ladamek/momentumvalidationoutput/Mar7_nocalib_inject_{inject}_correct/Output.root"
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

       output_location = "/project/def-psavard/ladamek/pymomentumvalidation/Mar7_nocalib_inject_{inject}_correct_plots/".format(inject = injection)

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



