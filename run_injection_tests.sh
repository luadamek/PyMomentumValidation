#parser = argparse.ArgumentParser(description='Parse Arguments')
#parser.add_argument('--outfile_base', type=str, required = False, dest='outfile_base', default = "output_{}.pkl")
#parser.add_argument('--detector_location', type=str, dest='detector_location', required=True)
#parser.add_argument('--output_location', type=str, dest='output_location', required=True)
#parser.add_argument('--inject', type=str, required=False, dest="inject")
#parser.add_argument('--file_type', type=str, required=True, dest="inject")
#parser.add_argument('', action="store_true", dest="test")
#args = parser.parse_args()
#python $MomentumValidationDir/Submission/submit_cov_matrix_jobs.py  --file_type Data --output /project/def-psavard/ladamek/sagitta_bias_matrices --job_base Injection_Nov24 --detector_location MS --version v03_v2 
#python $MomentumValidationDir/Submission/submit_cov_matrix_jobs.py  --file_type MC --output /project/def-psavard/ladamek/sagitta_bias_matrices --job_base Injection_Nov24 --detector_location MS --version v03_v2
#python $MomentumValidationDir/Submission/submit_cov_matrix_jobs.py  --inject Global --file_type MC --output /project/def-psavard/ladamek/sagitta_bias_matrices --job_base Injection_Nov24 --detector_location MS --version v03_v2
#python $MomentumValidationDir/Submission/submit_cov_matrix_jobs.py  --inject GlobalPlusLocal --file_type MC --output /project/def-psavard/ladamek/sagitta_bias_matrices --job_base Injection_Nov24 --detector_location MS --version v03_v2
#python $MomentumValidationDir/Submission/submit_cov_matrix_jobs.py  --inject Local --file_type MC --output /project/def-psavard/ladamek/sagitta_bias_matrices --job_base Injection_Nov24 --detector_location MS --version v03_v2
#python $MomentumValidationDir/Submission/submit_cov_matrix_jobs.py  --inject Null --file_type MC --output /project/def-psavard/ladamek/sagitta_bias_matrices --job_base Injection_Nov24 --detector_location MS --version v03_v2
python $MomentumValidationDir/Submission/submit_cov_matrix_jobs.py  --inject Data --file_type MC --output /project/def-psavard/ladamek/sagitta_bias_matrices --job_base Injection_Nov24 --detector_location MS --version v03_v2

#python $MomentumValidationDir/Submission/submit_cov_matrix_jobs.py  --file_type Data --output /project/def-psavard/ladamek/sagitta_bias_matrices --job_base Injection_Nov24 --detector_location ID --version v03_v2
#python $MomentumValidationDir/Submission/submit_cov_matrix_jobs.py  --file_type MC --output /project/def-psavard/ladamek/sagitta_bias_matrices --job_base Injection_Nov24 --detector_location ID --version v03_v2
#python $MomentumValidationDir/Submission/submit_cov_matrix_jobs.py  --inject Global --file_type MC --output /project/def-psavard/ladamek/sagitta_bias_matrices --job_base Injection_Nov24 --detector_location ID --version v03_v2
#python $MomentumValidationDir/Submission/submit_cov_matrix_jobs.py  --inject GlobalPlusLocal --file_type MC --output /project/def-psavard/ladamek/sagitta_bias_matrices --job_base Injection_Nov24 --detector_location ID --version v03_v2
#python $MomentumValidationDir/Submission/submit_cov_matrix_jobs.py  --inject Local --file_type MC --output /project/def-psavard/ladamek/sagitta_bias_matrices --job_base Injection_Nov24 --detector_location ID --version v03_v2
##python $MomentumValidationDir/Submission/submit_cov_matrix_jobs.py  --inject Null --file_type MC --output /project/def-psavard/ladamek/sagitta_bias_matrices --job_base Injection_Nov24 --detector_location ID --version v03_v2
python $MomentumValidationDir/Submission/submit_cov_matrix_jobs.py  --inject Data --file_type MC --output /project/def-psavard/ladamek/sagitta_bias_matrices --job_base Injection_Nov24 --detector_location ID --version v03_v2
