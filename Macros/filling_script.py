from variables import calc_id_mass, calc_ms_mass, calc_cb_mass
from selections import range_selection_function
from histogram_filler import create_selection_function

#This is a script that fills the histograms for
def fill_histograms(hist_filler, output_filename):
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
    hist_filler.DumpHistograms()
