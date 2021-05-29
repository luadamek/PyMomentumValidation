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
    def __init__(self, s0=None, s1=None, r0=None, r1=None, r2=None, pos_selections = [], neg_selections = [],flavour = "", store_uncorr = False):
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

        self.s0 = s0
        self.s1 = s1
        self.r0 = r0
        self.r1 = r1
        self.r2 = r2
        self.edges_x = {}
        self.edges_y = {}

        self.store_uncorr = store_uncorr

        self.selection_cache = {}

        self.branches = []
        for key in self.__dict__:
            if hasattr(self.__dict__[key], "branches"):
                self.branches = list(set(self.branches + self.__dict__[key].branches))

    def calibrate(self, data):
        extra_corrections = ["Pair_{}_Mass", "Pair_{}_Pt", "Pair_{}_Eta", "Pair_{}_Phi"]

        passes_pos_selection = []
        passes_neg_selection = []
        #add temporary branches to the data to speed up evaluation
        for el in self.pos_selections:
            if type(el) == dict:
                args = [data] + el["args"]
                descr = el["func"].__name__ + "_".join([str(e) for e in el["args"]])
                if descr not in data:
                    data[descr] = el["func"](*args)
                passes_pos_selection.append( data[descr] )
            else:
                descr = el.name + "__EVAL__"
                if descr not in data:
                    data[descr] = el.eval(data)
                passes_pos_selection.append(data[descr])

        for el in self.neg_selections:
            if type(el) == dict:
                args = [data] + el["args"]
                descr = el["func"].__name__ + "_".join([str(e) for e in el["args"]])
                if descr not in data:
                    data[descr] = el["func"](*args)
                passes_neg_selection.append( data[descr] )
            else:
                descr = el.name + "__EVAL__"
                if descr not in data:
                    data[descr] = el.eval(data)
                passes_neg_selection.append(data[descr])

        passes_pos_selection = np.logical_and.reduce(passes_pos_selection)
        passes_neg_selection = np.logical_and.reduce(passes_neg_selection)


        npass_pos = np.sum(1 * passes_pos_selection)
        npass_neg = np.sum(1 * passes_neg_selection)

        random_pos = np.random.normal(npass_pos)
        random_neg = np.random.normal(npass_neg)

        pos_pt = data["Pos_{}_Pt".format(self.flavour)][passes_pos_selection]
        neg_pt = data["Neg_{}_Pt".format(self.flavour)][passes_neg_selection]

        third_term_pos = self.r2*pos_pt
        third_term_neg = self.r2*neg_pt

        if self.flavour == "ID":
            pos_etas = self.pos_eta_var.eval(data)[passes_pos_selection]
            neg_etas = self.neg_eta_var.eval(data)[passes_neg_selection]

            pos_abs_etas = np.abs(pos_etas)
            neg_abs_etas = np.abs(neg_etas)

            forward_pos = (pos_abs_etas > 2.0) & (pos_abs_etas < 2.8)
            forward_neg = (neg_abs_etas > 2.0) & (neg_abs_etas < 2.8)

            tan_theta_pos = np.tan(2.0 * np.arctan(np.exp(-1.0 * pos_abs_etas)))
            tan_theta_neg = np.tan(2.0 * np.arctan(np.exp(-1.0 * neg_abs_etas)))

            third_term_pos[forward_pos] = third_term_pos[forward_pos]/(tan_theta_pos[forward_pos])
            third_term_neg[forward_neg] = third_term_neg[forward_neg]/(tan_theta_neg[forward_neg])


        #print("s0", self.s0)
        #print("s1", self.s1)
        #print("r0", self.r0)
        #print("r1", self.r1)
        #print("r2", self.r2)

        quad_sum_one_pos = (self.r0/(pos_pt)) ** 2
        quad_sum_one_neg = (self.r0/(neg_pt)) ** 2

        quad_sum_two_pos = self.r1 ** 2
        quad_sum_two_neg = self.r1 ** 2

        quad_sum_three_pos = (self.r2 * (third_term_pos )) ** 2
        quad_sum_three_neg = (self.r2 * (third_term_neg )) ** 2

        n_pos = np.sum(1*passes_pos_selection)
        n_neg = np.sum(1*passes_neg_selection)

        smear_pos = ((quad_sum_one_pos + quad_sum_two_pos + quad_sum_three_pos )**0.5)
        smear_neg = ((quad_sum_one_neg + quad_sum_two_neg + quad_sum_three_neg )**0.5)

        den_pos = 1.0 + (np.random.normal(size=n_pos)*smear_pos)
        den_neg = 1.0 + (np.random.normal(size=n_neg)*smear_neg)

        print("Correcting {} of {}".format(n_pos, len(data)))
        print("Correcting {} of {}".format(n_neg, len(data)))

        print("Smeared by")
        print(smear_pos)
        print(smear_neg)

        print("pos change")
        print(den_pos)

        print("neg change")
        print(den_neg)


        if  "Pos_{}_Pt_UNCORR".format(self.flavour) not in data and self.store_uncorr:
            data["Pos_{}_Pt_UNCORR".format(self.flavour)] = np.zeros(len(data["Pos_{}_Pt".format(self.flavour)]))
            data["Pos_{}_Pt_UNCORR".format(self.flavour)][:] = data["Pos_{}_Pt".format(self.flavour)]
        if  "Neg_{}_Pt_UNCORR".format(self.flavour) not in data and self.store_uncorr:
            data["Neg_{}_Pt_UNCORR".format(self.flavour)] = np.zeros(len(data["Neg_{}_Pt".format(self.flavour)]))
            data["Neg_{}_Pt_UNCORR".format(self.flavour)][:] = data["Neg_{}_Pt".format(self.flavour)]

        print("Before MC Correction {}".format(data["Pos_{}_Pt".format(self.flavour)][passes_pos_selection]))
        data["Pos_{}_Pt".format(self.flavour)][passes_pos_selection] = \
        (self.s0 + (( 1.0 + self.s1 ) * pos_pt)) / den_pos
        print("After MC Correction {}".format(data["Pos_{}_Pt".format(self.flavour)][passes_pos_selection]))

        print("Before MC Correction {}".format(data["Neg_{}_Pt".format(self.flavour)][passes_neg_selection]))
        data["Neg_{}_Pt".format(self.flavour)][passes_neg_selection] = \
        (self.s0 + ((1.0 + self.s1) * neg_pt)) / den_neg
        print("After MC Correction {}".format(data["Neg_{}_Pt".format(self.flavour)][passes_neg_selection]))

        if hasattr(data, "dtype"): keys =  data.dtype.names
        else: keys = list(data.keys())
        do_extra_corrections = any([ (el.format(self.flavour) in keys) for el in extra_corrections])
        print("CALIBRATED PTS")

        if do_extra_corrections:
            correction_keys = self.pos_pt_var.branches + self.neg_pt_var.branches + self.pos_phi_var.branches + self.neg_phi_var.branches + self.pos_eta_var.branches + self.neg_eta_var.branches
            to_correct_data = {}
            for key in correction_keys:
                to_correct_data[key] = data[key]
            safe =  check_safe_event(to_correct_data,"Pos", self.flavour) & check_safe_event(to_correct_data,"Neg", self.flavour)
            to_correct_selection = np.logical_or(passes_pos_selection, passes_neg_selection) & safe

            for key in correction_keys:
                to_correct_data[key] = to_correct_data[key][to_correct_selection]
            pos_pt = self.pos_pt_var.eval(to_correct_data)
            neg_pt = self.neg_pt_var.eval(to_correct_data)

            pos_px = pos_pt * np.cos(self.pos_phi_var.eval(to_correct_data))
            neg_px = neg_pt * np.cos(self.neg_phi_var.eval(to_correct_data))

            pos_py = pos_pt * np.sin(self.pos_phi_var.eval(to_correct_data))
            neg_py = neg_pt * np.sin(self.neg_phi_var.eval(to_correct_data))

            pos_pz = pos_pt * np.sinh(self.pos_eta_var.eval(to_correct_data))
            neg_pz = neg_pt * np.sinh(self.neg_eta_var.eval(to_correct_data))

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

