#the location of the directories on eos
import os
if os.getenv("USER") == "ladamek":
    if "gra" in os.getenv("HOSTNAME"): dir_v03="/project/def-psavard/ladamek/ForLukas/muonptcalib_v03_combined/"
    if "gra" in os.getenv("HOSTNAME"): dir_v03_v2="/project/def-psavard/ladamek/ForLukas/muonptcalib_v03_combined/v2/"
    if "cedar" in os.getenv("HOSTNAME") or "cdr" in os.getenv("HOSTNAME"): dir_v03="/project/def-psavard/ForLukas/muonptcalib_v03_combined/"
    if "cedar" in os.getenv("HOSTNAME") or "cdr" in os.getenv("HOSTNAME"): dir_v03_v2="/project/def-psavard/ForLukas/muonptcalib_v03_combined/v2/"
    if "cedar" in os.getenv("HOSTNAME") or "cdr" in os.getenv("HOSTNAME"): dir_v05="/project/def-psavard/ForLukas/muonptcalib_v05_merged_Min/"
    if "graham" in os.getenv("HOSTNAME") or "gra" in os.getenv("HOSTNAME"): dir_v05="/project/def-psavard/ladamek/ForLukas/muonptcalib_v05_merged_Min/"
    if "graham" in os.getenv("HOSTNAME") or "gra" in os.getenv("HOSTNAME"): dir_v05_standardvars="/project/def-psavard/ladamek/ForLukas/muonptcalib_v05_standardvars/"
    if "cedar" in os.getenv("HOSTNAME") or "cdr" in os.getenv("HOSTNAME"): dir_v05_standardvars="/project/def-psavard/ladamek/ForLukas/muonptcalib_v05_standardvars/"

directories = {}
directories["v03"] = dir_v03
directories["v03_v2"] = dir_v03_v2
directories["v05"] = dir_v05
directories["v05_standardvars"] = dir_v05_standardvars
directories["v05_standardvars_trimmed"] = dir_v05_standardvars
directories["TEST"] = dir_v05_standardvars

files = {}
files["v03"] = {}
files["v03"]["Data"] = ["merge/data_{}.root".format(el) for el in ["1516", "17", "18"]]
files["v03"]["MC"] = ["merged/Sig_Z_mc16{}.root".format(el) for el in ["d", "e"]]
files["v03"]["Data1516"] = ["merged/data_{}.root".format(el) for el in ["1516"]]
files["v03"]["Data17"] = ["merged/data_{}.root".format(el) for el in ["17"]]
files["v03"]["Data18"] = ["merged/data_{}.root".format(el) for el in ["18"]]
#files["v03"]["MC"] = ["merged/Sig_Z_mc16{}.root".format(el) for el in ["d", "e"]] #will be updated when available
files["v03"]["MC17"] = ["merged/Sig_Z_mc16{}.root".format(el) for el in ["d"]]
files["v03"]["MC18"] = ["merged/Sig_Z_mc16{}.root".format(el) for el in ["e"]]

files["v03_v2"] = {}
files["v03_v2"]["Data"] = ["data/data{}_13TeV.*.physics_Main.PhysCont*.root".format(el) for el in ["15", "16", "17", "18"]]
files["v03_v2"]["MC"] = ["split/mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r9364", "r10201", "r10724"]]
files["v03_v2"]["MCCalib"] = ["split/mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r9364", "r10201", "r10724"]]
files["v03_v2"]["MC_JPSI"] = ["split/mc16_13TeV.*.Pythia8B_A14_CTEQ6L1_Jpsimu6*{}*.root".format(el) for el in ["r9364", "r10201", "r10724"]]
files["v03_v2"]["Data1516"] = ["data/data{}_13TeV.*.physics_Main.PhysCont*.root".format(el) for el in ["15", "16"]]
files["v03_v2"]["Data17"] = ["data/data{}_13TeV.*.physics_Main.PhysCont*.root".format(el) for el in ["17"]]
files["v03_v2"]["Data18"] = ["data/data{}_13TeV.*.physics_Main.PhysCont*.root".format(el) for el in ["18"]]
files["v03_v2"]["MC1516"] = ["split/mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r9364"]]
files["v03_v2"]["MC17"] = ["split/mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r10201"]]
files["v03_v2"]["MC18"] = ["split/mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r10724"]]
files["v03_v2"]["MC1516Calib"] = ["split/mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r9364"]]
files["v03_v2"]["MC17Calib"] = ["split/mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r10201"]]
files["v03_v2"]["MC18Calib"] = ["split/mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r10724"]]
files["v03_v2"]["MC1516_JPSI"] = ["split/mc16_13TeV.*.Pythia8B_A14_CTEQ6L1_Jpsimu6*{}*.root".format(el) for el in ["r9364"]]
files["v03_v2"]["MC17_JPSI"] = ["split/mc16_13TeV.*.Pythia8B_A14_CTEQ6L1_Jpsimu6*{}*.root".format(el) for el in ["r10201"]]
files["v03_v2"]["MC18_JPSI"] = ["split/mc16_13TeV.*.Pythia8B_A14_CTEQ6L1_Jpsimu6*{}*.root".format(el) for el in ["r10724"]]

files["v05"] = {}
files["v05"]["Data"] = ["data{}_13TeV.*.physics_Main.PhysCont*.root".format(el) for el in ["15", "16", "17", "18"]]
files["v05"]["DataTEST"] = ["data15_13TeV.periodAllYear.physics_Main.PhysCont.DAOD_MUON1.grp15_v01_p4144_muonptcalib_v05_EXT0_0.root"]
files["v05"]["MC"] = ["mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r9364", "r10201", "r10724"]]
#files["v05"]["MCCalib"] = ["mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r9364", "r10201", "r10724"]]
files["v05"]["MCSherpa"] = ["mc16_13TeV.364*.Sh_*{}*.root".format(el) for el in ["r9364", "r10201", "r10724"]]
files["v05"]["MCMadGraph"] = ["mc16_13TeV.363*.MG_Ht*{}*.root".format(el) for el in ["r9364", "r10201", "r10724"]]
files["v05"]["MCTTbar"] = ["mc16_13TeV.41047*ttbar*nonallhad*{}*.root".format(el) for el in ["r9364", "r10201", "r10724"]]
#files["v05"]["MCSherpaCalib"] = ["mc16_13TeV.364*.Sh_*{}*.root".format(el) for el in ["r9364", "r10201", "r10724"]]
files["v05"]["MC_JPSI"] = ["mc16_13TeV.*.Pythia8B_A14_CTEQ6L1_Jpsimu6*{}*.root".format(el) for el in ["r9364", "r10201", "r10724"]]
files["v05"]["Data1516"] = ["data{}_13TeV.*.physics_Main.PhysCont*.root".format(el) for el in ["15", "16"]]
files["v05"]["Data17"] = ["data{}_13TeV.*.physics_Main.PhysCont*.root".format(el) for el in ["17"]]
files["v05"]["Data18"] = ["data{}_13TeV.*.physics_Main.PhysCont*.root".format(el) for el in ["18"]]
files["v05"]["MC1516"] = ["mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r9364"]]

files["v05"]["Data18_Rel22"] = ["/../muonptcalib_rel22_v01/data18*.root"]
files["v05"]["Data17_Rel22"] = ["/../muonptcalib_rel22_v01/data17*.root"]

#files["v05"]["MC17_resbias_up"] = ["mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r10201"]]
#files["v05"]["MC18_resbias_up"] = ["mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r10724"]]
#files["v05"]["MC1516_resbias_up"] = ["mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r9364"]]

#files["v05"]["MC17_resbias_down"] = ["mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r10201"]]
#files["v05"]["MC18_resbias_down"] = ["mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r10724"]]
#files["v05"]["MC1516_resbias_down"] = ["mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r9364"]]

#files["v05"]["MC17_resbias_up_ID"] = ["mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r10201"]]
#files["v05"]["MC18_resbias_up_ID"] = ["mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r10724"]]
#files["v05"]["MC1516_resbias_up_ID"] = ["mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r9364"]]

#files["v05"]["MC17_resbias_down_ID"] = ["mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r10201"]]
#files["v05"]["MC18_resbias_down_ID"] = ["mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r10724"]]
#files["v05"]["MC1516_resbias_down_ID"] = ["mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r9364"]]

#files["v05"]["MC17_resbias_up_ME"] = ["mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r10201"]]
#files["v05"]["MC18_resbias_up_ME"] = ["mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r10724"]]
#files["v05"]["MC1516_resbias_up_ME"] = ["mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r9364"]]

#files["v05"]["MC17_resbias_down_ME"] = ["mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r10201"]]
#files["v05"]["MC18_resbias_down_ME"] = ["mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r10724"]]
#files["v05"]["MC1516_resbias_down_ME"] = ["mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r9364"]]

files["v05"]["MC17_stat_up"] = ["mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r10201"]]
files["v05"]["MC18_stat_up"] = ["mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r10724"]]
files["v05"]["MC1516_stat_up"] = ["mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r9364"]]

files["v05"]["MC17_stat_down"] = ["mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r10201"]]
files["v05"]["MC18_stat_down"] = ["mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r10724"]]
files["v05"]["MC1516_stat_down"] = ["mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r9364"]]

#################
files["v05"]["MC17_scale_up"] = ["mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r10201"]]
files["v05"]["MC18_scale_up"] = ["mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r10724"]]
files["v05"]["MC1516_scale_up"] = ["mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r9364"]]

files["v05"]["MC17_scale_down"] = ["mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r10201"]]
files["v05"]["MC18_scale_down"] = ["mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r10724"]]
files["v05"]["MC1516_scale_down"] = ["mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r9364"]]


######################
files["v05"]["MC17_res_up"] = ["mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r10201"]]
files["v05"]["MC18_res_up"] = ["mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r10724"]]
files["v05"]["MC1516_res_up"] = ["mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r9364"]]

files["v05"]["MC17_res_down"] = ["mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r10201"]]
files["v05"]["MC18_res_down"] = ["mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r10724"]]
files["v05"]["MC1516_res_down"] = ["mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r9364"]]

#files["v05"]["MC17_stat_random_up"] = ["data{}_13TeV.*.physics_Main.PhysCont*.root".format(el) for el in ["17"]]
#files["v05"]["MC18_stat_random_up"] = ["data{}_13TeV.*.physics_Main.PhysCont*.root".format(el) for el in ["18"]]
#files["v05"]["MC1516_stat_random_up"] = ["mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r9364"]]

#files["v05"]["MC17_stat_random_down"] = ["data{}_13TeV.*.physics_Main.PhysCont*.root".format(el) for el in ["17"]]
#files["v05"]["MC18_stat_random_down"] = ["data{}_13TeV.*.physics_Main.PhysCont*.root".format(el) for el in ["18"]]
#files["v05"]["MC1516_stat_random_down"] = ["mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r9364"]]

files["v05"]["MC17"] = ["mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r10201"]]
files["v05"]["MC18"] = ["mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r10724"]]
files["v05"]["MCSherpa1516"] = ["mc16_13TeV.364*.Sh_*{}*.root".format(el) for el in ["r9364"]]
files["v05"]["MCSherpa17"] = ["mc16_13TeV.364*.Sh_*{}*.root".format(el) for el in ["r10201"]]
files["v05"]["MCSherpa18"] = ["mc16_13TeV.364*.Sh_*{}*.root".format(el) for el in ["r10724"]]
#files["v05"]["MC1516Calib"] = ["mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r9364"]]
#files["v05"]["MC17Calib"] = ["mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r10201"]]
#files["v05"]["MC18Calib"] = ["mc16_13TeV.*.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu*{}*.root".format(el) for el in ["r10724"]]
#files["v05"]["MCSherpa1516Calib"] = ["mc16_13TeV.364*.Sh_*{}*.root".format(el) for el in ["r9364"]]
#files["v05"]["MCSherpa17Calib"] = ["mc16_13TeV.364*.Sh_*{}*.root".format(el) for el in ["r10201"]]
#files["v05"]["MCSherpa18Calib"] = ["mc16_13TeV.364*.Sh_*{}*.root".format(el) for el in ["r10724"]]
files["v05"]["MC1516_JPSI"] = ["mc16_13TeV.*.Pythia8B_A14_CTEQ6L1_Jpsimu6*{}*.root".format(el) for el in ["r9364"]]
files["v05"]["MC17_JPSI"] = ["mc16_13TeV.*.Pythia8B_A14_CTEQ6L1_Jpsimu6*{}*.root".format(el) for el in ["r10201"]]
files["v05"]["MC18_JPSI"] = ["mc16_13TeV.*.Pythia8B_A14_CTEQ6L1_Jpsimu6*{}*.root".format(el) for el in ["r10724"]]
files["v05"]["MCTTbar1516"] = ["mc16_13TeV.41047*ttbar*nonallhad*{}*.root".format(el) for el in ["r9364"]]
files["v05"]["MCTTbar17"] = ["mc16_13TeV.41047*ttbar*nonallhad*{}*.root".format(el) for el in ["r10201"]]
files["v05"]["MCTTbar18"] = ["mc16_13TeV.41047*ttbar*nonallhad*{}*.root".format(el) for el in ["r10724"]]

files["v05_standardvars"] = files["v05"]
files["v05_standardvars_trimmed"] = {key:files["v05_standardvars"][key] for key in files["v05_standardvars"] if ("1516" in key or "17" in key or "18" in key) }
files["TEST"] = {"TEST":files["v05"]["MC1516"]}
