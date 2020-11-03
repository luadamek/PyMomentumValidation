#the location of the directories on eos
import os
if os.getenv("USER") == "ladamek":
    dir_v03="/project/def-psavard/ForLukas/muonptcalib_v03_combined/merged/"

directories = {}
directories["v03"] = dir_v03

files = {}
files["v03"] = {}
files["v03"]["Data"] = ["data_{}.root".format(el) for el in ["1516", "17", "18"]]
files["v03"]["MC"] = ["Sig_Z_mc16{}.root".format(el) for el in ["d", "e"]]
