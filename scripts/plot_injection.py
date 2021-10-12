import atlasplots
from atlasplots import set_atlas_style, atlas_label
set_atlas_style()

import argparse
from histogram_manager import HistogramManager
from BiasCorrection import calculate_sagitta_bias
import ROOT
from binnings import global_pt_binning, global_pt_binning_zipped
from MatrixInversion import get_deltas_from_job
import os
from BiasInjection import injection_histogram_local, injection_histogram_global, injection_histogram_globalpluslocal, solution_histogram, injection_histogram_data, injection_histogram_random
from plotting_utils import draw_text, draw_2d_histogram

detector_locations = ["ID", "ME"]
for detector_location in detector_locations:
    for function, name in zip([injection_histogram_random, injection_histogram_local, injection_histogram_global, injection_histogram_globalpluslocal, injection_histogram_data],\
            ["Random", "local", "global", "globalpluslocal"]):#, "data"]):
        histogram = function(detector_location)
        histogram = solution_histogram(histogram)
        histogram.SetName("Injection_{}_{}".format(name, detector_location))
        histogram.SetTitle("Injection_{}_{}".format(detector_location, name))
        histogram.GetXaxis().SetTitle("#eta_{#mu}")
        #histogram.GetXaxis().SetTitleOffset(0.7)
        #histogram.GetXaxis().SetTitleSize(25)
        histogram.GetYaxis().SetTitle("#phi_{#mu}")
        #histogram.GetYaxis().SetTitleOffset(0.7)
        #histogram.GetYaxis().SetTitleSize(25)
        histogram.GetZaxis().SetTitle("#delta_{Injected}^{"+detector_location+"}[TeV^{-1}]")
        #histogram.GetZaxis().SetTitleOffset(0.7)
        #histogram.GetZaxis().SetTitleSize(25)
        #0.03500000014901161
        #1.0
        #0.03500000014901161
        #0.0
        #histogram.GetXaxis().SetTitleOffset(1.0)
        histogram.GetXaxis().SetTitleSize(histogram.GetXaxis().GetTitleSize() * 1.3)
        histogram.GetYaxis().SetTitleOffset(histogram.GetYaxis().GetTitleOffset()*0.7)
        histogram.GetYaxis().SetTitleSize(histogram.GetYaxis().GetTitleSize() * 1.3)
        histogram.Scale(1000.0)
        output_location = os.path.join(os.getenv("MomentumValidationDir"), "InjectionHistograms")
        if not os.path.exists(output_location): os.makedirs(output_location)
        draw_2d_histogram(histogram, description = "     Injected Bias", output_location = output_location, normalize=True, fix_axes = False)

