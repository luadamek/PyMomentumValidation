import pandas as pd

directory = "/project/def-psavard/ladamek/momentumvalidationoutput/"
from histogram_manager import HistogramManager
import os

job_names = [\
"Jan28_matrix_calib_7_uncorr",\
"Jan28_matrix_calib_7_MC_only",\
"Jan28_matrix_calib_7",\
"Jan28_deltaqm_calib_21_uncorr",\
"Jan28_deltaqm_calib_21_MC_only",\
"Jan28_deltaqm_calib_21",\
"Jan28_nocalib",\
]

job_names_to_method = {\
"Jan28_matrix_calib_7_uncorr":"matrix",\
"Jan28_matrix_calib_7_MC_only":"matrix",\
"Jan28_matrix_calib_7":"matrix",\
"Jan28_deltaqm_calib_21_uncorr":"deltaqm",\
"Jan28_deltaqm_calib_21_MC_only":"deltaqm",\
"Jan28_deltaqm_calib_21":"deltaqm",\
"Jan28_nocalib":"none",
}

job_names_to_correction = {\
"Jan28_matrix_calib_7_uncorr":"N",\
"Jan28_matrix_calib_7_MC_only":"N",\
"Jan28_matrix_calib_7":"Y",\
"Jan28_deltaqm_calib_21_uncorr":"N",\
"Jan28_deltaqm_calib_21_MC_only":"N",\
"Jan28_deltaqm_calib_21":"Y",\
"Jan28_nocalib":"N",
}

job_names_to_file = {\
"Jan28_matrix_calib_7_uncorr":"Data",\
"Jan28_matrix_calib_7_MC_only":"MC",\
"Jan28_matrix_calib_7":"Data",\
"Jan28_deltaqm_calib_21_uncorr":"Data",\
"Jan28_deltaqm_calib_21_MC_only":"MC",\
"Jan28_deltaqm_calib_21":"Data",\
"Jan28_nocalib":"Data,MC",
}



data = {"Method":[], "Corrected":[], "Data_or_MC":[], "RMS [GeV]":[], "RMS Stat Err [GeV]": [], "Mean [GeV]":[], "Mean Stat Err [GeV]": [], "Track Type": []}
for location in ["ID", "ME"]:
    for jn in job_names:
       method = job_names_to_method[jn]
       corrected = job_names_to_correction[jn]
       filetype = job_names_to_file[jn]
       for ft in filetype.split(","):
           data["Method"].append(method)
           data["Corrected"].append(corrected)
           data["Data_or_MC"].append(ft)
           data["Track Type"].append(location)

           file_to_read = os.path.join(directory, jn, "Output.root")
           histogram_to_get = "MassSpectrum_{location}_{identified}".format(location=location, identified="Inclusive")

           histogram_manager = HistogramManager(file_to_read)
           histogram = histogram_manager.get_histograms(histogram_to_get)[ft] 

           rms = histogram.GetRMS()
           rms_err = histogram.GetRMSError()
           mean = histogram.GetMean()
           mean_err = histogram.GetMeanError()

           data["RMS [GeV]"].append(rms)
           data["RMS Stat Err [GeV]"].append(rms_err)
           data["Mean [GeV]"].append(mean)
           data["Mean Stat Err [GeV]"].append(mean_err)

dataframe = pd.DataFrame.from_dict(data)
dataframe.reset_index()
for to_sel in ["Data", "MC"]:

    sel_df = dataframe.query(" Data_or_MC == \"{}\"".format(to_sel))[[c for c in dataframe.columns if "Data" not in c]]
    to_print = sel_df.to_latex(formatters={"RMS Stat Err [GeV]":lambda x : "{:0.4f}".format(x), "RMS [GeV]":lambda x : "{:0.4f}".format(x), "Mean [GeV]":lambda x : "{:0.4f}".format(x), "Mean Stat Err [GeV]":lambda x : "{:0.4f}".format(x)})
    print(to_print)

