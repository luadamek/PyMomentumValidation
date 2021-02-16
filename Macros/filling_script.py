from variables import calc_id_mass, calc_ms_mass, calc_cb_mass, calc_me_mass
from selections import range_selection_function
from histogram_filler import create_selection_function, write_histograms
import ROOT
from BiasCorrection import SagittaBiasCorrection
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
                      calc_pos_cb_phi, calc_neg_cb_phi,\
                      calc_leading_id_pt, calc_subleading_id_pt,\
                      calc_leading_me_pt, calc_subleading_me_pt,\
                      calc_leading_id_eta, calc_subleading_id_eta,\
                      calc_leading_me_eta, calc_subleading_me_eta,\
                      calc_leading_id_phi, calc_subleading_id_phi,\
                      calc_leading_me_phi, calc_subleading_me_phi

###################################################################
from selections import sel_pos_leading_id, sel_neg_leading_id
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
    histogram_name = histogram_name_base.format(count="Inclusive", location="MS", histsetname=histsetname)
    hist_filler.book_histogram_fill(histogram_name,\
                                         calc_ms_mass,\
                                         selections = [],\
                                         bins = 200,\
                                         range_low = 86.0-10.0,\
                                         range_high = 86.0+10.0,\
                                         xlabel ='M_{#mu#mu}^{MS} [GeV]',\
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

    mass_MS = calc_ms_mass
    mass_sel_func_ID = create_selection_function(range_selection_function, [mass_ID], mass_ID, 91.2 - 10.0, 91.2 + 10.0)
    mass_sel_func_CB = create_selection_function(range_selection_function, [mass_CB], mass_CB, 91.2 - 10.0, 91.2 + 10.0)
    mass_sel_func_MS = create_selection_function(range_selection_function, calc_ms_mass.branches, calc_ms_mass, 86.0 - 10.0, 86.0 + 10.0)
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

    from selections import sel_pos_leading_id, sel_neg_leading_id
    from selections import sel_pos_leading_me, sel_neg_leading_me
    from variables import calc_leading_id_pt, calc_leading_id_phi, calc_leading_id_eta

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
        phi_selection_pos_ms = create_selection_function(range_selection_function, ["Pos_MS_Phi"], "Pos_MS_Phi", phi_bin_lo, phi_bin_high)
        phi_selection_neg_ms = create_selection_function(range_selection_function, ["Neg_MS_Phi"], "Neg_MS_Phi", phi_bin_lo, phi_bin_high)
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

        #book a tprofile of the average mass
        histogram_name = histogram_name_base.format(charge="Pos", count=i, location="MS", histsetname=histsetname)
        hist_filler.book_2dtprofile_fill(histogram_name, \
                                              calc_pos_ms_eta,\
                                              calc_pos_ms_phi,\
                                              calc_ms_mass,\
                                              selections = base_selections_MS+[phi_selection_pos_ms],\
                                              bins_x = eta_bin_options["nbins"],\
                                              range_low_x = eta_bin_options["etalow"],\
                                              range_high_x = eta_bin_options["etahigh"],\
                                              xlabel = "#eta_{#mu}",\
                                              ylabel="<M_{#mu#mu}> [Gev]",\
                                              error_option="")

        histogram_name = histogram_name_base.format(charge="Neg", count=i, location="MS", histsetname=histsetname)
        hist_filler.book_2dtprofile_fill(histogram_name, \
                                              calc_neg_ms_eta,\
                                              calc_neg_ms_phi,\
                                              calc_ms_mass,\
                                              selections = base_selections_MS+[phi_selection_neg_ms],\
                                              bins_x = eta_bin_options["nbins"],\
                                              range_low_x = eta_bin_options["etalow"],\
                                              range_high_x = eta_bin_options["etahigh"],\
                                              xlabel = "#eta_{#mu}",\
                                              ylabel="<M_{#mu#mu}> [Gev]",\
                                              error_option="")

    for i, (pt_bin_lo, pt_bin_high) in enumerate(zip(pt_bins[:-1], pt_bins[1:])):
        pt_selection_pos_id = create_selection_function(range_selection_function, ["Pos_ID_Pt"], "Pos_ID_Pt", pt_bin_lo, pt_bin_high)
        pt_selection_neg_id = create_selection_function(range_selection_function, ["Neg_ID_Pt"], "Neg_ID_Pt", pt_bin_lo, pt_bin_high)
        pt_selection_pos_cb = create_selection_function(range_selection_function, ["Pos_CB_Pt"], "Pos_CB_Pt", pt_bin_lo, pt_bin_high)
        pt_selection_neg_cb = create_selection_function(range_selection_function, ["Neg_CB_Pt"], "Neg_CB_Pt", pt_bin_lo, pt_bin_high)
        pt_selection_pos_ms = create_selection_function(range_selection_function, ["Pos_MS_Pt"], "Pos_MS_Pt", pt_bin_lo, pt_bin_high)
        pt_selection_neg_ms = create_selection_function(range_selection_function, ["Neg_MS_Pt"], "Neg_MS_Pt", pt_bin_lo, pt_bin_high)
        #correction_ID = SagittaBiasCorrection([],  calc_pos_id_eta, calc_neg_id_eta, calc_pos_id_phi, calc_neg_id_phi, pos_selections = [pt_selection_pos_id], neg_selections = [pt_selection_neg_id], flavour = "ID",)
        #correction_CB = SagittaBiasCorrection([], calc_pos_cb_eta, calc_neg_cb_eta, calc_pos_cb_phi, calc_neg_cb_phi, pos_selections = [pt_selection_pos_cb], neg_selections = [pt_selection_neg_cb], flavour = "CB")
        #correction_MS = SagittaBiasCorrection([], flavour = "MS", calc_pos_ms_eta, calc_neg_ms_eta, calc_pos_ms_phi, calc_neg_ms_phi, pos_elections = [pt_selection_pos_ms], neg_selections = [pt_selection_neg_ms])


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

        #book a tprofile of the average mass
        histogram_name = histogram_name_base.format(charge="Pos", count=i, location="MS", histsetname=histsetname)
        hist_filler.book_2dtprofile_fill(histogram_name, \
                                              calc_pos_ms_eta,\
                                              calc_pos_ms_phi,\
                                              calc_ms_mass,\
                                              selections = base_selections_MS+[pt_selection_pos_ms],\
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
                                              calc_neg_ms_eta,\
                                              calc_neg_ms_phi,\
                                              calc_ms_mass,\
                                              selections = base_selections_MS+[pt_selection_neg_ms],\
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

        histogram_name = histogram_name_base.format(charge="Pos", count=i, location="MS", histsetname=histsetname)
        hist_filler.book_histogram_fill(histogram_name,\
                                         calc_ms_mass,\
                                         selections = [pt_selection_pos_ms],\
                                         bins = 100,\
                                         range_low = 86.0-10.0,\
                                         range_high = 86.0+10.0,\
                                         xlabel ='M_{#mu#mu}^{varname} [GeV]',\
                                         ylabel = 'Number Events')

        histogram_name = histogram_name_base.format(charge="Neg", count=i, location="MS", histsetname=histsetname)
        hist_filler.book_histogram_fill(histogram_name,\
                                         calc_ms_mass,\
                                         selections = [pt_selection_neg_ms],\
                                         bins = 100,\
                                         range_low = 86.0-10.0,\
                                         range_high = 86.0+10.0,\
                                         xlabel ='M_{#mu#mu}^{varname} [GeV]',\
                                         ylabel = 'Number Events')

#This is a script that fills the histograms for
def fill_histograms(hist_filler, output_filename):



    for varname, var in zip(["ID", "CB", "MS", "ME"], [calc_id_mass, calc_cb_mass, calc_ms_mass, calc_me_mass]):
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


    mass_MS = calc_ms_mass
    mass_ID = "Pair_ID_Mass"
    mass_CB = "Pair_CB_Mass"
    mass_ME = "Pair_ME_Mass"
    mass_selZ_func_ID = create_selection_function(range_selection_function, [mass_ID], mass_ID, 91.2 - 12.0, 91.2 + 12.0)
    mass_selZ_func_CB = create_selection_function(range_selection_function, [mass_CB], mass_CB, 91.2 - 12.0, 91.2 + 12.0)
    mass_selZ_func_MS = create_selection_function(range_selection_function, calc_ms_mass.branches, calc_ms_mass, 86.0 - 12.0, 86.0 + 12.0)
    mass_selZ_func_ME = create_selection_function(range_selection_function, [mass_ME], mass_ME, 91.2 - 12.0, 91.2 + 12.0)

    mass_MS = calc_ms_mass
    mass_selJPSI_func_ID = create_selection_function(range_selection_function, [mass_ID], mass_ID, 2.8, 3.4)
    mass_selJPSI_func_CB = create_selection_function(range_selection_function, [mass_CB], mass_CB, 2.8, 3.4)
    mass_selJPSI_func_MS = create_selection_function(range_selection_function, calc_ms_mass.branches, calc_ms_mass, 2.2, 3.4)
    mass_selJPSI_func_ME = create_selection_function(range_selection_function, [mass_ME], mass_ME, 2.8, 3.4)

    from variables import calc_cos_theta_star_id, calc_cos_theta_star_ms, calc_cos_theta_star_me
    from variables import sel_forward_id, sel_backward_id, sel_forward_me, sel_backward_me

    for sel_id, sel_me, name in zip([[sel_forward_id], [sel_backward_id]],\
                                    [[sel_forward_me], [sel_backward_me]],\
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

    for sel_id, sel_me, name in zip([[sel_pos_leading_id], [sel_neg_leading_id], []],\
                                    [[sel_pos_leading_me], [sel_neg_leading_me], []],\
                                    ["poslead", "neglead", "Inclusive"]):

        #I will come back and fix this

        varlist = \
        [\
         calc_leading_id_pt, calc_subleading_id_pt,\
         calc_leading_me_pt, calc_subleading_me_pt,\
         calc_leading_id_eta, calc_subleading_id_eta,\
         calc_leading_me_eta, calc_subleading_me_eta,\
         calc_leading_id_phi, calc_subleading_id_phi,\
         calc_leading_me_phi, calc_subleading_me_phi,\
        ]

        histnames = \
        [\
         "PT_Leading_ID", "PT_Subleading_ID",\
         "PT_Leading_ME", "PT_Subleading_ME",\
         "Eta_Leading_ID", "Eta_Subleading_ID",\
         "Eta_Leading_ME", "Eta_Subleading_ME",\
         "Phi_Leading_ID", "Phi_Subleading_ID",\
         "Phi_Leading_ME", "Phi_Subleading_ME",\
        ]

        x_ranges = \
        [\
         (5.0, 100.0), (5.0, 70.0),\
         (5.0, 100.0), (5.0, 70.0),\
         (-2.5, 2.5), (-2.5, 2.5),\
         (-2.7, 2.7), (-2.7, 2.7),\
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
        ]

        x_labels = \
        [\
         "P_{T}^{ID, Lead} [GeV]", "P_{T}^{ID, Sub} [GeV]",\
         "P_{T}^{ME, Lead} [GeV]", "P_{T}^{ME, Sub} [GeV]",\
         "#eta^{ID, Lead}", "#eta^{ID, Sub}",\
         "#eta^{ME, Lead}", "#eta^{ME, Sub}",\
         "#phi^{ID, Lead}", "#phi^{ID, Sub}",\
         "#phi^{ME, Lead}", "#phi^{ME, Sub}",\
        ]

        from selections import sel_nom_delta_selection_id, sel_nom_delta_selection_me
        for xvar, histname, x_range, x_label, nbins  in zip(varlist, histnames, x_ranges, x_labels, nbins_all):
            if "ID" in histname:
                base_sel = [sel_nom_delta_selection_id]
                sel = sel_id
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
                                             selections = sel_id + [mass_selZ_func_ID],\
                                             bins = 100,\
                                             range_low = -1.0,\
                                             range_high = 1.0,\
                                             xlabel ='cos#theta*_{ID}',\
                                             ylabel = 'Number Events')

        histogram_name_base = "CosThetaStar_ME_{identified}"
        histogram_name = histogram_name_base.format(identified = name)
        hist_filler.book_histogram_fill(histogram_name,\
                                             calc_cos_theta_star_me,\
                                             selections = sel_me + [mass_selZ_func_ME],\
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
