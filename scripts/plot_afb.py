import ROOT
import os
from plotting_utils import get_systematically_varied_histograms

def calc_afb(nf, nb, nf_err, nb_err):
    afb = (nf - nb)/(nf + nb)

    def err_term(a, b):
        return (2.0 * b)/( ( a + b ) ** 2 )

    afb_err = ( (err_term(nf, nb) * nf_err)**2 + (err_term(nb, nf) ** nb_err)**2)**0.5

    return afb, afb_err


def get_afb_hist(hist_nf, hist_nb, descr):
    hist_return = hist_nf.Clone(hist_nf.GetName() + "_AFB_Symmetry" + descr)
    for i in range(1, hist_nf.GetNbinsX() + 1):
        nf = hist_nf.GetBinContent(i)
        nf_err = hist_nf.GetBinError(i)
        nb = hist_nb.GetBinContent(i)
        nb_err = hist_nb.GetBinError(i)
        afb, afb_err = calc_afb(nf, nb, nf_err, nb_err)
        hist_return.SetBinContent(i, afb)
        hist_return.SetBinError(i, afb_err)

    return hist_return

from plotting_utils import draw_syst

histogram_name = "MassSpectrum_{region}_{for_or_bwd}"
#Apr2_v05_matrix
input_files = [\
#"/project/def-psavard/ladamek/momentumvalidationoutput/Apr2_v05_nocalib/Output.root",\
#"/project/def-psavard/ladamek/momentumvalidationoutput/Apr2_v05_matrix/Output.root",\
#Apr2_defaultcorr_v05_standardvars_nocalib
#"/project/def-psavard/ladamek/momentumvalidationoutput/Apr2_defaultcorr_v05_standardvars_nocalib/Output.root",\
"/project/def-psavard/ladamek/momentumvalidationoutput/Apr2_defaultcorr_cbcomb_v05_standardvars_matrix/Output.root",\
]
output_location = "AfbPlots_Apr2_defaultcorr_cbcomb"

systematics =      {"Sagitta_Stat": {"Up": "_stat_up", "Down":"_stat_down"}, "Sagitta_ResBias" : {"Up" : "_resbias_up", "Down" : "_resbias_down"}}
systematic_names = {"Sagitta_Stat": {"Up": " stat up", "Down":" stat down"}, "Sagitta_ResBias" : {"Up" : " resbias up", "Down" : " resbias down"}} 

CB_color_cycle = [r'#377eb8', r'#ff7f00',r'#dede00', r'#4daf4a',\
                  r'#f781bf', r'#a65628', r'#e41a1c', r'#984ea3']

extra_colours = [ROOT.TColor.GetColor(c) for c in CB_color_cycle]
skip_syst = True

from plotting_utils import draw_histograms
for input_f in input_files:
    from histogram_manager import HistogramManager
    hm = HistogramManager(input_f, rebin=4)
    hm.merge_channels("MC", ["MC1516", "MC17", "MC18"])
    hm.merge_channels("MCSherpa", ["MCSherpa1516", "MCSherpa17", "MCSherpa18"])
    hm.merge_channels("Data", ["Data1516", "Data17", "Data18"])
    hm.merge_channels("MC_stat_up", ["MC1516_stat_up", "MC17_stat_up", "MC18_stat_up"])
    hm.merge_channels("MC_stat_down", ["MC1516_stat_down", "MC17_stat_down", "MC18_stat_down"])
    hm.merge_channels("MC_resbias_up", ["MC1516_resbias_up", "MC17_resbias_up", "MC18_resbias_up"])
    hm.merge_channels("MC_resbias_down", ["MC1516_resbias_down", "MC17_resbias_down", "MC18_resbias_down"])
    for mc_channel,\
        data_channel,\
        mc_channel_sherpa,\
        mc_stat_up,\
        mc_stat_down,\
        mc_resbias_up,\
        mc_resbias_down\
        in zip(\
        ["MC", "MC1516", "MC17", "MC18"], \
        ["Data", "Data1516", "Data17", "Data18"],\
        ["MCSherpa", "MCSherpa1516", "MCSherpa17", "MCSherpa18"], \
        ["MC_stat_up", "MC1516_stat_up", "MC17_stat_up", "MC18_stat_up"],\
        ["MC_stat_down", "MC1516_stat_down", "MC17_stat_down", "MC18_stat_down"],\
        ["MC_resbias_up", "MC1516_resbias_up", "MC17_resbias_up", "MC18_resbias_up"],\
        ["MC_resbias_down", "MC1516_resbias_down", "MC17_resbias_down", "MC18_resbias_down"]\
        ):
       for det_location in ["ID", "ME", "CB"]: #"CB"]: add cb tracks in the future
           if data_channel == "Data":
               integrated_lumi = "139"
           elif data_channel == "Data1516":
               integrated_lumi = "36.2"
           elif data_channel == "Data17":
               integrated_lumi = "44.3"
           elif data_channel == "Data18":
               integrated_lumi = "58.5"
           colour_counter = 0
           colors = {data_channel: ROOT.kBlack, mc_channel: ROOT.kBlue, mc_channel_sherpa: extra_colours[colour_counter]}
           styles = {data_channel: 24, mc_channel:26, mc_channel_sherpa:25}
           legend_labels = {data_channel: data_channel, mc_channel: "PP8 Z#rightarrow#mu#mu", mc_channel_sherpa: "Sherpa Z#rightarrow#mu#mu"}
           colour_counter += 1
           extra_channels = []
           for syst in systematics:
               for key in systematics[syst]:
                   colors[mc_channel + systematics[syst][key]] = extra_colours[colour_counter]
                   legend_labels[mc_channel  + systematics[syst][key]] = legend_labels[mc_channel] + systematic_names[syst][key]
                   styles[mc_channel + systematics[syst][key]] = styles[mc_channel] + colour_counter
                   extra_channels.append(mc_channel + systematics[syst][key])
                   colour_counter += 1
           if skip_syst: extra_channels = []
           x_axis_label = "M_{#mu#mu}^{"+det_location+"} [GeV]"
           fwd_hist = hm.get_histograms(histogram_name.format(region=det_location, for_or_bwd="forward"))
           bwd_hist = hm.get_histograms(histogram_name.format(region=det_location, for_or_bwd="backward"))
           afb_hist = {}
           for chan in ([mc_channel, data_channel, mc_channel_sherpa] + extra_channels):
               afb_hist[chan] = get_afb_hist(fwd_hist[chan], bwd_hist[chan], descr = input_f.split("/")[-2])
               afb_hist[chan].SetName("{}_{}_{}_{}".format(data_channel, mc_channel, input_f.split("/")[-2], det_location))
           draw_histograms(afb_hist,  colours = colors, styles = styles, legend_labels = legend_labels, legend_coordinates = (0.5, 0.7, 0.8, 0.9), logy=False, to_return = False, ftype = ".pdf", plot_dir = output_location, x_axis_label = x_axis_label, y_axis_label = "AFB",         extra_descr="#splitline:#sqrt{s} = 13 TeV, " + integrated_lumi + " fb^{-1}", savename="{}_{}_{}_{}".format(data_channel, mc_channel, input_f.split("/")[-2], det_location))
           if skip_syst: continue

           histograms = get_systematically_varied_histograms(afb_hist, data_channel, mc_channel, mc_stat_up, mc_stat_down)


           legend_labels = {}
           legend_labels[mc_channel + "_total_up"] = "Syst + Stat"
           legend_labels[mc_channel + "_sagitta_stat_up"] = "Sagitta Syst"
           legend_labels[mc_channel + "_stat_up"] = "MC Stat"

           draw_syst(histograms,  colours = None, styles = None, legend_labels = legend_labels, legend_coordinates = (0.65, 0.7, 0.9, 0.9), x_axis_label = x_axis_label, y_axis_label="Data - MC", logy=False, extra_descr="#splitline:#sqrt{s} = 13 TeV, " + integrated_lumi + " fb^{-1}", to_return = False, ftype = ".png", plot_dir = output_location, x_range = None, mins_maxes = None, savename="{}_{}_{}_{}_Systematics".format(data_channel, mc_channel, input_f.split("/")[-2], det_location), data_key = data_channel)




