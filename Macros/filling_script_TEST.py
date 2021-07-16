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


    histograms = hist_filler.DumpHistograms()
    output_file = ROOT.TFile(output_filename, "RECREATE")
    for histogram_name in histograms:
        write_histograms(histograms[histogram_name], output_file)


    output_file.Close()

    print("__Finished__")
