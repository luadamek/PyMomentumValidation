## Setup

Start by working inside of a singularity container. 
```
setupATLAS -c centos7+batch
```

## Create a python virtual environment with and setup an lcg view.
```
git clone https://gitlab.cern.ch/luadamek/lcg_virtualenv.git 
git clone https://gitlab.cern.ch/luadamek/PyMomentumValidation.git
setupATLAS -c centos7+batch
cd PyMomentumValidation
CMTCONFIG=x86_64-centos7-gcc8-opt ./../lcg_virtualenv/create_lcg_virtualenv venv_PyMomentumValidation LCG_94python3
source venv_PyMomentumValidation/bin/activate
git clone https://github.com/joeycarter/atlas-plots.git
cd atlas-plots
rm -rf .git
pip install . --no-dependencies
cd ..
pip install uproot
pip install openpyxl
pip install atlasify #making plots in matplotlob with atlas style
```

## Finally, run the setup script
```
source ./setup.sh
```

## Calculating the sagitta bias estimates
The user needs to update the file paths in the filelists/filelists.py file. The paths point to the location of the root files needed to measure the sagitta bias.

The steering script for the sagitta bias estimates is $MomentumValidationDir/Submission/submit_delta_calculation_jobs.py 

The script takes the following commands:

--file_type : The key to the dictionary of files process, as listed in the filelists.py file

--job_base : The name of the job. 

--detector_location : The kind of track to process -- either CB, ME or ID

--version : The version of files, as listed in the filelists.py file

--inject : The injection to perform. Those are listed in SagittaBiasCorrection/BiasInjection.py

--output : Where the output file is. Will be located at output/job_base

--preselection : The selection to apply before injection

--select_after_corrections : The selection to apply after corrections and injections

--select_before_corrections : The selection to apply before sagitta bias correction but after injection

--corrections : Past corrections to load. If a past job also used a correction, all of those corrections will be loaded, too. If multiple corrections must be loaded, they will be added together. I.E. the set of deltas will be added together.

--method : The method used for estimating the sagitta bias. Either delta_qm or matrix

--merge : merge the single test job into a complete output. This is for testing the plotting. This step happend automatically when submitting to batch and not running a test job.

here is an example job submission, running one job locally as a test
```
python Submission/submit_delta_calculation_jobs.py --file_type DataTEST --jobdir $PWD/Testing --job_base Just_A_Test --detector_location ID --version v05 --output $PWD/TestingOutputs --preselection "( abs(Pair_{}_Mass - 91.2) < 40) and (Pos_{}_Pt < 500) and (Neg_{}_Pt < 500)" --method matrix --select_after_corrections "( abs(Pair_{}_Mass - 91.2) < 12) and (Pos_{}_Pt < 100) and (Neg_{}_Pt < 100)" --test --merge
```

here is an example job submission, submitting jobs with a slurm batch system
```
python Submission/submit_delta_calculation_jobs.py --file_type DataTEST --jobdir $PWD/Testing --job_base Just_A_Test --detector_location ID --version v05 --output $PWD/TestingOutputs --preselection "( abs(Pair_{}_Mass - 91.2) < 40) and (Pos_{}_Pt < 500) and (Neg_{}_Pt < 500)" --method matrix --select_after_corrections "( abs(Pair_{}_Mass - 91.2) < 12) and (Pos_{}_Pt < 100) and (Neg_{}_Pt < 100)" 
```

An example of how to run many different injection tests for ID, ME and CB tracks is shown in the script run_injection_tests.sh. The script also derives the estimates iteratively.

## Retrieveing the Sagitta Bias Histograms
Once a job has completed, functions are available to plot the sagitta bias histograms:
```
import os
directory = os.path.join(os.getenv("PWD"), "TestingOutputs/Just_A_Test/OutputFiles/")
from MatrixInversion import get_deltas_from_job
#from DeltaQMIterativeMethod import get_deltas_from_job
sagitta_hist, _, __ = get_deltas_from_job(directory) #this is the histogram of sagitta bias values, in 1/GeV
```

## Making Plots
The class responsible for filling histograms is called a HistogramFiller. The submission script is Submission/prepare_submission.py. The script takes the following arguments:

--filling_script: The name of the file that contains the instructions for what histogram to fill. Take a look at Macros/filling_script.py to see an example of how this is accomplished. That macro imports a set of selections and variables, and creates histograms for plotting.

--tree_name: The name of the ttree in the root files to read

--n_jobs: The number of batch jobs to submit for making plots

--test: run one job locally, for debugging

--load_calibration: The sagitta bias correction to load. This can be default_matrix or default_delataqm.  (calls the apply_calibrations function in Submission/prepare_submission.py .

--memory: The amount of memory for each job.

--latest_mc_correction: whether or not to load the MC corrections

--cov_combination: Do the combination using a weight for the ID and ME 1/p defined from the ID and ME covariance matrices. This redefines all CB variables, i.e. the CB mass, the CB pt, eta, phi, etc. This is performed in the file SagittaBiasCorrection/WeightedCBCorrectionCov.py

--cov_combination_percent: Do the combination using a weight for the ID and ME 1/p defined from the ID and ME covariance matrices. Apply the percent change in the pt from the combination with and without corrections as a correction for the CB pt. The corrections are the scale and resolution MC corrections and sagitta bias corrections for data.

--fullcov_combination: Do the combination using the full ID and ME covariance matrices. This redefines all CB variables, i.e. the CB mass, the CB pt, eta, phi, etc. This is performed in the file SagittaBiasCorrection/WeightedCBCorrectionCov.py

--fullcov_combination_percent: Do the combination using the full ID and ME covariance matrices. Apply the percent change in the pt from the combination with and without corrections as a correction for the CB pt. The corrections are the scale and resolution MC corrections and sagitta bias corrections for data.

--simple_combination: Do the combination with a weighted sum of ID and ME pts. pT_cb = f pt_id + (1-f) pt_me, apply the corrections to id and me, and then recalculate the cb pt with the same formula and weight

--skip_baseline_selection: Apply a set of baseline selections. Those are defined in HistogramFillingTools/selections.py with the class sel_z_selection_cb.

--add_BDT_combination: Use a bdt for the combination, as defined in the file SagittaBiasCorrection/BDTCombination.py

--merge: Merge the single test job (if test is true) into a full output file ready for plotting. For debugging.

Here is an example running one job locally:
```
python Submission/prepare_submission.py --tree_name MuonMomentumCalibrationTree --n_jobs 300 --job_name TESTING_v05 --queue_flavour 01\:30:\00 --file_flavour v05_trimmed --filling_script Macros\/filling_script_TEST.py --memory=10000M --latest_mc_correction  --skip_baseline_selection   --test --merge
```

Once a job has completed, you can get open the output root file and make plots

```
from histogram_manager import HistogramManager
import os
hm = HistogramManager("/project/def-psavard/{}/momentumvalidationoutput/TESTING_v05/Output.root".format(os.getenv("USER")))
histogram_name = "MeanMassProfile_ID"
histograms = hm.get_histograms(histogram_name)
print(histograms)
```

### Additional Material

## Common software used in data analysis:
uproot: https://github.com/scikit-hep/uproot
root_numpy: http://scikit-hep.org/root_numpy/
ROOT: https://root.cern.ch/
RooFit: https://root.cern.ch/roofit-20-minutes, https://root.cern.ch/download/doc/RooFit_Users_Manual_2.91-33.pdf
Documentation on how to use computecanada: https://docs.computecanada.ca/wiki/Running_jobs

CERN releases software packages called LCG views. These are great ways to setup an envorinment with popular python software such as: uproot, matplotlib, jupyter, ROOT, tensorflow, keras etc. Documentation of available software is shown here: https://ep-dep-sft.web.cern.ch/document/lcg-releases .

When working with python it is common to work with virtual environments, information about those is found at this link: https://docs.python.org/3/tutorial/venv.html .

## Connecting to compute canada
```
ssh USER@graham.computecanada.ca
```

## Connecting to LXPlus
```
ssh USER@lxplus.cern.ch
```

## Setup
Sometimes on systems that are not LXPlus, you need to setup the commands that will allow you to work with ATLAS software. We tend to work inside of these things called singularity containers. These emulate operating systems, such as centos7 or slc6. Currently ATLAS is transitioning from slc6 to centos7, and compute canada requires you to work inside of a container when using ATLAS software. In order to setup ATLAS software, you need to copy the following lines into your ~/.bashrc file.

```
if [ -d /project/atlas/Tier3/ ]; then
        source /project/atlas/Tier3/AtlasUserSiteSetup.sh
        alias sa='setupATLAS -c slc6+batch'
fi
```

The execute your .bashrc file:
```
source ./.bashrc
```
## Login on ComputeCanada
When you normally login, you don't need to install all of the software again. There is a setup script provided that should restore your environment exactly as it was after installing everything. When working on graham, we don't work on the login node, but rather request a specific computing node with the salloc command.
```
ssh USER@graham.computecanada.ca
salloc --mem=30000M --time=03:00:00
setupATLAS -c centos7+batch
cd >>THE PROJECT DIRECTORY<<
source ./setup.sh
```

## Playing around with Jupyter notebooks
Jupyter notebooks are a great way to play around with data and quickly plot and test things. You can read about them here: https://jupyter.org/ . The following lines of code document how to setup a jupyter notebook.

Open a terminal on your local machine -- not graham -- and do:
```
pip install sshutil
```

Then run the following lines and follow the printed insructions on the terminal ssh'd into graham.
```
source start_notebook.sh
```

After copying the URL provided into your local machine's browser, you can open the a jupyter session in your browser. You will be prompted in for a token in the browser, which should be printed on the terminal connected to compute canada.

## Generating a grid proxy
You need a grid proxy to access data stored on EOS, or to use rucio to download ATLAS datasets. If you need to do this the following lines of code should set one up. If you need a grid certificate, get one here: https://ca.cern.ch/ca/user/Request.aspx?template=EE2User .

After you have followed the previous instructions, great instructions for how to export your grid certificate from your browser and transfer it to graham (or any machine for that matter) are found here: https://www.racf.bnl.gov/docs/howto/grid/installcert .
```
setupATLAS -c centos7+batch
cd PyMomentumValidation
lsetup rucio
export PyMomentumValidationDir=$PWD
export X509_USER_PROXY=${PyMomentumValidationDir}/grid_proxy
voms-proxy-init --voms atlas --hours 10000
exit
```

## Installing RooFit Extensions
```
git clone https://gitlab.cern.ch/atlas_higgs_combination/software/RooFitExtensions.git
cd RooFitExtensions
mkdir build
cd build
cmake .. && make
cd ../../
```
