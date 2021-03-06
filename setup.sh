export MomentumValidationDir=$PWD
export HOSTNAME=$HOSTNAME
source venv_PyMomentumValidation/bin/activate
export X509_USER_PROXY=${MomentumValidationDir}/grid_proxy
export PYTHONPATH=${MomentumValidationDir}/HistogramFillingTools:${PYTHONPATH}
export PYTHONPATH=${MomentumValidationDir}/Submission:${PYTHONPATH}
export PYTHONPATH=${MomentumValidationDir}/utils:${PYTHONPATH}
export PYTHONPATH=${MomentumValidationDir}/SagittaBiasCorrection:${PYTHONPATH}
export PYTHONPATH=${MomentumValidationDir}/Macros:${PYTHONPATH}
export PYTHONPATH=${MomentumValidationDir}/atlasplots/:${PYTHONPATH}
chmod 777 ${X509_USER_PROXY}
