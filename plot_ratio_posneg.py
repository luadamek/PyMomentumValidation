
from histogram_manager import HistogramManager
import atlasplots
from BiasCorrection import calculate_sagitta_bias
import ROOT
from binnings import global_pt_binning, global_pt_binning_zipped
from plotting_utils import draw_2d_histogram, draw_histograms
from utils import draw_text
from atlasplots import set_atlas_style, atlas_label
from MatrixInversion import get_deltas_from_job
import os


input_files = ["/project/def-psavard/ladamek/momentumvalidationoutput/Dec3_nocalib/Output.root", "/project/def-psavard/ladamek/momentumvalidationoutput/Dec12_calib/Output.root"]
output_locations = [os.path.join(os.getenv("PWD"), "PosNegOutputFiles_Dec3"), os.path.join(os.getenv("PWD"), "PosNegOutputFilesCalib_Dec12")]

colors = {"Data": ROOT.kBlack, "MC": ROOT.kBlue}
styles = {"Data": 24, "MC": 24}
legend_labels = {"Data": "Data", "MC": "PP8 Z#rightarrow#mu#mu"}

for input_file, output_location in zip(input_files, output_locations):

    set_atlas_style()

    hist_manager = HistogramManager(input_file)
    hist_manager.list_histograms("Mass")

    for histogram_name_base in ["MassSpectrum_{location}_{identified}", "CosThetaStar_{location}_{identified}"]:
        for location in ["ID", "MS"]:
            #make a plot of the ratio of the mass distribution for +'ve and ='ve tracks
            sets_of_histograms = {}
            for name in ["poslead", "neglead"]:
               #make invariant mass histograms for ID tracks
               hist_name = histogram_name_base.format(location=location, identified=name)
               histograms = hist_manager.get_histograms(hist_name)
               sets_of_histograms[name] = histograms
               to_plot = ["Data", "MC"]
               new_histograms = {}
               for key in histograms:
                    if key not in to_plot: continue
                    new_histograms[key] = histograms[key]
               if "CosTheta" in histogram_name_base:
                   x_axis_label = "cos#theta*_{"+location+"}"
                   x_range=(-0.9, 0.9)
                   mins_maxes=None
               else:
                   x_axis_label = "M_{#mu#mu}^{"+location+"}[GeV]"
                   x_range=None
                   mins_maxes=None

               draw_histograms(new_histograms,  colours = colors, styles = styles, legend_labels = legend_labels, legend_coordinates = (0.5, 0.7, 0.8, 0.9), logy=False, extra_descr="", to_return = False, ftype = ".pdf", plot_dir = output_location, x_axis_label = x_axis_label, x_range=x_range, mins_maxes=mins_maxes)

            divided_histograms = {}
            pos_histograms = sets_of_histograms["poslead"]
            neg_histograms = sets_of_histograms["neglead"]
            for key in pos_histograms:
                if key != "Data" and key != "MC": continue
                divided_histograms[key] = pos_histograms[key].Clone( pos_histograms[key].GetName() + "_OVER_" + neg_histograms[key].GetName() )
                divided_histograms[key].Divide(neg_histograms[key])
                divided_histograms[key].GetXaxis().SetTitle(pos_histograms[key].GetXaxis().GetTitle())



            #ok now draw the divided histograms
            #draw_data_vs_mc(divided_histograms, ratio_min = 0.9, ratio_max = 1.1, colours = colors, legend_labels = legend_labels, legend_coordinates = (0.6, 0.9, 0.5, 0.9), x_axis_label = "M_{#mu#mu} [GeV]", y_axis_label="N(+)/N(-)", logy=False, extra_descr="", to_return = False, ftype = ".pdf", plot_dir = output_location, datakey = "Data", extra_str = None)
            if "CosTheta" in histogram_name_base:
                 x_axis_label = "cos#theta*_{"+location+"}"
                 x_range=(-0.9, 0.9)
                 mins_maxes=(0.5, 1.5)
            else:
                 x_axis_label = "M_{#mu#mu}^{"+location+"}[GeV]"
                 x_range=None
                 mins_maxes=None
            draw_histograms(divided_histograms,  colours = colors, styles = styles, legend_labels = legend_labels, legend_coordinates = (0.5, 0.7, 0.8, 0.9), y_axis_label="N(+ leading)/N(- leading)", logy=False, extra_descr="", to_return = False, ftype = ".pdf", plot_dir = output_location, x_axis_label = x_axis_label, x_range=x_range, mins_maxes=mins_maxes)
