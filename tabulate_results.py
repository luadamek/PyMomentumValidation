import pandas as pd

directory = "/project/def-psavard/ladamek/momentumvalidationoutput/"
from histogram_manager import HistogramManager
import os

job_names = [\
"Feb10_matrix_uncorr_calib_7",\
"Feb10_matrix_mconly_calib_7",\
"Feb10_matrix_calib_7",\
"Feb10_deltaqm_uncorr_calib_21",\
"Feb10_deltaqm_mconly_calib_21",\
"Feb10_deltaqm_calib_21",\
"Feb10_nocalib",\
]

job_names_to_method = {\
"Feb10_matrix_uncorr_calib_7":"varmin",\
"Feb10_matrix_mconly_calib_7":"varmin",\
"Feb10_matrix_calib_7":"varmin",\
"Feb10_deltaqm_uncorr_calib_21":"deltaqm",\
"Feb10_deltaqm_mconly_calib_21":"deltaqm",\
"Feb10_deltaqm_calib_21":"deltaqm",\
"Feb10_nocalib":"none",
}

job_names_to_correction = {\
"Feb10_matrix_uncorr_calib_7":"N",\
"Feb10_matrix_mconly_calib_7":"N",\
"Feb10_matrix_calib_7":"Y",\
"Feb10_deltaqm_uncorr_calib_21":"N",\
"Feb10_deltaqm_mconly_calib_21":"N",\
"Feb10_deltaqm_calib_21":"Y",\
"Feb10_nocalib":"N",
}

job_names_to_file = {\
"Feb10_matrix_uncorr_calib_7":"Data",\
"Feb10_matrix_mconly_calib_7":"MC",\
"Feb10_matrix_calib_7":"Data",\
"Feb10_deltaqm_uncorr_calib_21":"Data",\
"Feb10_deltaqm_mconly_calib_21":"MC",\
"Feb10_deltaqm_calib_21":"Data",\
"Feb10_nocalib":"Data,MC",
}


for data_key, mc_key in zip(["Data", "Data1516", "Data17", "Data18"], ["MC", "MC1516", "MC17", "MC18"]):
    data = {"Track Type": [],"Method":[], "Corrected":[], "Data_or_MC":[], "RMS [GeV]":[], "RMS Stat Err [GeV]": [], "Mean [GeV]":[], "Mean Stat Err [GeV]": []}
    for location in ["ID", "ME"]:
        for jn in job_names:
           method = job_names_to_method[jn]
           corrected = job_names_to_correction[jn]
           filetype = job_names_to_file[jn]
           for ft in filetype.split(","):
               if ft == "MC": ft = mc_key
               if ft == "Data": ft = data_key
               data["Method"].append(method)
               data["Corrected"].append(corrected)
               data["Data_or_MC"].append(ft)
               data["Track Type"].append(location)

               file_to_read = os.path.join(directory, jn, "Output.root")
               histogram_to_get = "MassSpectrum_{location}_{identified}".format(location=location, identified="Inclusive")

               histogram_manager = HistogramManager(file_to_read)
               histogram_manager.merge_channels("MC", ["MC1516", "MC17", "MC18"])
               histogram_manager.merge_channels("Data", ["Data1516", "Data17", "Data18"])

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
    print(data_key, mc_key)
    for to_sel in [data_key, mc_key]:

        sel_df = dataframe.query(" Data_or_MC == \"{}\"".format(to_sel))[[c for c in dataframe.columns if "Data" not in c]]
        sel_df.reset_index(drop=True)
        to_print = sel_df.to_latex(formatters={"RMS Stat Err [GeV]":lambda x : "{:0.4f}".format(x), "RMS [GeV]":lambda x : "{:0.4f}".format(x), "Mean [GeV]":lambda x : "{:0.4f}".format(x), "Mean Stat Err [GeV]":lambda x : "{:0.4f}".format(x)}, index=False)
        print(to_print)

