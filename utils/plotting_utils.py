import numpy as np
import ROOT
import array
import os
from atlasplots import set_atlas_style, atlas_label

def draw_2d_histogram(histogram, description = "", normalize = True, output_location=""):
    if normalize:
        extrema = [ abs(histogram.GetMaximum()), abs(histogram.GetMinimum())]
        histogram.SetMaximum(max(*extrema))
        histogram.SetMinimum(min(*[-1.0 * el for el in extrema]))
    canvas = ROOT.TCanvas("Canvas_" + histogram.GetName())
    histogram.Draw("COLZ")
    histogram.GetYaxis().SetTitleOffset(0.7*histogram.GetYaxis().GetTitleOffset())
    canvas.SetTopMargin(0.1)
    if description: atlas_label(0.15, 0.94, "Internal   {}".format(description))
    else: atlas_label(0.2, 0.94, "Internal")
    canvas.SetRightMargin(0.25)
    histogram.GetZaxis().SetTitleOffset(1.2 * histogram.GetZaxis().GetTitleOffset())
    canvas.SetBottomMargin(0.25)
    canvas.Draw()
    ROOT.gStyle.SetPalette(ROOT.kTemperatureMap)
    canvas.Print(os.path.join(output_location, canvas.GetName() + ".pdf"))

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
    l.SetTextSize(size)
    l.SetNDC()
    l.SetTextColor(color)
    l.DrawLatex(x, y, text)

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
    return graph

alive = []
def draw_data_vs_mc(histograms, ratio_min = 0.9, ratio_max = 1.1, colours = None, legend_labels = None, legend_coordinates = (0.6, 0.9, 0.5, 0.9), x_axis_label = "M_{#mu#mu} [GeV]", y_axis_label="Events", logy=False, extra_descr="", to_return = False, ftype = ".pdf", plot_dir = "plots", datakey = "data", extra_str = None):


    from atlasplots import set_atlas_style 
    set_atlas_style()
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
    minimum = min(summed.GetMinimum() /1.2, data_histogram.GetMinimum()/1.2)
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
    top.SetTopMargin(top.GetTopMargin()*1.1)

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
    x_size = stack.GetXaxis().GetTitleSize() * 1.6
    stack.GetYaxis().SetTitleSize(x_size)
    stack.GetXaxis().SetTitleSize(x_size)
    stack.GetYaxis().SetTitleOffset(stack.GetYaxis().GetTitleOffset() * 1.3)
    stack.GetXaxis().SetTitleOffset(stack.GetXaxis().GetTitleOffset() * 1.6)
    bin_width = stack.GetStack().Last().GetBinLowEdge(3) - stack.GetStack().Last().GetBinLowEdge(2)
    units = x_axis_label.split(" ")[-1].replace("[","").replace("]","") #get the units of the x-axis
    stack.GetYaxis().SetTitle("{} / {:.2f} {}".format(y_axis_label, bin_width, units))
    if logy: top.SetLogy()

    scale_ratio = (top.GetWh()*top.GetAbsHNDC())/(bottom.GetWh() * bottom.GetAbsHNDC())
    ratio_hist_for_axes.GetXaxis().SetLabelSize(stack.GetXaxis().GetLabelSize()*(scale_ratio))
    ratio_hist_for_axes.GetYaxis().SetLabelSize(stack.GetYaxis().GetLabelSize()*(scale_ratio))
    ratio_hist_for_axes.GetXaxis().SetTitleSize(stack.GetXaxis().GetTitleSize()*(scale_ratio))
    ratio_hist_for_axes.GetYaxis().SetTitleSize(stack.GetYaxis().GetTitleSize()*(scale_ratio))
    ratio_hist_for_axes.GetXaxis().SetTitleOffset(stack.GetXaxis().GetTitleOffset()/(0.6*scale_ratio))
    ratio_hist_for_axes.GetYaxis().SetTitleOffset(stack.GetYaxis().GetTitleOffset()/(scale_ratio))
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
    atlas_label(0.15, 0.90, "Internal")

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



def draw_histograms(histograms,  colours = None, styles = None, legend_labels = None, legend_coordinates = (0.6, 0.9, 0.5, 0.9), x_axis_label = "M_{#mu#mu} [GeV]", y_axis_label="Events", logy=False, extra_descr="", to_return = False, ftype = ".pdf", plot_dir = "plots"):

    from atlasplots import set_atlas_style
    set_atlas_style()
    ROOT.gStyle.SetLineWidth(1)
    ROOT.gStyle.SetFrameLineWidth(1)

    to_plot = {key:hist_to_tgrapherrors(histograms[key]) for key in histograms}
    if colours is not None: [to_plot[key].SetMarkerColor(colours[key]) for key in to_plot]
    if styles is not None: [to_plot[key].SetMarkerStyle(styles[key]) for key in to_plot]
    for key in to_plot: to_plot[key].SetMarkerSize(to_plot[key].GetMarkerSize()*1.5)
    for key in to_plot: to_plot[key].GetXaxis().SetTitleSize(to_plot[key].GetXaxis().GetTitleSize()*2.0)
    for key in to_plot: to_plot[key].GetYaxis().SetTitleSize(to_plot[key].GetYaxis().GetTitleSize()*2.0)

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

    mins = []
    maxs = []
    for i, key in enumerate(to_plot):
        stack = histograms[key]
        mins.append(stack.GetMinimum())
        maxs.append(stack.GetMaximum())

    minimum = min(mins)
    maximum = max(maxs)

    for i, key in enumerate(to_plot):
        stack = to_plot[key]
        bin_width = histograms[key].GetBinLowEdge(3) - histograms[key].GetBinLowEdge(2)
        stack.GetYaxis().SetTitle(y_axis_label)
        stack.GetXaxis().SetTitle(x_axis_label)
        stack.SetMaximum(maximum + (0.6 * (maximum-minimum)))
        stack.SetMinimum(minimum)
        if i == 0: stack.Draw("AP")
        else: stack.Draw("P SAME")
       

    legend.Draw("SAME")

    if logy: canvas.SetLogy()

    global alive
    alive.append(locals())
    if to_return: return canvas, keep_alive
    else:
         if not os.path.exists(plot_dir):
             os.makedirs(plot_dir)
         canvas.Print(os.path.join(plot_dir, identifier + ftype))