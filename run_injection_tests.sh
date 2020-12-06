#parser = argparse.ArgumentParser(description='Parse Arguments')
#parser.add_argument('--outfile_base', type=str, required = False, dest='outfile_base', default = "output_{}.pkl")
#parser.add_argument('--detector_location', type=str, dest='detector_location', required=True)
#parser.add_argument('--output_location', type=str, dest='output_location', required=True)
#parser.add_argument('--inject', type=str, required=False, dest="inject")
#parser.add_argument('--file_type', type=str, required=True, dest="inject")
#parser.add_argument('', action="store_true", dest="test")
#args = parser.parse_args()

for pt_threshold in 100 -1
do
    for range in 12 16 20
    do
        for detector_location in ID MS
        do
    	#python $MomentumValidationDir/Submission/submit_cov_matrix_jobs.py  --file_type Data --output /project/def-psavard/ladamek/sagitta_bias_matrices --job_base Injection_Dec3 --detector_location ${detector_location} --version v03_v2 --range ${range}  --pt_threshold ${pt_threshold} 
    	    for inject in Global Local None #GlobalPlusLocal
    	    do
    	        python $MomentumValidationDir/Submission/submit_cov_matrix_jobs.py  --file_type MC --output /project/def-psavard/ladamek/sagitta_bias_matrices --job_base Injection_Dec3 --detector_location ${detector_location} --version v03_v2 --range ${range} --inject ${inject} --pt_threshold ${pt_threshold} 
    	    done
        done
    done
done
