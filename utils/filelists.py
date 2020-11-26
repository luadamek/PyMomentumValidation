#the location of the directories on eos
import os
if os.getenv("USER") == "ladamek":

    if "gra" in os.getenv("HOSTNAME"): dir_v03="/project/def-psavard/ladamek/ForLukas/muonptcalib_v03_combined/merged/"
    if "gra" in os.getenv("HOSTNAME"): dir_v03_v2="/project/def-psavard/ladamek/ForLukas/muonptcalib_v03_combined/v2/"
    if "cedar" in os.getenv("HOSTNAME"): dir_v03="/project/def-psavard/ForLukas/muonptcalib_v03_combined/merged/"

directories = {}
directories["v03"] = dir_v03
directories["v03_v2"] = dir_v03_v2

files = {}
files["v03"] = {}
files["v03"]["Data"] = ["data_{}.root".format(el) for el in ["1516", "17", "18"]]
files["v03"]["MC"] = ["Sig_Z_mc16{}.root".format(el) for el in ["d", "e"]]
files["v03"]["Data1516"] = ["data_{}.root".format(el) for el in ["1516"]]
files["v03"]["Data17"] = ["data_{}.root".format(el) for el in ["17"]]
files["v03"]["Data18"] = ["data_{}.root".format(el) for el in ["18"]]
#files["v03"]["MC"] = ["Sig_Z_mc16{}.root".format(el) for el in ["d", "e"]] #will be updated when available
files["v03"]["MC17"] = ["Sig_Z_mc16{}.root".format(el) for el in ["d"]]
files["v03"]["MC18"] = ["Sig_Z_mc16{}.root".format(el) for el in ["e"]]

files["v03_v2"] = {}
files["v03_v2"]["Data"] = ["data/data{}_13TeV.*.physics_Main.PhysCont*.root".format(el) for el in ["15", "16", "17", "18"]]
files["v03_v2"]["MC"] = ["split/mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r9364", "r10201", "r10724"]]
files["v03_v2"]["MC_JPSI"] = ["split/mc16_13TeV.*.Pythia8B_A14_CTEQ6L1_Jpsimu6*{}*.root".format(el) for el in ["r9364", "r10201", "r10724"]]
files["v03_v2"]["Data1516"] = ["data/data{}_13TeV.*.physics_Main.PhysCont*.root".format(el) for el in ["15", "16"]]
files["v03_v2"]["Data17"] = ["data/data{}_13TeV.*.physics_Main.PhysCont*.root".format(el) for el in ["17"]]
files["v03_v2"]["Data18"] = ["data/data{}_13TeV.*.physics_Main.PhysCont*.root".format(el) for el in ["18"]]
files["v03_v2"]["MC1516"] = ["split/mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r9364"]]
files["v03_v2"]["MC17"] = ["split/mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r10201"]]
files["v03_v2"]["MC18"] = ["split/mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r10724"]]
files["v03_v2"]["MC1516_JPSI"] = ["split/mc16_13TeV.*.Pythia8B_A14_CTEQ6L1_Jpsimu6*{}*.root".format(el) for el in ["r9364"]]
files["v03_v2"]["MC17_JPSI"] = ["split/mc16_13TeV.*.Pythia8B_A14_CTEQ6L1_Jpsimu6*{}*.root".format(el) for el in ["r10201"]]
files["v03_v2"]["MC18_JPSI"] = ["split/mc16_13TeV.*.Pythia8B_A14_CTEQ6L1_Jpsimu6*{}*.root".format(el) for el in ["r10724"]]
