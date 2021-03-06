import numpy as np
import ROOT
import array
import os
from atlasplots import set_atlas_style, atlas_label

from atlasplots import set_atlas_style 
set_atlas_style()
def draw_2d_histogram(histogram, description = "", normalize = True, output_location="", palette_override = None, ftype = "png", fix_axes = True):

    if palette_override is None: ROOT.gStyle.SetPalette(ROOT.kTemperatureMap)
    else: ROOT.gStyle.SetPalette(palette_override)

    if normalize:
        extrema = [ abs(histogram.GetMaximum()), abs(histogram.GetMinimum())]
        histogram.SetMaximum(max(*extrema))
        histogram.SetMinimum(min(*[-1.0 * el for el in extrema]))

    text_size = 0.07
    
    label_size = 0.06

    if fix_axes:
       histogram.GetZaxis().SetTitleSize(text_size)
       histogram.GetYaxis().SetTitleSize(text_size)
       histogram.GetXaxis().SetTitleSize(text_size)
       histogram.GetZaxis().SetLabelSize(label_size)
       histogram.GetYaxis().SetLabelSize(label_size)
       histogram.GetXaxis().SetLabelSize(label_size)

    canvas = ROOT.TCanvas("Canvas_" + histogram.GetName())
    histogram.Draw("COLZ")
    if fix_axes: histogram.GetYaxis().SetTitleOffset(0.88)
    if fix_axes: histogram.GetXaxis().SetTitleOffset(1.1)
    canvas.SetTopMargin(0.1)
    if description: atlas_label(0.15, 0.94, "Internal   {}".format(description))
    else: atlas_label(0.2, 0.94, "Internal")
    canvas.SetRightMargin(0.25)
    histogram.GetZaxis().SetTitleOffset(1.2)
    canvas.SetBottomMargin(0.25)
    canvas.Draw()

    canvas.Print(os.path.join(output_location, canvas.GetName() + ".{}".format(ftype)))

def draw_text(x, y, text, color=1, size=0.05):
    '''Draw text.
    Parameters
    ----------
    x : float
        x position in NDC coordinates
    y : float
        y position in NDC coordinates
    text : string, optional
        The text
    color : int, optional
        Text colour (the default is 1, i.e. black).
        See https://ROOT.cern.ch/doc/master/classTColor.html.
        If you know the hex code, rgb values, etc., use ``ROOT.TColor.GetColor()``
    size : float, optional
        Text size
        See https://ROOT.cern.ch/doc/master/classTLatex.html
    '''
    l = ROOT.TLatex()
    l.SetTextSize(22)
    l.SetNDC()
    l.SetTextColor(color)
    l.DrawLatex(x, y, text)

def ATLASLabel(x, y, text=None, color=1, size = None, extra_descr = None):
    """Draw the ATLAS Label.
    Parameters
    ----------
    x : float
        x position in NDC coordinates
    y : float
        y position in NDC coordinates
    text : string, optional
        Text displayed next to label (the default is None)
    color : TColor, optional
        Text colour (the default is 1, i.e. black).
        See https://ROOT.cern.ch/doc/master/classTColor.html
    """
    l = ROOT.TLatex()
    l.SetNDC()
    l.SetTextColor(color)
    if size != None:
        l.SetTextSize(size)
    if extra_descr is not None and len(extra_descr) != 0:
        if "#splitline:" not in extra_descr: l.DrawLatex(x, y, r"#bf{#it{ATLAS}} " + text + extra_descr)
        else:
            extra_descr = extra_descr.split(":")[-1]
            l.DrawLatex(x, y, r"#splitline{#bf{#it{ATLAS}} " + text +"}{"+ extra_descr + "}")


def hist_to_tgrapherrors(hist):
    xs = []
    xerrs = []
    ys = []
    yerrs = []
    for i in range(1, hist.GetNbinsX() + 1):
        xs.append(hist.GetBinCenter(i))
        xerrs.append(0.0)
        ys.append(hist.GetBinContent(i))
        yerrs.append(hist.GetBinError(i))
    xs = array.array('d', xs)
    xerrs = array.array('d', xerrs)
    ys = array.array('d', ys)
    yerrs = array.array('d', yerrs)
    graph = ROOT.TGraphErrors(len(xs),xs,ys,xerrs,yerrs)
    graph.SetName("Graph_{}".format(hist.GetName()))
    graph.GetXaxis().SetTitle(hist.GetXaxis().GetTitle())
    graph.GetYaxis().SetTitle(hist.GetYaxis().GetTitle())
    return graph

alive = []
def draw_data_vs_mc(histograms, ratio_min = 0.9, ratio_max = 1.1, colours = None, legend_labels = None, legend_coordinates = (0.6, 0.9, 0.5, 0.9), x_axis_label = "M_{#mu#mu} [GeV]", y_axis_label="Events", logy=False, extra_descr="", to_return = False, ftype = ".png", plot_dir = "plots", datakey = "data", extra_str = None):


    ROOT.gStyle.SetLineWidth(1)
    ROOT.gStyle.SetFrameLineWidth(1)

    integrals = {}
    data_histogram = histograms[datakey]
    mc_histograms = {key:histograms[key] for key in histograms if datakey not in key}
    for channel in histograms:
        integrals[channel] = sum([histograms[channel].GetBinContent(i) \
                              for i in range(1, histograms[channel].GetNbinsX() + 1)])

    unordered_keys = list(mc_histograms.keys())
    unordered_integrals = [integrals[key] for key in mc_histograms]
    sort_index = np.argsort(unordered_integrals)
    ordered_keys = [unordered_keys[i] for i in sort_index]

    #ok the histograms are now plotted in ascending order. Lets make a THStack
    stack = ROOT.THStack("histograms", "histograms")
    summed = None
    for key in ordered_keys:
        if not colours is None:
            mc_histograms[key].SetFillColor(colours[key])
            mc_histograms[key].SetLineColor(colours[key])
            mc_histograms[key].SetMarkerColor(colours[key])

        if summed is None:
            summed = mc_histograms[key].Clone()
        else:
            summed.Add(mc_histograms[key])
        mc_histograms[key].SetFillStyle(1001)
        stack.Add(mc_histograms[key])

    maximum = max(summed.GetMaximum() * 1.4, data_histogram.GetMaximum() * 1.2)
    minimum = min(summed.GetMinimum() /1.2, data_histogram.GetMinimum() / 1.2)
    stack.SetMaximum(maximum)
    stack.SetMinimum(min(0.001,minimum))

    legend = ROOT.TLegend(*legend_coordinates)
    if not legend_labels is None:
        for key in ordered_keys[::-1]:
            label = legend_labels[key]
            if not datakey == key: legend.AddEntry(histograms[key], label, "F")

    legend.SetBorderSize(0)

    ratio_hist = data_histogram.Clone()
    ratio_hist.Divide(summed)

    ratio_hist.GetYaxis().SetTitle("Data/MC")
    ratio_hist.GetXaxis().SetTitle(x_axis_label)
    ratio_hist.SetLineColor(ROOT.kBlack)
    ratio_hist.SetMarkerColor(ROOT.kBlack)

    identifier = " ".join([histograms[key].GetName() for key in histograms])
    canvas = ROOT.TCanvas("canv" + identifier, "canv " + identifier, 2 * 800 , 2 * 600)
    canvas.Draw()
    canvas.cd()
    top = ROOT.TPad("top" + identifier, identifier, 0.0, 0.4, 1.0, 1.0)
    top.SetBottomMargin(0.0)
    bottom = ROOT.TPad("botom" + identifier, identifier, 0.0, 0.0, 1.0, 0.4)
    bottom.SetTopMargin(0.0)

    canvas.cd()
    top.Draw()
    top.SetTopMargin(0.1)

    canvas.cd()
    bottom.Draw()

    bottom.cd()
    ratio_hist_for_axes = ratio_hist
    ratio_hist = hist_to_tgrapherrors(ratio_hist)
    ratio_hist_for_axes.Draw("AXIS")

    ratio_hist.Draw("P SAME")
    bottom.SetBottomMargin(0.4)
    #ratio_hist.GetXaxis().SetTitleOffset(2.0*ratio_hist.GetXaxis().GetTitleOffset())
    #ratio_hist.GetYaxis().SetTitleOffset(2.0*ratio_hist.GetYaxis().GetTitleOffset())
    #ratio_hist.GetXaxis().SetTitleSize(1.5*ratio_hist.GetXaxis().GetTitleSize())
    #ratio_hist.GetYaxis().SetTitleSize(1.5*ratio_hist.GetYaxis().GetTitleSize())

    top.cd()
    data_histogram.SetMarkerSize(0.5)
    data_histogram.SetMarkerStyle(2)

    smallest_positive = None
    for i in range(1, summed.GetNbinsX() + 1):
        this_content = summed.GetBinContent(i)
        if smallest_positive is None and this_content > 0.0 : smallest_positive = this_content
        elif this_content > 0.0 and smallest_positive > this_content: smallest_positive = this_content

    stack.SetMinimum(0.0)
    if logy:
        stack.SetMinimum(smallest_positive / 2.0)
    stack.Draw("HIST")
    stack.GetYaxis().SetTitleOffset(stack.GetYaxis().GetTitleOffset() * 1.0)
    stack.GetXaxis().SetTitleOffset(stack.GetXaxis().GetTitleOffset() * 1.4)
    text_size = 60
    label_size = 45
    stack.GetYaxis().SetTitleSize(text_size)
    stack.GetXaxis().SetTitleSize(text_size)
    stack.GetYaxis().SetLabelSize(label_size)
    stack.GetXaxis().SetLabelSize(label_size)
    bin_width = stack.GetStack().Last().GetBinLowEdge(3) - stack.GetStack().Last().GetBinLowEdge(2)
    units = x_axis_label.split(" ")[-1].replace("[","").replace("]","") #get the units of the x-axis
    stack.GetYaxis().SetTitle("{} / {:.2f} {}".format(y_axis_label, bin_width, units))
    if logy: top.SetLogy()

    x_factor = top.GetAbsWNDC()/top.GetAbsWNDC();
    y_factor = top.GetAbsHNDC()/top.GetAbsHNDC();

    ratio_hist_for_axes.GetXaxis().SetLabelSize(label_size)
    ratio_hist_for_axes.GetYaxis().SetLabelSize(label_size)
    ratio_hist_for_axes.GetXaxis().SetTitleSize(text_size)
    ratio_hist_for_axes.GetYaxis().SetTitleSize(text_size)
    ratio_hist_for_axes.GetXaxis().SetTitleOffset(y_factor * stack.GetXaxis().GetTitleOffset() / x_factor)
    ratio_hist_for_axes.GetYaxis().SetTitleOffset(x_factor * stack.GetYaxis().GetTitleOffset() / y_factor)
    ratio_hist_for_axes.SetMaximum(ratio_max)
    ratio_hist_for_axes.SetMinimum(ratio_min)

    summed.SetFillStyle(3135)
    summed.SetMarkerSize(0.0)
    ROOT.gStyle.SetErrorX(0.5)
    summed.Draw("SAME E2")
    summed.SetLineColor(ROOT.kBlack)
    summed.SetFillColor(ROOT.kBlack)
    summed.SetMarkerColor(ROOT.kBlack)

    data_plot = hist_to_tgrapherrors(data_histogram)
    data_plot.SetMarkerSize(data_plot.GetMarkerSize()*1.5)
    data_plot.Draw("P SAME")
    data_plot.SetLineWidth(data_plot.GetLineWidth()+2)
    legend.AddEntry(data_plot, legend_labels[datakey], "LP")
    legend.Draw()
    ATLASLabel(0.25, 0.77, "Internal", size = text_size)
    legend.SetTextSize(40)

    bottom.cd()
    ##Draw a set of solid and dotted lines on the ratio plot to guide the reader's eyes
    straight_line = ROOT.TF1("line1" + identifier, str(1.0) , -10e6, + 10e6)
    straight_line.SetLineWidth(2)
    straight_line.Draw("Same")

    straight_line_up = ROOT.TF1("line2" + identifier,  str(1.0 + (2.0 * (ratio_max - 1.0)/4)) , -10e6, + 10e6)
    straight_line_up.SetLineWidth(1)
    straight_line_up.SetLineStyle(1)
    straight_line_up.Draw("Same")

    straight_line_up2 = ROOT.TF1("line3" + identifier,  str(1.0 + (1.0 * (ratio_max - 1.0)/4)) , -10e6, + 10e6)
    straight_line_up2.SetLineWidth(1)
    straight_line_up2.SetLineStyle(3)
    straight_line_up2.Draw("Same")

    straight_line_up3 = ROOT.TF1("line4" + identifier,  str(1.0 + (3.0 * (ratio_max - 1.0)/4)) , -10e6, + 10e6)
    straight_line_up3.SetLineWidth(1)
    straight_line_up3.SetLineStyle(3)
    straight_line_up3.Draw("Same")

    straight_line_down3 = ROOT.TF1("line5" + identifier,  str(1.0 - (3.0 * (ratio_max - 1.0)/4)) , -10e6, + 10e6)
    straight_line_down3.SetLineWidth(1)
    straight_line_down3.SetLineStyle(3)
    straight_line_down3.Draw("Same")

    straight_line_down = ROOT.TF1("line6" + identifier,  str(1.0 - (2.0 * (ratio_max - 1.0)/4)) , -10e6, + 10e6)
    straight_line_down.SetLineWidth(1)
    straight_line_down.SetLineStyle(1)
    straight_line_down.Draw("Same")

    straight_line_down2 = ROOT.TF1("line7" + identifier,  str(1.0 - (1.0 * (ratio_max - 1.0)/4)) , -10e6, + 10e6)
    straight_line_down2.SetLineWidth(1)
    straight_line_down2.SetLineStyle(3)
    straight_line_down2.Draw("Same")
    #bottom.Draw()

    global alive
    alive.append(locals())
    if to_return: return canvas, keep_alive
    else:
         if not os.path.exists(plot_dir):
             os.makedirs(plot_dir)
         canvas.Print(os.path.join(plot_dir, identifier + ftype))

def get_extrema(histogram, minimum=True, bounds=None):
     extreme = 9999999999999
     if not minimum: extreme = -1 * extreme

     for i in range(1, histogram.GetNbinsX() + 1):
         if histogram.GetBinContent(i) < extreme and minimum:
             if bounds is None or (histogram.GetBinCenter(i) < bounds[1] and histogram.GetBinCenter(i) > bounds[0]):
                 extreme = histogram.GetBinContent(i)
         if histogram.GetBinContent(i) > extreme and not minimum:
             if bounds is None or (histogram.GetBinCenter(i) < bounds[1] and histogram.GetBinCenter(i) > bounds[0]):
                 extreme = histogram.GetBinContent(i)
     return extreme

def get_systematic_histograms(histograms, systematic_histograms, add_stat = True):
    to_plot_errors = {}
    to_plot_errors_components = {}
    to_plot = {key:hist_to_tgrapherrors(histograms[key]) for key in histograms}
    for key in to_plot:
        if key not in systematic_histograms: continue 
        try: to_plot_errors[key] = histograms[key].ProjectionX(histograms[key].GetName() + "SystematicVariation")
        except Exception as e: to_plot_errors[key] = histograms[key].Clone(histograms[key].GetName() + "SystematicVariation")
        for i in range(1, to_plot_errors[key].GetNbinsX() + 1):
            if not add_stat: to_plot_errors[key].SetBinError(i, 0.0)
            else: to_plot_errors[key].SetBinError(i, histograms[key].GetBinError(i)) #add the stat err to the plot
            for systematic in systematic_histograms[key]:
                up = systematic_histograms[key][systematic]["up"].GetBinContent(i)
                down = systematic_histograms[key][systematic]["down"].GetBinContent(i)
                nom = to_plot_errors[key].GetBinContent(i)
                #take the max difference between the var and the nominal as the systematic. Sum in quadrature
                to_plot_errors[key].SetBinError(i, ( max(abs(up-nom), abs(down-nom))**2 + (to_plot_errors[key].GetBinError(i)**2) )**0.5 )
    return to_plot_errors

def draw_histograms(histograms,  colours = None, styles = None, legend_labels = None, legend_coordinates = (0.6, 0.9, 0.5, 0.9), x_axis_label = "M_{#mu#mu} [GeV]", y_axis_label="Events", logy=False, extra_descr="", to_return = False, ftype = ".png", plot_dir = "plots", x_range = None, mins_maxes = None, savename=None, systematic_histograms={}):

    from atlasplots import set_atlas_style
    set_atlas_style()
    ROOT.gStyle.SetErrorX(0.5)
    ROOT.gStyle.SetLineWidth(1)
    ROOT.gStyle.SetFrameLineWidth(1)

    key = list(histograms.keys())[0]
    if x_axis_label is None:  x_axis_label= histograms[key].GetXaxis().GetTitle()
    if y_axis_label is None: y_axis_label= histograms[key].GetYaxis().GetTitle()

    to_plot = {key:hist_to_tgrapherrors(histograms[key]) for key in histograms}
    to_plot_errors = get_systematic_histograms(histograms, systematic_histograms)

    if colours is not None: [to_plot[key].SetMarkerColor(colours[key]) for key in to_plot]
    if styles is not None: [to_plot[key].SetMarkerStyle(styles[key]) for key in to_plot]
    for key in to_plot: to_plot[key].SetMarkerSize(to_plot[key].GetMarkerSize()*1.5)
    for key in to_plot: to_plot[key].GetXaxis().SetTitleSize(22)
    for key in to_plot: to_plot[key].GetYaxis().SetTitleSize(22)

    legend = ROOT.TLegend(*legend_coordinates)
    if not legend_labels is None:
        for key in histograms:
            label = legend_labels[key]
            legend.AddEntry(to_plot[key], label, "P")
    legend.SetBorderSize(0)

    identifier = " ".join([to_plot[key].GetName() for key in to_plot])
    canvas = ROOT.TCanvas("canv" + identifier, "canv " + identifier, 2 * 800 , 2 * 600)
    canvas.Draw()
    canvas.cd()

    canvas.SetTopMargin(canvas.GetTopMargin()*1.1)
    canvas.SetBottomMargin(canvas.GetBottomMargin()*1.1)
    canvas.SetRightMargin(canvas.GetRightMargin()*1.1)
    canvas.SetLeftMargin(canvas.GetLeftMargin()*1.1)

    if mins_maxes is None:
        mins = []
        maxs = []
        for i, key in enumerate(to_plot):
            stack = histograms[key]
            mins.append(get_extrema(stack, minimum=True, bounds=x_range))
            maxs.append(get_extrema(stack, minimum=False, bounds=x_range))

        minimum = min(mins)
        maximum = max(maxs)
    else:
        minimum = mins_maxes[0]
        maximum = mins_maxes[1]

    text_size = 70
    label_size = 60

    for i, key in enumerate(to_plot):
        stack = to_plot[key]
        bin_width = histograms[key].GetBinLowEdge(3) - histograms[key].GetBinLowEdge(2)
        if y_axis_label is not None:
            stack.GetYaxis().SetTitle(y_axis_label)
        else: y_axis_label = stack.GetXaxis().GetTitle()
        if x_axis_label is not None:
            stack.GetXaxis().SetTitle(x_axis_label)
        else: x_axis_label = stack.GetYaxis().GetTitle()

        if x_range is not None: stack.GetXaxis().SetRangeUser(*x_range)
        stack.SetMaximum(maximum + (0.6 * (maximum-minimum)))
        stack.SetMinimum(minimum)

        stack.GetYaxis().SetTitleSize(text_size)
        stack.GetXaxis().SetTitleSize(text_size)
        stack.GetYaxis().SetLabelSize(label_size)
        stack.GetXaxis().SetLabelSize(label_size)
        #stack.GetXaxis().SetTitleOffset(1.05)
        err_drawn = False
        if i == 0: stack.Draw("AP")
        else: stack.Draw("P SAME")

        if key in to_plot_errors:
            to_plot_errors[key].SetMarkerSize(0.0)
            to_plot_errors[key].SetFillColor(ROOT.kGray)
            to_plot_errors[key].SetFillStyle(1001)
            to_plot_errors[key].Draw("E2 SAME")

        stack.Draw("P SAME")

    ATLASLabel(0.20, 0.8, "Internal", size = 50, extra_descr = extra_descr)
    legend.SetTextSize(40)
    legend.Draw("SAME")

    if logy: canvas.SetLogy()

    global alive
    alive.append(locals())
    if to_return: return canvas, keep_alive
    else:
         if not os.path.exists(plot_dir):
             os.makedirs(plot_dir)
         if savename is None: canvas.Print(os.path.join(plot_dir, identifier + ftype))
         else: canvas.Print(os.path.join(plot_dir, savename + ftype))


def get_systematically_varied_histograms(to_plot_hists, data_channel, mc_channel, mc_stat_up, mc_stat_down):
    #ok make a ratio plot
    data_hist = to_plot_hists[data_channel]
    mc_hist = to_plot_hists[mc_channel]
    sagitta_stat_syst_content = to_plot_hists[mc_stat_up].Clone()
    sagitta_stat_syst_content.Add(to_plot_hists[mc_stat_down], -1.0)
    #for i in range(1, afb_hist[mc_stat_up].GetNbinsX()):
    #    print(afb_hist[mc_stat_up],afb_hist[mc_channel] ,  afb_hist[mc_stat_down])
    #    print(afb_hist[mc_stat_up].GetBinContent(i), afb_hist[mc_channel].GetBinContent(i), afb_hist[mc_stat_down].GetBinContent(i))
    sagitta_stat_syst_content.Scale(0.5)
    [sagitta_stat_syst_content.SetBinContent(i, abs(sagitta_stat_syst_content.GetBinContent(i))) for i in range(1, sagitta_stat_syst_content.GetNbinsX() + 1)]

    mc_hist_divisor = mc_hist.Clone()
    [mc_hist_divisor.SetBinError(i, 0.0) for i in range(0, mc_hist_divisor.GetNbinsX() + 1)]

    data_hist.Add(mc_hist_divisor, -1.0)
    mc_hist.Add(mc_hist_divisor, -1.0)
    sagitta_stat_syst_content.Add(mc_hist, -1.0)

    sagitta_stat_syst = mc_hist.Clone()
    [sagitta_stat_syst.SetBinError(i,  sagitta_stat_syst_content.GetBinContent(i)) for i in range(1, sagitta_stat_syst_content.GetNbinsX() + 1)]

    total_syst = mc_hist.Clone()
    [total_syst.SetBinError(i, ( sagitta_stat_syst.GetBinError(i)**2 + mc_hist.GetBinError(i)**2) ** 0.5)  for i in range(1, mc_hist.GetNbinsX() + 1)]

    #ok we are ready to draw the histogams to show the systematics
    histograms = {}
    mc_hist_up = mc_hist.Clone()
    mc_hist_down = mc_hist.Clone()

    total_syst_up = total_syst.Clone()
    total_syst_down = total_syst.Clone()

    sagitta_stat_syst_up = sagitta_stat_syst.Clone()
    sagitta_stat_syst_down = sagitta_stat_syst.Clone()

    for i in range(1, mc_hist.GetNbinsX() + 1):
        mc_hist_up.SetBinContent(i, mc_hist.GetBinContent(i) + mc_hist.GetBinError(i))
        mc_hist_down.SetBinContent(i, mc_hist.GetBinContent(i) - mc_hist.GetBinError(i))
        mc_hist_up.SetBinError(i, 0.0)
        mc_hist_down.SetBinError(i, 0.0)

        total_syst_up.SetBinContent(i, total_syst.GetBinContent(i) + total_syst.GetBinError(i))
        total_syst_down.SetBinContent(i, total_syst.GetBinContent(i) - total_syst.GetBinError(i))
        total_syst_up.SetBinError(i, 0.0)
        total_syst_down.SetBinError(i, 0.0)

        sagitta_stat_syst_up.SetBinContent(i, sagitta_stat_syst.GetBinContent(i) + sagitta_stat_syst.GetBinError(i))
        sagitta_stat_syst_down.SetBinContent(i, sagitta_stat_syst.GetBinContent(i) - sagitta_stat_syst.GetBinError(i))
        sagitta_stat_syst_up.SetBinError(i, 0.0)
        sagitta_stat_syst_down.SetBinError(i, 0.0)

    histograms = {}

    histograms[data_channel] = data_hist
    histograms[mc_channel + "_total_up"] = total_syst_up
    histograms[mc_channel + "_total_down"] = total_syst_down
    histograms[mc_channel + "_total_up"].SetLineColor(ROOT.kBlue)
    histograms[mc_channel + "_total_down"].SetLineColor(ROOT.kBlue)

    histograms[mc_channel + "_sagitta_stat_up"] = sagitta_stat_syst_up
    histograms[mc_channel + "_sagitta_stat_down"] = sagitta_stat_syst_down
    histograms[mc_channel + "_sagitta_stat_up"].SetLineColor(ROOT.kRed)
    histograms[mc_channel + "_sagitta_stat_down"].SetLineColor(ROOT.kRed)

    histograms[mc_channel + "_stat_up"] = mc_hist_up
    histograms[mc_channel + "_stat_down"] = mc_hist_down
    histograms[mc_channel + "_stat_up"].SetLineColor(ROOT.kGreen + 2)
    histograms[mc_channel + "_stat_down"].SetLineColor(ROOT.kGreen + 2)

    return histograms

def draw_syst(histograms,  colours = None, styles = None, legend_labels = None, legend_coordinates = (0.6, 0.9, 0.5, 0.9), x_axis_label = "M_{#mu#mu} [GeV]", y_axis_label="Events", logy=False, extra_descr="", to_return = False, ftype = ".png", plot_dir = "plots", x_range = None, mins_maxes = None, savename=None, data_key = ""):

    from atlasplots import set_atlas_style
    set_atlas_style()
    ROOT.gStyle.SetLineWidth(1)
    ROOT.gStyle.SetFrameLineWidth(1)

    key = list(histograms.keys())[0]
    if x_axis_label is None:  x_axis_label= histograms[key].GetXaxis().GetTitle()
    if y_axis_label is None: y_axis_label= histograms[key].GetYaxis().GetTitle()

    to_plot = {key:histograms[key] for key in histograms if key != data_key}
    data = hist_to_tgrapherrors(histograms[data_key])
    if colours is not None: [to_plot[key].SetMarkerColor(colours[key]) for key in to_plot]
    if styles is not None: [to_plot[key].SetMarkerStyle(styles[key]) for key in to_plot]
    for key in to_plot: to_plot[key].SetMarkerSize(to_plot[key].GetMarkerSize()*1.5)
    for key in to_plot: to_plot[key].GetXaxis().SetTitleSize(22)
    for key in to_plot: to_plot[key].GetYaxis().SetTitleSize(22)

    legend = ROOT.TLegend(*legend_coordinates)
    if not legend_labels is None:
        for key in histograms:
            if key in legend_labels and key in to_plot:
               label = legend_labels[key]
               legend.AddEntry(to_plot[key], label, "F")
    if data_key in legend_labels:
        legend.AddEntry(histograms[data_key], legend_labels[data_key], "P")
    legend.SetBorderSize(0)

    identifier = " ".join([to_plot[key].GetName() for key in to_plot])
    canvas = ROOT.TCanvas("canv" + identifier, "canv " + identifier, 2 * 800 , 2 * 600)
    canvas.Draw()
    canvas.cd()

    canvas.SetTopMargin(canvas.GetTopMargin()*1.1)
    canvas.SetBottomMargin(canvas.GetBottomMargin()*1.1)
    canvas.SetRightMargin(canvas.GetRightMargin()*1.1)
    canvas.SetLeftMargin(canvas.GetLeftMargin()*1.1)

    if mins_maxes is None:
        mins = []
        maxs = []
        for i, key in enumerate(to_plot):
            stack = histograms[key]
            mins.append(get_extrema(stack, minimum=True, bounds=x_range))
            maxs.append(get_extrema(stack, minimum=False, bounds=x_range))

        mins.append(get_extrema(histograms[data_key], minimum=True, bounds=x_range))
        maxs.append(get_extrema(histograms[data_key], minimum=False, bounds=x_range))

        minimum = min(mins)
        maximum = max(maxs)
    else:
        minimum = mins_maxes[0]
        maximum = mins_maxes[1]

    text_size = 70
    label_size = 60

    for i, key in enumerate(to_plot):
        stack = to_plot[key]
        bin_width = histograms[key].GetBinLowEdge(3) - histograms[key].GetBinLowEdge(2)
        if y_axis_label is not None:
            stack.GetYaxis().SetTitle(y_axis_label)
        else: y_axis_label = stack.GetXaxis().GetTitle()
        if x_axis_label is not None:
            stack.GetXaxis().SetTitle(x_axis_label)
        else: x_axis_label = stack.GetYaxis().GetTitle()

        if x_range is not None: stack.GetXaxis().SetRangeUser(*x_range)
        stack.SetMaximum(maximum + (0.6 * (maximum-minimum)))
        stack.SetMinimum(minimum)

        stack.GetYaxis().SetTitleSize(text_size)
        stack.GetXaxis().SetTitleSize(text_size)
        stack.GetYaxis().SetLabelSize(label_size)
        stack.GetXaxis().SetLabelSize(label_size)
        #stack.GetXaxis().SetTitleOffset(1.05)
        if i == 0: stack.Draw("L HIST")
        else: stack.Draw("L HIST SAME")

    data.Draw("P SAME")

    ATLASLabel(0.20, 0.8, "Internal", size = 50, extra_descr = extra_descr)
    legend.SetTextSize(40)
    legend.Draw("SAME")

    if logy: canvas.SetLogy()

    global alive
    alive.append(locals())
    if to_return: return canvas, keep_alive
    else:
         if not os.path.exists(plot_dir):
             os.makedirs(plot_dir)
         if savename is None: canvas.Print(os.path.join(plot_dir, identifier + ftype))
         else: canvas.Print(os.path.join(plot_dir, savename + ftype))
