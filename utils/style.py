import ROOT as root
def set_style(style):
    """Sets the global ROOT plot style to the ATLAS Style.
    Parameters
    ----------
    tsize : float, optional
        Text size in pixels. The default is `None`, in which case it will use
        the default text size defined in `AtlasStyle()`.
    """
    print("\u001b[34;1mApplying ATLAS style settings\u001b[0m")

    # Release ownership, otherwise lost when moved out of scope
    root.SetOwnership(style, False)

    root.gROOT.SetStyle("ATLAS")
    root.gROOT.ForceStyle()

def get_atlas_style():
    import atlasplots
    return atlasplots.atlasstyle.atlas_style()
