import ROOT

def calc_afb(nf, nb, nf_err, nb_err):
    afb = (nf - nb)/(nf + nb)
    print(afb)

    def err_term(a, b):
        return (2.0 * b)/( ( a + b ) ** 2 )

    afb_err = afb * ( (err_term(nf, nb) * nf_err)**2 + (err_term(nb, nf) ** nb_err)**2)**0.5

    return afb, afb_err


def get_afb_hist(hist_nf, hist_nb):
    hist_return = hist_nf.Clone(hist_nf.GetName() + "_AFB_Symmetry")
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

input_files = [\
"/project/def-psavard/ladamek/momentumvalidationoutput/Mar12_v05_nocalib/Output.root",\
"/project/def-psavard/ladamek/momentumvalidationoutput/Mar12_v05_matrix/Output.root",\
]

from plotting_utils import draw_histograms
colors = {"Data": ROOT.kBlack, "MC": ROOT.kBlue}
styles = {"Data": 24, "MC":26}
legend_labels = {"Data": "Data", "MC": "PP8 Z#rightarrow#mu#mu"}
for input_f in input_files:
    from histogram_manager import HistogramManager
    hm = HistogramManager(input_f)
    hm.merge_channels("MC", ["MC1516", "MC17", "MC18"])
    output_location = "AfbPlots"
    for det_location in ["ID", "ME"]: #"CB"]: add cb tracks in the future
        x_axis_label = "M_{#mu#mu}^{"+det_location+"} [GeV]"
        fwd_hist = hm.get_histograms(histogram_name.format(region=det_location, for_or_bwd="forward"))
        bwd_hist = hm.get_histograms(histogram_name.format(region=det_location, for_or_bwd="backward"))
        afb_hist = {}
        for chan in ["Data", "MC"]:
            afb_hist[chan] = get_afb_hist(fwd_hist[chan], bwd_hist[chan])
        draw_histograms(afb_hist,  colours = colors, styles = styles, legend_labels = legend_labels, legend_coordinates = (0.45, 0.7, 0.8, 0.9), logy=False, extra_descr="", to_return = False, ftype = ".pdf", plot_dir = output_location, x_axis_label = x_axis_label, y_axis_label="(N(cos#theta > 0) - N(cos#theta < 0))/(N(cos#theta > 0) + N(cos#theta < 0))")





