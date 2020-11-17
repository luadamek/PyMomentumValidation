from variables import calc_id_mass, calc_ms_mass, calc_cb_mass
from selections import range_selection_function
from histogram_filler import create_selection_function, write_histograms
import ROOT
from BiasCorrection import SagittaBiasCorrection
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
from selections import sel_pos_leading_id, sel_neg_leading_id
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
                                         range_low = 91.2-10.0,\
                                         range_high = 91.2+10.0,\
                                         xlabel ='M_{#mu#mu}^{varname} [GeV]',\
                                         ylabel = 'Number Events')

    histogram_name_base = "{histsetname}_{location}_Mass_Histogram_{count}"
    histogram_name = histogram_name_base.format(count="Inclusive", location="CB", histsetname=histsetname)
    hist_filler.book_histogram_fill(histogram_name,\
                                         calc_id_mass,\
                                         selections = [],\
                                         bins = 200,\
                                         range_low = 91.2-10.0,\
                                         range_high = 91.1+10.0,\
                                         xlabel ='M_{#mu#mu}^{varname} [GeV]',\
                                         ylabel = 'Number Events')

    '''
    histogram_name_base = "{histsetname}_{location}_Mass_Histogram_{count}"
    histogram_name = histogram_name_base.format(count="Inclusive", location="CB", histsetname=histsetname)
    hist_filler.book_histogram_fill(histogram_name,\
                                         calc_id_mass,\
                                         selections = [pt_selection_pos_id],\
                                         bins = 100,\
                                         range_low = 91.2-10.0,\
                                         range_high = 91.2+10.0,\
                                         xlabel ='M_{#mu#mu}^{varname} [GeV]',\
                                         ylabel = 'Number Events')
    '''


    phi_bins = np.linspace(phi_bin_options["philow"], phi_bin_options["phihigh"], phi_bin_options["nbins"] + 1)

    #book a tprofile of the average mass
    mass_ID = "Pair_ID_Mass"
    mass_CB = "Pair_CB_Mass"
    mass_MS = "Pair_MS_Mass"
    mass_sel_func_ID = create_selection_function(range_selection_function, [mass_ID], mass_ID, 91.2 - 10.0, 91.2 + 10.0)
    mass_sel_func_CB = create_selection_function(range_selection_function, [mass_CB], mass_CB, 91.2 - 10.0, 91.2 + 10.0)
    mass_sel_func_MS = create_selection_function(range_selection_function, [mass_MS], mass_MS, 91.2 - 10.0, 91.2 + 10.0)
    base_selections_ID = [mass_sel_func_ID]
    base_selections_CB = [mass_sel_func_CB]
    base_selections_MS = [mass_sel_func_MS]
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

    from selections import sel_pos_leading_id, sel_neg_leading_id
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
        '''
        histogram_name_base = "{charge}_{location}_AverageMassProfile_{count}"
        histogram_name = histogram_name_base.format(charge="Pos", count=i, location="MS")
        hist_filler.book_2dtprofile_fill(histogram_name, \
                                              calc_pos_ms_eta,\
                                              calc_pos_ms_phi,\
                                              calc_ms_mass,\
                                              selections = base_selections+[phi_selection_pos_ms],\
                                              bins_x = eta_bin_options["nbins"],\
                                              range_low_x = eta_bin_options["etalow"],\
                                              range_high_x = eta_bin_options["etahigh"],\
                                              xlabel = "#eta_{#mu}",\
                                              ylabel="<M_{#mu#mu}> [Gev]",\
                                              error_option="")

        histogram_name_base = "{charge}_{location}_AverageMassProfile_{count}"
        histogram_name = histogram_name_base.format(charge="Neg", count=i, location="MS")
        hist_filler.book_2dtprofile_fill(histogram_name, \
                                              calc_neg_ms_eta,\
                                              calc_neg_ms_phi,\
                                              calc_ms_mass,\
                                              selections = base_selections+[phi_selection_neg_ms],\
                                              bins_x = eta_bin_options["nbins"],\
                                              range_low_x = eta_bin_options["etalow"],\
                                              range_high_x = eta_bin_options["etahigh"],\
                                              xlabel = "#eta_{#mu}",\
                                              ylabel="<M_{#mu#mu}> [Gev]",\
                                              error_option="")
        '''

    for i, (pt_bin_lo, pt_bin_high) in enumerate(zip(pt_bins[:-1], pt_bins[1:])):
        pt_selection_pos_id = create_selection_function(range_selection_function, ["Pos_ID_Pt"], "Pos_ID_Pt", pt_bin_lo, pt_bin_high)
        pt_selection_neg_id = create_selection_function(range_selection_function, ["Neg_ID_Pt"], "Neg_ID_Pt", pt_bin_lo, pt_bin_high)
        pt_selection_pos_cb = create_selection_function(range_selection_function, ["Pos_CB_Pt"], "Pos_CB_Pt", pt_bin_lo, pt_bin_high)
        pt_selection_neg_cb = create_selection_function(range_selection_function, ["Neg_CB_Pt"], "Neg_CB_Pt", pt_bin_lo, pt_bin_high)
        #pt_selection_pos_ms = create_selection_function(range_selection_function, ["Pos_MS_Pt"], "Pos_MS_Pt", pt_bin_lo, pt_bin_high)
        #pt_selection_neg_ms = create_selection_function(range_selection_function, ["Neg_MS_Pt"], "Neg_MS_Pt", pt_bin_lo, pt_bin_high)
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
        '''
        histogram_name_base = "{charge}_{location}_AverageMassProfile_{count}"
        histogram_name = histogram_name_base.format(charge="Pos", count=i, location="MS")
        hist_filler.book_2dtprofile_fill(histogram_name, \
                                              calc_pos_ms_eta,\
                                              calc_pos_ms_phi,\
                                              calc_ms_mass,\
                                              selections = base_selections+[pt_selection_pos_ms],\
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

        histogram_name_base = "{charge}_{location}_AverageMassProfile_{count}"
        histogram_name = histogram_name_base.format(charge="Neg", count=i, location="MS")
        hist_filler.book_2dtprofile_fill(histogram_name, \
                                              calc_neg_ms_eta,\
                                              calc_neg_ms_phi,\
                                              calc_ms_mass,\
                                              selections = base_selections+[pt_selection_neg_ms],\
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
        '''

        histogram_name_base = "{histsetname}_{charge}_{location}_Mass_Histogram_{count}"
        histogram_name = histogram_name_base.format(charge="Pos", count=i, location="ID", histsetname=histsetname)
        hist_filler.book_histogram_fill(histogram_name,\
                                         calc_id_mass,\
                                         selections = [pt_selection_pos_id],\
                                         bins = 100,\
                                         range_low = 91.2-10.0,\
                                         range_high = 91.2+10.0,\
                                         xlabel ='M_{#mu#mu}^{varname} [GeV]',\
                                         ylabel = 'Number Events')

        histogram_name = histogram_name_base.format(charge="Neg", count=i, location="ID", histsetname=histsetname)
        hist_filler.book_histogram_fill(histogram_name,\
                                         calc_id_mass,\
                                         selections = [pt_selection_neg_id],\
                                         bins = 100,\
                                         range_low = 91.2-10.0,\
                                         range_high = 91.2+10.0,\
                                         xlabel ='M_{#mu#mu}^{varname} [GeV]',\
                                         ylabel = 'Number Events')

        histogram_name = histogram_name_base.format(charge="Pos", count=i, location="CB", histsetname=histsetname)
        hist_filler.book_histogram_fill(histogram_name,\
                                         calc_cb_mass,\
                                         selections = [pt_selection_pos_cb],\
                                         bins = 100,\
                                         range_low = 91.2-10.0,\
                                         range_high = 91.2+10.0,\
                                         xlabel ='M_{#mu#mu}^{varname} [GeV]',\
                                         ylabel = 'Number Events')

        histogram_name = histogram_name_base.format(charge="Neg", count=i, location="CB", histsetname=histsetname)
        hist_filler.book_histogram_fill(histogram_name,\
                                         calc_cb_mass,\
                                         selections = [pt_selection_neg_cb],\
                                         bins = 100,\
                                         range_low = 91.2-10.0,\
                                         range_high = 91.2+10.0,\
                                         xlabel ='M_{#mu#mu}^{varname} [GeV]',\
                                         ylabel = 'Number Events')

        '''
        histogram_name = histogram_name_base.format(charge="Pos", count=i, location="MS")
        hist_filler.book_histogram_fill(histogram_name,\
                                         var,\
                                         selections = [pt_selection_pos_ms],\
                                         bins = 100,\
                                         range_low = 91.2-10.0,\
                                         range_high = 91.2+10.0,\
                                         xlabel ='M_{#mu#mu}^{varname} [GeV]',\
                                         ylabel = 'Number Events')

        histogram_name = histogram_name_base.format(charge="Neg", count=i, location="MS")
        hist_filler.book_histogram_fill(histogram_name,\
                                         var,\
                                         selections = [pt_selection_neg_ms],\
                                         bins = 100,\
                                         range_low = 91.2-10.0,\
                                         range_high = 91.2+10.0,\
                                         xlabel ='M_{#mu#mu}^{varname} [GeV]',\
                                         ylabel = 'Number Events')
        '''

#This is a script that fills the histograms for
def fill_histograms(hist_filler, output_filename, calibrations = None):
    #book a calibration for the sagitta bias correction
    if calibrations is not None:
        import pickle as pkl
        with open(calibrations, "rb") as f:
            calibrations = pkl.load(f)
        for c in calibrations:
            hist_filler.apply_calibration_for_channel("Data", c)

    for varname, var in zip(["ID", "CB"], [calc_id_mass, calc_cb_mass]):
        histogram_name = "{}_mass".format(varname)
        variable_name_for_selection = "Pair_{}_Mass".format(varname)
        sel_func = create_selection_function(range_selection_function, [variable_name_for_selection], variable_name_for_selection, 91.2 - 50.0, 91.2 + 50.0)
        hist_filler.book_histogram_fill(histogram_name,\
                                    var,\
                                    selections = [sel_func],\
                                    bins = 100,\
                                    range_low = 91.2-10.0,\
                                    range_high = 91.2+10.0,\
                                    xlabel ='M_{#mu#mu}^{varname} [GeV]',\
                                    ylabel = 'Number Events')




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

    for sel, name in zip([sel_pos_leading_id, sel_neg_leading_id], ["poslead", "neglead"]):
        #make invariant mass histograms for ID tracks
        histogram_name_base = "MassSpectrum_{identified}"
        histogram_name = histogram_name_base.format(identified = name)
        hist_filler.book_histogram_fill(histogram_name,\
                                             calc_id_mass,\
                                             selections = [sel],\
                                             bins = 100,\
                                             range_low = 91.2-10.0,\
                                             range_high = 91.2+10.0,\
                                             xlabel ='M_{#mu#mu}^{ID} [GeV]',\
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