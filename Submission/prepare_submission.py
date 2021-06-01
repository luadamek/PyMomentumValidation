import utils
from BDTCombination import BDTCombination
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
from selections import sel_nom_delta_preselection_id, sel_nom_delta_preselection_me, sel_nom_delta_preselection_cb
from WeightedCBCorrectionCov import WeightedCBCorrectionCov
import pandas as pd
from RecalculateMass import RecalculateMasses

def apply_calibrations(kind, hist_fillers):
    if kind is None or len(kind) == 0: return
    if "deltaqm" in kind:
         base_filename = "/scratch/ladamek/sagittabias_matrices/Injection_Feb10_{filetype}_inject_None_method_delta_qm_region_{region}_loose_preselection_tight_select_after_correction_nom_round_21/OutputFiles"
         import DeltaQMIterativeMethod
         func = DeltaQMIterativeMethod.get_deltas_from_job
    elif "matrix" in kind:
         base_filename = "/project/def-psavard/ladamek/sagittabias_matrices/Injection_Mar10_{filetype}_inject_None_method_matrix_region_{region}_loose_preselection_tight_select_after_correction_nom_round_5/OutputFiles/"
         import MatrixInversion
         func = MatrixInversion.get_deltas_from_job
    else: raise ValueError("Calibration {} not found".format(kind))

    for region in ["ID", "ME", "CB"]:
        for data, mc in [("Data1516", "MC1516"), ("Data17", "MC17"), ("Data18", "MC18")]:
            #if region == "CB":
            #    base_filename = "/project/def-psavard/ladamek/sagittabias_matrices/NoTrigThresh_Injection_Mar10_{filetype}_inject_None_method_matrix_region_{region}_loose_preselection_tight_select_after_correction_nom_round_5/OutputFiles/"
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
            calib = SagittaBiasCorrection([deltas], xvar_pos, xvar_neg, yvar_pos, yvar_neg, flavour = region, store_uncorr=True)
            for hist_filler in hist_fillers:
                apply_to = data
                if "mconly" in kind: apply_to = mc
                hist_filler.apply_calibration_for_channel(apply_to, calib, selections=selections)

from selections import define_eta_selection

def apply_standard_mc_calibrations(hist_fillers):
    import pandas
    import openpyxl
    from openpyxl import load_workbook
    wb = load_workbook(os.path.join(os.getenv("MomentumValidationDir"), "MCCorrection", "RegionOrdering.xlsx"))
    df = pandas.DataFrame(wb["Sheet1"].values)
    new_df = {}
    for i, (region_name, eta_low, eta_high, sector) in enumerate(zip(df[0].values, df[1].values, df[2].values, df[3].values)):
        if i == 0:
           new_df[region_name] = []
           new_df[eta_low] = []
           new_df[eta_high] = []
           new_df[sector] = []
           region_name_header = region_name
           eta_low_header = eta_low
           eta_high_header = eta_high
           sector_header = sector
        else:
           new_df[region_name_header].append(region_name)
           new_df[eta_low_header].append(eta_low)
           new_df[eta_high_header].append(eta_high)
           new_df[sector_header].append(sector)
    df = pandas.DataFrame.from_dict(new_df)

    from selections import \
    sel_large_sector_ID_Pos,\
    sel_large_sector_ME_Pos,\
    sel_large_sector_ID_Neg,\
    sel_large_sector_ME_Neg,\
    sel_small_sector_ID_Pos,\
    sel_small_sector_ME_Pos,\
    sel_small_sector_ID_Neg,\
    sel_small_sector_ME_Neg

    from calculation import Calculation
    from MCCorrection import MCCorrection

    for period in ["1516", "17", "18"]:
        #get the parameters for the correction
        if period == "1516": descr = "15" #the params for 15 are the same as the params for 16
        else: descr = period

        basedir_params = os.path.join(os.getenv("MomentumValidationDir"), "MCCorrection", "Recs2021_04_18_Prelim")
        scale_params = os.path.join(basedir_params, "Scale_muons_Data{descr}_Recs2021_04_18_Prelim.dat".format(descr=descr))
        smearing_params = os.path.join(basedir_params, "Smearing_muons_Data{descr}_Recs2021_04_18_Prelim.dat".format(descr=descr))
        scale_params = pd.read_csv(scale_params, sep=r'\s{1,}', engine='python')
        smearing_params = pd.read_csv(smearing_params, sep=r'\s{1,}', engine='python')

        for detector_location in ["ID", "ME"]:
            for region_int, (region_name, eta_low, eta_high, sector) in enumerate(zip(df["RegionName"].values, df["Eta low"].values, df["Eta High"].values, df["Phi Sector"].values)):

                sel_pos = []
                sel_neg = []

                if sector == "Large":
                    if detector_location == "ID":
                        sel_pos.append(sel_large_sector_ID_Pos)
                        sel_neg.append(sel_large_sector_ID_Neg)
                    if detector_location == "ME":
                        sel_pos.append(sel_large_sector_ME_Pos)
                        sel_neg.append(sel_large_sector_ME_Neg)

                if sector == "Small":
                    if detector_location == "ID":
                        sel_pos.append(sel_small_sector_ID_Pos)
                        sel_neg.append(sel_small_sector_ID_Neg)
                    if detector_location == "ME":
                        sel_pos.append(sel_small_sector_ME_Pos)
                        sel_neg.append(sel_small_sector_ME_Neg)

                sel_pos.append({"func":define_eta_selection, "args":[eta_low, eta_high, detector_location, "Pos"]})
                sel_neg.append({"func":define_eta_selection, "args":[eta_low, eta_high, detector_location, "Neg"]})

                these_scale_params = scale_params.loc[region_int]
                these_smearing_params = smearing_params.loc[region_int]

                s0_ID = 0.0
                s1_ID = these_scale_params["Scale_ID"]
                r0_ID = 0.0
                r1_ID = these_smearing_params["r1_ID"]
                r2_ID = these_smearing_params["r2_ID"]

                s0_ID_up = 0.0
                s1_ID_up = these_scale_params["Scale_ID_SUp"]
                r0_ID_up = 0.0
                r1_ID_up = these_smearing_params["SUp_r1_ID"]
                r2_ID_up = these_smearing_params["SUp_r2_ID"]

                s0_ID_down = 0.0
                s1_ID_down = these_scale_params["Scale_ID_SDw"]
                r0_ID_down = 0.0
                r1_ID_down = these_smearing_params["SDw_r1_ID"]
                r2_ID_down = these_smearing_params["SDw_r2_ID"]

                s0_ME = these_scale_params["s0_MS"]
                s1_ME = these_scale_params["Scale_MS"]
                r0_ME = these_smearing_params["r0_MS"]
                r1_ME = these_smearing_params["r1_MS"]
                r2_ME = these_smearing_params["r2_MS"]

                s0_ME_up = these_scale_params["s0_MS_SUp"]
                s1_ME_up = these_scale_params["Scale_MS_SUp"]
                r0_ME_up = these_smearing_params["SUp_r0_MS"]
                r1_ME_up = these_smearing_params["SUp_r1_MS"]
                r2_ME_up = these_smearing_params["SUp_r2_MS"]

                s0_ME_down = these_scale_params["s0_MS_SDw"]
                s1_ME_down = these_scale_params["Scale_MS_SDw"]
                r0_ME_down = these_smearing_params["SDw_r0_MS"]
                r1_ME_down = these_smearing_params["SDw_r1_MS"]
                r2_ME_down = these_smearing_params["SDw_r2_MS"]

                if detector_location == "ID":
                    s0 = s0_ID
                    s1 = s1_ID
                    r0 = r0_ID
                    r1 = r1_ID
                    r2 = r2_ID

                    s0_up = s0_ID_up
                    s1_up = s1_ID_up
                    r0_up = r0_ID_up
                    r1_up = r1_ID_up
                    r2_up = r2_ID_up

                    s0_down = s0_ID_down
                    s1_down = s1_ID_down
                    r0_down = r0_ID_down
                    r1_down = r1_ID_down
                    r2_down = r2_ID_down

                if detector_location == "ME":
                    s0 = s0_ME
                    s1 = s1_ME
                    r0 = r0_ME
                    r1 = r1_ME
                    r2 = r2_ME

                    s0_up = s0_ME_up
                    s1_up = s1_ME_up
                    r0_up = r0_ME_up
                    r1_up = r1_ME_up
                    r2_up = r2_ME_up

                    s0_down = s0_ME_down
                    s1_down = s1_ME_down
                    r0_down = r0_ME_down
                    r1_down = r1_ME_down
                    r2_down = r2_ME_down

                mccorr = MCCorrection(s0=s0, s1=s1, r0=r0, r1=r1, r2=r2, pos_selections = sel_pos, neg_selections = sel_neg, flavour = detector_location, store_uncorr=True)
                mccorr_scale_up = MCCorrection(s0=s0_up, s1=s1_up, r0=r0, r1=r1, r2=r2, pos_selections = sel_pos, neg_selections = sel_neg, flavour = detector_location, store_uncorr=True)
                mccorr_scale_down = MCCorrection(s0=s0_down, s1=s1_down, r0=r0, r1=r1, r2=r2, pos_selections = sel_pos, neg_selections = sel_neg, flavour = detector_location, store_uncorr=True)
                mccorr_res_up = MCCorrection(s0=s0, s1=s1, r0=r0_up, r1=r1_up, r2=r2_up, pos_selections = sel_pos, neg_selections = sel_neg, flavour = detector_location, store_uncorr=True)
                mccorr_res_down = MCCorrection(s0=s0, s1=s1, r0=r0_down, r1=r1_down, r2=r2_down, pos_selections = sel_pos, neg_selections = sel_neg, flavour = detector_location, store_uncorr=True)

                for i, hist_filler in enumerate(hist_fillers):
                    for channel in hist_filler.channels:
                        if "MC" in channel and period in channel:
                            if i == 0: print("Applying to {}".format(channel))
                            if "_scale_" in channel:
                               if "_up" in channel: hist_filler.apply_calibration_for_channel(channel, mccorr_scale_up)
                               elif "_down" in channel: hist_filler.apply_calibration_for_channel(channel, mccorr_scale_down)
                               else: assert False
                            elif "_res_" in channel:
                               if "_up" in channel: hist_filler.apply_calibration_for_channel(channel, mccorr_res_up)
                               elif "_down" in channel: hist_filler.apply_calibration_for_channel(channel, mccorr_res_down)
                               else: assert False
                            else: hist_filler.apply_calibration_for_channel(channel, mccorr)

def apply_systematic_variations(hist_fillers, stat_syst = False, resbias_syst = False):
    syst_var_file = "/project/def-psavard/ladamek/stat_variations/stat_syst_vars.root"
    #ok go and get the histograms from this root_file and apply the systematic variations
    #histname = "{}_{}_{}".format(file_type, detector_location, "staterr")
    for period in ["17", "18", "1516"]:
        for detector_location in ["ID", "ME"]:
            if detector_location == "ID":
                xvar_pos = calc_pos_id_eta
                xvar_neg = calc_neg_id_eta
                selections = [sel_nom_delta_preselection_id]
            elif detector_location == "MS":
                xvar_pos = calc_pos_ms_eta
                xvar_neg = calc_neg_ms_eta
                selections = []
            elif detector_location == "CB":
                xvar_pos = calc_pos_cb_eta
                xvar_neg = calc_neg_cb_eta
                selections = [sel_nom_delta_preselection_cb]
            elif detector_location == "ME":
                xvar_pos = calc_pos_me_eta
                xvar_neg = calc_neg_me_eta
                selections = [sel_nom_delta_preselection_me]
            else: raise ValueError()
            if detector_location == "ID":
                yvar_pos = calc_pos_id_phi
                yvar_neg = calc_neg_id_phi
            elif detector_location == "MS":
                yvar_pos = calc_pos_ms_phi
                yvar_neg = calc_neg_ms_phi
            elif detector_location == "CB":
                yvar_pos = calc_pos_cb_phi
                yvar_neg = calc_neg_cb_phi
            elif detector_location == "ME":
                yvar_pos = calc_pos_me_phi
                yvar_neg = calc_neg_me_phi
            else: raise ValueError()

            if stat_syst:
                rf = ROOT.TFile(syst_var_file, "READ")
                rf.ls()
                histname = "Data{}_{}_{}".format(period, detector_location, "staterr")
                hist = rf.Get(histname)
                hist.Clone()
                hist.SetDirectory(0)
                rf.Close()

            if resbias_syst:
                #get the resbias systematic histogram
                resbias_histograms = "/project/def-psavard/ladamek/sagittabias_matrices/ResbiasInjection_MC{period}_inject_ResbiasData{period}_method_matrix_region_{detector_location}_loose_preselection_tight_select_after_correction_nom/OutputFiles/".format(period=period, detector_location=detector_location)
                resbias_sub = "/project/def-psavard/ladamek/sagittabias_matrices/Injection_Mar10_MC{period}_inject_None_method_matrix_region_{region}_loose_preselection_tight_select_after_correction_nom_round_0/OutputFiles/".format(period=period, region=detector_location)
                from MatrixInversion import get_deltas_from_job
                hist = get_deltas_from_job(resbias_histograms)[0]
                hist = hist.Clone()
                hist_sub = get_deltas_from_job(resbias_sub)[0]
                hist.Add(hist_sub, -1.0)
                hist.SetDirectory(0)

            hist_up = hist.Clone()
            hist_up.Scale(1.0)
            hist_down = hist.Clone()
            hist_down.Scale(-1.0)

            for var, varhist in zip(["up", "down"], [hist_up, hist_down]):
                for hist_filler in hist_fillers:
                    calib = SagittaBiasCorrection([varhist], xvar_pos, xvar_neg, yvar_pos, yvar_neg, flavour = detector_location)
                    if stat_syst:
                        channel = "MC{}_stat_{}".format(period, var)
                    if resbias_syst:
                        channel = "MC{}_resbias_{}".format(period, var)
                    hist_filler.apply_calibration_for_channel(channel, calib, selections=selections)
                    hist_filler.apply_calibration_for_channel(channel + "_{}".format(detector_location), calib, selections=selections)


def submit_jobs(tree_name, job_name, n_jobs, queue_flavour, file_flavour, filling_script, slurm_directories, load_calibrations, inject = None, inject_channels="", default_correction=False, cov_combination=False, memory="6000M", latest_mc_correction = False, simple_combination = False, skip_mass_recalc=False, skip_baseline_selection = False, add_BDT_combination=False, cov_combination_percent=False, fullcov_combination_percent=False, fullcov_combination=False):
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

        if not skip_mass_recalc:
            for hist_filler in filler_list: hist_filler.apply_calibration_for_channel("__ALL__", RecalculateMasses())

        from selections import sel_z_selection_cb
        if not skip_baseline_selection: 
            for hist_filler in filler_list:     hist_filler.apply_selection_for_channel("__ALL__", [sel_z_selection_cb])

        '''
        apply the default calibration to the calib channels, if they exist
        '''

        for hist_filler in filler_list:
            if default_correction: continue
            for channel in ["MCCalib", "MC1516Calib", "MC17Calib", "MC18Calib", "MCSherpaCalib", "MCSherpa1516Calib", "MCSherpa17Calib", "MCSherpa18Calib"]:
                hist_filler.apply_calibration_for_channel(channel, DefaultCorrection())

        '''
        apply the default calibration to all channels
        '''
        if default_correction:
            for hist_filler in filler_list: hist_filler.apply_calibration_for_channel("__ALL__", DefaultCorrection())

        '''
        apply the latest mc calibration to the channels
        '''
        if latest_mc_correction:
            apply_standard_mc_calibrations(filler_list)

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

        '''
        apply the sagitta bias systematic uncertainty
        '''
        apply_systematic_variations(filler_list, stat_syst=True)
        apply_systematic_variations(filler_list, resbias_syst=True)

        '''
        Redefine the CB track using the covariance matrix combination for all channels
        '''
        if cov_combination:
            for hist_filler in filler_list: hist_filler.apply_calibration_for_channel("__ALL__", WeightedCBCorrectionCov())

        if cov_combination_percent:
            for hist_filler in filler_list: hist_filler.apply_calibration_for_channel("__ALL__", WeightedCBCorrectionCov(do_percent_corr=True))

        if fullcov_combination_percent:
            for hist_filler in filler_list: hist_filler.apply_calibration_for_channel("__ALL__", WeightedCBCorrectionCov(do_percent_corr=True, do_full_matrix=True))

        if fullcov_combination:
            for hist_filler in filler_list: hist_filler.apply_calibration_for_channel("__ALL__", WeightedCBCorrectionCov(do_percent_corr=False, do_full_matrix=True))


        from DefaultSimpleCombination import DefaultCombination
        if simple_combination:
            for hist_filler in filler_list: hist_filler.apply_calibration_for_channel("__ALL__", DefaultCombination())

        if add_BDT_combination:
            for hist_filler in filler_list: hist_filler.apply_calibration_for_channel("__ALL__", BDTCombination(os.path.join(os.getenv("MomentumValidationDir"), "BDTs/SecondBDTs/15_qop_False.pkl")))

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
            job = Job(job_name + "_" + str(i), os.path.join(slurm_directory, "job_{}".format(i)), commands, time = queue_flavour, memory=memory)
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
        parser.add_argument('--file_flavour', '-file_flavour', dest="file_flavour", type=str, default='tomorrow', help='What kind of files should I run on?')
        parser.add_argument('--filling_script', '-fs', dest="filling_script", type=str, default='inclusive', help='What is the name of the script that takes the input root file and makes histograms?')
        parser.add_argument('--load_calibrations', '-lmc', dest="load_calibrations", type=str, default='', help='the name of the calibrations to be applied. They are defined in the apply_calibration function in prepare_submission.py')
        parser.add_argument('--testjob', '-tj', dest="test_job", action="store_true", help="Submit a test job")
        parser.add_argument('--inject', "-inj", dest="inject", type=str, default="")
        parser.add_argument('--inject_channels', "-inj_ch", dest="inject_channels", type=str, default="MC,MC1516,MC17,MC18")
        parser.add_argument('--default_correction', "-def_calib", dest="default_correction", action="store_true")
        parser.add_argument('--latest_mc_correction', "-def_mc_calib", dest="latest_mc_correction", action="store_true")
        parser.add_argument('--cov_combination', '-cov_comb', dest="cov_combination", action="store_true")
        parser.add_argument('--cov_combination_percent', '-cov_comb_per', dest="cov_combination_percent", action="store_true")
        parser.add_argument('--fullcov_combination', '-fullcov_comb', dest="fullcov_combination", action="store_true")
        parser.add_argument('--fullcov_combination_percent', '-fullcov_comb_per', dest="fullcov_combination_percent", action="store_true")
        parser.add_argument('--simple_combination', '-simple_comb', dest="simple_combination", action="store_true")
        parser.add_argument('--skip_mass_recalc', '-smrecalc', dest="skip_mass_recalc", action="store_true")
        parser.add_argument('--skip_baseline_selection', '-skbase', dest="skip_baseline_selection", action="store_true")
        parser.add_argument('--memory', '-mem', dest="memory", type=str, required=True)
        parser.add_argument("--add_BDT_combination", '-aBDTc', dest="add_BDT_combination", action="store_true")
        args = parser.parse_args()

        #Create a pickle file and list for each submission
        tree_name = args.tree_name
        job_name = args.job_name
        n_jobs = args.n_jobs
        queue_flavour = args.queue_flavour
        if args.test_job: args.file_flavour = "TEST"
        file_flavour = args.file_flavour
        filling_script = args.filling_script
        inject = args.inject
        inject_channels = args.inject_channels
        if inject == "":
            inject = None
        slurm_directories = ["/project/def-psavard/ladamek/momentumvalidationoutput/", args.job_name]

        jobset_file, slurm_directory = submit_jobs(tree_name, job_name, n_jobs, queue_flavour, file_flavour, filling_script, slurm_directories, args.load_calibrations, inject=inject, inject_channels=inject_channels, default_correction=args.default_correction, cov_combination=args.cov_combination, memory=args.memory, latest_mc_correction = args.latest_mc_correction, simple_combination=args.simple_combination, skip_mass_recalc=args.skip_mass_recalc, skip_baseline_selection=args.skip_baseline_selection, add_BDT_combination = args.add_BDT_combination, cov_combination_percent=args.cov_combination_percent, fullcov_combination_percent=args.fullcov_combination_percent, fullcov_combination=args.fullcov_combination)

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
            os.system("hadd -f -j 10 {final_file} ".format(final_file = os.path.join(slurm_directory, "Output.root")) + " ".join(to_merge))
            print("SUCCESS!")


