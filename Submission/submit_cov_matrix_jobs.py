import utils
from batchsub import Job, JobSet
import os
import argparse



#file_type = "MC"
#detector_location = "ID"
#injection = "Global"
#outfile_base = "output_{}.pkl"
#output_location = "/project/def-psavard/ladamek/sagitta_bias_matrices"

parser = argparse.ArgumentParser(description='Parse Arguments')
parser.add_argument('--outfile_base', type=str, required = False, dest='outfile_base', default = "output_{}.pkl")
parser.add_argument('--detector_location', type=str, dest='detector_location', required=True)
parser.add_argument('--output', type=str, dest='output', required=True)
parser.add_argument('--inject', type=str, required=False, dest="inject")
parser.add_argument('--file_type', type=str, required=True, dest="file_type")
parser.add_argument('--job_base', type=str, required=True, dest="job_base")
parser.add_argument('--test', action="store_true", dest="test")
parser.add_argument('--version', type=str, required=False, default="v03", dest="version")
args = parser.parse_args()

file_type = args.file_type
detector_location = args.detector_location
outfile_base = args.outfile_base
inject = args.inject
output = args.output
test = args.test
job_base = args.job_base
version = args.version

job_descr = "{}_{}_{}_Inject_{}".format(job_base, detector_location, file_type, inject)
if job_descr[-1] == "_": job_descr = job_descr[:-1]
commands = utils.get_setup_commands()
jobname = "covmatrix_job_{}".format(job_descr) + "_{}"

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
        exec_file = os.path.join(os.getenv("MomentumValidationDir"), "SagittaBiasCorrection/MatrixInversion.py")

        jobdir = os.path.join(output, job_descr)
        output_location = os.path.join(jobdir, "OutputFiles")
        if not os.path.exists(output_location): os.makedirs(output_location)
        output_filename = outfile_base.format(job_counter)
        output_filename = os.path.join(output_location, output_filename)

        this_jobname = jobname.format(job_counter)
        this_jobdir = os.path.join(jobdir, this_jobname)
        command = "python {executable} --filename {filename} --start {start} --stop {stop} --detector_location {detector_location} --output_filename {output_filename}"
        command = command.format(executable = exec_file, filename = root_file, start=start, stop=stop, detector_location=detector_location, output_filename = output_filename)
        if inject != "": command += " --inject {}".format(inject)
        these_commands = commands + [command]

        job = Job(this_jobname, this_jobdir, these_commands, time = "00:20:00", memory="15000M")
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


