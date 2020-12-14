#parser = argparse.ArgumentParser(description='Parse Arguments')
#parser.add_argument('--outfile_base', type=str, required = False, dest='outfile_base', default = "jobdir_{}.pkl")
#parser.add_argument('--detector_location', type=str, dest='detector_location', required=True)
#parser.add_argument('--jobdir_location', type=str, dest='output_location', required=True)
#parser.add_argument('--inject', type=str, required=False, dest="inject")
#parser.add_argument('--file_type', type=str, required=True, dest="inject")
#parser.add_argument('', action="store_true", dest="test")
#args = parser.parse_args()

for pt_threshold in 100
do
    for range in 12
        #20
        # 16 12
    do
        for detector_location in ID MS
        do
	        python $MomentumValidationDir/Submission/submit_cov_matrix_jobs.py  --file_type Data --jobdir /scratch/ladamek/sagittabias_jobdir/ --job_base Injection_Dec12_round_1 --detector_location ${detector_location} --version v03_v2 --range ${range} --pt_threshold ${pt_threshold} --output /project/def-psavard/ladamek/sagitta_bias_matrices/
	        python $MomentumValidationDir/Submission/submit_cov_matrix_jobs.py  --file_type Data --jobdir /project/def-psavard/ladamek/sagitta_bias_matrices --job_base Injection_Dec12_round_2 --detector_location ${detector_location} --version v03_v2 --range ${range} --pt_threshold ${pt_threshold} --corrections /project/def-psavard/ladamek/sagitta_bias_matrices/Injection_Dec12_round_1_${detector_location}_Data_Inject_None_v03_v2_range_${range}_0000_pt_threshold_${pt_threshold}_0000_selfirst_False/OutputFiles --output /project/def-psavard/ladamek/sagitta_bias_matrices/
	        python $MomentumValidationDir/Submission/submit_cov_matrix_jobs.py  --file_type Data --jobdir /project/def-psavard/ladamek/sagitta_bias_matrices --job_base Injection_Dec12_round_3 --detector_location ${detector_location} --version v03_v2 --range ${range} --pt_threshold ${pt_threshold} --corrections /project/def-psavard/ladamek/sagitta_bias_matrices/Injection_Dec12_round_2_${detector_location}_Data_Inject_None_v03_v2_range_${range}_0000_pt_threshold_${pt_threshold}_0000_selfirst_False/OutputFiles --output /project/def-psavard/ladamek/sagitta_bias_matrices/
	        python $MomentumValidationDir/Submission/submit_cov_matrix_jobs.py  --file_type Data --jobdir /project/def-psavard/ladamek/sagitta_bias_matrices --job_base Injection_Dec12_round_4 --detector_location ${detector_location} --version v03_v2 --range ${range} --pt_threshold ${pt_threshold} --corrections /project/def-psavard/ladamek/sagitta_bias_matrices/Injection_Dec12_round_3_${detector_location}_Data_Inject_None_v03_v2_range_${range}_0000_pt_threshold_${pt_threshold}_0000_selfirst_False/OutputFiles --output /project/def-psavard/ladamek/sagitta_bias_matrices/
    	    for inject in Global Local None GlobalPlusLocal
    	    do
                echo
    	        #python $MomentumValidationDir/Submission/submit_cov_matrix_jobs.py  --file_type MC --jobdir /scratch/ladamek/sagittabias_jobdir/ --job_base Injection_Dec12_round_1 --detector_location ${detector_location} --version v03_v2 --range ${range} --inject ${inject} --pt_threshold ${pt_threshold} --output /project/def-psavard/ladamek/sagitta_bias_matrices/
    	        #python $MomentumValidationDir/Submission/submit_cov_matrix_jobs.py  --file_type MC --jobdir /project/def-psavard/ladamek/sagitta_bias_matrices --job_base Injection_Dec12_round_2 --detector_location ${detector_location} --version v03_v2 --range ${range} --inject ${inject} --pt_threshold ${pt_threshold} --corrections /project/def-psavard/ladamek/sagitta_bias_matrices/Injection_Dec12_round_1_${detector_location}_MC_Inject_${inject}_v03_v2_range_${range}_0000_pt_threshold_${pt_threshold}_0000_selfirst_False/OutputFiles --output /project/def-psavard/ladamek/sagitta_bias_matrices/
    	        #python $MomentumValidationDir/Submission/submit_cov_matrix_jobs.py  --file_type MC --jobdir /project/def-psavard/ladamek/sagitta_bias_matrices --job_base Injection_Dec12_round_3 --detector_location ${detector_location} --version v03_v2 --range ${range} --inject ${inject} --pt_threshold ${pt_threshold} --corrections /project/def-psavard/ladamek/sagitta_bias_matrices/Injection_Dec12_round_2_${detector_location}_MC_Inject_${inject}_v03_v2_range_${range}_0000_pt_threshold_${pt_threshold}_0000_selfirst_False/OutputFiles --output /project/def-psavard/ladamek/sagitta_bias_matrices/
    	        #python $MomentumValidationDir/Submission/submit_cov_matrix_jobs.py  --file_type MC --jobdir /project/def-psavard/ladamek/sagitta_bias_matrices --job_base Injection_Dec12_round_4 --detector_location ${detector_location} --version v03_v2 --range ${range} --inject ${inject} --pt_threshold ${pt_threshold} --corrections /project/def-psavard/ladamek/sagitta_bias_matrices/Injection_Dec12_round_3_${detector_location}_MC_Inject_${inject}_v03_v2_range_${range}_0000_pt_threshold_${pt_threshold}_0000_selfirst_False/OutputFiles --output /project/def-psavard/ladamek/sagitta_bias_matrices/
    	    done
        done
    done
done
