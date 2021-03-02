import numpy as np
import numexpr as ne
import ROOT
from array import array
from variables import \
                      calc_pos_id_pt, calc_neg_id_pt,\
                      calc_pos_ms_pt, calc_neg_ms_pt,\
                      calc_pos_me_pt, calc_neg_me_pt,\
                      calc_pos_cb_pt, calc_neg_cb_pt,\
                      calc_pos_id_eta, calc_neg_id_eta,\
                      calc_pos_ms_eta, calc_neg_ms_eta,\
                      calc_pos_me_eta, calc_neg_me_eta,\
                      calc_pos_cb_eta, calc_neg_cb_eta,\
                      calc_pos_id_phi, calc_neg_id_phi,\
                      calc_pos_ms_phi, calc_neg_ms_phi,\
                      calc_pos_me_phi, calc_neg_me_phi,\
                      calc_pos_cb_phi, calc_neg_cb_phi
from selections import check_safe_event

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

class MCCorrection:

    #the histogram is a segitta bias correction map for delta s
    def __init__(self, so=None, s1=None, r0=None, r1=None, r2=None,  pos_varx, neg_varx, pos_vary, neg_vary, pos_selections = [], neg_selections = [],flavour = ""):
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
        if flavour == "ME":
            self.pos_pt_var = calc_pos_me_pt
            self.neg_pt_var = calc_neg_me_pt
            self.pos_phi_var = calc_pos_me_phi
            self.neg_phi_var = calc_neg_me_phi
            self.pos_eta_var = calc_pos_me_eta
            self.neg_eta_var = calc_neg_me_eta
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

        self.s0 = s0
        self.s1 = s1
        self.r0 = r0
        self.r1 = r1
        self.r2 = r2
        self.edges_x = {}
        self.edges_y = {}
        self.corrections = {}
        self.inject = False

        self.branches = []
        for v in [self.pos_varx, self.pos_vary, self.neg_varx, self.neg_vary] + all_extra_vars + self.pos_selections + self.neg_selections:
            self.branches = list(set(self.branches + v.branches))

        for attr in ["s0", "s1", "r0", "r1", "r2"]:
           histogram = self.getattr(attr)
           if histogram is not None:
               edges = extract_binning_from_histogram(histogram)
               #load some information about the histogram, such as the bin edges
               self.edges_x[attr] = np.array(edges["x"], np.float32)
               self.edges_y[attr] = np.array(edges["y"], np.float32)

               self.corrections[attr] = np.zeros((len(self.edges_x)-1, len(self.edges_y)-1))
               for i in range(1, len(self.edges_x )):
                   for j in range(1, len(self.edges_y)):
                       self.corrections[attr][i-1, j-1] = sum([el.GetBinContent(i, j) for el in self.histograms])
           else:
               self.edges_x[attr] = None
               self.edges_y[attr] = None
               self.corrections[attr] = None

    def calibrate(self, data):

        #ok, now correct the pT
        pos_pt_name = "Pos_{}_Pt".format(self.flavour)
        neg_pt_name = "Neg_{}_Pt".format(self.flavour)
        corrections_pos = {key:None for key in ["s0", "s1", "r0", "r1", "r2"]}
        corrections_neg = {key:None for key in ["s0", "s1", "r0", "r1", "r2"]}
        for variable in corrections:
           if getattr(self, variable) is None:
               corrections_pos[variables] = np.zeros(len(data))
               corrections_neg[variables] = np.zeros(len(data))
               continue
           print("CALIBRATING VARIABLES")
           nbins_x = len(self.edges_x[variable]) -1
           bindex_x_pos = np.digitize(self.pos_varx.eval(data), self.edges_x[variable]) - 1
           underflow_x_pos = bindex_x_pos == -1
           overflow_x_pos = bindex_x_pos == nbins_x
           bindex_x_pos[underflow_x_pos] = 0
           bindex_x_pos[overflow_x_pos] = nbins_x - 1

           bindex_x_neg = np.digitize(self.neg_varx.eval(data), self.edges_x[variable]) - 1
           underflow_x_neg = bindex_x_neg == -1
           overflow_x_neg = bindex_x_neg == nbins_x
           bindex_x_neg[underflow_x_neg] = 0
           bindex_x_neg[overflow_x_neg] = nbins_x - 1

           nbins_y = len(self.edges_y[variable]) -1
           bindex_y_pos = np.digitize(self.pos_vary.eval(data), self.edges_y[variable]) - 1
           underflow_y_pos = bindex_y_pos == -1
           overflow_y_pos = bindex_y_pos == nbins_y
           bindex_y_pos[underflow_y_pos] = 0
           bindex_y_pos[overflow_y_pos] = nbins_y - 1

           bindex_y_neg = np.digitize(self.neg_vary.eval(data), self.edges_y[variable]) - 1
           underflow_y_neg = bindex_y_neg == -1
           overflow_y_neg = bindex_y_neg == nbins_y
           bindex_y_neg[underflow_y_neg] = 0
           bindex_y_neg[overflow_y_neg] = nbins_y - 1

           #don't correct overflow!
           not_overflow_pos = np.logical_and.reduce([np.logical_not(el) for el in [underflow_x_pos, underflow_y_pos,  overflow_x_pos, overflow_y_pos]])
           not_overflow_neg = np.logical_and.reduce([np.logical_not(el) for el in [underflow_x_neg, underflow_y_neg, overflow_x_neg, overflow_y_neg]])
           not_overflow = np.logical_and(not_overflow_pos, not_overflow_neg)

           print("The amount of overflow, positive:")
           print(min(self.edges_x[variable]), max(self.edges_x[variable]))
           print(np.sum(1 * np.logical_not(not_overflow_pos)))
           print("The amount of overflow, negative:")
           print(min(self.edges_y[variable]), max(self.edges_y[variable]))
           print(np.sum(1 * np.logical_not(not_overflow_neg)))

           correction_for_data_pos = self.corrections[bindex_x_pos, bindex_y_pos]
           correction_for_data_neg = self.corrections[bindex_x_neg, bindex_y_neg]

           pos_selection = np.logical_and.reduce([el.eval(data) for el in self.pos_selections] + [not_overflow_pos])
           neg_selection = np.logical_and.reduce([el.eval(data) for el in self.neg_selections] + [not_overflow_neg])

           corrections_pos[variable]= np.zeros(len(data))
           corrections_neg[variable] = np.zeros(len(data))

           corrections_pos[variable][pos_selection] = correction_for_data_pos[pos_selection]
           corrections_neg[variable][neg_selection] = correction_for_data_neg[neg_selection]

        extra_corrections = ["Pair_{}_Mass", "Pair_{}_Pt", "Pair_{}_Eta", "Pair_{}_Phi"]

        #apply the calibration
        if not self.injection:
            df[pos_pt_name] = corrections_pos["s0"] + (1.0 + corrections_pos["s1"]) * df["pos_pt_name"].values
            df[neg_pt_name] = corrections_neg["s0"] + (1.0 + corrections_neg["s1"]) * df["neg_pt_name"].values
        else:
            df[pos_pt_name] = (df["pos_pt_name"].values - corrections_pos["s0"])/(1.0 + corrections_pos["s1"])
            df[neg_pt_name] = (df["neg_pt_name"].values - corrections_neg["s0"])/(1.0 + corrections_neg["s1"])

        if hasattr(data, "dtype"): keys =  data.dtype.names
        else: keys = list(data.keys())
        do_extra_corrections = any([ (el.format(self.flavour) in keys) for el in extra_corrections])
        print("CALIBRATED PTS")

        if do_extra_corrections:
            to_correct_data = {}
            for key in keys:
                to_correct_data[key] = data[key]
            safe =  check_safe_event(to_correct_data,"Pos", self.flavour) & check_safe_event(to_correct_data,"Neg", self.flavour)
            to_correct_selection = safe
            for key in keys:
                to_correct_data[key] = to_correct_data[key][to_correct_selection]
            pos_pt = self.pos_pt_var.eval(to_correct_data)
            neg_pt = self.neg_pt_var.eval(to_correct_data)

            pos_px = pos_pt * np.cos(self.pos_phi_var.eval(to_correct_data))
            neg_px = neg_pt * np.cos(self.neg_phi_var.eval(to_correct_data))

            pos_py = pos_pt * np.sin(self.pos_phi_var.eval(to_correct_data))
            neg_py = neg_pt * np.sin(self.neg_phi_var.eval(to_correct_data))

            pos_pz = pos_pt * np.sinh(self.pos_eta_var.eval(to_correct_data))
            neg_pz = neg_pt * np.sinh(self.neg_eta_var.eval(to_correct_data))
            #copy the code from tlorentz vector
            #pos_pz = pos_pt/np.tan(2.0*np.arctan(np.exp(-1.0 * self.pos_eta_var.eval(to_correct_data))))
            #neg_pz = neg_pt/np.tan(2.0*np.arctan(np.exp(-1.0 * self.neg_eta_var.eval(to_correct_data))))

            dimuon_pt_str = "sqrt( (pos_px**2) + (neg_px**2))"
            muon_mass = 105.658/1000.0
            pos_e_str = "sqrt( (muon_mass**2) + (pos_px ** 2) + (pos_py ** 2) + (pos_pz ** 2))"
            neg_e_str = "sqrt( (muon_mass**2) + (neg_px ** 2) + (neg_py ** 2) + (neg_pz ** 2))"
            if "Pair_{}_Mass".format(self.flavour) in keys:

                mass_sqrd = ne.evaluate("( ( {p_pos} + {p_neg}) ** 2 ) - ( (pos_px + neg_px) ** 2 ) - ( (pos_py + neg_py) ** 2 ) - ( (pos_pz + neg_pz) ** 2 )".format(p_pos=pos_e_str, p_neg=neg_e_str))
                data["Pair_{}_Mass".format(self.flavour)][to_correct_selection] = np.sign(mass_sqrd) * np.sqrt(mass_sqrd * np.sign(mass_sqrd))

            if "Pair_{}_Pt".format(self.flavour) in keys:
                data["Pair_{}_Pt".format(self.flavour)][to_correct_selection] = ne.evaluate(dimuon_pt_str)

            if "Pair_{}_Phi".format(self.flavour) in keys:
                data["Pair_{}_Phi".format(self.flavour)][to_correct_selection] = ne.evaluate("arccos((pos_px + neg_px)/({dimuon_pt_str}))".format(dimuon_pt_str))

            if "Pair_{}_Eta".format(self.flavour) in keys:
                data["Pair_{}_Eta".format(self.flavour)][to_correct_selection] = ne.evaluate("arcsinh((pos_pz + neg_pz)/({dimuon_pt_str}))".format(dimuon_pt_str))
        return data

