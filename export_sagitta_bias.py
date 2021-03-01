DATE = "Feb10"
base_directory = "/scratch/ladamek/sagittabias_matrices/Injection_" + DATE + "_{file_type}_inject_{inject}_method_{method}_region_{detector_location}_{end_string}_{syst_var}_round_{round}/OutputFiles/"
methods = ["delta_qm", "matrix"]

import ROOT as r
matrix_round = 7
delta_qm_round = 21
for mc_ftype, data_ftype in zip(["MC1516", "MC17", "MC18"], ["Data1516", "Data17", "Data18"]):
    for method in methods:
        if "matrix" == method:
            from MatrixInversion import get_deltas_from_job
            global get_deltas_from_job
            roun = matrix_round
            descriptor = "varmin_{}".format(data_ftype)

        elif "delta_qm" == method:
            from DeltaQMIterativeMethod import get_deltas_from_job
            global get_deltas_from_job
            roun = delta_qm_round
            descriptor = "delta_qm_{}".format(data_ftype)

        output_filename = "{}.root".format(descriptor)
        f = r.TFile(output_filename, "RECREATE")

        for detector_location in ["ID", "ME"]:
            nom_dir = base_directory.format(file_type=data_ftype, inject="None", method=method, detector_location=detector_location, end_string="loose_preselection_tight_select_after_correction", syst_var = "nom", round = roun)
            sub_dir = base_directory.format(file_type=mc_ftype, inject="None", method=method, detector_location=detector_location, end_string="loose_preselection_tight_select_after_correction", syst_var = "nom", round = roun)

            nom_dir = nom_dir.format(detector_location = detector_location, round = roun)
            sub_dir = sub_dir.format(detector_location = detector_location, round = roun)

            nom_hist = get_deltas_from_job(nom_dir)[0]
            sub_hist = get_deltas_from_job(sub_dir)[0]

            nom_hist.SetName("deltas_GeV_WARNING_UNCORRECTED_WARNING_{}_{}".format(descriptor, detector_location))
            nom_hist.Write()

            nom_hist.Add(sub_hist, -1.0)
            nom_hist.SetName("deltas_GeV_{}_{}".format(descriptor, detector_location))

            nom_hist.Write()
        f.Close()

