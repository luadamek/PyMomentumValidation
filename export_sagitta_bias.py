base_directories = {}
base_directories["delta_qm"] = "/scratch/ladamek/sagittabias_matrices/Injection_Dec17_inject_{inject}_method_{method}_region_{detector_location}_{end_string}_round_{round}/OutputFiles"
base_directories["matrix"] = "/scratch/ladamek/sagittabias_matrices/Injection_Dec17_inject_{inject}_region_{detector_location}_{end_string}_round_{round}/OutputFiles"
methods = ["delta_qm", "matrix"]

delta_qm_data_dir = "/scratch/ladamek/sagittabias_matrices/Data_Dec17_inject_None_method_delta_qm_region_{detector_location}_loose_preselection_tight_select_after_correction_round_{round}/OutputFiles"
delta_qm_mc_dir = base_directories["delta_qm"].format(inject="None", end_string="loose_preselection_tight_select_after_correction", method="delta_qm", detector_location="{detector_location}", round="{round}")
matrix_data_dir = "/scratch/ladamek/sagittabias_matrices/Injection_Dec17_Data_inject_None_region_{detector_location}_tight_select_after_correction_round_{round}/OutputFiles"
matrix_mc_dir = base_directories["matrix"].format(inject="None", end_string="loose_preselection_tight_select_after_correction", method="delta_qm", detector_location="{detector_location}", round="{round}")


files = [(), ()] #files for ID and ME
import ROOT as r
matrix_round = 7
delta_qm_round = 21
for method in methods:
    if "matrix" == method:
        from MatrixInversion import get_deltas_from_job
        global get_deltas_from_job
        roun = matrix_round
        nom_dir = delta_qm_data_dir
        sub_dir = matrix_mc_dir
        descriptor = "varmin"

    elif "delta_qm" == method:
        from DeltaQMIterativeMethod import get_deltas_from_job
        global get_deltas_from_job
        roun = delta_qm_round
        nom_dir = delta_qm_data_dir
        sub_dir = delta_qm_mc_dir
        descriptor = "detla_qm"

    output_filename = "{}.root".format(descriptor)
    f = r.TFile(output_filename, "RECREATE")

    for detector_location in ["ID", "ME"]:
        nom_dir = nom_dir.format(detector_location = detector_location, round = roun)
        sub_dir = sub_dir.format(detector_location = detector_location, round = roun)

        nom_hist = get_deltas_from_job(nom_dir)[0]
        sub_hist = get_deltas_from_job(sub_dir)[0]

        nom_hist.Add(sub_hist, -1.0)
        nom_hist.SetName("deltas_GeV_{}_{}".format(descriptor, detector_location))

        nom_hist.Write()
    f.Close()

