from variables import calc_id_mass, calc_ms_mass, calc_cb_mass
from selections import range_selection_function
from histogram_filler import create_selection_function, write_histograms
import ROOT
from IterativeBiasCorrection import SagittaBiasCorrection
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

#This is a script that fills the histograms for
def fill_histograms(hist_filler, output_filename, start_from_correction = None):
    for varname, var in zip(["ID", "CB"], [calc_id_mass, calc_cb_mass]):
        histogram_name = "{}_mass".format(varname)
        variable_name_for_selection = "Pair_{}_Mass".format(varname)
        sel_func = create_selection_function(range_selection_function, [variable_name_for_selection], variable_name_for_selection, 91.2 - 50.0, 91.2 + 50.0)
        hist_filler.book_histogram_fill(histogram_name,\
                                    var,\
                                    selections = [sel_func],\
                                    bins = 100,\
                                    range_low = 91.2-20.0,\
                                    range_high = 92.1+20.0,\
                                    xlabel ='M_{#mu#mu}^{varname} [GeV]',\
                                    ylabel = 'Number Events')


    #put this as the default pt binning somewhere
    pt_bins = []
    pt_bins.append(18.0)
    pt_bins.append(26.0)
    pt_bins.append(36.0)
    pt_bins.append(45.0)
    pt_bins.append(65.0)
    pt_bins.append(100.0)
    pt_bins.append(150.0)
    pt_bins.append(200.0)
    pt_bins.append(350.0)
    pt_bins.append(600.0)
    pt_bins.append(800.0)
    pt_bins.append(1000.0)
    pt_bins.append(2000.0)

    corrections_ID = []
    corrections_CB = []
    corrections_MS = []

    eta_bin_options = {"nbins": 32, "etalow":-2.7, "etahigh":+2.7}
    phi_bin_options = {"nbins": 30, "philow":-3.142, "phihigh":+3.142}

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
        mass_sel_func = create_selection_function(range_selection_function, [variable_name_for_selection], variable_name_for_selection, 91.2 - 15.0, 91.2 + 15.0)

        base_selections = [mass_sel_func]

        #book a tprofile of the average mass
        histogram_name_base = "{charge}_{location}_AverageMassProfile_{count}"
        histogram_name = histogram_name_base.format(charge="Pos", count=i, location="ID")
        hist_filler.book_2dtprofile_fill(histogram_name, \
                                         calc_pos_id_eta,\
                                         calc_pos_id_phi,\
                                         calc_id_mass,\
                                         selections = base_selections+[pt_selection_pos_id],\
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
        histogram_name = histogram_name_base.format(charge="Neg", count=i, location="ID")
        hist_filler.book_2dtprofile_fill(histogram_name, \
                                         calc_neg_id_eta,\
                                         calc_neg_id_phi,\
                                         calc_id_mass,\
                                         selections = base_selections+[pt_selection_neg_id],\
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
        histogram_name_base = "{charge}_{location}_AverageMassProfile_{count}"
        histogram_name = histogram_name_base.format(charge="Pos", count=i, location="CB")
        hist_filler.book_2dtprofile_fill(histogram_name, \
                                         calc_pos_cb_eta,\
                                         calc_pos_cb_phi,\
                                         calc_cb_mass,\
                                         selections = base_selections+[pt_selection_pos_cb],\
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
        histogram_name = histogram_name_base.format(charge="Neg", count=i, location="CB")
        hist_filler.book_2dtprofile_fill(histogram_name, \
                                         calc_neg_cb_eta,\
                                         calc_neg_cb_phi,\
                                         calc_cb_mass,\
                                         selections = base_selections+[pt_selection_neg_cb],\
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

        histogram_name_base = "{charge}_{location}_Mass_Histogram_{count}"
        histogram_name = histogram_name_base.format(charge="Pos", count=i, location="ID")
        hist_filler.book_histogram_fill(histogram_name,\
                                    var,\
                                    selections = [pt_selection_pos_id],\
                                    bins = 100,\
                                    range_low = 91.2-20.0,\
                                    range_high = 92.1+20.0,\
                                    xlabel ='M_{#mu#mu}^{varname} [GeV]',\
                                    ylabel = 'Number Events')

        histogram_name = histogram_name_base.format(charge="Neg", count=i, location="ID")
        hist_filler.book_histogram_fill(histogram_name,\
                                    var,\
                                    selections = [pt_selection_neg_id],\
                                    bins = 100,\
                                    range_low = 91.2-20.0,\
                                    range_high = 92.1+20.0,\
                                    xlabel ='M_{#mu#mu}^{varname} [GeV]',\
                                    ylabel = 'Number Events')

        histogram_name = histogram_name_base.format(charge="Pos", count=i, location="CB")
        hist_filler.book_histogram_fill(histogram_name,\
                                    var,\
                                    selections = [pt_selection_pos_cb],\
                                    bins = 100,\
                                    range_low = 91.2-20.0,\
                                    range_high = 92.1+20.0,\
                                    xlabel ='M_{#mu#mu}^{varname} [GeV]',\
                                    ylabel = 'Number Events')

        histogram_name = histogram_name_base.format(charge="Neg", count=i, location="CB")
        hist_filler.book_histogram_fill(histogram_name,\
                                    var,\
                                    selections = [pt_selection_neg_cb],\
                                    bins = 100,\
                                    range_low = 91.2-20.0,\
                                    range_high = 92.1+20.0,\
                                    xlabel ='M_{#mu#mu}^{varname} [GeV]',\
                                    ylabel = 'Number Events')

        '''
        histogram_name = histogram_name_base.format(charge="Pos", count=i, location="MS")
        hist_filler.book_histogram_fill(histogram_name,\
                                    var,\
                                    selections = [pt_selection_pos_ms],\
                                    bins = 100,\
                                    range_low = 91.2-20.0,\
                                    range_high = 92.1+20.0,\
                                    xlabel ='M_{#mu#mu}^{varname} [GeV]',\
                                    ylabel = 'Number Events')

        histogram_name = histogram_name_base.format(charge="Neg", count=i, location="MS")
        hist_filler.book_histogram_fill(histogram_name,\
                                    var,\
                                    selections = [pt_selection_neg_ms],\
                                    bins = 100,\
                                    range_low = 91.2-20.0,\
                                    range_high = 92.1+20.0,\
                                    xlabel ='M_{#mu#mu}^{varname} [GeV]',\
                                    ylabel = 'Number Events')
        '''


    histograms = hist_filler.DumpHistograms()
    output_file = ROOT.TFile(output_filename, "RECREATE")
    for histogram_name in histograms:
        write_histograms(histograms[histogram_name], output_file)

    output_file.Close()

    print("__Finished__")
