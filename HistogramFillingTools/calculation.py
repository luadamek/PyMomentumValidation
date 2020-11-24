from pyximport import install
import numpy as np
import os
cython_cache = os.path.join(os.getenv("MomentumValidationDir"), "cython_cache")
#if not os.path.exists(cython_cache): os.makedirs(cython_cache)
#install(setup_args={"include_dirs":np.get_include()},reload_support=True, build_dir=cython_cache)
#from utils_cython import get_weights_from_bins, get_weights_from_2dbins

class CalculationDataMC:
    def __init__(self, function, list_of_branches):
        self.function = function
        self.name = function.__name__
        self.needsDataFlag = True
        self.branches = list_of_branches

    def eval(self, data, dataFlag):
        return self.function(data, dataFlag)

class Calculation:
    def __init__(self, function, list_of_branches):
        self.function = function
        self.name = function.__name__
        self.needsDataFlag = False
        self.branches = list_of_branches

    def eval(self, data):
        return self.function(data)

def WeightsToNormalizeToHistogram(variable_in_histogram, histogram):
    '''normalize the weights to the histogram'''
    low_edges = []
    high_edges = []
    normalizations = []
    #get the low bin edges of the histograms
    for bin in range(1, histogram.GetNbinsX() + 1):
        low_edges.append(histogram.GetBinLowEdge(bin))
        high_edges.append(histogram.GetBinLowEdge(bin + 1))
        normalizations.append(histogram.GetBinContent(bin))

    low_edges = np.array(low_edges, np.float)
    high_edges = np.array(high_edges, np.float)
    hist_weights = np.array(normalizations, np.float)

    weights = get_weights_from_bins(variable_in_histogram, low_edges, high_edges, hist_weights)

    weights[variable_in_histogram > high_edges[-1]] = 0.0 #set the weights of those events not in the reweighting histogram to 0
    weights[variable_in_histogram < low_edges[0]] = 0.0 #set the weights of those events not in the reweighting histogram to 0

    return weights

def WeightsToNormalizeTo2DHistogram(xvariable_in_histogram, yvariable_in_histogram, histogram):
    '''normalize the weights to the histogram'''
    xlow_edges = []
    ylow_edges = []
    xhigh_edges = []
    yhigh_edges = []

    #get the bin edges along the x axis
    for bin in range(1, histogram.GetNbinsX() + 1):
        xlow_edges.append(histogram.GetXaxis().GetBinLowEdge(bin))
        xhigh_edges.append(histogram.GetXaxis().GetBinLowEdge(bin + 1))
    #get the bbin edges along the y axis
    for bin in range(1, histogram.GetNbinsY() + 1):
        ylow_edges.append(histogram.GetYaxis().GetBinLowEdge(bin))
        yhigh_edges.append(histogram.GetYaxis().GetBinLowEdge(bin + 1))
    #get the normalizations from the histogram
    normalizations = np.ones((len(xlow_edges), len(ylow_edges)))
    for xbin in range(1, histogram.GetNbinsX() + 1):
        for ybin in range(1, histogram.GetNbinsY() + 1):
            normalizations[xbin-1,ybin-1] = histogram.GetBinContent(xbin, ybin)

    xlow_edges = np.array(xlow_edges, np.float)
    xhigh_edges = np.array(xhigh_edges, np.float)
    ylow_edges = np.array(ylow_edges, np.float)
    yhigh_edges = np.array(yhigh_edges, np.float)

    weights = get_weights_from_2dbins(xvariable_in_histogram,yvariable_in_histogram, xlow_edges, xhigh_edges, ylow_edges, yhigh_edges, normalizations)

    weights[xvariable_in_histogram > xhigh_edges[-1]] = 0.0 #set the weights of those events not in the reweighting histogram to 0
    weights[xvariable_in_histogram < xlow_edges[0]] = 0.0 #set the weights of those events not in the reweighting histogram to 0
    weights[yvariable_in_histogram > yhigh_edges[-1]] = 0.0 #set the weights of those events not in the reweighting histogram to 0
    weights[yvariable_in_histogram < ylow_edges[0]] = 0.0 #set the weights of those events not in the reweighting histogram to 0

    return weights

class WeightCalculation:
    def __init__(self, function, list_of_branches):
        self.function = function
        self.name = function.__name__
        self.branches = list_of_branches
        self.reweightDictionary = {}

    def eval(self, data, channel):
        weights = self.function(data)
        if channel in self.reweightDictionary:
            for variables, histogram, selection in zip(self.reweightDictionary[channel]["variables"], self.reweightDictionary[channel]["histograms"], self.reweightDictionary[channel]["selections"]):
                if len(variables) == 1:
                   variable = variables[0]
                   print("Reweighting variable " + variable.name + " in channel " + channel)
                   total_selection = np.ones(len(data)) > 0.5

                   for s in selection:
                       total_selection &= s.eval(data)

                   extra_weight = WeightsToNormalizeToHistogram(variable.eval(data), histogram)
                   weights[total_selection] *= extra_weight[total_selection]

                elif len(variables) == 2:
                   xvariable = variables[0]
                   yvariable = variables[1]
                   print("Reweighting variable x " + xvariable.name + " and variable y " +  yvariable.name +" in channel " + channel)

                   total_selection = np.ones(len(data)) > 0.5
                   for s in selection:
                       total_selection &= s.eval(data)

                   extra_weight = WeightsToNormalizeTo2DHistogram(xvariable.eval(data), yvariable.eval(data), histogram)
                   weights[total_selection] *= extra_weight[total_selection]
                else:
                    raise ValueError("Too many variables!")
        return weights

    def add_reweight_histogram(self, channel, variables, histogram, selection=[]):
        assert len(variables) == 1 or len(variables) == 2
        histogram.SetDirectory(0)
        if channel not in self.reweightDictionary:
            self.reweightDictionary[channel] = {}
            self.reweightDictionary[channel]["variables"] = []
            self.reweightDictionary[channel]["histograms"] = []
            self.reweightDictionary[channel]["selections"] = []

            self.reweightDictionary[channel]["variables"].append(variables)
            self.reweightDictionary[channel]["histograms"].append(histogram)
            self.reweightDictionary[channel]["selections"].append(selection)
            ##make sure that we always read the variable that we need for the histogram reweighting
            for variable in variables:
               for branch_name in variable.branches:
                   if branch_name not in self.branches:
                       self.branches.append(branch_name)
               for s in selection:
                   for branch_name in s.branches:
                       if branch_name not in self.branches:
                           self.branches.append(branch_name)
        else:
            self.reweightDictionary[channel]["variables"].append(variables)
            self.reweightDictionary[channel]["histograms"].append(histogram)
            self.reweightDictionary[channel]["selections"].append(selection)
            ##make sure that we always read the variable that we need for the histogram reweighting
            for variable in variables:
               for branch_name in variable.branches:
                   if branch_name not in self.branches:
                       self.branches.append(branch_name)
            for s in selection:
                for branch_name in s.branches:
                    if branch_name not in self.branches:
                        self.branches.append(branch_name)
