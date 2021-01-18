import argparse
from histogram_manager import HistogramManager
import atlasplots
from BiasCorrection import calculate_sagitta_bias
import ROOT
from binnings import global_pt_binning, global_pt_binning_zipped
from plotting_utils import draw_text, draw_2d_histogram
from atlasplots import set_atlas_style, atlas_label
import os
set_atlas_style()

def get_extrema(directory):
    sagitta_hist, _, __ = get_deltas_from_job(directory)
    sagitta_hist.Scale(1000.0)
    extrema = (abs(sagitta_hist.GetMinimum()), abs(sagitta_hist.GetMaximum()))
    return extrema

def get_effect_histogram(target, meas=None, scale=0.045, name=None):
    global histogram_scales
    import ROOT
    ROOT.gStyle.SetPalette(ROOT.kInvertedDarkBodyRadiator)
    from BiasCorrection import extract_binning_from_histogram
    binning = extract_binning_from_histogram(target)
    #create a new histogram
    from array import array
    bins_array_x = array('d',binning["x"])
    bins_array_y = array('d',binning["y"])
    if name is not None: newname = name
    elif meas is None: newname = target.GetName() + "PercentEffect"
    else: newname = meas.GetName() + "PercentEffect"
    new_hist = ROOT.TH2D(newname, newname, len(bins_array_x)-1, bins_array_x, len(bins_array_y)-1, bins_array_y)
    values = []
    for i in range(1, new_hist.GetNbinsX() + 1):
        for j in range(1, new_hist.GetNbinsY() + 1):
            if meas is not None: remaining_bias = target.GetBinContent(i,j) - meas.GetBinContent(i,j)
            else: remaining_bias = target.GetBinContent(i,j)
            print(remaining_bias, target.GetBinContent(i,j))
            new_hist.SetBinContent(i, j, 100.0 * abs((scale * remaining_bias)/(1 + (scale * remaining_bias))))
            values.append(100.0 * abs((scale * remaining_bias)/(1 + (scale * remaining_bias))))
    new_hist.GetXaxis().SetTitle("#eta")
    new_hist.GetYaxis().SetTitle("#phi")
    new_hist.GetZaxis().SetTitle("Percent Effect")
    new_hist.SetMaximum(max(values))
    new_hist.SetMinimum(0.0)
    return new_hist

def get_sagitta_bias_histogram(directory, subtraction_directory = None, is_data = False):
    sagitta_hist, _, __ = get_deltas_from_job(directory)
    sagitta_hist.SetName(directory.split("/")[-2] + "_delta_hist")
    sagitta_hist.GetXaxis().SetTitle("#eta_{#mu}^{"+region+"}")
    sagitta_hist.GetYaxis().SetTitle("#phi_{#mu}^{"+region+"}")
    sagitta_hist.Scale(1000.0)
    sagitta_hist.GetZaxis().SetTitle("#delta^{"+region+"} [TeV^{-1}]")
    if not is_data: description = "    #sqrt{s} = 13 TeV, Simulation"
    else: description = "    #sqrt{s} = 13 TeV, 139 fb^{-1}"

    if subtraction_directory is None: return sagitta_hist

    sagitta_hist_subtraction, _, __ = get_deltas_from_job(subtraction_dir)
    sagitta_hist_subtraction.Scale(1000.0)
    sagitta_hist = sagitta_hist.Clone(sagitta_hist.GetName() + "Corr")
    sagitta_hist.Add(sagitta_hist_subtraction, -1.0)
    sagitta_hist.SetName(directory.split("/")[-2] + "_delta_hist_corr")
    sagitta_hist.GetZaxis().SetTitle("#delta^{"+region+"}_{Corr} [TeV^{-1}]")
    return sagitta_hist

from MatrixInversion import get_histogram_function
from BiasInjection import solution_histogram
def get_solution_histogram(bias):
    histogram_function = get_histogram_function(bias)
    histogram = histogram_function(detector_location = region)
    histogram = solution_histogram(histogram)
    return histogram

def get_difference_histogram(meas, injected, name, low_hi = None):
    import ROOT
    import numpy as np
    values = []
    for i in range(1, meas.GetNbinsX() +1):
        for j in range(1, meas.GetNbinsY() + 1):
            values.append(meas.GetBinContent(i, j) - injected.GetBinContent(i, j))
    values = np.array(values)
    import root_numpy as rnp
    if low_hi is None: histogram = ROOT.TH1D(name, name, 20, min(values), max(values))
    else: histogram = ROOT.TH1D(name, name, 20, low_hi[0], low_hi[1])
    rnp.fill_hist(histogram, values)
    return histogram, np.mean(values), np.std(values)

sagitta_histograms = {}
base_directories = {}
base_directories["delta_qm"] = "/scratch/ladamek/sagittabias_matrices/Injection_Dec17_inject_{inject}_method_{method}_region_{detector_location}_{end_string}_round_{round}/OutputFiles"
base_directories["matrix"] = "/scratch/ladamek/sagittabias_matrices/Injection_Dec17_inject_{inject}_region_{detector_location}_{end_string}_round_{round}/OutputFiles"
methods = ["delta_qm", "matrix"]
delta_qm_round = 11
matrix_round = 2

for region in ["ID", "ME"]:
    for end_string in ["tight_preselection", "loose_preselection_tight_select_before_correction", "loose_preselection_tight_select_after_correction"]:
            for bias in ["Random", "Global" , "Local", "None", "GlobalPlusLocal"]: #, "Data"]:#, "Null"]:A
                extrema_uncorr = -10000000
                extrema_corr = -10000000
                extrema_effect = -10000000
                for iteration in [1,2]:
                    for method in methods:
                        if "matrix" == method:
                            from MatrixInversion import get_deltas_from_job
                            global get_deltas_from_job
                            roun = matrix_round

                        elif "delta_qm" == method:
                            from DeltaQMIterativeMethod import get_deltas_from_job
                            global get_deltas_from_job
                            roun = delta_qm_round
                        base_directory = base_directories[method]

                        output_location = os.path.join(os.getenv("MomentumValidationDir"), "SolutionHistograms_Injection_Dec17_method_{method}_region_{detector_location}_{end_string}_round_{round}".format(detector_location=region, end_string=end_string, round=roun, method=method))
                        if not os.path.exists(output_location): os.makedirs(output_location)

                        #####################################################
                        ## A plot of the sagitta bias estimates            ##
                        directory = base_directory.format(detector_location=region, inject=bias, end_string=end_string, round=roun, method=method)
                        sagitta_hist = get_sagitta_bias_histogram(directory, is_data = False)
                        description = "    #sqrt{s} = 13 TeV, Simulation"
                        if extrema_uncorr < abs(sagitta_hist.GetMinimum()): extrema_uncorr = abs(sagitta_hist.GetMinimum())
                        if extrema_uncorr < abs(sagitta_hist.GetMaximum()): extrema_uncorr = abs(sagitta_hist.GetMaximum())
                        sagitta_hist.SetMinimum(-1.0 * extrema_uncorr)
                        sagitta_hist.SetMaximum(1.0 * extrema_uncorr)
                        if iteration == 2: draw_2d_histogram(sagitta_hist, description, normalize = False, output_location=output_location)
                        #####################################################

                        #####################################################
                        ## A plot of the correction sagitta bias estimates ##
                        directory = base_directory.format(detector_location=region, inject=bias, end_string=end_string, round=roun, method=method)
                        subtraction_dir = base_directory.format(detector_location=region, inject="None", end_string=end_string, round=roun, method=method)
                        sagitta_hist = get_sagitta_bias_histogram(directory, subtraction_dir, is_data = False)
                        description = "    #sqrt{s} = 13 TeV, Simulation"
                        if extrema_corr < abs(sagitta_hist.GetMinimum()): extrema_corr = abs(sagitta_hist.GetMinimum())
                        if extrema_corr < abs(sagitta_hist.GetMaximum()): extrema_corr = abs(sagitta_hist.GetMaximum())
                        sagitta_hist.SetMinimum(-1.0 * extrema_corr)
                        sagitta_hist.SetMaximum(1.0 * extrema_corr)
                        if iteration == 2: draw_2d_histogram(sagitta_hist, description, normalize = False, output_location=output_location)
                        #####################################################

                         #make plots of the percent effect and remaining bias after the N iterations of both methods
                        if bias == "None": continue
                        solution = get_solution_histogram(bias)
                        solution.Scale(1000.0)
                        sagitta_hist.GetXaxis().SetTitle("#eta_{#mu}^{"+region+"}")
                        sagitta_hist.GetYaxis().SetTitle("#phi_{#mu}^{"+region+"}")
                        sagitta_hist.SetName(bias + "_Delta_" + region)
                        sagitta_hist_ratio = sagitta_hist.Clone(sagitta_hist.GetName() + "Ratio")
                        sagitta_hist_ratio.Divide(solution)

                        sagitta_hist_ratio.GetZaxis().SetTitle("#delta^{"+region+"}_{Corr}/#delta^{"+region+"}_{Injected}")
                        draw_2d_histogram(sagitta_hist_ratio, "    #sqrt{s}= 13 TeV, Simulation", normalize = False, output_location=output_location)

                        sagitta_hist_diff = sagitta_hist.Clone(sagitta_hist.GetName() + "Diff")
                        sagitta_hist_diff.Add(solution, -1.0)

                        sagitta_hist_diff.GetZaxis().SetTitle("#delta^{"+region+"}_{Corr} - #delta^{"+region+"}_{Injected} [TeV^{-1}]")
                        draw_2d_histogram(sagitta_hist_diff, "    #sqrt{s}= 13 TeV, Simulation", normalize = True, output_location=output_location)

                        #make a histogram showing the distribution of differences between the injected and corrected
                        histogram, mean, std = get_difference_histogram(sagitta_hist, solution, bias + "Difference", low_hi = None)
                        histogram.GetXaxis().SetTitle("#delta^{"+region+"} - #delta^{"+region+"}_{Injected} [TeV^{-1}]")
                        histogram.GetYaxis().SetTitle("Number of Estimates")
                        canvas = ROOT.TCanvas(histogram.GetName() + "Canvas", histogram.GetName() + "Canvas")
                        histogram.Draw("HIST")
                        canvas.SetBottomMargin(0.25)
                        ptext = ROOT.TPaveText(.15,.5,.5,.95)
                        ptext.AddText("Mean: {}".format(mean))
                        ptext.AddText("Std. Dev: {}".format(std))
                        ptext.Draw()
                        canvas.Print(os.path.join(output_location,"Difference_{}_{}_{}.png".format(histogram.GetName(), region, bias)))

                        name = "{}_{}_{}".format("RemainingBias", bias, region)
                        effect_correction = get_effect_histogram(solution, sagitta_hist, name = name)
                        name = "{}_{}_{}".format("InjectionBias", bias, region)
                        effect_injection = get_effect_histogram(solution, name = name)

                        if extrema_effect < abs(effect_correction.GetMaximum()): extrema_effect = abs(effect_correction.GetMaximum())
                        effect_correction.SetMaximum(extrema_effect)
                        effect_correction.SetMinimum(0.0)

                        if iteration == 2: draw_2d_histogram(effect_correction, "    #sqrt{s}= 13 TeV, Simulation", normalize = False, output_location=output_location, palette_override = ROOT.kInvertedDarkBodyRadiator)
                        draw_2d_histogram(effect_injection, "    #sqrt{s}= 13 TeV, Simulation", normalize = False, output_location=output_location, palette_override = ROOT.kInvertedDarkBodyRadiator)
