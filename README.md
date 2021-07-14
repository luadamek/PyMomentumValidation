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

## Plotting the sagitta bias matrices
Once a job has completed, functions are available to plot the sagitta bias histograms:
```
import os
directory = os.path.join(os.getenv("PWD"), "TestingOutputs/Just_A_Test/OutputFiles/")
from MatrixInversion import get_deltas_from_job
#from DeltaQMIterativeMethod import get_deltas_from_job
sagitta_hist, _, __ = get_deltas_from_job(directory) #this is the histogram of sagitta bias values, in 1/GeV
```

## Filling Histograms
The class responsible for filling histograms is called a HistogramFiller.

```
from calculation import Calculation
def pt_over_mass(event):
    return event["Pos_ID_PT"]/event["Pair_ID_Mass"]
branches = ["Pos_ID_PT", "Paid_ID_Mass"]
calc_mass = Calculation(mass, branches)

def central(event):
    return np.abs(event["Pos_ID_Eta"]) < 2.0
branches = ["Pos_ID_Eta"]
sel_central = Calculation(central, branches)
```

```
def fill_histograms(hist_filler, outputRootFileName):
    outFile = ROOT.TFile(outputRootFileName, "RECREATE")

    #count the number of tracks in each channel
    histogram_name = "mass"
    selections = [sel_TightIso]
    eventCountHist = hist_filler.book_histogram_fill(histogram_name,\
                                                         calc_pt_over_mass,\
                                                         selections = selections,\
                                                         bins = 100,\
                                                         range_low = -0.5,\
                                                         range_high = +3.5,\
                                                         xlabel ='E/P',\
                                                         ylabel = 'Number of Tracks')
    histograms = hist_filler.DumpHistograms()
    for histogram_name in histograms:
        write_histograms(histograms[histogram_name], outFile)

    outFile.Close()
```

## Test one of the jobs locally
```
python Submission/prepare_submission.py --tree_name MuonMomentumCalibrationTree --n_jobs 200 --job_name Nov26_nocalib --queue_flavour 00\:10:\00 --file_flavour v03_v2 --filling_script Macros\/filling_script.py --test
```

## Submit all of the jobs to the batch system
```
python Submission/prepare_submission.py --tree_name MuonMomentumCalibrationTree --n_jobs 200 --job_name Nov26_nocalib --queue_flavour 00\:10:\00 --file_flavour v03_v2 --filling_script Macros\/filling_script.py
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
