
import utils
from batchsub import Job, JobSet
import os
import argparse

from variables import \
                      calc_pos_id_pt, calc_neg_id_pt,\
                      calc_pos_ms_pt, calc_neg_ms_pt,\
                      calc_pos_cb_pt, calc_neg_cb_pt,\
                      calc_pos_id_eta, calc_neg_id_eta,\
                      calc_pos_ms_eta, calc_neg_ms_eta,\
                      calc_pos_cb_eta, calc_neg_cb_eta,\
                      calc_pos_id_phi, calc_neg_id_phi,\
                      calc_pos_ms_phi, calc_neg_ms_phi,\
                      calc_pos_cb_phi, calc_neg_cb_phi

#file_type = "MC"
#detector_location = "ID"
#injection = "Global"
#outfile_base = "output_{}.pkl"
#output_location = "/project/def-psavard/ladamek/sagitta_bias_matrices"

parser = argparse.ArgumentParser(description='Parse Arguments')
parser.add_argument('--outfile_base', type=str, required = False, dest='outfile_base', default = "output_{}.pkl")
parser.add_argument('--output', type=str, dest='output', required=True)
parser.add_argument('--job_base', type=str, required=True, dest="job_base")
parser.add_argument('--test', action="store_true", dest="test")
parser.add_argument('--version', type=str, required=True, dest="version")
args = parser.parse_args()

outfile_base = args.outfile_base
output = args.output
test = args.test
job_base = args.job_base
version = args.version

def get_vars(variables):
    xvar_name = variables["x_var"]
    yvar_name = variables["y_var"]
    if xvar_name == "ID_Eta":
        xvar_pos = calc_pos_id_eta
        xvar_neg = calc_neg_id_eta
    elif xvar_name == "MS_Eta":
        xvar_pos = calc_pos_ms_eta
        xvar_neg = calc_neg_ms_eta
    else: raise ValueError()
    if yvar_name == "ID_Phi":
        yvar_pos = calc_pos_id_phi
        yvar_neg = calc_neg_id_phi
    elif yvar_name == "MS_Phi":
        yvar_pos = calc_pos_ms_phi
        yvar_neg = calc_neg_ms_phi
    else: raise ValueError()
    return xvar_pos, xvar_neg, yvar_pos, yvar_neg

inject_corrections = []

from MatrixInversion import get_deltas_from_job
from BiasCorrection import SagittaBiasCorrection
#for the first correction, load the global correction
base_directory = "/project/def-psavard/ladamek/sagitta_bias_matrices/Injection_Nov24_{region}_{channel}_Inject_{inject_type}_v03_v2/OutputFiles"
for detector_location in ["MS", "ID"]:
    for injection in ["Data", "Global", "Local", "GlobalPlusLocal", "None"]:
        directory = base_directory.format(region = detector_location, inject_type = injection, channel="MC")
        print(directory)
        deltas, variables, detector_location = get_deltas_from_job(directory)
        xvar_pos, xvar_neg, yvar_pos, yvar_neg = get_vars(variables)
        inject_corrections.append({"inject": injection, "correction": SagittaBiasCorrection([deltas.Clone(deltas.GetName() + "Clone")], xvar_pos, xvar_neg, yvar_pos, yvar_neg, flavour = detector_location), "channel":"MC", "extra_str":"TestMC", "detector_location": detector_location})

        directory = base_directory.format(region = detector_location, inject_type = "None", channel="MC")
        deltas_sub, variables, detector_location = get_deltas_from_job(directory)
        deltas.Add(deltas_sub, -1.0) #apply the correction
        inject_corrections.append({"inject": injection, "correction": SagittaBiasCorrection([deltas.Clone(deltas.GetName() + "Clone")], xvar_pos, xvar_neg, yvar_pos, yvar_neg, flavour = detector_location), "channel":"MC", "extra_str":"TestMCCorr", "detector_location": detector_location})
        if args.test: break

    deltas.Add(deltas_sub, -1.0) #apply the correction

    directory = base_directory.format(region = detector_location, inject_type = "None", channel="Data")
    deltas, variables, detector_location = get_deltas_from_job(directory)

    xvar_pos, xvar_neg, yvar_pos, yvar_neg = get_vars(variables)
    inject_corrections.append({"inject": "None", "correction": SagittaBiasCorrection([deltas.Clone(deltas.GetName() + "Clone")], xvar_pos, xvar_neg, yvar_pos, yvar_neg, flavour = detector_location), "channel":"Data", "extra_str":"TestData", "detector_location": detector_location})

    directory = base_directory.format(region = detector_location, inject_type = "None", channel="MC")
    deltas_sub, variables, detector_location = get_deltas_from_job(directory)

    deltas.Add(deltas_sub, -1.0) #apply the correction
    inject_corrections.append({"inject": "None", "correction": SagittaBiasCorrection([deltas.Clone(deltas.GetName() + "Clone")], xvar_pos, xvar_neg, yvar_pos, yvar_neg, flavour = detector_location), "channel":"Data", "extra_str":"TestDataCorr", "detector_location": detector_location})
    if args.test: break


base_commands = utils.get_setup_commands()

job_descr = "Stats_{}".format(version)
jobset = JobSet(job_descr)
for ij in inject_corrections:
    detector_location = ij["detector_location"]
    correction = ij["correction"]
    inject = ij["inject"]
    channel = ij["channel"]
    extra_str = ij["extra_str"]
    descriptor = "{}_{}_{}_{}".format(detector_location, inject, channel, extra_str)

    output_location = os.path.join(output, descriptor)
    if not os.path.exists(output_location): os.makedirs(output_location)

    this_correction_pkl_file = os.path.join(output_location, "Correction.pkl")
    with open(this_correction_pkl_file, "wb") as f:
        import pickle as pkl
        pkl.dump(correction, f)

    root_files = utils.get_files(version)[channel]
    for file_count, root_file in enumerate(root_files):
        entrysteps = utils.get_entry_steps(root_file, step_size = 2000000, tree_name = "MuonMomentumCalibrationTree")
        for job_count, startstop in enumerate(entrysteps):
            print(startstop)
            start = startstop[0]
            stop = startstop[1]
            jobname = "stats_job_{}".format(descriptor) + "_file_{}_job_{}".format(file_count, job_count)
            output_filename = outfile_base.format(job_count)
            base_output_path = os.path.join(output_location, "OutputFiles")
            if not os.path.exists(base_output_path): os.makedirs(base_output_path)
            output_filename = os.path.join(base_output_path, output_filename)
            exec_file = os.path.join(os.getenv("MomentumValidationDir"), "SagittaBiasCorrection/AccumulateStatistics.py")
            this_jobdir = os.path.join(output, descriptor, jobname)
            if not os.path.exists(this_jobdir): os.makedirs(this_jobdir)

            command = "python {executable} --filename {filename} --start {start} --stop {stop} --detector_location {detector_location} --output_filename {output_filename} --inject {inject} --correct {correction} --resonance {resonance}"
            command = command.format(\
            executable = exec_file,\
            filename = root_file,\
            start=start,\
            stop=stop,\
            detector_location=detector_location,\
            output_filename = output_filename,\
            inject=inject,\
            correction=this_correction_pkl_file,\
            resonance="Z",\
            )


            job = Job(jobname, this_jobdir, base_commands + [command], time = "00:12:00", memory="5000M")
            jobset.add_job(job)

if test: jobset.jobs[0].run_local()
else:
    jobset.submit()
    import time
    while not jobset.check_completion():
        print("Checking compleition")
        time.sleep(100)
    print("FINISHED")
