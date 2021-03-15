import utils
import os
from histogram_filler import HistogramFiller
from variables import calc_weight, calc_pos_id_eta, calc_pos_id_phi, calc_neg_id_eta, calc_neg_id_phi,\
calc_pos_ms_eta, calc_pos_ms_phi, calc_neg_ms_eta, calc_neg_ms_phi,\
calc_pos_me_eta, calc_pos_me_phi, calc_neg_me_eta, calc_neg_me_phi,\
calc_pos_cb_eta, calc_pos_cb_phi, calc_neg_cb_eta, calc_neg_cb_phi
import ROOT
import pickle
import argparse
from batchsub import Job, JobSet
from MatrixInversion import get_deltas_from_job
from BiasCorrection import SagittaBiasCorrection
import pickle as pkl

def apply_calibrations(kind, hist_fillers):
    if kind is None or len(kind) == 0: return
    if "deltaqm" in kind:
         base_filename = "/scratch/ladamek/sagittabias_matrices/Injection_Feb10_{filetype}_inject_None_method_delta_qm_region_{region}_loose_preselection_tight_select_after_correction_nom_round_21/OutputFiles"
         import DeltaQMIterativeMethod
         func = DeltaQMIterativeMethod.get_deltas_from_job
    elif "matrix" in kind:
         #base_filename = "/scratch/ladamek/sagittabias_matrices/Injection_Feb10_{filetype}_inject_None_method_matrix_region_{region}_loose_preselection_tight_select_after_correction_nom_round_7/OutputFiles"
         base_filename = "/project/def-psavard/ladamek/sagittabias_matrices/Injection_Mar10_{filetype}_inject_None_method_matrix_region_{region}_loose_preselection_tight_select_after_correction_nom_round_3/OutputFiles/"
         import MatrixInversion
         func = MatrixInversion.get_deltas_from_job
    else: raise ValueError("Calibration {} not found".format(kind))

    from selections import sel_nom_delta_preselection_id, sel_nom_delta_preselection_me, sel_nom_delta_preselection_cb
    for region in ["ID", "ME", "CB"]:
        for data, mc in [("Data1516", "MC1516"), ("Data17", "MC17"), ("Data18", "MC18")]:
            dir_data = base_filename.format(filetype=data, region=region)
            dir_mc = base_filename.format(filetype=mc, region=region)

            deltas, variables, detector_location = get_deltas_from_job(dir_data)
            delta_subtraction, _, __ = get_deltas_from_job(dir_mc)
            if "uncorr" not in kind: deltas.Add(delta_subtraction, -1.0)
            if "mconly" in kind: deltas = delta_subtraction
            xvar_name = variables["x_var"]
            yvar_name = variables["y_var"]
            if xvar_name == "ID_Eta":
                xvar_pos = calc_pos_id_eta
                xvar_neg = calc_neg_id_eta
                selections = [sel_nom_delta_preselection_id]
            elif xvar_name == "MS_Eta":
                xvar_pos = calc_pos_ms_eta
                xvar_neg = calc_neg_ms_eta
                selections = []
            elif xvar_name == "CB_Eta":
                xvar_pos = calc_pos_cb_eta
                xvar_neg = calc_neg_cb_eta
                selections = [sel_nom_delta_preselection_cb]
            elif xvar_name == "ME_Eta":
                xvar_pos = calc_pos_me_eta
                xvar_neg = calc_neg_me_eta
                selections = [sel_nom_delta_preselection_me]
            else: raise ValueError()
            if yvar_name == "ID_Phi":
                yvar_pos = calc_pos_id_phi
                yvar_neg = calc_neg_id_phi
            elif yvar_name == "MS_Phi":
                yvar_pos = calc_pos_ms_phi
                yvar_neg = calc_neg_ms_phi
            elif yvar_name == "CB_Phi":
                yvar_pos = calc_pos_cb_phi
                yvar_neg = calc_neg_cb_phi
            elif yvar_name == "ME_Phi":
                yvar_pos = calc_pos_me_phi
                yvar_neg = calc_neg_me_phi
            else: raise ValueError()
            calib = SagittaBiasCorrection([deltas], xvar_pos, xvar_neg, yvar_pos, yvar_neg, flavour = region)
            for hist_filler in hist_fillers:
                apply_to = data
                if "mconly" in kind: apply_to = mc
                hist_filler.apply_calibration_for_channel(apply_to, calib, selections=selections)

def submit_jobs(tree_name, job_name, n_jobs, queue_flavour, file_flavour, filling_script, slurm_directories, load_calibrations, inject = None, inject_channels="", default_correction=False):
        from DefaultCalibration import DefaultCorrection
        project_dir = os.getenv("MomentumValidationDir")
        assert project_dir is not None

        files = utils.get_files(file_flavour)
        trees = utils.tchain_files_together(args.tree_name, files)
        partitions = utils.generate_partitions(trees, n_jobs)

        slurm_directory = project_dir
        for path in slurm_directories:
            if not os.path.exists(os.path.join(slurm_directory, path)):
                os.makedirs(os.path.join(slurm_directory, path))
            slurm_directory = os.path.join(slurm_directory, path)

        #create the executables for the slurm jobs
        executable = os.path.join(slurm_directory, "plot.sh")
        executable_local = os.path.join(slurm_directory, "plot_local.sh")
        python_executable = os.path.join(slurm_directory, "plot.py")

        #create the python script that is needed for plotting
        plotting_instructions_python = []
        plotting_instructions_python.append("from histogram_filler import HistogramFiller")
        plotting_instructions_python.append("from {} import fill_histograms".format(filling_script.split("/")[-1].split(".")[0]))
        plotting_instructions_python.append("import pickle")
        plotting_instructions_python.append("import argparse")
        plotting_instructions_python.append("parser = argparse.ArgumentParser(description=\'Submit plotting batch jobs for the MuonMomentumAnalysis plotting\')")
        plotting_instructions_python.append("parser.add_argument(\'--num\', '-n', dest=\"num\", type=int, required=True, help=\'Which submission number was this?\')")
        plotting_instructions_python.append("parser.add_argument('--picklefile' '-p', dest='picklefile', type=str, default=\"\", help='Where to get the plotter')")
        plotting_instructions_python.append("parser.add_argument('--jobName', '-j', dest=\"jobname\", type=str, default='\"\"', help='the names of the batch jobs')")
        plotting_instructions_python.append("args = parser.parse_args()")
        plotting_instructions_python.append("i = args.num")
        plotting_instructions_python.append("file = args.picklefile")
        plotting_instructions_python.append("name = args.jobname")
        plotting_instructions_python.append("plots = pickle.load(open(file, \"rb\"))[i]")

        #put the output file in the job directory:
        outfile_name =  "\"" + os.path.join(slurm_directory, job_name + "_{}.root\".format(str(i))")


        plotting_instructions_python.append("fill_histograms(plots, {}".format(outfile_name)) 
        plotting_instructions_python[-1] += ")"
        with open(python_executable, 'w') as f:
            for line in plotting_instructions_python:
                f.write(line+"\n")

        #create the shell script to be executed
        plotting_instruction_script = []
        plotting_instruction_script.append("#!/bin/bash")
        plotting_instruction_script.append("cd {}".format(os.getenv("MomentumValidationDir")))
        activate_location = os.path.join(os.getenv("MomentumValidationDir"),"venv_MomentumValidationDir/bin/activate")
        plotting_instruction_script.append("source {}".format(activate_location))
        plotting_instruction_script.append("source ./setup_slurm.sh")
        plotting_instruction_script.append("printf \"Start time: \"; /bin/date")
        plotting_instruction_script.append("printf \"Job is running on node: \"; /bin/hostname")
        plotting_instruction_script.append("printf \"Job running as user: \"; /usr/bin/id")
        plotting_instruction_script.append("printf \"Job is running in directory: \"; /bin/pwd")
        plotting_instruction_script.append("ls -al")
        plotting_instruction_script.append("python {} ".format("plot.py") + " --num ${1} --picklefile ${2} --jobName ${3}")
        with open(executable, 'w') as f:
            for line in plotting_instruction_script:
                f.write(line+"\n")

        #create the shell script that runs jobs locally
        plotting_instruction_local_script = ["cp {} {}".format(filling_script, filling_script.split("/")[-1])]
        plotting_instruction_local_script += ["cp {} {}".format(python_executable, python_executable.split("/")[-1])]
        plotting_instruction_local_script +=  plotting_instruction_script
        plotting_instruction_local_script += ["rm {}".format(filling_script.split("/")[-1])]
        plotting_instruction_local_script += ["rm {}".format(python_executable.split("/")[-1])]
        with open(executable_local, 'w') as f:
            for line in plotting_instruction_local_script:
                f.write(line+"\n")

        #iterate over the number of jobs
        #create a joblist. save the joblistfile somewhere
        filler_file = os.path.join(slurm_directory, "histogram_fillers.pkl")
        filler_list = []
        for i in range(0, n_jobs):
            partition = {}
            for channel in partitions:
                partition[channel] =  partitions[channel][i]
            assert len(partitions[channel]) == n_jobs
            hist_filler = HistogramFiller(trees, tree_name, calc_weight, selection_string = "", partitions = partition)
            filler_list.append(hist_filler)

        for hist_filler in filler_list:
            for channel in ["MCCalib", "MC1516Calib", "MC17Calib", "MC18Calib", "MCSherpaCalib", "MCSherpa1516Calib", "MCSherpa17Calib", "MCSherpa18Calib"]:
                hist_filler.apply_calibration_for_channel(channel, DefaultCorrection())

        if inject is not None:
           injections = []
           from BiasInjection import injection_histogram_local, injection_histogram_global, injection_histogram_globalpluslocal, injection_histogram_random
           if inject == "Local":
               inject_hist_func = injection_histogram_local
           if inject == "Global":
               inject_hist_func = injection_histogram_global
           if inject == "GlobalPlusLocal":
               inject_hist_func = injection_histogram_globalpluslocal
           if inject == "Random":
               inject_hist_func = injection_histogram_random

           for region in ["ID", "ME"]:
               inject_hist = inject_hist_func(detector_location = region)
               if region == "ID":
                   xvar_pos = calc_pos_id_eta
                   xvar_neg = calc_neg_id_eta
                   yvar_pos = calc_pos_id_phi
                   yvar_neg = calc_neg_id_phi

               if region == "ME":
                   xvar_pos = calc_pos_me_eta
                   xvar_neg = calc_neg_me_eta
                   yvar_pos = calc_pos_me_phi
                   yvar_neg = calc_neg_me_phi
               injections.append(SagittaBiasCorrection([inject_hist], xvar_pos, xvar_neg, yvar_pos, yvar_neg, flavour = region))

           for inject_channel in inject_channels.split(","):
               for injection in injections:
                   for hist_filler in filler_list: hist_filler.apply_calibration_for_channel(inject_channel, injection)

        if load_calibrations is not None:
            apply_calibrations(load_calibrations, filler_list)


        #create a pickle file for each submission
        pickle.dump(filler_list, open(filler_file, "wb" ) )
        print("Created the submission file. Ready to go!")

        jobset = JobSet(job_name)
        for i in range(0, len(filler_list)):
            commands  = []
            commands.append("cd {}".format(os.getenv("MomentumValidationDir")))
            commands.append("export USER=ladamek")
            commands.append("source ./setup.sh")
            commands.append("python {py_exec} --num={num} --picklefile={picklefile} --jobName={jobName}".format(py_exec=python_executable, num=i, jobName = job_name + "_" + str(i), picklefile=filler_file))
            job = Job(job_name + "_" + str(i), os.path.join(slurm_directory, "job_{}".format(i)), commands, time = queue_flavour, memory="8000M")
            jobset.add_job(job)

        jobset_file = os.path.join(slurm_directory, "jobset.pkl")
        with open(jobset_file, "wb") as f:
            pkl.dump(jobset, f)
        return jobset_file, slurm_directory

if __name__ == "__main__":
        parser = argparse.ArgumentParser(description='Submit plotting batch jobs for the MuonMomentumAnalysis plotting')
        parser.add_argument('--tree_name', '-tn', dest="tree_name", type=str, required=True, help='the name of the tree to read from')
        parser.add_argument('--n_jobs', '-np', dest="n_jobs", type=int, default='0', help='the number of plotting jobs to submit')
        parser.add_argument('--job_name', '-job_name', dest="job_name", type=str, default='""', help='the name of the job to be submitted')
        parser.add_argument('--queue_flavour', '-queue_flavour', dest="queue_flavour", type=str, default='tomorrow', help='What slurm queue should the jobs run on?')
        parser.add_argument('--file_flavour', '-ff', dest="file_flavour", type=str, default='inclusive', help='What is the flavour of the jobs that you want to submit?')
        parser.add_argument('--filling_script', '-fs', dest="filling_script", type=str, default='inclusive', help='What is the name of the script that takes the input root file and makes histograms?')
        parser.add_argument('--load_calibrations', '-lmc', dest="load_calibrations", type=str, default='', help='the name of the calibrations to be applied. They are defined in the apply_calibration function in prepare_submission.py')
        parser.add_argument('--testjob', '-tj', dest="test_job", action="store_true", help="Submit a test job")
        parser.add_argument('--inject', "-inj", dest="inject", type=str, default="")
        parser.add_argument('--inject_channels', "-inj_ch", dest="inject_channels", type=str, default="MC,MC1516,MC17,MC18")
        parser.add_argument('--default_correction', "-def_calib", dest="default_correction", action="store_true")
        args = parser.parse_args()

        #Create a pickle file and list for each submission
        tree_name = args.tree_name
        job_name = args.job_name
        n_jobs = args.n_jobs
        queue_flavour = args.queue_flavour
        file_flavour = args.file_flavour
        filling_script = args.filling_script
        inject = args.inject
        inject_channels = args.inject_channels
        if inject == "":
            inject = None
        slurm_directories = ["/project/def-psavard/ladamek/momentumvalidationoutput/", args.job_name]

        jobset_file, slurm_directory = submit_jobs(tree_name, job_name, n_jobs, queue_flavour, file_flavour, filling_script, slurm_directories, args.load_calibrations, inject=inject, inject_channels=inject_channels, default_correction=args.default_correction)

        print("Job saved in {}, the jobset is {}".format(slurm_directory, jobset_file))
        #submit the jobs, and wait until completion
        import pickle as pkl
        jobset = pkl.load(open(jobset_file, "rb"))
        if args.test_job: jobset.jobs[0].run_local()

        else:
            jobset.submit()
            import time
            while not jobset.check_completion():
                print("Checking compleition")
                time.sleep(100)
            import glob
            to_merge = glob.glob(os.path.join(slurm_directory, "{}*.root".format(job_name)))
            os.system("hadd -f {final_file} ".format(final_file = os.path.join(slurm_directory, "Output.root")) + " ".join(to_merge))
            print("SUCCESS!")


