import argparse
from array import array
from histogram_manager import HistogramManager
import atlasplots
from BiasCorrection import calculate_sagitta_bias
import ROOT
from binnings import global_pt_binning, global_pt_binning_zipped
from plotting_utils import draw_text, draw_2d_histogram
from atlasplots import atlas_label
from BiasCorrection import extract_binning_from_histogram
import os

def get_extrema(directory):
    sagitta_hist, _, __ = get_deltas_from_job(directory)
    sagitta_hist.Scale(1000.0)
    extrema = (abs(sagitta_hist.GetMinimum()), abs(sagitta_hist.GetMaximum()))
    return extrema

def calculate_pt(pt, delta, q = 1.0):
    return pt / (1 + ( q * pt * delta ) )

def calculate_effect(target, meas = None, pt = 45.0, q = 1.0):
    pt_biased = calculate_pt(pt, -1.0 * target/1000.0, q = q)
    if meas is not None: pt_biased = calculate_pt(pt_biased, 1.0 * meas/1000.0, q = q)
    return abs(pt_biased - pt)/abs(pt) * 100.0

def calculate_difference(calib_one, calib_two, pt=45.0, q=1.0):
    pt_one = calculate_pt(pt, calib_one/1000.0, q=q)
    pt_two = calculate_pt(pt, calib_two/1000.0, q=q)
    return abs(pt_one - pt_two)/(pt) * 100.0

def get_effect_histogram(target, meas=None, scale=0.045, name=None, template = None, compare=False):
    ROOT.gStyle.SetPalette(ROOT.kInvertedDarkBodyRadiator)
    binning = extract_binning_from_histogram(target)
    #create a new histogram
    bins_array_x = array('d',binning["x"])
    bins_array_y = array('d',binning["y"])

    if not compare:
        description_string = "Percent_Effect"
    else:
        description_string = "Percent_Difference"

    if name is not None: newname = name
    elif meas is None: newname = target.GetName() + description_string
    else: newname = meas.GetName() + description_string

    if template is not None: new_hist = template.Clone(newname)
    else:
        new_hist = ROOT.TH2D(newname, newname, len(bins_array_x)-1, bins_array_x, len(bins_array_y)-1, bins_array_y)
        new_hist.GetXaxis().SetTitle("#eta")
        new_hist.GetYaxis().SetTitle("#phi")

    values = []
    for i in range(1, new_hist.GetNbinsX() + 1):
        for j in range(1, new_hist.GetNbinsY() + 1):
            if meas is not None: remaining_bias = target.GetBinContent(i,j) - meas.GetBinContent(i,j)
            else: remaining_bias = target.GetBinContent(i,j)
            meas_content = None
            if meas is not None:
                meas_content = meas.GetBinContent(i,j)
            if not compare: effect = calculate_effect(target.GetBinContent(i, j), meas = meas_content)
            else: effect = calculate_difference(target.GetBinContent(i, j), meas.GetBinContent(i, j))
            values.append(effect)
            new_hist.SetBinContent(i, j, effect)

    new_hist.GetZaxis().SetTitle(description_string.replace("_", " "))
    new_hist.SetMaximum(max(values))
    new_hist.SetMinimum(0.0)
    return new_hist


def get_sagitta_bias_histogram(directory, subtraction_directory = None, is_data = False):
    sagitta_hist, _, __ = get_deltas_from_job(directory)
    sagitta_hist = sagitta_hist.Clone()
    sagitta_hist.SetName(directory.split("/")[-2] + "_delta_hist")
    sagitta_hist.GetXaxis().SetTitle("#eta_{#mu}^{"+region+"}")
    sagitta_hist.GetYaxis().SetTitle("#phi_{#mu}^{"+region+"}")
    sagitta_hist.Scale(1000.0)
    sagitta_hist.GetZaxis().SetTitle("#delta^{"+region+"} [TeV^{-1}]")
    if not is_data: description = "    #sqrt{s} = 13 TeV "+mc_descr+""
    else: description = "    #sqrt{s} = 13 TeV, " + integrated_lumi + " fb^{-1}"

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
def get_solution_histogram(bias, region = None):
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

DATE = "Jan29"
#base_directory = "/scratch/ladamek/sagittabias_matrices/Injection_" + DATE + "_{file_type}_inject_{inject}_method_{method}_region_{detector_location}_{end_string}_{syst_var}_round_{round}/OutputFiles/"
base_directory = "/scratch/ladamek/sagittabias_matrices/Injection_" + DATE + "_{file_type}_inject_{inject}_method_{method}_region_{detector_location}_loose_preselection_tight_select_after_correction__fold_{syst_var}_round_{round}/OutputFiles/"

delta_qm_round = 21
matrix_round = 5
methods = ["delta_qm", "matrix"]

for region in ["ID", "ME"]:
    continue
    for end_string in ["loose_preselection_tight_select_after_correction"]:#"tight_preselection", "loose_preselection_tight_select_before_correction", "loose_preselection_tight_select_after_correction"]:
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
                       description = "    #sqrt{s} = 13 TeV "+mc_descr+""
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
                       description = "    #sqrt{s} = 13 TeV "+mc_descr+""
                       if extrema_corr < abs(sagitta_hist.GetMinimum()): extrema_corr = abs(sagitta_hist.GetMinimum())
                       if extrema_corr < abs(sagitta_hist.GetMaximum()): extrema_corr = abs(sagitta_hist.GetMaximum())
                       sagitta_hist.SetMinimum(-1.0 * extrema_corr)
                       sagitta_hist.SetMaximum(1.0 * extrema_corr)
                       if iteration == 2: draw_2d_histogram(sagitta_hist, description, normalize = False, output_location=output_location)
                       #####################################################

                        #make plots of the percent effect and remaining bias after the N iterations of both methods
                       if bias == "None": continue
                       solution = get_solution_histogram(bias, region = region)
                       solution.Scale(1000.0)
                       sagitta_hist.GetXaxis().SetTitle("#eta_{#mu}^{"+region+"}")
                       sagitta_hist.GetYaxis().SetTitle("#phi_{#mu}^{"+region+"}")
                       sagitta_hist.SetName(bias + "_Delta_" + region)
                       sagitta_hist_ratio = sagitta_hist.Clone(sagitta_hist.GetName() + "Ratio")
                       sagitta_hist_ratio.Divide(solution)

                       sagitta_hist_ratio.GetZaxis().SetTitle("#delta^{"+region+"}_{Corr}/#delta^{"+region+"}_{Injected}")
                       draw_2d_histogram(sagitta_hist_ratio, "    #sqrt{s}= 13 TeV "+mc_descr+"", normalize = False, output_location=output_location)

                       sagitta_hist_diff = sagitta_hist.Clone(sagitta_hist.GetName() + "Diff")
                       sagitta_hist_diff.Add(solution, -1.0)

                       sagitta_hist_diff.GetZaxis().SetTitle("#delta^{"+region+"}_{Corr} - #delta^{"+region+"}_{Injected} [TeV^{-1}]")
                       draw_2d_histogram(sagitta_hist_diff, "    #sqrt{s}= 13 TeV "+mc_descr+"", normalize = True, output_location=output_location)

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
                       effect_correction = get_effect_histogram(solution, sagitta_hist, name = name, template = sagitta_hist)
                       name = "{}_{}_{}".format("InjectionBias", bias, region)
                       effect_injection = get_effect_histogram(solution, name = name, template = sagitta_hist)

                       if extrema_effect < abs(effect_correction.GetMaximum()): extrema_effect = abs(effect_correction.GetMaximum())
                       effect_correction.SetMaximum(extrema_effect)
                       effect_correction.SetMinimum(0.0)
                       effect_correction.GetXaxis().SetTitle("#eta_{#mu}^{"+region+"}")
                       effect_correction.GetYaxis().SetTitle("#phi_{#mu}^{"+region+"}")
                       if iteration == 2: draw_2d_histogram(effect_correction, "    #sqrt{s}= 13 TeV "+mc_descr+"", normalize = False, output_location=output_location, palette_override = ROOT.kInvertedDarkBodyRadiator)

                       draw_2d_histogram(effect_injection, "    #sqrt{s}= 13 TeV "+mc_descr+"", normalize = False, output_location=output_location, palette_override = ROOT.kInvertedDarkBodyRadiator)

matrix_round = 7
delta_qm_round = 21
end_string = "loose_preselection_tight_select_after_correction"
dict_histograms = {}
for variation in ["one", "two"]:#"nom"]:#, "up", "down"]:
    dict_histograms[variation] = {}
    for data_filetype, mc_filetype in [("Data1516", "MC1516"), ("Data17", "MC17"), ("Data18", "MC18")]:
        dict_histograms[variation][data_filetype+"_"+mc_filetype]={}
        if data_filetype == "Data1516":
            integrated_lumi = "36.2"
        elif data_filetype == "Data17":
            integrated_lumi = "44.3"
        elif data_filetype == "Data18":
            integrated_lumi = "58.5"
        if mc_filetype == "MC1516":
            mc_descr = "mc16a"
        elif mc_filetype == "MC17":
            mc_descr = "mc16d"
        elif mc_filetype == "MC18":
            mc_descr = "mc16e"

        for region in ["ME", "ID"]:
            dict_histograms[variation][data_filetype+"_"+mc_filetype][region]={}
            extrema_uncorr = -10000000
            extrema_corr = -10000000
            extrema_effect = -10000000
            extrema_mc = -100000000
            for iteration in [1,2]:
                difference = None
                difference_uncorr = None
                difference_mc = None
                method_histograms_data = []
                method_histograms_mc = []
                method_histograms_data_corr = []
                corr_hists = []
                for method in methods:
                    if "matrix" == method:
                        from MatrixInversion import get_deltas_from_job
                        global get_deltas_from_job
                        roun = matrix_round

                    elif "delta_qm" == method:
                        from DeltaQMIterativeMethod import get_deltas_from_job
                        global get_deltas_from_job
                        roun = delta_qm_round

                    output_location = os.path.join(os.getenv("MomentumValidationDir"), "SolutionHistograms_Injection_{date}_method_{method}_region_{detector_location}_{end_string}_round_{round}_{syst_var}_{mc_filetype}_{data_filetype}".format(detector_location=region, end_string=end_string, round=roun, method=method, date=DATE, syst_var = variation, mc_filetype=mc_filetype, data_filetype=data_filetype))
                    if not os.path.exists(output_location): os.makedirs(output_location)

                    #####################################################
                    ## A plot of the sagitta bias estimates            ##
                    ##base_directory = "/scratch/ladamek/sagittabias_matrices/Injection_Jan29_{file_type}_inject_{inject}_method_{method}_region_{detector_location}_{end_string}_{syst_var}_round_{round}"
                    directory = base_directory.format(inject = "None", detector_location=region, round=roun, method=method, file_type=data_filetype, syst_var=variation, end_string = end_string)
                    sagitta_hist = get_sagitta_bias_histogram(directory, is_data = True)
                    description = "    #sqrt{s} = 13 TeV, "+ integrated_lumi + " fb^{-1}"
                    if extrema_uncorr < abs(sagitta_hist.GetMinimum()): extrema_uncorr = abs(sagitta_hist.GetMinimum())
                    if extrema_uncorr < abs(sagitta_hist.GetMaximum()): extrema_uncorr = abs(sagitta_hist.GetMaximum())
                    sagitta_hist.SetMinimum(-1.0 * extrema_uncorr)
                    sagitta_hist.SetMaximum(1.0 * extrema_uncorr)
                    method_histograms_data.append(sagitta_hist)
                    if iteration == 2: draw_2d_histogram(sagitta_hist, description, normalize = False, output_location=output_location)
                    #####################################################

                    if difference_uncorr is None:
                        difference_uncorr = sagitta_hist.Clone("DifferenceBetweenDeltaQMAndVarMin_UnCorr_{}".format(region))
                    else: difference_uncorr.Add(sagitta_hist, -1.0)

                    subtraction_dir = base_directory.format(inject = "None", detector_location=region, round=roun, method=method, file_type=mc_filetype, syst_var=variation, end_string = end_string)
                    sagitta_hist_sub = get_sagitta_bias_histogram(subtraction_dir,  is_data = True)
                    sagitta_hist_sub.SetName(sagitta_hist_sub.GetName() + "MCOnly")
                    description = "    #sqrt{s} = 13 TeV, " + mc_descr
                    if extrema_mc < abs(sagitta_hist_sub.GetMinimum()): extrema_mc = abs(sagitta_hist_sub.GetMinimum())
                    if extrema_mc < abs(sagitta_hist_sub.GetMaximum()): extrema_mc = abs(sagitta_hist_sub.GetMaximum())

                    sagitta_hist_sub.SetMinimum(-1.0 * extrema_mc)
                    sagitta_hist_sub.SetMaximum(1.0 * extrema_mc)
                    method_histograms_mc.append(sagitta_hist_sub)
                    if iteration == 2: draw_2d_histogram(sagitta_hist_sub, description, normalize = False, output_location=output_location)

                    if difference_mc is None:
                        difference_mc = sagitta_hist_sub.Clone("DifferenceBetweenDeltaQMAndVarMin_MC_{}".format(region))
                    else: difference_mc.Add(sagitta_hist_sub, -1.0)

                    sagitta_hist = get_sagitta_bias_histogram(directory, subtraction_dir, is_data = True)
                    description = "    #sqrt{s} = 13 TeV, " + integrated_lumi + " fb^{-1}"
                    if extrema_corr < abs(sagitta_hist.GetMinimum()): extrema_corr = abs(sagitta_hist.GetMinimum())
                    if extrema_corr < abs(sagitta_hist.GetMaximum()): extrema_corr = abs(sagitta_hist.GetMaximum())
                    sagitta_hist.SetMinimum(-1.0 * extrema_corr)
                    sagitta_hist.SetMaximum(1.0 * extrema_corr)
                    dict_histograms[variation][data_filetype+"_"+mc_filetype][region][method]=sagitta_hist
                    method_histograms_data_corr.append(sagitta_hist)
                    if iteration == 2: draw_2d_histogram(sagitta_hist, description, normalize = False, output_location=output_location)
                    #####################################################

                    if difference is None:
                        difference = sagitta_hist.Clone()
                        difference.SetName("DifferenceBetweenDeltaQMAndVarMin_Corr_{}".format(region))
                    else: difference.Add(sagitta_hist, -1.0)
                    corr_hists.append(sagitta_hist)

                extrema_difference = abs(difference.GetMinimum())
                extrema_difference = max(abs(difference.GetMaximum()), extrema_difference)
                difference.SetMinimum(-1.0 * extrema_difference)
                difference.SetMaximum(1.0 * extrema_difference)
                difference.GetZaxis().SetTitle("#delta_{Corr}^{DeltaQM} - #delta_{Corr}^{VarMin} [TeV^{-1}]")

                description = "    #sqrt{s} = 13 TeV, " + integrated_lumi + " fb^{-1}"
                difference.SetName(difference.GetName() + "Difference_{mc_filetype}_{data_filetype}".format(data_filetype=data_filetype, mc_filetype=mc_filetype))
                draw_2d_histogram(difference, description, normalize = False, output_location=os.getenv("MomentumValidationDir"))

                one_d_diff_hist = get_difference_histogram(corr_hists[0], corr_hists[1], difference.GetName()+"1DDiffHist")[0]
                one_d_diff_hist.GetXaxis().SetTitle(difference.GetZaxis().GetTitle())
                c = ROOT.TCanvas()
                c.SetBottomMargin(0.2)
                one_d_diff_hist.GetYaxis().SetTitle("Number of Estimates")
                one_d_diff_hist.Draw()
                c.Draw()
                c.Print(os.path.join(output_location, one_d_diff_hist.GetName() + ".png"))
                

                extrema_difference_uncorr = abs(difference_uncorr.GetMinimum())
                extrema_difference_uncorr = max(abs(difference_uncorr.GetMaximum()), extrema_difference_uncorr)
                difference_uncorr.SetMinimum(-1.0 * extrema_difference_uncorr)
                difference_uncorr.SetMaximum(1.0 * extrema_difference_uncorr)
                difference_uncorr.GetZaxis().SetTitle("#delta^{DeltaQM} - #delta^{VarMin} [TeV^{-1}]")

                description = "    #sqrt{s} = 13 TeV, " + integrated_lumi + " fb^{-1}"
                difference_uncorr.SetName(difference_uncorr.GetName()  + "Difference_{mc_filetype}_{data_filetype}".format(data_filetype=data_filetype, mc_filetype=mc_filetype))
                draw_2d_histogram(difference_uncorr, description, normalize = False, output_location=os.getenv("MomentumValidationDir"))

                extrema_difference_mc = abs(difference_mc.GetMinimum())
                extrema_difference_mc = max(abs(difference_mc.GetMaximum()), extrema_difference_mc)
                difference_mc.SetMinimum(-1.0 * extrema_difference_mc)
                difference_mc.SetMaximum(1.0 * extrema_difference_mc)
                difference_mc.SetName(difference_mc.GetName()  + "Difference_{mc_filetype}_{data_filetype}".format(data_filetype=data_filetype, mc_filetype=mc_filetype))
                difference_mc.GetZaxis().SetTitle("#delta^{DeltaQM} - #delta^{VarMin} [TeV^{-1}]")

                description = "    #sqrt{s} = 13 TeV "+mc_descr+""
                draw_2d_histogram(difference_mc, description, normalize = False, output_location=os.getenv("MomentumValidationDir"))

                #make a plot of the percent difference between both calibrations for a 45 GeV muon
                method_histograms_data = [m.Clone(m.GetName() + "PercentDifference_{mc_filetype}_{data_filetype}_{region}".format(data_filetype=data_filetype, mc_filetype=mc_filetype, region=region)) for m in method_histograms_data]
                method_histograms_mc = [m.Clone(m.GetName() + "PercentDifference_{mc_filetype}_{data_filetype}_{region}".format(data_filetype=data_filetype, mc_filetype=mc_filetype, region=region)) for m in method_histograms_mc]
                method_histograms_data_corr = [m.Clone(m.GetName() + "PercentDifference_{mc_filetype}_{data_filetype}_{region}".format(data_filetype=data_filetype, mc_filetype=mc_filetype, region=region)) for m in method_histograms_data_corr]

                diff_data       = get_effect_histogram(method_histograms_data[0], meas=method_histograms_data[1], compare = True, template=method_histograms_data[0])
                description = "    #sqrt{s} = 13 TeV, " + integrated_lumi + " fb^{-1}"
                draw_2d_histogram(diff_data, description, normalize = False, output_location=os.getenv("MomentumValidationDir"), palette_override = ROOT.kInvertedDarkBodyRadiator)
                diff_mc         = get_effect_histogram(method_histograms_mc[0], meas=method_histograms_mc[1], compare = True, template=method_histograms_data[0])
                description = "    #sqrt{s} = 13 TeV "+mc_descr+""
                draw_2d_histogram(diff_mc, description, normalize = False, output_location=os.getenv("MomentumValidationDir"), palette_override = ROOT.kInvertedDarkBodyRadiator)
                diff_data_corr  = get_effect_histogram(method_histograms_data_corr[0], meas=method_histograms_data_corr[1], compare = True, template=method_histograms_data[0])
                description = "    #sqrt{s} = 13 TeV, " + integrated_lumi + " fb^{-1}"
                draw_2d_histogram(diff_data_corr, description, normalize = False, output_location=os.getenv("MomentumValidationDir"), palette_override = ROOT.kInvertedDarkBodyRadiator)


up_differences = {}
down_differences = {}
for ftype in dict_histograms["nom"]:
    data_filetype=ftype.split("_")[0]
    if data_filetype == "Data1516":
        integrated_lumi = "36.2"
    elif data_filetype == "Data17":
        integrated_lumi = "44.3"
    elif data_filetype == "Data18":
        integrated_lumi = "58.5"
    for region in dict_histograms["nom"][ftype]:
        for method in dict_histograms["nom"][ftype][region]:
            name = "{}_{}_{}_{}".format("{}", ftype, region, method)
            up_hist = dict_histograms["up"][ftype][region][method].Clone(name.format("up"))
            down_hist = dict_histograms["down"][ftype][region][method].Clone(name.format("down"))
            nom_hist = dict_histograms["nom"][ftype][region][method]
            diff_up = get_effect_histogram(up_hist, meas=nom_hist, compare = True, template=up_hist)
            diff_down = get_effect_histogram(down_hist, meas=nom_hist, compare = True, template=down_hist)

            output_location = os.path.join(os.getenv("MomentumValidationDir"), "ComparisonHistograms_Injection_{date}_method_{method}_region_{detector_location}_{syst_var}_{filetype}".format(detector_location=region, method=method, date=DATE, syst_var = variation, filetype=ftype))
            if not os.path.exists(output_location): os.makedirs(output_location)

            description = "    #sqrt{s} = 13 TeV, " + integrated_lumi + " fb^{-1}"
            up_hist.Add(nom_hist, -1.0)
            up_hist.GetZaxis().SetTitle("#delta^{"+region+", Up}_{Corr} - #delta^{"+region+", Nom}_{Corr} [TeV^{-1}]")
            down_hist.Add(nom_hist, -1.0)
            down_hist.GetZaxis().SetTitle("#delta^{"+region+", Down}_{Corr} - #delta^{"+region+", Nom}_{Corr} [TeV^{-1}]")
            description = "    #sqrt{s} = 13 TeV, " + integrated_lumi + " fb^{-1}"
            draw_2d_histogram(up_hist, description, normalize = True, output_location=output_location)
            draw_2d_histogram(down_hist, description, normalize = True, output_location=output_location)



            diff_up.GetZaxis().SetTitle("Percent Difference")
            diff_up = diff_up.Clone(diff_up.GetName() + "PercentDiffUp")
            diff_down.GetZaxis().SetTitle("Percent Difference")
            diff_down = diff_down.Clone(diff_down.GetName() + "PercentDiffDown")

            draw_2d_histogram(diff_up, description, normalize = False, output_location=output_location, palette_override = ROOT.kInvertedDarkBodyRadiator)
            draw_2d_histogram(diff_down, description, normalize = False, output_location=output_location, palette_override = ROOT.kInvertedDarkBodyRadiator)

