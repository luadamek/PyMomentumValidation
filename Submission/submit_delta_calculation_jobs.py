import utils
from batchsub import Job, JobSet
import os
import argparse

parser = argparse.ArgumentParser(description='Parse Arguments')
parser.add_argument('--outfile_base', type=str, required = False, dest='outfile_base', default = "output_{}.pkl")
parser.add_argument('--detector_location', type=str, dest='detector_location', required=True)
parser.add_argument('--output', type=str, dest='output', required=True)
parser.add_argument('--jobdir', type=str, dest='jobdir', required=True)
parser.add_argument('--inject', type=str, required=False, dest="inject")
parser.add_argument('--file_type', type=str, required=True, dest="file_type")
parser.add_argument('--job_base', type=str, required=True, dest="job_base")
parser.add_argument('--test', action="store_true", dest="test")
parser.add_argument('--version', type=str, required=True, dest="version")
parser.add_argument('--corrections', '-c', type=str, required=False, dest="corrections", default="")
parser.add_argument('--preselection', "-presel", type=str, required=False, dest="preselection", default="")
parser.add_argument('--select_before_corrections', "-sel_bf_corr", type=str, required=False, dest="select_before_corrections", default="")
parser.add_argument('--select_after_corrections', "-sel_af_corr", type=str, required=False, dest="select_after_corrections", default="")
parser.add_argument('--method' , '-meth', type=str, default="matrix", required=False)
args = parser.parse_args()

file_type = args.file_type
detector_location = args.detector_location
outfile_base = args.outfile_base
inject = args.inject
output = args.output
test = args.test
job_base = args.job_base
version = args.version
corrections = args.corrections
jobdir = args.jobdir
preselection = args.preselection
select_before_corrections = args.select_before_corrections
select_after_corrections = args.select_after_corrections

job_descr = args.job_base
if job_descr[-1] == "_": job_descr = job_descr[:-1]
commands = utils.get_setup_commands()
jobname = "covmatrix_job_{}".format(job_descr) + "_{}"

output_dir = os.path.join(output, job_descr)
output_location = os.path.join(output_dir, "OutputFiles")

job_counter = 0
jobset = JobSet(job_descr)
files = utils.get_files(version)[file_type]
for root_file in files:
    entrysteps = utils.get_entry_steps(root_file, step_size = 1000000, tree_name = "MuonMomentumCalibrationTree")
    for startstop in entrysteps:
        start = startstop[0]
        stop = startstop[1]
        tree_name = "MuonMomentumCalibrationTree"
        root_file = root_file
        if args.method == "matrix": exec_file = os.path.join(os.getenv("MomentumValidationDir"), "SagittaBiasCorrection/MatrixInversion.py")
        elif args.method == "delta_qm": exec_file = os.path.join(os.getenv("MomentumValidationDir"), "SagittaBiasCorrection/DeltaQMIterativeMethod.py")
        else: raise ValueError("Method {} doesn't exists".format(args.method))

        if not os.path.exists(output_location): os.makedirs(output_location)
        output_filename = outfile_base.format(job_counter)
        output_filename = os.path.join(output_location, output_filename)

        this_jobname = jobname.format(job_counter)
        this_jobdir = os.path.join(jobdir, job_descr)
        this_jobdir = os.path.join(this_jobdir, this_jobname)
        command = "python {executable} --filename {filename} --start {start} --stop {stop} --detector_location {detector_location} --output_filename {output_filename}"
        command = command.format(executable = exec_file, filename = root_file, start=start, stop=stop, detector_location=detector_location, output_filename = output_filename)
        if corrections: command += " --corrections {}".format(corrections)
        if inject != "": command += " --inject {}".format(inject)
        if preselection: command += " --preselection \"{}\"".format(preselection)
        if select_before_corrections: command += " --select_before_corrections \"{}\"".format(select_before_corrections)
        if select_after_corrections: command += " --select_after_corrections \"{}\"".format(select_after_corrections)
        these_commands = commands + [command]

        if args.method == "matrix": time = "00:12:00"
        elif args.method == "delta_qm": time = "00:03:00"
        job = Job(this_jobname, this_jobdir, these_commands, time = time, memory="15000M")
        jobset.add_job(job)
        job_counter += 1

if test: jobset.jobs[0].run_local()
else:
    jobset.submit()
    import time
    while not jobset.check_completion():
        print("Checking compleition")
        time.sleep(100)
    print("FINISHED")

    #create the cache file for the delta file
    if "matrix" == args.method:
        from MatrixInversion import get_deltas_from_job
        global get_deltas_from_job
    elif "delta_qm" == args.method:
        from DeltaQMIterativeMethod import get_deltas_from_job
        global get_deltas_from_job
    get_deltas_from_job(output_location, update_cache=True)

