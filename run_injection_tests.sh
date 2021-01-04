#parser = argparse.ArgumentParser(description='Parse Arguments')
#parser.add_argument('--outfile_base', type=str, required = False, dest='outfile_base', default = "jobdir_{}.pkl")
#parser.add_argument('--detector_location', type=str, dest='detector_location', required=True)
#parser.add_argument('--jobdir_location', type=str, dest='output_location', required=True)
#parser.add_argument('--inject', type=str, required=False, dest="inject")
#parser.add_argument('--file_type', type=str, required=True, dest="inject")
#parser.add_argument('', action="store_true", dest="test")
#args = parser.parse_args()


#ok apply a selection of 
jobdir=/scratch/ladamek/sagittabias_matrices
tight_selection="( abs(Pair_{}_Mass - 91.2) < 12) and (Pos_{}_Pt < 100) and (Pos_{}_Pt < 100)"
loose_selection="( abs(Pair_{}_Mass - 91.2) < 40) and (Pos_{}_Pt < 500) and (Pos_{}_Pt < 500)"
for detector_location in ME ID
do
        '''
        inject=None
        job_base=Injection_Dec17_Data_inject_${inject}_region_${detector_location}_tight_select_after_correction
    	python $MomentumValidationDir/Submission/submit_cov_matrix_jobs.py  --file_type Data --jobdir /scratch/ladamek/sagittabias_jobdir/ --job_base ${job_base}_round_1 --detector_location ${detector_location} --version v03_v2 --inject ${inject} --output ${jobdir} --preselection "${loose_selection}" --select_after_corrections "${tight_selection}" ##### --test
    	python $MomentumValidationDir/Submission/submit_cov_matrix_jobs.py  --file_type Data --jobdir /scratch/ladamek/sagittabias_jobdir/ --job_base ${job_base}_round_2 --detector_location ${detector_location} --version v03_v2 --inject ${inject} --output ${jobdir} --preselection "${loose_selection}" --select_after_corrections "${tight_selection}" --corrections ${jobdir}/${job_base}_round_1/OutputFiles ##### --test
        '''
    	for inject in None Random Global Local GlobalPlusLocal
    	do
              #the jobs with just a preselection, thats it
              job_base=Injection_Dec17_inject_${inject}_region_${detector_location}_tight_preselection
    	        python $MomentumValidationDir/Submission/submit_cov_matrix_jobs.py  --file_type MC --jobdir /scratch/ladamek/sagittabias_jobdir/ --job_base ${job_base}_round_1 --detector_location ${detector_location} --version v03_v2 --inject ${inject} --output ${jobdir} --preselection "${tight_selection}" ##### --test
    	        python $MomentumValidationDir/Submission/submit_cov_matrix_jobs.py  --file_type MC --jobdir /scratch/ladamek/sagittabias_jobdir/ --job_base ${job_base}_round_2 --detector_location ${detector_location} --version v03_v2 --inject ${inject} --output ${jobdir} --corrections ${jobdir}/${job_base}_round_1/OutputFiles --preselection "${tight_selection}" ##### --test

              # the jobs with a looser preselection, and then a selection before corrections
              job_base=Injection_Dec17_inject_${inject}_region_${detector_location}_loose_preselection_tight_select_before_correction
    	        python $MomentumValidationDir/Submission/submit_cov_matrix_jobs.py  --file_type MC --jobdir /scratch/ladamek/sagittabias_jobdir/ --job_base ${job_base}_round_1 --detector_location ${detector_location} --version v03_v2 --inject ${inject} --output ${jobdir} --preselection "${loose_selection}" --select_before_corrections "${tight_selection}" ##### --test
    	        python $MomentumValidationDir/Submission/submit_cov_matrix_jobs.py  --file_type MC --jobdir /scratch/ladamek/sagittabias_jobdir/ --job_base ${job_base}_round_2 --detector_location ${detector_location} --version v03_v2 --inject ${inject} --output ${jobdir} --corrections ${jobdir}/${job_base}_round_1/OutputFiles --preselection "${tight_selection}" --select_before_corrections "${tight_selection}" ##### --test

              # the jobs with a looser preselection, and then a selection after corrections
              job_base=Injection_Dec17_inject_${inject}_region_${detector_location}_loose_preselection_tight_select_after_correction
    	        python $MomentumValidationDir/Submission/submit_cov_matrix_jobs.py  --file_type MC --jobdir /scratch/ladamek/sagittabias_jobdir/ --job_base ${job_base}_round_1 --detector_location ${detector_location} --version v03_v2 --inject ${inject} --output ${jobdir} --preselection "${loose_selection}" --select_after_corrections "${tight_selection}" ##### --test
    	        python $MomentumValidationDir/Submission/submit_cov_matrix_jobs.py  --file_type MC --jobdir /scratch/ladamek/sagittabias_jobdir/ --job_base ${job_base}_round_2 --detector_location ${detector_location} --version v03_v2 --inject ${inject} --output ${jobdir} --corrections ${jobdir}/${job_base}_round_1/OutputFiles --preselection "${tight_selection}" --select_after_corrections "${tight_selection}" ##### --test
      done
done
