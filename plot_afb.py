import ROOT

def calc_afb(nf, nb, nf_err, nb_err):
    afb = (nf - nb)/(nf + nb)
    print(afb)

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

histogram_name = "MassSpectrum_{region}_{for_or_bwd}"
#Apr2_v05_matrix
input_files = [\
"/project/def-psavard/ladamek/momentumvalidationoutput/Apr2_v05_nocalib/Output.root",\
"/project/def-psavard/ladamek/momentumvalidationoutput/Apr2_v05_matrix/Output.root",\
]

from plotting_utils import draw_histograms
for input_f in input_files:
    from histogram_manager import HistogramManager
    hm = HistogramManager(input_f)
    hm.merge_channels("MC", ["MC1516", "MC17", "MC18"])
    hm.merge_channels("Data", ["Data1516", "Data17", "Data18"])
    output_location = "AfbPlots"
    for mc_channel,\
        data_channel,\
        mc_stat_up,\
        mc_stat_down,\
        mc_resbias_up,\
        mc_resbias_down\
        in zip(\
        ["MC", "MC1516", "MC17", "MC18"], \
        ["Data", "Data1516", "Data17", "Data18"],\
        ["MC_stat_up", "MC1516_stat_up", "MC17_stat_up", "MC18_stat_up"],\
        ["MC_stat_down", "MC1516_stat_down", "MC17_stat_down", "MC18_stat_down"]):
        ["MC_resbias_up", "MC1516_resbias_up", "MC17_resbias_up", "MC18_resbias_up"],\
        ["MC_resbias_down", "MC1516_resbias_down", "MC17_resbias_down", "MC18_resbias_down"]):
       for det_location in ["CB", "ID", "ME"]: #"CB"]: add cb tracks in the future
           if data_channel == "Data":
               integrated_lumi = "139"
           elif data_channel == "Data1516":
               integrated_lumi = "36.2"
           elif data_channel == "Data17":
               integrated_lumi = "44.3"
           elif data_channel == "Data18":
               integrated_lumi = "58.5"
           colors = {data_channel: ROOT.kBlack, mc_channel: ROOT.kBlue}
           styles = {data_channel: 24, mc_channel:26}
           legend_labels = {data_channel: data_channel, mc_channel: "PP8 Z#rightarrow#mu#mu"}
           x_axis_label = "M_{#mu#mu}^{"+det_location+"} [GeV]"
           fwd_hist = hm.get_histograms(histogram_name.format(region=det_location, for_or_bwd="forward"))
           bwd_hist = hm.get_histograms(histogram_name.format(region=det_location, for_or_bwd="backward"))
           afb_hist = {}
           for chan in [mc_channel, data_channel]:
               afb_hist[chan] = get_afb_hist(fwd_hist[chan], bwd_hist[chan], descr = input_f.split("/")[-2])
           draw_histograms(afb_hist,  colours = colors, styles = styles, legend_labels = legend_labels, legend_coordinates = (0.5, 0.7, 0.8, 0.9), logy=False, to_return = False, ftype = ".pdf", plot_dir = output_location, x_axis_label = x_axis_label, y_axis_label = "AFB",         extra_descr="#splitline:#sqrt{s} = 13 TeV, " + integrated_lumi + " fb^{-1}")



