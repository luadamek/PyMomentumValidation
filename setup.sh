export MomentumValidationDir=$PWD
source venv_PyMomentumValidation/bin/activate
export X509_USER_PROXY=${MomentumValidationDir}/grid_proxy
chmod 777 ${X509_USER_PROXY}
