#the location of the files on eos
if os.getenv("USER") == "ladamek":
    dir_v03="/project/def-psavard/ForLukas/muonptcalib_v03_combined/merged/"

def merge_basedir_into_files(basedir, files):
    with_directory = []
    for el in files:
        with_directory.append(os.path.join(basedir, el))
    return with_directory

files["v03"] = {}
files["v03"]["Data"] = merge_basedir_into_files( dir_v03,  ["data_{}.root".format(el) for el in ["1516", "17", "18"])
files["v03"]["DY_MC"] = merge_basedir_into_files( dir_v03,  ["DYmumu_mc16{}.root".format(el) for el in ["a", "d", "e"])
