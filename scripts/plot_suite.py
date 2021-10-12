import argparse
from histogram_manager import HistogramManager
import atlasplots
import ROOT
from binnings import global_pt_binning, global_pt_binning_zipped
from utils import draw_text
from atlasplots import set_atlas_style, atlas_label
from MatrixInversion import get_deltas_from_job
import os
set_atlas_style()

#write argument parsing code
parser = argparse.ArgumentParser(description='Make a suite of plots for the muon momentum scale calibration')
parser.add_argument('--file_name', '-fn', dest="file_name", type=str, required=True, help='the name of the file to read from')
parser.add_argument('--output_location', '-ol', dest="output_location", type=str, required=True, help="The name of the output folder in which to store the plots")
parser.add_argument('--mc_channel', '-mch', dest="MC", type=str, default="MC")
#'/project/def-psavard/ladamek/momentumvalidationoutput/Mar1_nocalib/Output.root'
args = parser.parse_args()
output_location = args.output_location
hm = HistogramManager(args.file_name)
hm.channels = ["Data", args.MC]

def draw_2d_histogram(histogram, description = "", normalize = True, output_location=""):
    if normalize:
        extrema = [ abs(histogram.GetMaximum()), abs(histogram.GetMinimum())]
        histogram.SetMaximum(max(*extrema))
        histogram.SetMinimum(min(*[-1.0 * el for el in extrema]))
    canvas = ROOT.TCanvas("Canvas_" + histogram.GetName())
    histogram.Draw("COLZ")
    histogram.GetYaxis().SetTitleOffset(0.7*histogram.GetYaxis().GetTitleOffset())
    canvas.SetTopMargin(0.1)
    if description: atlas_label(0.15, 0.94, "Internal   {}".format(description))
    else: atlas_label(0.2, 0.94, "Internal")
    canvas.SetRightMargin(0.25)
    histogram.GetZaxis().SetTitleOffset(1.2 * histogram.GetZaxis().GetTitleOffset())
    canvas.SetBottomMargin(0.25)
    canvas.Draw()
    ROOT.gStyle.SetPalette(ROOT.kTemperatureMap)
    canvas.Print(os.path.join(output_location, canvas.GetName() + ".pdf"))

histogram_flavours = ["coarsest", "finer", "finest"]
detector_locations = ["ID", "CB", "ME"]
for histogram_flavour in histogram_flavours:
    for detector_location in detector_locations:

        Neg_histograms = ["{}_Neg_{}_AverageMassProfile_{}".format(histogram_flavour, detector_location, i) for i in range(0, 12)]
        Pos_histograms = ["{}_Pos_{}_AverageMassProfile_{}".format(histogram_flavour, detector_location, i) for i in range(0, 12)]
        for Pos_histogram, Neg_histogram, binlow, binhigh in zip(Pos_histograms,\
                                                                 Neg_histograms,\
                                                                 global_pt_binning[:-1],\
                                                                 global_pt_binning[1:]):
            description = r"{:.1f} < {} < {:.1f}".format(binlow, "P_{T}^{ID}", binhigh)
            h_pos = hm.get_histograms(Pos_histogram)
            h_neg = hm.get_histograms(Neg_histogram)
            draw_2d_histogram(h_pos["Data"], description, output_location = output_location)
            draw_2d_histogram(h_neg["Data"], description, output_location = output_location)
            bias_hist = calculate_sagitta_bias(h_pos["Data"], h_neg["Data"])
            draw_2d_histogram(bias_hist, description, output_location = output_location)

            draw_2d_histogram(h_pos[args.MC], description, output_location = output_location)
            draw_2d_histogram(h_neg[args.MC], description, output_location = output_location)
            bias_hist = calculate_sagitta_bias(h_pos[args.MC], h_neg[args.MC])
            draw_2d_histogram(bias_hist, description, output_location = output_location)

        histograms = ["{}_{}_Mass_Histogram_{}".format(histogram_flavour, detector_location, i) for i in ["Inclusive"]]
        for histogram_name in histograms:
            continue
            histograms = hm.get_histograms(histogram_name)
            #for key in histograms:
            #    print("location: {}, channel: {}, RME {:.4f}".format(detector_location ,key, histograms[key].GetRME()))
            #input()
            from plotting_utils import draw_data_vs_mc, draw_histograms
            draw_data_vs_mc(histograms,\
                                ratio_min = 0.9,\
                                ratio_max = 1.1,\
                                colours = {args.MC:ROOT.kGreen +2, "Data":ROOT.kBlack},\
                                legend_labels = {"Data":"Data", args.MC:"PP8 Z#rightarrow#mu#mu"},\
                                legend_coordinates = (0.6, 0.6, 0.9, 0.85),\
                                x_axis_label = "M_{#mu#mu}^{"+detector_location+"} [GeV]",\
                                y_axis_label="Events",\
                                logy=False,\
                                extra_descr="",\
                                to_return = False,\
                                ftype = ".pdf",\
                                plot_dir = output_location,\
                                datakey = "Data")

        for charge in ["Pos", "Neg"]:
            continue
            histograms = ["{}_{}_{}_Mass_Histogram_{}".format(histogram_flavour, charge, detector_location, i) for i in range(0, 12)]
            from plotting_utils import draw_data_vs_mc, draw_histograms
            for hname in histograms:
                histograms = hm.get_histograms(hname)
                draw_data_vs_mc(histograms,\
                                ratio_min = 0.9,\
                                ratio_max = 1.1,\
                                colours = {args.MC:ROOT.kGreen +2, "Data":ROOT.kBlack},\
                                legend_labels = {"Data":"Data", args.MC:"PP8 Z#rightarrow#mu#mu"},\
                                legend_coordinates = (0.6, 0.6, 0.9, 0.9),\
                                x_axis_label = "M_{#mu#mu} [GeV]",\
                                y_axis_label="Events",\
                                logy=False,\
                                extra_descr="",\
                                to_return = False,\
                                ftype = ".pdf",\
                                plot_dir = output_location,\
                                datakey = "Data")

        Neg_histograms = ["{}_Neg_{}_AverageMassProfile_{}".format(histogram_flavour, detector_location, i) for i in ["Inclusive"]]
        Pos_histograms = ["{}_Pos_{}_AverageMassProfile_{}".format(histogram_flavour, detector_location, i) for i in ["Inclusive"]]
        for Pos_histogram, Neg_histogram in zip(Pos_histograms, Neg_histograms):
            #if detector_location == "ME" and  "Inclusive" in Pos_histogram and "Inclusive" in Neg_histogram: continue
            continue
            h_pos = hm.get_histograms(Pos_histogram)
            h_neg = hm.get_histograms(Neg_histogram)
            draw_2d_histogram(h_pos["Data"], "    #sqrt{s} = 13 TeV, 139 fb^{-1}", output_location = output_location)
            draw_2d_histogram(h_neg["Data"], "    #sqrt{s} = 13 TeV, 139 fb^{-1}", output_location = output_location)
            bias_hist = calculate_sagitta_bias(h_pos["Data"], h_neg["Data"])
            draw_2d_histogram(bias_hist, "    #sqrt{s} = 13 TeV, 139 fb^{-1}", output_location = output_location)

            draw_2d_histogram(h_pos[args.MC], "    #sqrt{s} = 13 TeV, Simulation", output_location = output_location)
            draw_2d_histogram(h_neg[args.MC], "    #sqrt{s} = 13 TeV, Simulation", output_location = output_location)
            bias_hist = calculate_sagitta_bias(h_pos[args.MC], h_neg[args.MC])
            draw_2d_histogram(bias_hist, "    #sqrt{s} = 13 TeV, Simulation", output_location = output_location)

        from binnings import binnings
        this_binning = None
        for el in binnings:
            if el["name"] == histogram_flavour: this_binning = el
        assert this_binning is not None
        histogram_base = "{histsetname}_{charge}_{location}_AverageMassProfile_Phi_{count}"
        Neg_histogram_names = [histogram_base.format(charge = "Neg", histsetname = histogram_flavour, location = detector_location, count=i) for i in range(0, this_binning["Phi"]["nbins"])]
        Pos_histogram_names = [histogram_base.format(charge = "Pos", histsetname = histogram_flavour, location = detector_location, count=i) for i in range(0, this_binning["Phi"]["nbins"])]
        print(this_binning["Phi"])
        import numpy as np
        edges = np.linspace(this_binning["Phi"]["philow"], this_binning["Phi"]["phihigh"], this_binning["Phi"]["nbins"])
        for Pos_histogram_name, Neg_histogram_name, philow, phihi in zip(Pos_histogram_names, Neg_histogram_names, edges[:-1], edges[1:]):
            continue
            description = r"{:.2f} < {} < {:.2f}".format(philow, "#phi^{ID}", phihi)
            Pos_histograms = hm.get_histograms(Pos_histogram_name)
            Neg_histograms = hm.get_histograms(Neg_histogram_name)
            histograms = {}
            for key in Pos_histograms:
                histograms["Pos_{}".format(key)] = Pos_histograms[key]
                histograms["Neg_{}".format(key)] = Neg_histograms[key]
            colors = {"Pos_Data": ROOT.kRed, "Neg_Data": ROOT.kBlue, "Pos_MC":ROOT.kRed, "Neg_MC":ROOT.kBlue}
            styles = {"Pos_Data": 24, "Neg_Data": 24, "Pos_MC":26, "Neg_MC":26}
            legend_labels = {"Pos_Data": "Pos, Data", "Neg_Data": "Neg, Data", "Pos_MC": "Pos, PP8 Z#rightarrow#mu#mu" , "Neg_MC": "Neg, PP8 Z#rightarrow#mu#mu"}
            #draws_string = [{"location":, "text":description}]
            draw_histograms(histograms,  colours = colors, styles = styles, legend_labels = legend_labels, legend_coordinates = (0.3, 0.7, 0.7, 0.9), x_axis_label = "#eta_{#mu}", y_axis_label="<M_{#mu#mu}> [GeV]", logy=False, extra_descr="", to_return = False, ftype = ".pdf", plot_dir = output_location)


            histograms = {}
            key = "Data"
            histograms["Pos_{}".format(key)] = Pos_histograms[key]
            histograms["Neg_{}".format(key)] = Neg_histograms[key]
            colors = {"Pos_Data": ROOT.kRed, "Neg_Data": ROOT.kBlue}#, "Pos_MC":ROOT.kRed, "Neg_MC":ROOT.kBlue}
            styles = {"Pos_Data": 24, "Neg_Data": 24}#, "Pos_MC":26, "Neg_MC":26}
            #draws_string = [{"location":, "text":description}]
            legend_labels = {"Pos_Data": "Pos, Data", "Neg_Data": "Neg, Data"}#, "Pos_MC": "Pos, PP8 Z#rightarrow#mu#mu" , "Neg_MC": "Neg, PP8 Z#rightarrow#mu#mu"}
            draw_histograms(histograms,  colours = colors, styles = styles, legend_labels = legend_labels, legend_coordinates = (0.3, 0.7, 0.7, 0.9), x_axis_label = "#eta_{#mu}", y_axis_label="<M_{#mu#mu}> [GeV]", logy=False, extra_descr="", to_return = False, ftype = ".pdf", plot_dir = output_location)


