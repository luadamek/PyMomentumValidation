def calc_afb(nf, nb, nf_err, nb_err):
    afb = (nf - nb)/(nf + nb)

    def err_term(a, b):
        return (2.0 * b)/( ( a + b ) ** 2 )

    afb_err = afb * ( (err_term(nf, nb) * nf_err)**2 + (err_term(nb, nf) ** nb_err)**2)**0.5

    return afb, afb_err


def get_afb_hist(hist_nf, hist_nb):
    hist_return = hist_nf.Clone(hist_nf.GetName() + "_AFB_Symmetry")
    for i in range(1, hist_nf.GetNbinsX() + 1):
        nf = hist_nf.GetBinContent(i)
        nf_err = hist_nf.GetBinError(i)
        nb = hist_nb.GetBinContent(i)
        nb_err = hist_nb.GetBinError(i)
        afb, afb_err = calc_afb(nf, nb, nf_err, nb_err)
        hist_return.SetBinContent(afb)
        hist_return.SetBinError(afb_err)

    return hist_return

