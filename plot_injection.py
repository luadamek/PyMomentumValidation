import argparse
from histogram_manager import HistogramManager
import atlasplots
from BiasCorrection import calculate_sagitta_bias
import ROOT
from binnings import global_pt_binning, global_pt_binning_zipped
from atlasplots import set_atlas_style, atlas_label
from MatrixInversion import get_deltas_from_job
import os
from BiasInjection import injection_histogram_local, injection_histogram_global, injection_histogram_globalpluslocal, solution_histogram, injection_histogram_data
from plotting_utils import draw_text, draw_2d_histogram

set_atlas_style()
detector_locations = ["ID", "MS"]
for detector_location in detector_locations:
    for function, name in zip([injection_histogram_local, injection_histogram_global, injection_histogram_globalpluslocal, injection_histogram_data],\
                        ["local", "global", "globalpluslocal", "data"]):
        histogram = function(detector_location)
        histogram = solution_histogram(histogram)
        histogram.SetName("Injection_{}_{}".format(name, detector_location))
        histogram.SetTitle("Injection_{}_{}".format(detector_location, name))
        histogram.GetXaxis().SetTitle("#eta_{#mu}")
        histogram.GetYaxis().SetTitle("#phi_{#mu}")
        histogram.GetZaxis().SetTitle("#delta_{Injected}^{"+detector_location+"}[TeV^{-1}]")
        histogram.Scale(1000.0)
        output_location = os.path.join(os.getenv("MomentumValidationDir"), "InjectionHistograms")
        if not os.path.exists(output_location): os.makedirs(output_location)
        draw_2d_histogram(histogram, description = "     Injected Bias", output_location = output_location, normalize=True)

