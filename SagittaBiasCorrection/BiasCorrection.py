import numpy as np
import numexpr as ne
import ROOT
from array import array
from variables import \
                      calc_pos_id_pt, calc_neg_id_pt,\
                      calc_pos_ms_pt, calc_neg_ms_pt,\
                      calc_pos_cb_pt, calc_neg_cb_pt,\
                      calc_pos_id_eta, calc_neg_id_eta,\
                      calc_pos_ms_eta, calc_neg_ms_eta,\
                      calc_pos_cb_eta, calc_neg_cb_eta,\
                      calc_pos_id_phi, calc_neg_id_phi,\
                      calc_pos_ms_phi, calc_neg_ms_phi,\
                      calc_pos_cb_phi, calc_neg_cb_phi

def extract_binning_from_axis(axis):
    '''
    Take a TAxis axis and return a list representing all bin edges along axis.
    '''
    edges = []
    for i in range(1, axis.GetNbins()+1):
        edges.append(axis.GetBinLowEdge(i))
    edges.append(axis.GetBinUpEdge(axis.GetNbins()))
    return edges

def extract_binning_from_histogram(hist):
    edges = {}
    if isinstance(hist, ROOT.TH1):
        nedges = 1
        axes = {"x": hist.GetXaxis()}
    if isinstance(hist, ROOT.TH2):
        nedges = 2
        axes = {"x":hist.GetXaxis(), "y":hist.GetYaxis()}
    if isinstance(hist, ROOT.TH3):
        nedges = 3
        axes = {"x":hist.GetXaxis(), "y": hist.GetYaxis(), "z":hist.GetZaxis()}
    for axisname in axes:
        these_edges = extract_binning_from_axis(axes[axisname])
        edges[axisname] = these_edges
    return edges

#write a function that takes the positive and negative mass histograms, and calculates the sagitta bias
def calculate_sagitta_bias(pos_hist, neg_hist, newname = None):
    #check that both histograms are tprofile 2ds
    assert isinstance(pos_hist, ROOT.TProfile2D)
    assert isinstance(neg_hist, ROOT.TProfile2D)

    edges_pos = extract_binning_from_histogram(pos_hist)
    edges_neg = extract_binning_from_histogram(neg_hist)

    #ok make sure that 
    for key in edges_pos:
        assert key in edges_neg
        for el in edges_pos[key]:
            assert el in edges_neg[key]
        for el in edges_neg[key]:
            assert el in edges_pos[key]

    bins_array_x = array('d',edges_pos["x"])
    bins_array_y = array('d',edges_neg["y"])

    if newname is None: newname = pos_hist.GetName().replace("Pos_", "Pos_Neg_Sagitta")
    new_hist = ROOT.TH2D(newname, newname, len(bins_array_x)-1, bins_array_x, len(bins_array_y)-1, bins_array_y)
    new_hist.GetXaxis().SetTitle(pos_hist.GetXaxis().GetTitle())
    new_hist.GetYaxis().SetTitle(pos_hist.GetYaxis().GetTitle())
    new_hist.GetZaxis().SetTitle("<qM_{#mu#mu}>/<M_{#mu#mu}>")
    max_content = 0.0
    for i in range(1, len(edges_pos["x"]) + 1):
        for j in range(1, len(edges_pos["y"]) + 1):
            pos_bindex = pos_hist.GetBin(i,j)
            pos_mean = pos_hist.GetBinContent(pos_bindex)
            pos_entries = pos_hist.GetBinEntries(pos_bindex)
            neg_bindex = neg_hist.GetBin(i,j)
            neg_mean = neg_hist.GetBinContent(neg_bindex)
            neg_entries = neg_hist.GetBinEntries(neg_bindex)
            if (pos_entries + neg_entries) > 0.0 and (pos_entries > 0.0) and (neg_entries > 0.0):
                qm_average = ((pos_mean * pos_entries) - (neg_mean * neg_entries))/(pos_entries + neg_entries)
                m_average = ((pos_mean * pos_entries) + (neg_mean * neg_entries))/(pos_entries + neg_entries)
                new_entry = (qm_average)/m_average
            else: new_entry = 0.0
            if abs(new_entry) > max_content: max_content=abs(new_entry)
            new_hist.SetBinContent(i, j, new_entry)
    new_hist.SetMaximum(max_content)
    new_hist.SetMinimum(-1.0 * max_content)
    return new_hist

class SagittaBiasCorrection:

    #the histogram is a segitta bias correction map for delta s
    def __init__(self, histograms,  pos_varx, neg_varx, pos_vary, neg_vary, pos_selections = [], neg_selections = [],flavour = "",):
        assert flavour in ["ID", "MS", "CB", "ME"]
        self.flavour = flavour
        if flavour == "ID":
            self.pos_pt_var = calc_pos_id_pt
            self.neg_pt_var = calc_neg_id_pt
            self.pos_phi_var = calc_pos_id_phi
            self.neg_phi_var = calc_neg_id_phi
            self.pos_eta_var = calc_pos_id_eta
            self.neg_eta_var = calc_neg_id_eta
        if flavour == "MS":
            self.pos_pt_var = calc_pos_ms_pt
            self.neg_pt_var = calc_neg_ms_pt
            self.pos_phi_var = calc_pos_ms_phi
            self.neg_phi_var = calc_neg_ms_phi
            self.pos_eta_var = calc_pos_ms_eta
            self.neg_eta_var = calc_neg_ms_eta
        if flavour == "CB":
            self.pos_pt_var = calc_pos_cb_pt
            self.neg_pt_var = calc_neg_cb_pt
            self.pos_phi_var = calc_pos_cb_phi
            self.neg_phi_var = calc_neg_cb_phi
            self.pos_eta_var = calc_pos_cb_eta
            self.neg_eta_var = calc_neg_cb_eta

        self.pos_selections = pos_selections
        self.neg_selections = neg_selections

        all_extra_vars = [calc_pos_cb_pt, calc_neg_cb_pt, \
                          calc_pos_cb_eta, calc_neg_cb_eta,\
                          calc_pos_cb_phi, calc_neg_cb_phi]

        self.pos_varx = pos_varx
        self.pos_vary = pos_vary

        self.neg_varx = neg_varx
        self.neg_vary = neg_vary

        self.histograms = histograms
        self.branches = []
        for v in [self.pos_varx, self.pos_vary, self.neg_varx, self.neg_vary] + all_extra_vars + self.pos_selections + self.neg_selections:
            self.branches = list(set(self.branches + v.branches))

        histogram = histograms[-1]
        edges = extract_binning_from_historgam(histogram)
        #load some information about the histogram, such as the bin edges
        self.edges_x = np.array(edges["x"], np.float32)
        self.edges_y = np.array(edges["y"], np.float32)

        corrections = np.zeros(len(edges_x), len(edges_y))
        for i, j in zip(range(1, len(edges_x + 1)), range(1, len(edges_y + 1))):
            corrections[i-1, j-1] = sum([el.GetBinContent(i, j) for el in self.histograms])
        self.corrections = corrections

    def calibrate(self, data):
        bindex_x = numpy.digitize(self.varx.eval(data), self.edges_x) - 1
        underflow_x = bindex_x == -1
        overflow_x = bindex_x == len(self.edges_x)
        bindex_x[underflow_x] = 0
        bindex_x[overflow_x] = len(self.edges_x)-1

        bindex_y = numpy.digitize(self.vary.eval(data), self.edges_y) - 1
        underflow_y = bindex_y == -1
        overflow_y = bindex_y == len(self.edges_y)
        bindex_y[underflow_y] = 0
        bindex_y[overflow_y] = len(self.edges_y)-1

        correction_for_data = self.corrections[bindex_x, bindex_y]

        #ok, now correct the pT
        pos_pt_name = "Pos_{}_Pt".format(self.flavour)
        neg_pt_name = "Neg_{}_Pt".format(self.flavour)

        pos_selection = np.logical_and.reduce([el.eval(data) for el in self.pos_selections])
        neg_selection = np.logical_and.reduce([el.eval(data) for el in self.neg_selections])

        #apply the calibration to the ntuple
        data[pos_pt_name][pos_selection] = data[pos_pt_name][pos_selection] / (1.0 + ((1.0) * data[pos_pt_name][pos_selection] * correction_for_data))

        data[neg_pt_name][neg_selection] = data[neg_pt_name][neg_selection] / (1.0 + ((-1.0) * data[neg_pt_name][neg_selection] * correction_for_data))

        extra_corrections = ["Pair_{}_Mass", "Pair_{}_Pt", "Pair_{}_Eta", "Pair_{}_Phi"]

        do_extra_correction = any([ (el.format(self.falvour) in data) for el in extra_corrections])

        if do_extra_corrections:
            to_correct_selection = np.logical_or(pos_selection, neg_selection)
            to_correct_data = {}
            for key in data:
                to_correct_data[key] = data[key][to_correct_selection]
            pos_px = self.pos_pt_var * np.cos(self.pos_phi_var.eval(to_correct_data))
            neg_px = self.neg_pt_var * np.cos(self.neg_phi_var.eval(to_correct_data))

            pos_py = self.pos_pt_var * np.sin(self.pos_phi_var.eval(to_correct_data))
            neg_py = self.neg_pt_var * np.sin(self.neg_phi_var.eval(to_correct_data))

            pos_pz = self.pos_pt_var * np.sinh(self.pos_eta_var.eval(to_correct_data))
            neg_pz = self.neg_pt_var * np.sinh(self.neg_eta_var.eval(to_correct_data))

            dimuon_pt_str = "sqrt( (pos_px**2) + (neg_px**2))"
            if "Pair_{}_Mass".format(self.flavour) in data:
                pos_p_str = "sqrt( (pos_px ** 2) + (pos_py ** 2) + (pos_pz ** 2))"
                neg_p_str = "sqrt( (neg_px ** 2) + (neg_py ** 2) + (neg_pz ** 2))"

                mass_sqrd = ne.evaluate(" ( ( {p_pos} + {p_neg}) ** 2 )".fromat(p_pos=pos_p_str, p_neg=neg_p_str) + \
                                          "- ( (pos_px + neg_px) ** 2 ) " + \
                                          "- ( (pos_py + neg_py) ** 2 ) " + \
                                          "- ( (pos_pz + neg_pz) ** 2 ) ")
                data["Pair_{}_Mass".format(self.flavour)][to_correct_selection] = np.sign(mass_sqrd) * np.sqrt(mass_sqrt * np.sign(mass_sqrd))

            if "Pair_{}_Pt".format(self.flavour) in data:
                data["Pair_{}_Pt".format(self.flavour)][to_correct_selection] = ne.evaluate(dimuon_pt_str)

            if "Pair_{}_Phi".format(self.flavour) in data:
                data["Pair_{}_Phi".format(self.flavour)][to_correct_selection] = ne.evaluate("arccos((pos_px + neg_px)/({dimuon_pt_str}))".format(dimuon_pt_str))

            if "Pair_{}_Eta".format(self.flavour) in data:
                data["Pair_{}_Eta".format(self.flavour)][to_correct_selection] = ne.evaluate("arcsinh((pos_pz + neg_pz)/({dimuon_pt_str}))".format(dimuon_pt_str))
        return data

