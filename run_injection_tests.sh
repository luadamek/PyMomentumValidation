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
method="delta_qm"
for detector_location in ID ME
do
      for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17
      do
          inject="None"
          y=$((i-1))
          job_base=Data_Dec17_inject_${inject}_method_${method}_region_${detector_location}_loose_preselection_tight_select_after_correction
   	      if [ $i -gt 1 ]
          then
              python $MomentumValidationDir/Submission/submit_delta_calculation_jobs.py  --file_type Data --jobdir /scratch/ladamek/sagittabias_jobdir/ --job_base ${job_base}_round_${i} --detector_location ${detector_location} --version v03_v2 --inject ${inject} --output ${jobdir} --preselection "${loose_selection}" --method ${method} --select_after_corrections "${tight_selection}" --corrections ${jobdir}/${job_base}_round_${y}/OutputFiles
          else 
              python $MomentumValidationDir/Submission/submit_delta_calculation_jobs.py  --file_type Data --jobdir /scratch/ladamek/sagittabias_jobdir/ --job_base ${job_base}_round_${i} --detector_location ${detector_location} --version v03_v2 --inject ${inject} --output ${jobdir} --preselection "${loose_selection}" --method ${method} --select_after_corrections "${tight_selection}"
          fi
      done
done
#   	for inject in Random Global Local GlobalPlusLocal None
#   	do
#             #the jobs with just a preselection, thats it
#             for i in 12 13 14 15 16 17
#             do
#               y=$((i-1))
#              job_base=Injection_Dec17_inject_${inject}_method_${method}_region_${detector_location}_tight_preselection
#  	          if [ $i -gt 1 ]
#              then
#                python $MomentumValidationDir/Submission/submit_delta_calculation_jobs.py  --file_type MC --jobdir /scratch/ladamek/sagittabias_jobdir/ --job_base ${job_base}_round_${i} --detector_location ${detector_location} --version v03_v2 --inject ${inject} --output ${jobdir} --preselection "${tight_selection}" --method ${method} --corrections ${jobdir}/${job_base}_round_${y}/OutputFiles 
#              else 
#                python $MomentumValidationDir/Submission/submit_delta_calculation_jobs.py  --file_type MC --jobdir /scratch/ladamek/sagittabias_jobdir/ --job_base ${job_base}_round_${i} --detector_location ${detector_location} --version v03_v2 --inject ${inject} --output ${jobdir} --preselection "${tight_selection}" --method ${method} 
#              fi

#              job_base=Injection_Dec17_inject_${inject}_method_${method}_region_${detector_location}_loose_preselection_tight_select_before_correction
#              if [ $i -gt 1 ]
#                then
#                  python $MomentumValidationDir/Submission/submit_delta_calculation_jobs.py  --file_type MC --jobdir /scratch/ladamek/sagittabias_jobdir/ --job_base ${job_base}_round_${i} --detector_location ${detector_location} --version v03_v2 --inject ${inject} --output ${jobdir} --preselection "${loose_selection}" --method ${method} --select_before_corrections "${tight_selection}" --corrections ${jobdir}/${job_base}_round_${y}/OutputFiles  ##### --test
#                else
#                  python $MomentumValidationDir/Submission/submit_delta_calculation_jobs.py  --file_type MC --jobdir /scratch/ladamek/sagittabias_jobdir/ --job_base ${job_base}_round_${i} --detector_location ${detector_location} --version v03_v2 --inject ${inject} --output ${jobdir} --preselection "${loose_selection}" --method ${method} --select_before_corrections "${tight_selection}"  ##### --test
#              fi

#               job_base=Injection_Dec17_inject_${inject}_method_${method}_region_${detector_location}_loose_preselection_tight_select_after_correction
#               if [ $i -gt 1 ]
#                  then
#   	                python $MomentumValidationDir/Submission/submit_delta_calculation_jobs.py  --file_type MC --jobdir /scratch/ladamek/sagittabias_jobdir/ --job_base ${job_base}_round_${i} --detector_location ${detector_location} --version v03_v2 --inject ${inject} --output ${jobdir} --preselection "${loose_selection}" --method ${method} --select_after_corrections "${tight_selection}" --corrections ${jobdir}/${job_base}_round_${y}/OutputFiles  ##### --test
#                 else
#   	                python $MomentumValidationDir/Submission/submit_delta_calculation_jobs.py  --file_type MC --jobdir /scratch/ladamek/sagittabias_jobdir/ --job_base ${job_base}_round_${i} --detector_location ${detector_location} --version v03_v2 --inject ${inject} --output ${jobdir} --preselection "${loose_selection}" --method ${method} --select_after_corrections "${tight_selection}"  ##### --test
#               fi
#             done
#     done
#done
