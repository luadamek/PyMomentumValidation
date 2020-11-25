from math import pi
import scipy
import scipy.stats
import numpy as np
import ROOT

def scale_to(to_scale, scale=0.3):
    val_max = abs(to_scale.flat[abs(to_scale).argmax()])
    to_scale = scale/(val_max * 1000.0) * to_scale
    return to_scale

def get_injection_values_local(eta_edges, phi_edges, detector_location = "ID"):
    values = np.ones((len(eta_edges)-1, len(phi_edges)-1))
    step_x = (max(eta_edges) - min(eta_edges))/float(len(eta_edges)-1)
    step_y = (max(phi_edges) - min(phi_edges))/float(len(phi_edges)-1)

    for bindex_x in range(0, len(eta_edges)-1):
        for bindex_y in range(0, len(phi_edges)-1):
            x_value = min(eta_edges) + step_x * bindex_x
            y_value = min(phi_edges) + step_y * bindex_y

            x_scaled = x_value/max(eta_edges)
            y_scaled = y_value/max(eta_edges)

            first_gaussian = scipy.stats.norm(0.5, 0.4).pdf(np.sqrt((x_scaled-0.5) ** 2 + y_scaled ** 2))
            if x_scaled > 0.0: second_gaussian = x_scaled * scipy.stats.norm(-0.2, 1.2).pdf(np.sqrt(x_scaled ** 2 + y_scaled ** 2))
            else: second_gaussian = 0.0
            third_gaussian = -1.0 * scipy.stats.norm(-0.5, 0.35).pdf(x_scaled*(y_scaled-0.4) + np.sqrt(abs(x_scaled - 0.5))*np.sqrt(abs(y_scaled)))

            values[bindex_x, bindex_y] = first_gaussian + second_gaussian + third_gaussian

    values = scale_to(values)
    return values

def injection_histogram_data(detector_location = "ID"):
    bias = "None"
    directory = "/project/def-psavard/ladamek/sagitta_bias_matrices/Injection_Nov13_ID_Data_Inject_{}/OutputFiles".format(bias)
    subtraction_dir = "/project/def-psavard/ladamek/sagitta_bias_matrices/Injection_Nov13_ID_MC_Inject_{}/OutputFiles".format("None")
    from MatrixInversion import get_deltas_from_job
    sagitta_hist, _, __ = get_deltas_from_job(directory)
    sagitta_hist_subtraction, _, __ = get_deltas_from_job(subtraction_dir)
    sagitta_hist.Add(sagitta_hist_subtraction, -1.0)
    return solution_histogram(sagitta_hist)

def get_injection_values_global(eta_edges, phi_edges, detector_location = "ID"):
    values = np.zeros((len(eta_edges)-1, len(phi_edges)-1))
    values -= 0.3
    values = scale_to(values)
    return values

def get_injection_values_null(eta_edges, phi_edges, detector_location = "ID"):
    values = np.zeros((len(eta_edges)-1, len(phi_edges)-1))
    return values

def get_injection_values_globalpluslocal(eta_edges, phi_edges, detector_location = "ID"):
    values_global = get_injection_values_global( eta_edges, phi_edges, detector_location = "ID")
    values_local = get_injection_values_local( eta_edges, phi_edges, detector_location = "ID")
    return values_global + values_local

def injection_histogram(values_function, detector_location = "ID"):
    from MatrixInversion import eta_edges_ID, eta_edges_else, phi_edges

    if detector_location == "ID":
        eta_edges = eta_edges_ID
    else:
        eta_edges = eta_edges_else

    values = values_function( eta_edges, phi_edges, detector_location = detector_location)

    from array import array
    delta_hist = ROOT.TH2D("delta_injection", "delta_injection", len(eta_edges) - 1, array('d',eta_edges), len(phi_edges) - 1, array('d',phi_edges))
    for bindex_x in range(0, len(eta_edges)-1):
        for bindex_y in range(0, len(phi_edges)-1):
            delta_hist.SetBinContent(bindex_x+1, bindex_y+1, values[bindex_x, bindex_y])

    return delta_hist

injection_histogram_local = lambda detector_location = "ID" , _ = get_injection_values_local :  injection_histogram(_, detector_location = detector_location)
injection_histogram_null = lambda detector_location = "ID" , _ = get_injection_values_null :  injection_histogram(_, detector_location = detector_location)
injection_histogram_global = lambda detector_location = "ID" , _ = get_injection_values_global :  injection_histogram(_, detector_location = detector_location)
injection_histogram_globalpluslocal = lambda detector_location = "ID" , _ = get_injection_values_globalpluslocal :  injection_histogram(_, detector_location = detector_location)

def solution_histogram(hist):
     hist.Scale(-1.0)
     return hist



