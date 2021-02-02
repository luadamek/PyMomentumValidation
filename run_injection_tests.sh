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
date_tag="Jan31"
for method in matrix delta_qm
do
    if [ "$method" = "matrix" ]
    then
        max_iter=17
    else
        max_iter=6
    fi

    for detector_location in ID ME
    do
        i=0
        until [ $i -eq $max_iter ]
        do
            for inject in None Random Global Local GlobalPlusLocal 
            do
                #y=$((i-1))
                #job_base=Injection_${date_tag}_inject_${inject}_method_${method}_region_${detector_location}_tight_preselection
                #if [ $i -gt 1 ]
                #then
                #    python $MomentumValidationDir/Submission/submit_delta_calculation_jobs.py  --file_type MC --jobdir /scratch/ladamek/sagittabias_jobdir/ --job_base ${job_base}_round_${i} --detector_location ${detector_location} --version v03_v2 --inject ${inject} --output ${jobdir} --preselection "${tight_selection}" --method ${method} --corrections ${jobdir}/${job_base}_round_${y}/OutputFiles 
                #else 
                #    python $MomentumValidationDir/Submission/submit_delta_calculation_jobs.py  --file_type MC --jobdir /scratch/ladamek/sagittabias_jobdir/ --job_base ${job_base}_round_${i} --detector_location ${detector_location} --version v03_v2 --inject ${inject} --output ${jobdir} --preselection "${tight_selection}" --method ${method} 
                #fi
                #job_base=Injection_${date_tag}_inject_${inject}_method_${method}_region_${detector_location}_loose_preselection_tight_select_before_correction
                #if [ $i -gt 1 ]
                #then
                #    python $MomentumValidationDir/Submission/submit_delta_calculation_jobs.py  --file_type MC --jobdir /scratch/ladamek/sagittabias_jobdir/ --job_base ${job_base}_round_${i} --detector_location ${detector_location} --version v03_v2 --inject ${inject} --output ${jobdir} --preselection "${loose_selection}" --method ${method} --select_before_corrections "${tight_selection}" --corrections ${jobdir}/${job_base}_round_${y}/OutputFiles  
                #else
                #    python $MomentumValidationDir/Submission/submit_delta_calculation_jobs.py  --file_type MC --jobdir /scratch/ladamek/sagittabias_jobdir/ --job_base ${job_base}_round_${i} --detector_location ${detector_location} --version v03_v2 --inject ${inject} --output ${jobdir} --preselection "${loose_selection}" --method ${method} --select_before_corrections "${tight_selection}"  
                #fi
                job_base=Injection_${date_tag}_inject_${inject}_method_${method}_region_${detector_location}_loose_preselection_tight_select_after_correction
                if [ $i -gt 1 ]
                then
      	            python $MomentumValidationDir/Submission/submit_delta_calculation_jobs.py  --file_type MC --jobdir /scratch/ladamek/sagittabias_jobdir/ --job_base ${job_base}_round_${i} --detector_location ${detector_location} --version v03_v2 --inject ${inject} --output ${jobdir} --preselection "${loose_selection}" --method ${method} --select_after_corrections "${tight_selection}" --corrections ${jobdir}/${job_base}_round_${y}/OutputFiles  
                else
      	            python $MomentumValidationDir/Submission/submit_delta_calculation_jobs.py  --file_type MC --jobdir /scratch/ladamek/sagittabias_jobdir/ --job_base ${job_base}_round_${i} --detector_location ${detector_location} --version v03_v2 --inject ${inject} --output ${jobdir} --preselection "${loose_selection}" --method ${method} --select_after_corrections "${tight_selection}"  
                fi
            done
            i=$((i+1))
        done
    done
done
