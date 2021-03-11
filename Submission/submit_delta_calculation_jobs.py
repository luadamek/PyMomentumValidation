import utils
from batchsub import Job, JobSet
import os
import argparse
import numpy as np

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
parser.add_argument('--fold', '-f', type=str, default="None", dest="fold")
parser.add_argument('--bootstraps', '-bs', type=int, default=-1, dest="bootstraps")
parser.add_argument('--default_correction', '-dc', action="store_true", dest="default_correction")
parser.add_argument('--coarse_binning', '-cb', action="store_true", dest="coarse_binning")
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
default_correction = args.default_correction
fold = args.fold
tree_name = "MuonMomentumCalibrationTree"

files = utils.get_files(version)[file_type]
bootstraps = {}
all_startstops = {}
total_events = 0
for root_file in files:
    startstops = utils.get_entry_steps(root_file, step_size = 1000000, tree_name = tree_name)
    all_startstops[root_file] = []
    total_events += startstops[-1][-1]
    bootstraps[root_file] = {}
    for startstop in startstops:
        all_startstops[root_file].append(startstop)
        bootstraps[root_file][startstop] = []
        
if args.bootstraps > 0:
    #ok now get the N bootstraps
    indices = np.arange(0, total_events)
    for i in range(0, args.bootstraps):
         print("selecting events")
         strapped_indices = np.sort(np.random.choice(indices, replace=True, size=total_events))
         edges = [0]
         root_files = []
         startstops = []
         for root_file in all_startstops:
             for startstop in all_startstops[root_file]:
                 entry = startstop[-1] - startstop[0]
                 root_files.append(root_file)
                 startstops.append(startstop)
                 edges.append(edges[-1] + entry)

         edges = np.array(edges)
         print("Getting each file for each event")
         binned = np.digitize(strapped_indices, edges) - 1
         print("Done binning according to files")
         bin_edges = np.where(binned[:-1] != binned[1:])[0] + 1

         nbins = len(edges) - 1
         bin_edges = [0] + list(bin_edges) + [total_events]
         assert len(bin_edges) == len(edges)

         cum_subtraction = 0
         for bindex ,(start, stop, edge_low, edge_high, root_file, startstop) in enumerate(zip(bin_edges[:-1], bin_edges[1:], edges[:-1], edges[1:], root_files, startstops)):
             assert len(np.unique(binned[start:stop])) == 1
             these_indices = strapped_indices[start:stop] - cum_subtraction
             cum_subtraction += (edge_high - edge_low)
             bootstraps[root_file][startstop].append(these_indices)
             assert np.all(these_indices > -1)

         print("Done strap {}".format(i))
    
job_descr = args.job_base
if job_descr[-1] == "_": job_descr = job_descr[:-1]
commands = utils.get_setup_commands()
jobname = "covmatrix_job_{}".format(job_descr) + "_{}"

output_dir = os.path.join(output, job_descr)
output_location = os.path.join(output_dir, "OutputFiles")

job_counter = 0
jobset = JobSet(job_descr)
for root_file in all_startstops:
    for startstop in all_startstops[root_file]:
        start = startstop[0]
        stop = startstop[1]
        if args.method == "matrix": exec_file = os.path.join(os.getenv("MomentumValidationDir"), "SagittaBiasCorrection/MatrixInversion.py")
        elif args.method == "delta_qm": exec_file = os.path.join(os.getenv("MomentumValidationDir"), "SagittaBiasCorrection/DeltaQMIterativeMethod.py")
        else: raise ValueError("Method {} doesn't exists".format(args.method))

        if not os.path.exists(output_location): os.makedirs(output_location)
        output_filename = outfile_base.format(job_counter)
        if args.bootstraps > 0:
            bootstrap_filename = os.path.join(output_location, "BOOTSTRAPS_{}.pkl".format(job_counter))
            with open(bootstrap_filename, "wb") as f:
                import pickle as pkl
                pkl.dump(bootstraps[root_file][startstop], f)
                print("Dumping to {}".format(bootstrap_filename))
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
        if fold != "None": command += " --fold {}".format(fold)
        if args.bootstraps> 0: command += "--bootstraps {}".format(bootstrap_filename)
        if args.default_correction: command += "  --default_correction  "
        if args.coarse_binning: command += " --coarse_binning"
        these_commands = commands + [command]

        if args.method == "matrix":
            if args.fold == "None":
                memory = "15000M"
                time = "00:03:00"
            else:
                memory="8000M"
                time = "00:03:00"
            if args.coarse_binning:
                memory="8000M"
                time="00:02:00"
        elif args.method == "delta_qm":
            if args.fold == "None":
                time = "00:02:00"
                memory = "6000M"
            else:
                time = "00:01:00"
                memory="6000M"
        job = Job(this_jobname, this_jobdir, these_commands, time = time, memory=memory)
        jobset.add_job(job)
        job_counter += 1

if test: jobset.jobs[0].run_local()
else:
    jobset.submit()
    import time
    while not jobset.check_completion():
        print("Checking compleition")
        time.sleep(30)
    print("FINISHED")

    #create the cache file for the delta file
    if "matrix" == args.method:
        from MatrixInversion import get_deltas_from_job
        global get_deltas_from_job
    elif "delta_qm" == args.method:
        from DeltaQMIterativeMethod import get_deltas_from_job
        global get_deltas_from_job
    get_deltas_from_job(output_location, update_cache=True)


