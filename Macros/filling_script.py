from variables import calc_id_mass, calc_cb_mass, calc_me_mass
from selections import range_selection_function, sel_nonzero_id_pts, sel_nonzero_me_pts, sel_min_fifteen_id_pts, sel_min_fifteen_me_pts, sel_unprescaled_trigger, sel_opp_charge
from selections import range_selection_function, sel_nonzero_id_pts, sel_nonzero_cb_pts, sel_min_fifteen_id_pts, sel_min_fifteen_cb_pts, sel_unprescaled_trigger, sel_opp_charge
from histogram_filler import create_selection_function, write_histograms
import ROOT
from BiasCorrection import SagittaBiasCorrection
from variables import \
                      calc_pos_id_pt, calc_neg_id_pt,\
                      calc_pos_me_pt, calc_neg_me_pt,\
                      calc_pos_cb_pt, calc_neg_cb_pt,\
                      calc_pos_id_eta, calc_neg_id_eta,\
                      calc_pos_me_eta, calc_neg_me_eta,\
                      calc_pos_cb_eta, calc_neg_cb_eta,\
                      calc_pos_id_phi, calc_neg_id_phi,\
                      calc_pos_me_phi, calc_neg_me_phi,\
                      calc_pos_cb_phi, calc_neg_cb_phi,\
                      calc_leading_id_pt, calc_subleading_id_pt,\
                      calc_leading_me_pt, calc_subleading_me_pt,\
                      calc_leading_id_eta, calc_subleading_id_eta,\
                      calc_leading_me_eta, calc_subleading_me_eta,\
                      calc_leading_id_phi, calc_subleading_id_phi,\
                      calc_leading_me_phi, calc_subleading_me_phi,\
                      calc_weight_var

from selections import sel_pos_leading_id, sel_neg_leading_id
from selections import sel_pos_leading_me, sel_neg_leading_me
from variables import calc_leading_id_pt, calc_leading_id_phi, calc_leading_id_eta
from variables import calc_leading_cb_pt, calc_leading_cb_phi, calc_leading_cb_eta
from variables import calc_leading_me_pt, calc_leading_me_phi, calc_leading_me_eta
from variables import calc_subleading_id_pt, calc_subleading_id_phi, calc_subleading_id_eta
from variables import calc_subleading_cb_pt, calc_subleading_cb_phi, calc_subleading_cb_eta
from variables import calc_subleading_me_pt, calc_subleading_me_phi, calc_subleading_me_eta

###################################################################
from selections import sel_pos_leading_id, sel_neg_leading_id
from selections import sel_pos_leading_cb, sel_neg_leading_cb
from selections import sel_pos_leading_me, sel_neg_leading_me
import numpy as np
#put this as the default pt binning somewhere
from binnings import global_pt_binning
pt_bins = global_pt_binning

def book_histograms(hist_filler, eta_ID_bin_options, eta_bin_options, phi_bin_options, histsetname):

    histogram_name_base = "{histsetname}_{location}_Mass_Histogram_{count}"
    histogram_name = histogram_name_base.format(count="Inclusive", location="ID", histsetname=histsetname)
    hist_filler.book_histogram_fill(histogram_name,\
                                         calc_id_mass,\
                                         selections = [],\
                                         bins = 200,\
                                         range_low = 91.2-12.0,\
                                         range_high = 91.2+12.0,\
                                         xlabel ='M_{#mu#mu}^{ID} [GeV]',\
                                         ylabel = 'Number Events')

    histogram_name_base = "{histsetname}_{location}_Mass_Histogram_{count}"
    histogram_name = histogram_name_base.format(count="Inclusive", location="CB", histsetname=histsetname)
    hist_filler.book_histogram_fill(histogram_name,\
                                         calc_cb_mass,\
                                         selections = [],\
                                         bins = 200,\
                                         range_low = 91.2-12.0,\
                                         range_high = 91.1+10.0,\
                                         xlabel ='M_{#mu#mu}^{CB} [GeV]',\
                                         ylabel = 'Number Events')


    histogram_name_base = "{histsetname}_{location}_Mass_Histogram_{count}"
    histogram_name = histogram_name_base.format(count="Inclusive", location="ME", histsetname=histsetname)
    hist_filler.book_histogram_fill(histogram_name,\
                                         calc_me_mass,\
                                         selections = [],\
                                         bins = 200,\
                                         range_low = 91.2-12.0,\
                                         range_high = 91.2+12.0,\
                                         xlabel ='M_{#mu#mu}^{ME} [GeV]',\
                                         ylabel = 'Number Events')


    phi_bins = np.linspace(phi_bin_options["philow"], phi_bin_options["phihigh"], phi_bin_options["nbins"] + 1)

    #book a tprofile of the average mass
    mass_ID = "Pair_ID_Mass"
    mass_CB = "Pair_CB_Mass"

    mass_sel_func_ID = create_selection_function(range_selection_function, [mass_ID], mass_ID, 91.2 - 10.0, 91.2 + 10.0)
    mass_sel_func_CB = create_selection_function(range_selection_function, [mass_CB], mass_CB, 91.2 - 10.0, 91.2 + 10.0)
    mass_sel_func_ME = create_selection_function(range_selection_function, [mass_ME], mass_ME, 91.2 - 10.0, 91.2 + 10.0)

    base_selections_ID = [mass_sel_func_ID]
    base_selections_CB = [mass_sel_func_CB]
    base_selections_MS = [mass_sel_func_MS]
    base_selections_ME = [mass_sel_func_ME]
    i = "Inclusive"
    histogram_name_base = "{histsetname}_{charge}_{location}_AverageMassProfile_{count}"
    histogram_name = histogram_name_base.format(charge="Pos", count=i, location="ID", histsetname=histsetname)
    hist_filler.book_2dtprofile_fill(histogram_name, \
                                              calc_pos_id_eta,\
                                              calc_pos_id_phi,\
                                              calc_id_mass,\
                                              selections = base_selections_ID,\
                                              bins_x = eta_ID_bin_options["nbins"],\
                                              range_low_x = eta_ID_bin_options["etalow"],\
                                              range_high_x = eta_ID_bin_options["etahigh"],\
                                              xlabel = "#eta_{#mu}",\
                                              bins_y=phi_bin_options["nbins"],\
                                              range_low_y=phi_bin_options["philow"],\
                                              range_high_y=phi_bin_options["phihigh"],\
                                              ylabel = "#phi_{#mu}",\
                                              zlabel="<M_{#mu#mu}> [Gev]",\
                                              error_option="")

    histogram_name = histogram_name_base.format(charge="Neg", count=i, location="ID", histsetname=histsetname)
    hist_filler.book_2dtprofile_fill(histogram_name, \
                                              calc_neg_id_eta,\
                                              calc_neg_id_phi,\
                                              calc_id_mass,\
                                              selections = base_selections_ID,\
                                              bins_x = eta_ID_bin_options["nbins"],\
                                              range_low_x = eta_ID_bin_options["etalow"],\
                                              range_high_x = eta_ID_bin_options["etahigh"],\
                                              xlabel = "#eta_{#mu}",\
                                              bins_y=phi_bin_options["nbins"],\
                                              range_low_y=phi_bin_options["philow"],\
                                              range_high_y=phi_bin_options["phihigh"],\
                                              ylabel = "#phi_{#mu}",\
                                              zlabel="<M_{#mu#mu}> [Gev]",\
                                              error_option="")

    #book a tprofile of the average mass
    histogram_name = histogram_name_base.format(charge="Pos", count=i, location="CB", histsetname=histsetname)
    hist_filler.book_2dtprofile_fill(histogram_name, \
                                              calc_pos_cb_eta,\
                                              calc_pos_cb_phi,\
                                              calc_cb_mass,\
                                              selections = base_selections_CB,\
                                              bins_x = eta_bin_options["nbins"],\
                                              range_low_x = eta_bin_options["etalow"],\
                                              range_high_x = eta_bin_options["etahigh"],\
                                              xlabel = "#eta_{#mu}",\
                                              bins_y=phi_bin_options["nbins"],\
                                              range_low_y=phi_bin_options["philow"],\
                                              range_high_y=phi_bin_options["phihigh"],\
                                              ylabel = "#phi_{#mu}",\
                                              zlabel="<M_{#mu#mu}> [Gev]",\
                                              error_option="")

    histogram_name = histogram_name_base.format(charge="Neg", count=i, location="CB", histsetname=histsetname)
    hist_filler.book_2dtprofile_fill(histogram_name, \
                                              calc_neg_cb_eta,\
                                              calc_neg_cb_phi,\
                                              calc_cb_mass,\
                                              selections = base_selections_CB,\
                                              bins_x = eta_bin_options["nbins"],\
                                              range_low_x = eta_bin_options["etalow"],\
                                              range_high_x = eta_bin_options["etahigh"],\
                                              xlabel = "#eta_{#mu}",\
                                              bins_y=phi_bin_options["nbins"],\
                                              range_low_y=phi_bin_options["philow"],\
                                              range_high_y=phi_bin_options["phihigh"],\
                                              ylabel = "#phi_{#mu}",\
                                              zlabel="<M_{#mu#mu}> [Gev]",\
                                              error_option="")

    histogram_name = histogram_name_base.format(charge="Pos", count=i, location="MS", histsetname=histsetname)
    hist_filler.book_2dtprofile_fill(histogram_name, \
                                              calc_pos_cb_eta,\
                                              calc_pos_cb_phi,\
                                              calc_cb_mass,\
                                              selections = base_selections_MS,\
                                              bins_x = eta_bin_options["nbins"],\
                                              range_low_x = eta_bin_options["etalow"],\
                                              range_high_x = eta_bin_options["etahigh"],\
                                              xlabel = "#eta_{#mu}",\
                                              bins_y=phi_bin_options["nbins"],\
                                              range_low_y=phi_bin_options["philow"],\
                                              range_high_y=phi_bin_options["phihigh"],\
                                              ylabel = "#phi_{#mu}",\
                                              zlabel="<M_{#mu#mu}> [Gev]",\
                                              error_option="")

    histogram_name = histogram_name_base.format(charge="Neg", count=i, location="MS", histsetname=histsetname)
    hist_filler.book_2dtprofile_fill(histogram_name, \
                                              calc_neg_cb_eta,\
                                              calc_neg_cb_phi,\
                                              calc_cb_mass,\
                                              selections = base_selections_MS,\
                                              bins_x = eta_bin_options["nbins"],\
                                              range_low_x = eta_bin_options["etalow"],\
                                              range_high_x = eta_bin_options["etahigh"],\
                                              xlabel = "#eta_{#mu}",\
                                              bins_y=phi_bin_options["nbins"],\
                                              range_low_y=phi_bin_options["philow"],\
                                              range_high_y=phi_bin_options["phihigh"],\
                                              ylabel = "#phi_{#mu}",\
                                              zlabel="<M_{#mu#mu}> [Gev]",\
                                              error_option="")


    #book a tprofile of the average mass
    histogram_name_base = "{histsetname}_{charge}_{location}_LeadingAverageMassProfile_{count}"
    histogram_name = histogram_name_base.format(charge="Pos", count=i, location="ID", histsetname=histsetname)
    hist_filler.book_2dtprofile_fill(histogram_name, \
                                              calc_leading_id_eta,\
                                              calc_leading_id_phi,\
                                              calc_id_mass,\
                                              selections = base_selections_ID + [sel_pos_leading_id],\
                                              bins_x = eta_bin_options["nbins"],\
                                              range_low_x = eta_bin_options["etalow"],\
                                              range_high_x = eta_bin_options["etahigh"],\
                                              xlabel = "#eta_{#mu}^{+Lead}",\
                                              bins_y=phi_bin_options["nbins"],\
                                              range_low_y=phi_bin_options["philow"],\
                                              range_high_y=phi_bin_options["phihigh"],\
                                              ylabel = "#phi_{#mu}^{+Lead}",\
                                              zlabel="<M_{#mu#mu}> [Gev]",\
                                              error_option="")

    #book a tprofile of the average mass
    histogram_name = histogram_name_base.format(charge="Neg", count=i, location="ID", histsetname=histsetname)
    hist_filler.book_2dtprofile_fill(histogram_name, \
                                              calc_leading_id_eta,\
                                              calc_leading_id_phi,\
                                              calc_id_mass,\
                                              selections = base_selections_ID + [sel_neg_leading_id],\
                                              bins_x = eta_bin_options["nbins"],\
                                              range_low_x = eta_bin_options["etalow"],\
                                              range_high_x = eta_bin_options["etahigh"],\
                                              xlabel = "#eta_{#mu}^{-Lead}",\
                                              bins_y=phi_bin_options["nbins"],\
                                              range_low_y=phi_bin_options["philow"],\
                                              range_high_y=phi_bin_options["phihigh"],\
                                              ylabel = "#phi_{#mu}^{-Lead}",\
                                              zlabel="<M_{#mu#mu}> [Gev]",\
                                              error_option="")



    for i, (phi_bin_lo, phi_bin_high) in enumerate(zip(phi_bins[:-1], phi_bins[1:])):
        phi_selection_pos_id = create_selection_function(range_selection_function, ["Pos_ID_Phi"], "Pos_ID_Phi", phi_bin_lo, phi_bin_high)
        phi_selection_neg_id = create_selection_function(range_selection_function, ["Neg_ID_Phi"], "Neg_ID_Phi", phi_bin_lo, phi_bin_high)
        phi_selection_pos_cb = create_selection_function(range_selection_function, ["Pos_CB_Phi"], "Pos_CB_Phi", phi_bin_lo, phi_bin_high)
        phi_selection_neg_cb = create_selection_function(range_selection_function, ["Neg_CB_Phi"], "Neg_CB_Phi", phi_bin_lo, phi_bin_high)
        #book tprofile histograms in each bin

        #book a tprofile of the average mass
        histogram_name_base = "{histsetname}_{charge}_{location}_AverageMassProfile_Phi_{count}"
        histogram_name = histogram_name_base.format(charge="Pos", count=i, location="ID", histsetname=histsetname)
        hist_filler.book_tprofile_fill(histogram_name, \
                                              calc_pos_id_eta,\
                                              calc_id_mass,\
                                              selections = base_selections_ID+[phi_selection_pos_id],\
                                              bins = eta_ID_bin_options["nbins"],\
                                              range_low = eta_ID_bin_options["etalow"],\
                                              range_high = eta_ID_bin_options["etahigh"],\
                                              xlabel = "#eta_{#mu}",\
                                              ylabel="<M_{#mu#mu}> [Gev]")

        histogram_name = histogram_name_base.format(charge="Neg", count=i, location="ID", histsetname=histsetname)
        hist_filler.book_tprofile_fill(histogram_name, \
                                              calc_neg_id_eta,\
                                              calc_id_mass,\
                                              selections = base_selections_ID+[phi_selection_neg_id],\
                                              bins = eta_ID_bin_options["nbins"],\
                                              range_low = eta_ID_bin_options["etalow"],\
                                              range_high = eta_ID_bin_options["etahigh"],\
                                              xlabel = "#eta_{#mu}",\
                                              ylabel="<M_{#mu#mu}> [Gev]")

        #book a tprofile of the average mass
        histogram_name = histogram_name_base.format(charge="Pos", count=i, location="CB", histsetname=histsetname)
        hist_filler.book_tprofile_fill(histogram_name, \
                                              calc_pos_cb_eta,\
                                              calc_cb_mass,\
                                              selections = base_selections_CB+[phi_selection_pos_cb],\
                                              bins = eta_bin_options["nbins"],\
                                              range_low = eta_bin_options["etalow"],\
                                              range_high = eta_bin_options["etahigh"],\
                                              xlabel = "#eta_{#mu}",\
                                              ylabel="<M_{#mu#mu}> [Gev]")

        histogram_name = histogram_name_base.format(charge="Neg", count=i, location="CB", histsetname=histsetname)
        hist_filler.book_tprofile_fill(histogram_name, \
                                              calc_neg_cb_eta,\
                                              calc_cb_mass,\
                                              selections = base_selections_CB+[phi_selection_neg_cb],\
                                              bins = eta_bin_options["nbins"],\
                                              range_low = eta_bin_options["etalow"],\
                                              range_high = eta_bin_options["etahigh"],\
                                              ylabel="<M_{#mu#mu}> [Gev]")


    for i, (pt_bin_lo, pt_bin_high) in enumerate(zip(pt_bins[:-1], pt_bins[1:])):
        pt_selection_pos_id = create_selection_function(range_selection_function, ["Pos_ID_Pt"], "Pos_ID_Pt", pt_bin_lo, pt_bin_high)
        pt_selection_neg_id = create_selection_function(range_selection_function, ["Neg_ID_Pt"], "Neg_ID_Pt", pt_bin_lo, pt_bin_high)
        pt_selection_pos_cb = create_selection_function(range_selection_function, ["Pos_CB_Pt"], "Pos_CB_Pt", pt_bin_lo, pt_bin_high)
        pt_selection_neg_cb = create_selection_function(range_selection_function, ["Neg_CB_Pt"], "Neg_CB_Pt", pt_bin_lo, pt_bin_high)
        #correction_ID = SagittaBiasCorrection([],  calc_pos_id_eta, calc_neg_id_eta, calc_pos_id_phi, calc_neg_id_phi, pos_selections = [pt_selection_pos_id], neg_selections = [pt_selection_neg_id], flavour = "ID",)
        #correction_CB = SagittaBiasCorrection([], calc_pos_cb_eta, calc_neg_cb_eta, calc_pos_cb_phi, calc_neg_cb_phi, pos_selections = [pt_selection_pos_cb], neg_selections = [pt_selection_neg_cb], flavour = "CB")


        #book a tprofile of the average mass
        histogram_name_base = "{histsetname}_{charge}_{location}_AverageMassProfile_{count}"
        histogram_name = histogram_name_base.format(charge="Pos", count=i, location="ID", histsetname=histsetname)
        hist_filler.book_2dtprofile_fill(histogram_name, \
                                              calc_pos_id_eta,\
                                              calc_pos_id_phi,\
                                              calc_id_mass,\
                                              selections = base_selections_ID+[pt_selection_pos_id],\
                                              bins_x = eta_ID_bin_options["nbins"],\
                                              range_low_x = eta_ID_bin_options["etalow"],\
                                              range_high_x = eta_ID_bin_options["etahigh"],\
                                              xlabel = "#eta_{#mu}",\
                                              bins_y=phi_bin_options["nbins"],\
                                              range_low_y=phi_bin_options["philow"],\
                                              range_high_y=phi_bin_options["phihigh"],\
                                              ylabel = "#phi_{#mu}",\
                                              zlabel="<M_{#mu#mu}> [Gev]",\
                                              error_option="")

        histogram_name = histogram_name_base.format(charge="Neg", count=i, location="ID", histsetname=histsetname)
        hist_filler.book_2dtprofile_fill(histogram_name, \
                                              calc_neg_id_eta,\
                                              calc_neg_id_phi,\
                                              calc_id_mass,\
                                              selections = base_selections_ID+[pt_selection_neg_id],\
                                              bins_x = eta_ID_bin_options["nbins"],\
                                              range_low_x = eta_ID_bin_options["etalow"],\
                                              range_high_x = eta_ID_bin_options["etahigh"],\
                                              xlabel = "#eta_{#mu}",\
                                              bins_y=phi_bin_options["nbins"],\
                                              range_low_y=phi_bin_options["philow"],\
                                              range_high_y=phi_bin_options["phihigh"],\
                                              ylabel = "#phi_{#mu}",\
                                              zlabel="<M_{#mu#mu}> [Gev]",\
                                              error_option="")

        #book a tprofile of the average mass
        histogram_name = histogram_name_base.format(charge="Pos", count=i, location="CB", histsetname=histsetname)
        hist_filler.book_2dtprofile_fill(histogram_name, \
                                              calc_pos_cb_eta,\
                                              calc_pos_cb_phi,\
                                              calc_cb_mass,\
                                              selections = base_selections_CB+[pt_selection_pos_cb],\
                                              bins_x = eta_bin_options["nbins"],\
                                              range_low_x = eta_bin_options["etalow"],\
                                              range_high_x = eta_bin_options["etahigh"],\
                                              xlabel = "#eta_{#mu}",\
                                              bins_y=phi_bin_options["nbins"],\
                                              range_low_y=phi_bin_options["philow"],\
                                              range_high_y=phi_bin_options["phihigh"],\
                                              ylabel = "#phi_{#mu}",\
                                              zlabel="<M_{#mu#mu}> [Gev]",\
                                              error_option="")

        histogram_name = histogram_name_base.format(charge="Neg", count=i, location="CB", histsetname=histsetname)
        hist_filler.book_2dtprofile_fill(histogram_name, \
                                              calc_neg_cb_eta,\
                                              calc_neg_cb_phi,\
                                              calc_cb_mass,\
                                              selections = base_selections_CB+[pt_selection_neg_cb],\
                                              bins_x = eta_bin_options["nbins"],\
                                              range_low_x = eta_bin_options["etalow"],\
                                              range_high_x = eta_bin_options["etahigh"],\
                                              xlabel = "#eta_{#mu}",\
                                              bins_y=phi_bin_options["nbins"],\
                                              range_low_y=phi_bin_options["philow"],\
                                              range_high_y=phi_bin_options["phihigh"],\
                                              ylabel = "#phi_{#mu}",\
                                              zlabel="<M_{#mu#mu}> [Gev]",\
                                              error_option="")

        histogram_name_base = "{histsetname}_{charge}_{location}_Mass_Histogram_{count}"
        histogram_name = histogram_name_base.format(charge="Pos", count=i, location="ID", histsetname=histsetname)
        hist_filler.book_histogram_fill(histogram_name,\
                                         calc_id_mass,\
                                         selections = [pt_selection_pos_id],\
                                         bins = 100,\
                                         range_low = 91.2-12.0,\
                                         range_high = 91.2+12.0,\
                                         xlabel ='M_{#mu#mu}^{varname} [GeV]',\
                                         ylabel = 'Number Events')

        histogram_name = histogram_name_base.format(charge="Neg", count=i, location="ID", histsetname=histsetname)
        hist_filler.book_histogram_fill(histogram_name,\
                                         calc_id_mass,\
                                         selections = [pt_selection_neg_id],\
                                         bins = 100,\
                                         range_low = 91.2-12.0,\
                                         range_high = 91.2+12.0,\
                                         xlabel ='M_{#mu#mu}^{varname} [GeV]',\
                                         ylabel = 'Number Events')

        histogram_name = histogram_name_base.format(charge="Pos", count=i, location="CB", histsetname=histsetname)
        hist_filler.book_histogram_fill(histogram_name,\
                                         calc_cb_mass,\
                                         selections = [pt_selection_pos_cb],\
                                         bins = 100,\
                                         range_low = 91.2-12.0,\
                                         range_high = 91.2+12.0,\
                                         xlabel ='M_{#mu#mu}^{varname} [GeV]',\
                                         ylabel = 'Number Events')

        histogram_name = histogram_name_base.format(charge="Neg", count=i, location="CB", histsetname=histsetname)
        hist_filler.book_histogram_fill(histogram_name,\
                                         calc_cb_mass,\
                                         selections = [pt_selection_neg_cb],\
                                         bins = 100,\
                                         range_low = 91.2-12.0,\
                                         range_high = 91.2+12.0,\
                                         xlabel ='M_{#mu#mu}^{varname} [GeV]',\
                                         ylabel = 'Number Events')


#This is a script that fills the histograms for
def fill_histograms(hist_filler, output_filename):
    from selections import sel_small_weight, sel_z_selection_cb, sel_z_selection_id, sel_z_selection_me
    hist_filler.apply_selection_for_channel("MCSherpa", [sel_small_weight])
    hist_filler.apply_selection_for_channel("MCSherpa1516", [sel_small_weight])
    hist_filler.apply_selection_for_channel("MCSherpa17", [sel_small_weight])
    hist_filler.apply_selection_for_channel("MCSherpa18", [sel_small_weight])
    hist_filler.apply_selection_for_channel("__ALL__", [sel_unprescaled_trigger, sel_opp_charge])

    for varname, var in zip(["ID", "CB", "ME"], [calc_id_mass, calc_cb_mass, calc_me_mass]):
        histogram_name = "{}_mass".format(varname)
        variable_name_for_selection = "Pair_{}_Mass".format(varname)
        hist_filler.book_histogram_fill(histogram_name,\
                                    var,\
                                    selections = [],\
                                    bins = 200,\
                                    range_low = 91.2-12.0,\
                                    range_high = 91.2+12.0,\
                                    xlabel ='M_{#mu#mu}^{varname} [GeV]',\
                                    ylabel = 'Number Events')



    '''
    binnings = []
    this_binning = {}
    this_binning["name"] = "coarsest"
    this_binning["EtaMS"] = {"nbins": 12, "etalow":-2.7, "etahigh":+2.7}
    this_binning["EtaID"] = {"nbins": 12, "etalow":-2.5, "etahigh":+2.5}
    this_binning["Phi"] = {"nbins": 8, "philow":-3.142, "phihigh":+3.142}
    binnings.append(this_binning)

    this_binning = {}
    this_binning["name"] = "finer"
    this_binning["EtaMS"] = {"nbins": 27, "etalow":-2.7, "etahigh":+2.7}
    this_binning["EtaID"] = {"nbins": 25, "etalow":-2.5, "etahigh":+2.5}
    this_binning["Phi"] = {"nbins": 16, "philow":-3.142, "phihigh":+3.142}
    binnings.append(this_binning)

    this_binning = {}
    this_binning["name"] = "finest"
    this_binning["EtaMS"] = {"nbins": 27, "etalow":-2.7, "etahigh":+2.7}
    this_binning["EtaID"] = {"nbins": 25, "etalow":-2.5, "etahigh":+2.5}
    this_binning["Phi"] = {"nbins": 32, "philow":-3.142, "phihigh":+3.142}
    binnings.append(this_binning)

    for binning in binnings:
        book_histograms(hist_filler, binning["EtaID"], binning["EtaMS"], binning["Phi"], binning["name"])
    '''


    mass_ID = "Pair_ID_Mass"
    mass_CB = "Pair_CB_Mass"
    mass_ME = "Pair_ME_Mass"
    mass_selZ_func_ID = create_selection_function(range_selection_function, [mass_ID], mass_ID, 91.2 - 12.0, 91.2 + 12.0)
    mass_selZ_func_CB = create_selection_function(range_selection_function, [mass_CB], mass_CB, 91.2 - 12.0, 91.2 + 12.0)
    mass_selZ_func_ME = create_selection_function(range_selection_function, [mass_ME], mass_ME, 91.2 - 12.0, 91.2 + 12.0)

    mass_selZ_func_ID_LucasBin = create_selection_function(range_selection_function, [mass_ID], mass_ID, 91.0 - 10.0, 91.0 + 10.0)
    mass_selZ_func_ME_LucasBin = create_selection_function(range_selection_function, [mass_ME], mass_ME, 91.0 - 10.0, 91.0 + 10.0)
    mass_selZ_func_CB_LucasBin = create_selection_function(range_selection_function, [mass_CB], mass_CB, 91.0 - 10.0, 91.0 + 10.0)

    mass_selJPSI_func_ID = create_selection_function(range_selection_function, [mass_ID], mass_ID, 2.8, 3.4)
    mass_selJPSI_func_CB = create_selection_function(range_selection_function, [mass_CB], mass_CB, 2.8, 3.4)
    mass_selJPSI_func_ME = create_selection_function(range_selection_function, [mass_ME], mass_ME, 2.8, 3.4)

    from variables import calc_cos_theta_star_id, calc_cos_theta_star_ms, calc_cos_theta_star_me, calc_cos_theta_star_cb
    from variables import sel_forward_id, sel_backward_id, sel_forward_me, sel_backward_me, sel_forward_cb, sel_backward_cb

    hist_filler.book_histogram_fill("WeightVariable_ID",\
                                     calc_weight_var,\
                                     selections = [mass_selZ_func_ID],\
                                     bins=200,\
                                     range_low=-100.0,\
                                     range_high=100.0,\
                                     xlabel="Event Weight",\
                                     ylabel="Number of Events")

    hist_filler.book_histogram_fill("WeightVariable_ME",\
                                     calc_weight_var,\
                                     selections = [mass_selZ_func_ME],\
                                     bins=200,\
                                     range_low=-100.0,\
                                     range_high=100.0,\
                                     xlabel="Event Weight",\
                                     ylabel="Number of Events")

    from variables import calc_pair_id_pt, calc_pair_me_pt

    hist_filler.book_histogram_fill("Pair_ID_Pt",\
                                     calc_pair_id_pt,\
                                     selections = [mass_selZ_func_ID],\
                                     bins=100,\
                                     range_low=0.0,\
                                     range_high=300.0,\
                                     xlabel="P_T",\
                                     ylabel="Number of Events")

    hist_filler.book_histogram_fill("Pair_ME_Pt",\
                                     calc_pair_me_pt,\
                                     selections = [mass_selZ_func_ME],\
                                     bins=100,\
                                     range_low=0.0,\
                                     range_high=300.0,\
                                     xlabel="P_T [GeV]",\
                                     ylabel="Number of Events")

    #book some tprofile histograms to study the average mass in bins of abs eta, phi, and both
    #fill_2d_tprofile_histograms(self, histogram_name, data, variable_x, variable_y, variable_z, selections = [], bins_x = 1, range_low_x = 0.000001, range_high_x=1. - 0.00001,  xlabel ="", bins_y=1, range_low_y=0.000001, range_high_y=1. - 0.00001, ylabel = "", zlabel="", error_option="")
    from variables import calc_leading_id_eta, calc_leading_id_phi, calc_leading_me_eta, calc_leading_me_phi, calc_leading_cb_eta, calc_leading_cb_phi
    from variables import calc_leading_id_abs_eta, calc_leading_me_abs_eta, calc_leading_cb_abs_eta
    hist_filler.book_2dtprofile_fill("2DAverageMassBinnedID",\
                                     calc_leading_id_eta,\
                                     calc_leading_id_phi,\
                                     calc_id_mass,\
                                     selections = [mass_selZ_func_ID],\
                                     bins_x = 20,\
                                     range_low_x = -2.5,\
                                     range_high_x = 2.5,\
                                     bins_y = 20,\
                                     range_low_y = -3.14,\
                                     range_high_y = 3.14,\
                                     xlabel = "#eta^{ID}",\
                                     ylabel = "#phi^{ID}")


    hist_filler.book_2dtprofile_fill("2DAverageMassBinnedME",\
                                     calc_leading_me_eta,\
                                     calc_leading_me_phi,\
                                     calc_me_mass,\
                                     selections = [mass_selZ_func_ME],\
                                     bins_x = 20,\
                                     range_low_x = -2.7,\
                                     range_high_x = 2.7,\
                                     bins_y = 20,\
                                     range_low_y = -3.14,\
                                     range_high_y = 3.14,\
                                     xlabel = "#eta^{ME}",\
                                     ylabel = "#phi^{ME}")

    hist_filler.book_2dtprofile_fill("2DAverageMassBinnedCB",\
                                     calc_leading_cb_eta,\
                                     calc_leading_cb_phi,\
                                     calc_cb_mass,\
                                     selections = [mass_selZ_func_CB],\
                                     bins_x = 20,\
                                     range_low_x = -2.5,\
                                     range_high_x = 2.5,\
                                     bins_y = 20,\
                                     range_low_y = -3.14,\
                                     range_high_y = 3.14,\
                                     xlabel = "#eta^{CB}",\
                                     ylabel = "#phi^{CB}")

    hist_filler.book_tprofile_fill("AverageMassBinnedID",\
                                     calc_leading_id_eta,\
                                     calc_id_mass,\
                                     selections = [mass_selZ_func_ID],\
                                     bins = 20,\
                                     range_low = -2.5,\
                                     range_high = 2.5,\
                                     xlabel = "#eta^{ID}")

    hist_filler.book_tprofile_fill("AverageMassBinnedME",\
                                     calc_leading_me_eta,\
                                     calc_me_mass,\
                                     selections = [mass_selZ_func_ME],\
                                     bins = 20,\
                                     range_low = -2.7,\
                                     range_high = 2.7,\
                                     xlabel = "#eta^{ME}")

    hist_filler.book_tprofile_fill("AverageMassBinnedCB",\
                                     calc_leading_cb_eta,\
                                     calc_cb_mass,\
                                     selections = [mass_selZ_func_CB],\
                                     bins = 20,\
                                     range_low = -2.5,\
                                     range_high = 2.5,\
                                     xlabel = "#eta^{CB}")


    hist_filler.book_tprofile_fill("AverageMassBinnedID_abseta",\
                                     calc_leading_id_abs_eta,\
                                     calc_id_mass,\
                                     selections = [mass_selZ_func_ID],\
                                     bins = 20,\
                                     range_low = 0.0,\
                                     range_high = 2.5,\
                                     xlabel = "|#eta^{ID}|")

    hist_filler.book_tprofile_fill("AverageMassBinnedME_abseta",\
                                     calc_leading_me_abs_eta,\
                                     calc_me_mass,\
                                     selections = [mass_selZ_func_ME],\
                                     bins = 20,\
                                     range_low = 0.0,\
                                     range_high = 2.7,\
                                     xlabel = "|#eta^{ME}|")

    hist_filler.book_tprofile_fill("AverageMassBinnedCB_abseta",\
                                     calc_leading_cb_abs_eta,\
                                     calc_cb_mass,\
                                     selections = [mass_selZ_func_CB],\
                                     bins = 20,\
                                     range_low = 0.0,\
                                     range_high = 2.5,\
                                     xlabel = "|#eta^{CB}|")

    #make mean mass histograms for ID, ME and CB Tracks
    histogram_name = "MeanMassProfile_ID"
    hist_filler.book_tprofile_fill(histogram_name,\
                                         calc_leading_id_eta,\
                                         calc_id_mass,\
                                         selections = [mass_selZ_func_ID],\
                                         bins = 25,\
                                         range_low = -2.5,\
                                         range_high = 2.5,\
                                         xlabel ='#eta^{ID} [GeV]',\
                                         ylabel = '<M_{\mu\mu}> [GeV]')

    #make mean mass histograms for ME, ME and CB Tracks
    histogram_name = "MeanMassProfile_ME"
    hist_filler.book_tprofile_fill(histogram_name,\
                                         calc_leading_me_eta,\
                                         calc_me_mass,\
                                         selections = [mass_selZ_func_ME],\
                                         bins = 27,\
                                         range_low = -2.7,\
                                         range_high = 2.7,\
                                         xlabel ='#eta^{ME} [GeV]',\
                                         ylabel = '<M_{\mu\mu}> [GeV]')

    #make mean mass histograms for CB, CB and CB Tracks
    histogram_name = "MeanMassProfile_CB"
    hist_filler.book_tprofile_fill(histogram_name,\
                                         calc_leading_cb_eta,\
                                         calc_cb_mass,\
                                         selections = [mass_selZ_func_CB],\
                                         bins = 27,\
                                         range_low = -2.7,\
                                         range_high = 2.7,\
                                         xlabel ='#eta^{CB} [GeV]',\
                                         ylabel = '<M_{\mu\mu}> [GeV]')

    #make mean mass histograms for ID, ME and CB Tracks
    histogram_name = "MassVsEta2D_ID_{identified}"
    hist_filler.book_2dhistogram_fill(histogram_name,\
                                         calc_leading_id_eta,\
                                         calc_id_mass,\
                                         selections = [mass_selZ_func_ID],\
                                         bins_x = 25,\
                                         range_low_x = -2.5,\
                                         range_high_x = 2.5,\
                                         bins_y = 200,\
                                         range_low_y = 91.2 - 12.0,\
                                         range_high_y = 91.2 + 12.0,\
                                         xlabel ='#eta^{ID} [GeV]',\
                                         ylabel = 'M_{\mu\mu} [GeV]')

    #make mean mass histograms for ME, ME and CB Tracks
    histogram_name = "MassVsEta2D_ME"
    hist_filler.book_2dhistogram_fill(histogram_name,\
                                         calc_leading_me_eta,\
                                         calc_me_mass,\
                                         selections = [mass_selZ_func_ME],\
                                         bins_x = 27,\
                                         range_low_x = -2.7,\
                                         range_high_x = 2.7,\
                                         bins_y = 200,\
                                         range_low_y = 91.2 - 12.0,\
                                         range_high_y = 91.2 + 12.0,\
                                         xlabel ='#eta^{ME} [GeV]',\
                                         ylabel = 'M_{\mu\mu} [GeV]')

    #make mean mass histograms for CB, CB and CB Tracks
    histogram_name = "MassVsEta2D_CB"
    hist_filler.book_2dhistogram_fill(histogram_name,\
                                         calc_leading_cb_eta,\
                                         calc_cb_mass,\
                                         selections = [mass_selZ_func_CB],\
                                         bins_x = 27,\
                                         range_low_x = -2.7,\
                                         range_high_x = 2.7,\
                                         bins_y = 200,\
                                         range_low_y = 91.2 - 12.0,\
                                         range_high_y = 91.2 + 12.0,\
                                         xlabel ='#eta^{CB} [GeV]',\
                                         ylabel = 'M_{\mu\mu} [GeV]')

    ### Lucas' Binning
    #make mean mass histograms for ID, ME and CB Tracks
    histogram_name = "MeanMassProfile_ID_LucasBin"
    hist_filler.book_tprofile_fill(histogram_name,\
                                         calc_leading_id_eta,\
                                         calc_id_mass,\
                                         selections = [mass_selZ_func_ID_LucasBin],\
                                         bins = 48,\
                                         range_low = -2.5,\
                                         range_high = 2.5,\
                                         xlabel ='#eta^{ID} [GeV]',\
                                         ylabel = '<M_{\mu\mu}> [GeV]')

    #make mean mass histograms for ME, ME and CB Tracks
    histogram_name = "MeanMassProfile_ME_LucasBin"
    hist_filler.book_tprofile_fill(histogram_name,\
                                         calc_leading_me_eta,\
                                         calc_me_mass,\
                                         selections = [mass_selZ_func_ME_LucasBin],\
                                         bins = 48,\
                                         range_low = -2.5,\
                                         range_high = 2.5,\
                                         xlabel ='#eta^{ME} [GeV]',\
                                         ylabel = '<M_{\mu\mu}> [GeV]')

    #make mean mass histograms for CB, CB and CB Tracks
    histogram_name = "MeanMassProfile_CB_LucasBin"
    hist_filler.book_tprofile_fill(histogram_name,\
                                         calc_leading_cb_eta,\
                                         calc_cb_mass,\
                                         selections = [mass_selZ_func_CB_LucasBin],\
                                         bins = 48,\
                                         range_low = -2.5,\
                                         range_high = 2.5,\
                                         xlabel ='#eta^{CB} [GeV]',\
                                         ylabel = '<M_{\mu\mu}> [GeV]')

    #make mean mass histograms for ID, ME and CB Tracks
    histogram_name = "MassVsEta2D_ID_{identified}_LucasBin"
    hist_filler.book_2dhistogram_fill(histogram_name,\
                                         calc_leading_id_eta,\
                                         calc_id_mass,\
                                         selections = [],\
                                         bins_x = 48,\
                                         range_low_x = -2.5,\
                                         range_high_x = 2.5,\
                                         bins_y = 400,\
                                         range_low_y = 75.0,\
                                         range_high_y = 105.0,\
                                         xlabel ='#eta^{ID} [GeV]',\
                                         ylabel = 'M_{\mu\mu} [GeV]')

    #make mean mass histograms for ME, ME and CB Tracks
    histogram_name = "MassVsEta2D_ME_LucasBin"
    hist_filler.book_2dhistogram_fill(histogram_name,\
                                         calc_leading_me_eta,\
                                         calc_me_mass,\
                                         selections = [],\
                                         bins_x = 48,\
                                         range_low_x = -2.5,\
                                         range_high_x = 2.5,\
                                         bins_y = 400,\
                                         range_low_y = 75.0,\
                                         range_high_y = 105.0,\
                                         xlabel ='#eta^{ME} [GeV]',\
                                         ylabel = 'M_{\mu\mu} [GeV]')

    #make mean mass histograms for CB, CB and CB Tracks
    histogram_name = "MassVsEta2D_CB_LucasBin"
    hist_filler.book_2dhistogram_fill(histogram_name,\
                                         calc_leading_cb_eta,\
                                         calc_cb_mass,\
                                         selections = [],\
                                         bins_x = 48,\
                                         range_low_x = -2.5,\
                                         range_high_x = 2.5,\
                                         bins_y = 400,\
                                         range_low_y = 75.0,\
                                         range_high_y = 105.0,\
                                         xlabel ='#eta^{CB} [GeV]',\
                                         ylabel = 'M_{\mu\mu} [GeV]')

    bins_pt = list(np.logspace(np.log10(5.0), np.log10(300.0), 30))
    bins_eta_id = list(np.linspace(-2.5, 2.5, 20))
    bins_eta_mecb = list(np.linspace(-2.7, 2.7, 20))
    bins_truth_over_reco = list(np.linspace(0.5, 1.5, 50))

    #make resolution histograms for ID, ME and CB Tracks

    from variables import\
    calc_pos_id_reco_over_truth_pt, calc_neg_id_reco_over_truth_pt,\
    calc_pos_me_reco_over_truth_pt, calc_neg_me_reco_over_truth_pt,\
    calc_pos_cb_reco_over_truth_pt, calc_neg_cb_reco_over_truth_pt,\
    calc_pos_truth_pt, calc_neg_truth_pt

    ##### ID PLOTS #########
    histogram_name = "3DEtaPtVsPtOverTruth_ID_Pos"
    hist_filler.book_3dhistogram_fill(histogram_name,\
                                         calc_pos_id_pt,\
                                         calc_pos_id_eta,\
                                         calc_pos_id_reco_over_truth_pt,\
                                         selections = [mass_selZ_func_ID],\
                                         bins_x = bins_pt,\
                                         bins_y = bins_eta_id,\
                                         bins_z = bins_truth_over_reco,\
                                         xlabel ='P_T^{ID} [GeV]',\
                                         ylabel ='#eta^{ID} ',\
                                         zlabel = 'P_T^{Reco}/P_T^{Truth}')

    histogram_name = "3DEtaPtVsPtOverTruth_ID_Neg"
    hist_filler.book_3dhistogram_fill(histogram_name,\
                                         calc_neg_id_pt,\
                                         calc_neg_id_eta,\
                                         calc_neg_id_reco_over_truth_pt,\
                                         selections = [mass_selZ_func_ID],\
                                         bins_x = bins_pt,\
                                         bins_y = bins_eta_id,\
                                         bins_z = bins_truth_over_reco,\
                                         xlabel ='P_T^{ID} [GeV]',\
                                         ylabel ='#eta^{ID} ',\
                                         zlabel = 'P_T^{Reco}/P_T^{Truth}')

    ##### ME PLOTS #########
    histogram_name = "3DEtaPtVsPtOverTruth_ME_Pos"
    hist_filler.book_3dhistogram_fill(histogram_name,\
                                         calc_pos_me_pt,\
                                         calc_pos_me_eta,\
                                         calc_pos_me_reco_over_truth_pt,\
                                         selections = [mass_selZ_func_ME],\
                                         bins_x = bins_pt,\
                                         bins_y = bins_eta_mecb,\
                                         bins_z = bins_truth_over_reco,\
                                         xlabel ='P_T^{ME} [GeV]',\
                                         ylabel ='#eta^{ME} ',\
                                         zlabel = 'P_T^{Reco}/P_T^{Truth}')

    histogram_name = "3DEtaPtVsPtOverTruth_ME_Neg"
    hist_filler.book_3dhistogram_fill(histogram_name,\
                                         calc_neg_me_pt,\
                                         calc_neg_me_eta,\
                                         calc_neg_me_reco_over_truth_pt,\
                                         selections = [mass_selZ_func_ME],\
                                         bins_x = bins_pt,\
                                         bins_y = bins_eta_mecb,\
                                         bins_z = bins_truth_over_reco,\
                                         xlabel ='P_T^{ME} [GeV]',\
                                         ylabel ='#eta^{ME} ',\
                                         zlabel = 'P_T^{Reco}/P_T^{Truth}')

    ##### CB PLOTS #########
    histogram_name = "3DEtaPtVsPtOverTruth_CB_Pos"
    hist_filler.book_3dhistogram_fill(histogram_name,\
                                         calc_pos_cb_pt,\
                                         calc_pos_cb_eta,\
                                         calc_pos_cb_reco_over_truth_pt,\
                                         selections = [mass_selZ_func_CB],\
                                         bins_x = bins_pt,\
                                         bins_y = bins_eta_mecb,\
                                         bins_z = bins_truth_over_reco,\
                                         xlabel ='P_T^{CB} [GeV]',\
                                         ylabel ='#eta^{CB} ',\
                                         zlabel = 'P_T^{Reco}/P_T^{Truth}')

    histogram_name = "3DEtaPtVsPtOverTruth_CB_Neg"
    hist_filler.book_3dhistogram_fill(histogram_name,\
                                         calc_neg_cb_pt,\
                                         calc_neg_cb_eta,\
                                         calc_neg_cb_reco_over_truth_pt,\
                                         selections = [mass_selZ_func_CB],\
                                         bins_x = bins_pt,\
                                         bins_y = bins_eta_mecb,\
                                         bins_z = bins_truth_over_reco,\
                                         xlabel ='P_T^{CB} [GeV]',\
                                         ylabel ='#eta^{CB} ',\
                                         zlabel = 'P_T^{Reco}/P_T^{Truth}')

    bins_pt = list(np.logspace(np.log10(5.0), np.log10(300.0), 30))
    bins_eta_id = list(np.linspace(-2.5, 2.5, 26))
    bins_eta_mecb = list(np.linspace(-2.7, 2.7, 28))
    bins_truth_over_reco = list(np.linspace(0.0, 2.0, 100))

    #make resolution histograms for ID, ME and CB Tracks

    from variables import\
    calc_pos_truth_pt, calc_neg_truth_pt

    ##### ID PLOTS #########
    histogram_name = "3DEtaPtVsPtOverTruth_ID_Pos_WIDER"
    hist_filler.book_3dhistogram_fill(histogram_name,\
                                         calc_pos_id_pt,\
                                         calc_pos_id_eta,\
                                         calc_pos_id_reco_over_truth_pt,\
                                         selections = [mass_selZ_func_ID],\
                                         bins_x = bins_pt,\
                                         bins_y = bins_eta_id,\
                                         bins_z = bins_truth_over_reco,\
                                         xlabel ='P_T^{ID} [GeV]',\
                                         ylabel ='#eta^{ID} ',\
                                         zlabel = 'P_T^{Reco}/P_T^{Truth}')

    histogram_name = "3DEtaPtVsPtOverTruth_ID_Neg_WIDER"
    hist_filler.book_3dhistogram_fill(histogram_name,\
                                         calc_neg_id_pt,\
                                         calc_neg_id_eta,\
                                         calc_neg_id_reco_over_truth_pt,\
                                         selections = [mass_selZ_func_ID],\
                                         bins_x = bins_pt,\
                                         bins_y = bins_eta_id,\
                                         bins_z = bins_truth_over_reco,\
                                         xlabel ='P_T^{ID} [GeV]',\
                                         ylabel ='#eta^{ID} ',\
                                         zlabel = 'P_T^{Reco}/P_T^{Truth}')

    ##### ME PLOTS #########
    histogram_name = "3DEtaPtVsPtOverTruth_ME_Pos_WIDER"
    hist_filler.book_3dhistogram_fill(histogram_name,\
                                         calc_pos_me_pt,\
                                         calc_pos_me_eta,\
                                         calc_pos_me_reco_over_truth_pt,\
                                         selections = [mass_selZ_func_ME],\
                                         bins_x = bins_pt,\
                                         bins_y = bins_eta_mecb,\
                                         bins_z = bins_truth_over_reco,\
                                         xlabel ='P_T^{ME} [GeV]',\
                                         ylabel ='#eta^{ME} ',\
                                         zlabel = 'P_T^{Reco}/P_T^{Truth}')

    histogram_name = "3DEtaPtVsPtOverTruth_ME_Neg_WIDER"
    hist_filler.book_3dhistogram_fill(histogram_name,\
                                         calc_neg_me_pt,\
                                         calc_neg_me_eta,\
                                         calc_neg_me_reco_over_truth_pt,\
                                         selections = [mass_selZ_func_ME],\
                                         bins_x = bins_pt,\
                                         bins_y = bins_eta_mecb,\
                                         bins_z = bins_truth_over_reco,\
                                         xlabel ='P_T^{ME} [GeV]',\
                                         ylabel ='#eta^{ME} ',\
                                         zlabel = 'P_T^{Reco}/P_T^{Truth}')

    ##### CB PLOTS #########
    histogram_name = "3DEtaPtVsPtOverTruth_CB_Pos_WIDER"
    hist_filler.book_3dhistogram_fill(histogram_name,\
                                         calc_pos_cb_pt,\
                                         calc_pos_cb_eta,\
                                         calc_pos_cb_reco_over_truth_pt,\
                                         selections = [mass_selZ_func_CB],\
                                         bins_x = bins_pt,\
                                         bins_y = bins_eta_mecb,\
                                         bins_z = bins_truth_over_reco,\
                                         xlabel ='P_T^{CB} [GeV]',\
                                         ylabel ='#eta^{CB} ',\
                                         zlabel = 'P_T^{Reco}/P_T^{Truth}')

    histogram_name = "3DEtaPtVsPtOverTruth_CB_Neg_WIDER"
    hist_filler.book_3dhistogram_fill(histogram_name,\
                                         calc_neg_cb_pt,\
                                         calc_neg_cb_eta,\
                                         calc_neg_cb_reco_over_truth_pt,\
                                         selections = [mass_selZ_func_CB],\
                                         bins_x = bins_pt,\
                                         bins_y = bins_eta_mecb,\
                                         bins_z = bins_truth_over_reco,\
                                         xlabel ='P_T^{CB} [GeV]',\
                                         ylabel ='#eta^{CB} ',\
                                         zlabel = 'P_T^{Reco}/P_T^{Truth}')

    from variables import\
    calc_pos_truth_pt, calc_neg_truth_pt

    ##### ID PLOTS #########
    histogram_name = "3DEtaTruthPtVsPtOverTruth_ID_Pos"
    hist_filler.book_3dhistogram_fill(histogram_name,\
                                         calc_pos_truth_pt,\
                                         calc_pos_id_eta,\
                                         calc_pos_id_reco_over_truth_pt,\
                                         selections = [mass_selZ_func_ID],\
                                         bins_x = bins_pt,\
                                         bins_y = bins_eta_id,\
                                         bins_z = bins_truth_over_reco,\
                                         xlabel ='P_T^{Truth} [GeV]',\
                                         ylabel ='#eta^{ID} ',\
                                         zlabel = 'P_T^{Reco}/P_T^{Truth}')

    histogram_name = "3DEtaTruthPtVsPtOverTruth_ID_Neg"
    hist_filler.book_3dhistogram_fill(histogram_name,\
                                         calc_neg_truth_pt,\
                                         calc_neg_id_eta,\
                                         calc_neg_id_reco_over_truth_pt,\
                                         selections = [mass_selZ_func_ID],\
                                         bins_x = bins_pt,\
                                         bins_y = bins_eta_id,\
                                         bins_z = bins_truth_over_reco,\
                                         xlabel ='P_T^{Truth} [GeV]',\
                                         ylabel ='#eta^{ID} ',\
                                         zlabel = 'P_T^{Reco}/P_T^{Truth}')

    ##### ME PLOTS #########
    histogram_name = "3DEtaTruthPtVsPtOverTruth_ME_Pos"
    hist_filler.book_3dhistogram_fill(histogram_name,\
                                         calc_pos_truth_pt,\
                                         calc_pos_me_eta,\
                                         calc_pos_me_reco_over_truth_pt,\
                                         selections = [mass_selZ_func_ME],\
                                         bins_x = bins_pt,\
                                         bins_y = bins_eta_mecb,\
                                         bins_z = bins_truth_over_reco,\
                                         xlabel ='P_T^{Truth} [GeV]',\
                                         ylabel ='#eta^{ME} ',\
                                         zlabel = 'P_T^{Reco}/P_T^{Truth}')

    histogram_name = "3DEtaTruthPtVsPtOverTruth_ME_Neg"
    hist_filler.book_3dhistogram_fill(histogram_name,\
                                         calc_neg_truth_pt,\
                                         calc_neg_me_eta,\
                                         calc_neg_me_reco_over_truth_pt,\
                                         selections = [mass_selZ_func_ME],\
                                         bins_x = bins_pt,\
                                         bins_y = bins_eta_mecb,\
                                         bins_z = bins_truth_over_reco,\
                                         xlabel ='P_T^{Truth} [GeV]',\
                                         ylabel ='#eta^{ME} ',\
                                         zlabel = 'P_T^{Reco}/P_T^{Truth}')

    ##### CB PLOTS #########
    histogram_name = "3DEtaTruthPtVsPtOverTruth_CB_Pos"
    hist_filler.book_3dhistogram_fill(histogram_name,\
                                         calc_pos_truth_pt,\
                                         calc_pos_cb_eta,\
                                         calc_pos_cb_reco_over_truth_pt,\
                                         selections = [mass_selZ_func_CB],\
                                         bins_x = bins_pt,\
                                         bins_y = bins_eta_mecb,\
                                         bins_z = bins_truth_over_reco,\
                                         xlabel ='P_T^{Truth} [GeV]',\
                                         ylabel ='#eta^{CB} ',\
                                         zlabel = 'P_T^{Reco}/P_T^{Truth}')

    histogram_name = "3DEtaTruthPtVsPtOverTruth_CB_Neg"
    hist_filler.book_3dhistogram_fill(histogram_name,\
                                         calc_neg_truth_pt,\
                                         calc_neg_cb_eta,\
                                         calc_neg_cb_reco_over_truth_pt,\
                                         selections = [mass_selZ_func_CB],\
                                         bins_x = bins_pt,\
                                         bins_y = bins_eta_mecb,\
                                         bins_z = bins_truth_over_reco,\
                                         xlabel ='P_T^{Truth} [GeV]',\
                                         ylabel ='#eta^{CB} ',\
                                         zlabel = 'P_T^{Reco}/P_T^{Truth}')

    bins_pt = list(np.logspace(np.log10(5.0), np.log10(300.0), 30))
    bins_eta_id = list(np.linspace(-2.5, 2.5, 20))
    bins_eta_mecb = list(np.linspace(-2.7, 2.7, 20))
    bins_truth_over_reco = list(np.linspace(0.0, 2.0, 1000))

    #make resolution histograms for ID, ME and CB Tracks

    from variables import\
    calc_pos_truth_pt, calc_neg_truth_pt

    ##### ID PLOTS #########
    histogram_name = "3DEtaTruthPtVsPtOverTruth_ID_Pos_WIDER"
    hist_filler.book_3dhistogram_fill(histogram_name,\
                                         calc_pos_truth_pt,\
                                         calc_pos_id_eta,\
                                         calc_pos_id_reco_over_truth_pt,\
                                         selections = [mass_selZ_func_ID],\
                                         bins_x = bins_pt,\
                                         bins_y = bins_eta_id,\
                                         bins_z = bins_truth_over_reco,\
                                         xlabel ='P_T^{Truth} [GeV]',\
                                         ylabel ='#eta^{ID} ',\
                                         zlabel = 'P_T^{Reco}/P_T^{Truth}')

    histogram_name = "3DEtaTruthPtVsPtOverTruth_ID_Neg_WIDER"
    hist_filler.book_3dhistogram_fill(histogram_name,\
                                         calc_neg_truth_pt,\
                                         calc_neg_id_eta,\
                                         calc_neg_id_reco_over_truth_pt,\
                                         selections = [mass_selZ_func_ID],\
                                         bins_x = bins_pt,\
                                         bins_y = bins_eta_id,\
                                         bins_z = bins_truth_over_reco,\
                                         xlabel ='P_T^{Truth} [GeV]',\
                                         ylabel ='#eta^{ID} ',\
                                         zlabel = 'P_T^{Reco}/P_T^{Truth}')

    ##### ME PLOTS #########
    histogram_name = "3DEtaTruthPtVsPtOverTruth_ME_Pos_WIDER"
    hist_filler.book_3dhistogram_fill(histogram_name,\
                                         calc_pos_truth_pt,\
                                         calc_pos_me_eta,\
                                         calc_pos_me_reco_over_truth_pt,\
                                         selections = [mass_selZ_func_ME],\
                                         bins_x = bins_pt,\
                                         bins_y = bins_eta_mecb,\
                                         bins_z = bins_truth_over_reco,\
                                         xlabel ='P_T^{Truth} [GeV]',\
                                         ylabel ='#eta^{ME} ',\
                                         zlabel = 'P_T^{Reco}/P_T^{Truth}')

    histogram_name = "3DEtaTruthPtVsPtOverTruth_ME_Neg_WIDER"
    hist_filler.book_3dhistogram_fill(histogram_name,\
                                         calc_neg_truth_pt,\
                                         calc_neg_me_eta,\
                                         calc_neg_me_reco_over_truth_pt,\
                                         selections = [mass_selZ_func_ME],\
                                         bins_x = bins_pt,\
                                         bins_y = bins_eta_mecb,\
                                         bins_z = bins_truth_over_reco,\
                                         xlabel ='P_T^{Truth} [GeV]',\
                                         ylabel ='#eta^{ME} ',\
                                         zlabel = 'P_T^{Reco}/P_T^{Truth}')

    ##### CB PLOTS #########
    histogram_name = "3DEtaTruthPtVsPtOverTruth_CB_Pos_WIDER"
    hist_filler.book_3dhistogram_fill(histogram_name,\
                                         calc_pos_truth_pt,\
                                         calc_pos_cb_eta,\
                                         calc_pos_cb_reco_over_truth_pt,\
                                         selections = [mass_selZ_func_CB],\
                                         bins_x = bins_pt,\
                                         bins_y = bins_eta_mecb,\
                                         bins_z = bins_truth_over_reco,\
                                         xlabel ='P_T^{Truth} [GeV]',\
                                         ylabel ='#eta^{CB} ',\
                                         zlabel = 'P_T^{Reco}/P_T^{Truth}')

    histogram_name = "3DEtaTruthPtVsPtOverTruth_CB_Neg_WIDER"
    hist_filler.book_3dhistogram_fill(histogram_name,\
                                         calc_neg_truth_pt,\
                                         calc_neg_cb_eta,\
                                         calc_neg_cb_reco_over_truth_pt,\
                                         selections = [mass_selZ_func_CB],\
                                         bins_x = bins_pt,\
                                         bins_y = bins_eta_mecb,\
                                         bins_z = bins_truth_over_reco,\
                                         xlabel ='P_T^{Truth} [GeV]',\
                                         ylabel ='#eta^{CB} ',\
                                         zlabel = 'P_T^{Reco}/P_T^{Truth}')




    for sel_id, sel_me, sel_cb, name in zip([[sel_forward_id, sel_min_fifteen_id_pts], [sel_backward_id, sel_min_fifteen_id_pts]],\
                                    [[sel_forward_me, sel_min_fifteen_me_pts], [sel_backward_me, sel_min_fifteen_me_pts]],\
                                    [[sel_forward_cb, sel_min_fifteen_cb_pts], [sel_backward_cb, sel_min_fifteen_cb_pts]],\
                                    ["forward", "backward"]):
        #make invariant mass histograms for ID tracks
        histogram_name_base = "MassSpectrum_ID_{identified}"
        histogram_name = histogram_name_base.format(identified = name)
        hist_filler.book_histogram_fill(histogram_name,\
                                             calc_id_mass,\
                                             selections = sel_id,\
                                             bins = 100,\
                                             range_low = 91.2-12.0,\
                                             range_high = 91.2+12.0,\
                                             xlabel ='M_{#mu#mu}^{ID} [GeV]',\
                                             ylabel = 'Number Events')

        histogram_name_base = "MassSpectrum_ME_{identified}"
        histogram_name = histogram_name_base.format(identified = name)
        hist_filler.book_histogram_fill(histogram_name,\
                                             calc_me_mass,\
                                             selections = sel_me,\
                                             bins = 100,\
                                             range_low = 91.2-12.0,\
                                             range_high = 91.2+12.0,\
                                             xlabel ='M_{#mu#mu}^{ME} [GeV]',\
                                             ylabel = 'Number Events')

        histogram_name_base = "MassSpectrum_CB_{identified}"
        histogram_name = histogram_name_base.format(identified = name)
        hist_filler.book_histogram_fill(histogram_name,\
                                             calc_cb_mass,\
                                             selections = sel_cb,\
                                             bins = 100,\
                                             range_low = 91.2-12.0,\
                                             range_high = 91.2+12.0,\
                                             xlabel ='M_{#mu#mu}^{CB} [GeV]',\
                                             ylabel = 'Number Events')


    for sel_id, sel_me, sel_cb, name in zip([[sel_pos_leading_id, sel_min_fifteen_id_pts], [sel_neg_leading_id, sel_min_fifteen_id_pts], []],\
                                    [[sel_pos_leading_me, sel_min_fifteen_me_pts], [sel_neg_leading_me, sel_min_fifteen_me_pts], []],\
                                    [[sel_pos_leading_cb, sel_min_fifteen_cb_pts], [sel_neg_leading_cb, sel_min_fifteen_cb_pts], []],\
                                    ["poslead", "neglead", "Inclusive"]):

        #I will come back and fix this

        varlist = \
        [\
         calc_leading_id_pt, calc_subleading_id_pt,\
         calc_leading_cb_pt, calc_subleading_cb_pt,\
         calc_leading_me_pt, calc_subleading_me_pt,\
         calc_leading_id_eta, calc_subleading_id_eta,\
         calc_leading_cb_eta, calc_subleading_cb_eta,\
         calc_leading_me_eta, calc_subleading_me_eta,\
         calc_leading_id_phi, calc_subleading_id_phi,\
         calc_leading_cb_phi, calc_subleading_cb_phi,\
         calc_leading_me_phi, calc_subleading_me_phi,\
        ]

        histnames = \
        [\
         "PT_Leading_ID", "PT_Subleading_ID",\
         "PT_Leading_CB", "PT_Subleading_CB",\
         "PT_Leading_ME", "PT_Subleading_ME",\
         "Eta_Leading_ID", "Eta_Subleading_ID",\
         "Eta_Leading_CB", "Eta_Subleading_CB",\
         "Eta_Leading_ME", "Eta_Subleading_ME",\
         "Phi_Leading_ID", "Phi_Subleading_ID",\
         "Phi_Leading_CB", "Phi_Subleading_CB",\
         "Phi_Leading_ME", "Phi_Subleading_ME",\
        ]

        x_ranges = \
        [\
         (5.0, 100.0), (5.0, 70.0),\
         (5.0, 100.0), (5.0, 70.0),\
         (5.0, 100.0), (5.0, 70.0),\
         (-2.5, 2.5), (-2.5, 2.5),\
         (-2.5, 2.5), (-2.5, 2.5),\
         (-2.7, 2.7), (-2.7, 2.7),\
         (-3.14, 3.14), (-3.14, +3.14),\
         (-3.14, 3.14), (-3.14, +3.14),\
         (-3.14, +3.14), (-3.14, +3.14),\
        ]

        nbins_all = \
        [\
         50, 50,\
         50, 50,\
         50, 50,\
         50, 50,\
         50, 50,\
         50, 50,\
         50, 50,\
         50, 50,\
         50, 50,\
        ]

        x_labels = \
        [\
         "P_{T}^{ID, Lead} [GeV]", "P_{T}^{ID, Sub} [GeV]",\
         "P_{T}^{CB, Lead} [GeV]", "P_{T}^{CB, Sub} [GeV]",\
         "P_{T}^{ME, Lead} [GeV]", "P_{T}^{ME, Sub} [GeV]",\
         "#eta^{ID, Lead}", "#eta^{ID, Sub}",\
         "#eta^{CB, Lead}", "#eta^{CB, Sub}",\
         "#eta^{ME, Lead}", "#eta^{ME, Sub}",\
         "#phi^{ID, Lead}", "#phi^{ID, Sub}",\
         "#phi^{CB, Lead}", "#phi^{CB, Sub}",\
         "#phi^{ME, Lead}", "#phi^{ME, Sub}",\
        ]

        from selections import sel_nom_delta_selection_id, sel_nom_delta_selection_me, sel_nom_delta_selection_cb
        for xvar, histname, x_range, x_label, nbins  in zip(varlist, histnames, x_ranges, x_labels, nbins_all):
            if "ID" in histname:
                base_sel = [sel_nom_delta_selection_id]
                sel = sel_id
            if "CB" in histname:
                base_sel = [sel_nom_delta_selection_cb]
                sel = sel_cb
            if "ME" in histname:
                base_sel = [sel_nom_delta_selection_me]
                sel = sel_me
            hist_filler.book_histogram_fill(histname + "_" + name,\
                                             xvar,\
                                             selections = sel + base_sel,\
                                             bins = nbins,\
                                             range_low = x_range[0],\
                                             range_high = x_range[1],\
                                             xlabel = x_label,\
                                             ylabel = 'Number Events')



        #make invariant mass histograms for ID tracks
        histogram_name_base = "MassSpectrum_ID_{identified}"
        histogram_name = histogram_name_base.format(identified = name)
        hist_filler.book_histogram_fill(histogram_name,\
                                             calc_id_mass,\
                                             selections = sel_id,\
                                             bins = 100,\
                                             range_low = 91.2-12.0,\
                                             range_high = 91.2+12.0,\
                                             xlabel ='M_{#mu#mu}^{ID} [GeV]',\
                                             ylabel = 'Number Events')

        #make invariant mass histograms for CB tracks
        histogram_name_base = "MassSpectrum_CB_{identified}"
        histogram_name = histogram_name_base.format(identified = name)
        hist_filler.book_histogram_fill(histogram_name,\
                                             calc_cb_mass,\
                                             selections = sel_cb,\
                                             bins = 100,\
                                             range_low = 91.2-12.0,\
                                             range_high = 91.2+12.0,\
                                             xlabel ='M_{#mu#mu}^{CB} [GeV]',\
                                             ylabel = 'Number Events')

        histogram_name_base = "MassSpectrum_ME_{identified}"
        histogram_name = histogram_name_base.format(identified = name)
        hist_filler.book_histogram_fill(histogram_name,\
                                             calc_me_mass,\
                                             selections = sel_me,\
                                             bins = 100,\
                                             range_low = 91.2-12.0,\
                                             range_high = 91.2+12.0,\
                                             xlabel ='M_{#mu#mu}^{ME} [GeV]',\
                                             ylabel = 'Number Events')

        histogram_name_base = "MassSpectrumJPSI_ID_{identified}"
        histogram_name = histogram_name_base.format(identified = name)
        hist_filler.book_histogram_fill(histogram_name,\
                                             calc_id_mass,\
                                             selections = sel_id,\
                                             bins = 100,\
                                             range_low = 2.8,\
                                             range_high = 3.4,\
                                             xlabel ='M_{#mu#mu}^{ID} [GeV]',\
                                             ylabel = 'Number Events')

        histogram_name_base = "MassSpectrumJPSI_ME_{identified}"
        histogram_name = histogram_name_base.format(identified = name)
        hist_filler.book_histogram_fill(histogram_name,\
                                             calc_me_mass,\
                                             selections = sel_me,\
                                             bins = 100,\
                                             range_low = 2.2,\
                                             range_high = 3.4,\
                                             xlabel ='M_{#mu#mu}^{ME} [GeV]',\
                                             ylabel = 'Number Events')

        histogram_name_base = "CosThetaStar_ID_{identified}"
        histogram_name = histogram_name_base.format(identified = name)
        hist_filler.book_histogram_fill(histogram_name,\
                                             calc_cos_theta_star_id,\
                                             selections = sel_id + [mass_selZ_func_ID, sel_nonzero_id_pts],\
                                             bins = 100,\
                                             range_low = -1.0,\
                                             range_high = 1.0,\
                                             xlabel ='cos#theta*_{ID}',\
                                             ylabel = 'Number Events')

        histogram_name_base = "CosThetaStar_CB_{cbentified}"
        histogram_name = histogram_name_base.format(cbentified = name)
        hist_filler.book_histogram_fill(histogram_name,\
                                             calc_cos_theta_star_cb,\
                                             selections = sel_cb + [mass_selZ_func_CB, sel_nonzero_cb_pts],\
                                             bins = 100,\
                                             range_low = -1.0,\
                                             range_high = 1.0,\
                                             xlabel ='cos#theta*_{CB}',\
                                             ylabel = 'Number Events')

        histogram_name_base = "CosThetaStar_ME_{identified}"
        histogram_name = histogram_name_base.format(identified = name)
        hist_filler.book_histogram_fill(histogram_name,\
                                             calc_cos_theta_star_me,\
                                             selections = sel_me + [mass_selZ_func_ME, sel_nonzero_me_pts],\
                                             bins = 100,\
                                             range_low = -1.0,\
                                             range_high = 1.0,\
                                             xlabel ='cos#theta*_{ME}',\
                                             ylabel = 'Number Events')


        histogram_name_base = "CosThetaStarJPSI_ID_{identified}"
        histogram_name = histogram_name_base.format(identified = name)
        hist_filler.book_histogram_fill(histogram_name,\
                                             calc_cos_theta_star_id,\
                                             selections = sel_id + [mass_selJPSI_func_ID],\
                                             bins = 100,\
                                             range_low = -1.0,\
                                             range_high = 1.0,\
                                             xlabel ='cos#theta*_{ID}',\
                                             ylabel = 'Number Events')

        histogram_name_base = "CosThetaStarJSPI_ME_{identified}"
        histogram_name = histogram_name_base.format(identified = name)
        hist_filler.book_histogram_fill(histogram_name,\
                                             calc_cos_theta_star_me,\
                                             selections = sel_me + [mass_selJPSI_func_ME],\
                                             bins = 100,\
                                             range_low = -1.0,\
                                             range_high = 1.0,\
                                             xlabel ='cos#theta*_{ME}',\
                                             ylabel = 'Number Events')

        '''
        from variables import calc_id_pt
        histogram_name_base = "PtSpectrum_{identified}"
        histogram_name = histogram_name_base.format(identified = name)
        hist_filler.book_histogram_fill(histogram_name,\
                                             calc_id_pt,\
                                             selections = [sel],\
                                             bins = 100,\
                                             range_low = 0.0,\
                                             range_high = 240.0,\
                                             xlabel ='{P_T}_{#mu#mu}^{ID} [GeV]',\
                                             ylabel = 'Number Events')
        '''

    histograms = hist_filler.DumpHistograms()
    output_file = ROOT.TFile(output_filename, "RECREATE")
    for histogram_name in histograms:
        write_histograms(histograms[histogram_name], output_file)


    output_file.Close()

    print("__Finished__")
