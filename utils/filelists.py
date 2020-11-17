#the location of the directories on eos
import os
if os.getenv("USER") == "ladamek":

    if "gra" in os.getenv("HOSTNAME"): dir_v03="/project/def-psavard/ladamek/ForLukas/muonptcalib_v03_combined/merged/"
    if "cedar" in os.getenv("HOSTNAME"): dir_v03="/project/def-psavard/ForLukas/muonptcalib_v03_combined/merged/"

directories = {}
directories["v03"] = dir_v03

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
