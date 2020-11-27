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

Now it should be possible for you to setup ATLAS software. Start by working inside of a singularity container. 
```
setupATLAS -c centos7+batch
```

For ComputeCanada, if setting up ALTAS software did not work for you, try logging into another login node:
```
ssh USER@gra-login>>NUM<<.computecanada.ca
```
Where >>NUM<< has been replaced by a node number such as 1, 2 or 3.

## Create a python virtual environment with and setup an lcg view. Install atlas-plots
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
pip install .
cd ..
pip install uproot
```
If you are working on ComputeCanada, creating the venv with lcg doesn't work for some reason if you're on a worker node. Make sure you're on the login node. 

## Finally, run the setup script
```
source ./setup.sh
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

## Package Philosophy
A plotting job is defined in a script such as macros/fill_script.py, which must have a function called fill_histograms. fill_histograms takes a HistogramFiller instance, an output rootfile name, and fills histograms. Take a look inside of the script fill_scipt.py to get an idea of how this works. From a user's perspective, one does not have to worry about creating an instance of a "HistogramFiller" or defining the name of the output rootfile. The scripts responsible for shipping jobs to condor handle everything. 

All selections and variables to be plotted are defined as instances of the class "Caclulation". To define a new selection for tracks in a plot, you could write the following function:
```
from calculation import Calculation
def TightIso(event):
    return event["event_nearest_dR_EM"] > 0.55
sel_TightIso = Calculation(TightIso, ["event_nearest_dR_EM"])
```
The initialization of Calculation takes a function that calculates the selection (event_nearest_dR_EM > 0.55), and a list of branches needed to perform the calculation (event_nearest_dR_EM).

Similarly, one can create a function that calculates E/P
```
from calculation import Calculation
def EOP(event):
    return (event["event_ClusterEnergy_EM_200"] + event["event_ClusterEnergy_HAD_200"])/event["event_p"]
branches = ["event_ClusterEnergy_EM_200", "event_ClusterEnergy_HAD_200", "event_p"]
calc_EOP = Calculation(EOP, branches)
```

To fill an EOP histogram for all tracks passing the TightIso selection, define a histogram filling script like macros/fill_script_test.py .
```
def fill_histograms(hist_filler, outputRootFileName):
    outFile = ROOT.TFile(outputRootFileName, "RECREATE")

    #count the number of tracks in each channel
    histogram_name = "EOP"
    selections = [sel_TightIso]
    eventCountHist = hist_filler.book_histogram_fill(histogram_name,\
                                                         calc_EOP,\
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

The following lines would prepare a batch job for submission. This job would use 200 slurm jobs, and run over v03_v2 files. The set of files that this corresponds to is visible in utils/filelists.py. The queue flavour describes the amount of time that the job is set to run for, and it is 10 minutes in the examples below.

## Test one of the jobs locally
```
python Submission/prepare_submission.py --tree_name MuonMomentumCalibrationTree --n_jobs 200 --job_name Nov26_nocalib --queue_flavour 00\:10:\00 --file_flavour v03_v2 --filling_script Macros\/filling_script.py --test
```

## Submit all of the jobs to the batch system
```
python Submission/prepare_submission.py --tree_name MuonMomentumCalibrationTree --n_jobs 200 --job_name Nov26_nocalib --queue_flavour 00\:10:\00 --file_flavour v03_v2 --filling_script Macros\/filling_script.py
```
