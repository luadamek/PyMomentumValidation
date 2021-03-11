jobdir=/project/def-psavard/ladamek/sagittabias_matrices
tight_selection_nom="( abs(Pair_{}_Mass - 91.2) < 12) and (Pos_{}_Pt < 100) and (Neg_{}_Pt < 100)"
tight_selection_up="( abs(Pair_{}_Mass - 91.2) < 9) and (Pos_{}_Pt < 90) and (Neg_{}_Pt < 90)"
tight_selection_down="( abs(Pair_{}_Mass - 91.2) < 15) and (Pos_{}_Pt < 110) and (Neg_{}_Pt < 110)"
loose_selection="( abs(Pair_{}_Mass - 91.2) < 40) and (Pos_{}_Pt < 500) and (Neg_{}_Pt < 500)"
inject=None

for method in matrix # delta_qm
do
    if [ "$method" = "matrix" ]
    then
        max_iter=5
    else
        max_iter=22
    fi

    for selection in nom
    do
        if [ "$selection" = "nom" ]
        then
            tight_selection="$tight_selection_nom"
        elif [ "$selection" = "up" ]
        then
            tight_selection="$tight_selection_up"
        else
            tight_selection="$tight_selection_down"
        fi

        for detector_location in CB #ID ME CB
        do
            i=0
            until [ $i -eq $max_iter ]
            do
                y=$((i-1))
                for file_type in MCSherpa MC Data MCSherpa1516 MCSherpa17 MCSherpa18 Data1516 Data17 Data18 MC1516 MC17 MC18 
                do
                    job_base=Injection_Mar1_${file_type}_inject_${inject}_method_${method}_region_${detector_location}_loose_preselection_tight_select_after_correction_${selection}_
                    if [ $i -gt 1 ]
                    then
                        python $MomentumValidationDir/Submission/submit_delta_calculation_jobs.py  --file_type ${file_type} --jobdir /project/def-psavard/ladamek/sagittabias_jobdir/ --job_base ${job_base}_round_${i} --detector_location ${detector_location} --version v05 --inject ${inject} --output ${jobdir} --preselection "${loose_selection}" --method ${method} --select_after_corrections "${tight_selection}" --corrections ${jobdir}/${job_base}_round_${y}/OutputFiles
                    else
                        python $MomentumValidationDir/Submission/submit_delta_calculation_jobs.py  --file_type ${file_type} --jobdir /project/def-psavard/ladamek/sagittabias_jobdir/ --job_base ${job_base}_round_${i} --detector_location ${detector_location} --version v05 --inject ${inject} --output ${jobdir} --preselection "${loose_selection}" --method ${method} --select_after_corrections "${tight_selection}"
                    fi
                done
#               for file_type in MC1516 MC17 MC18 
#               do
#                   job_base=Injection_Mar1_${file_type}_inject_${inject}_method_${method}_region_${detector_location}_loose_preselection_tight_select_after_correction_${selection}_v03_v2_default_corr
#                   if [ $i -gt 1 ]
#                   then
#                       python $MomentumValidationDir/Submission/submit_delta_calculation_jobs.py  --file_type ${file_type} --jobdir /project/def-psavard/ladamek/sagittabias_jobdir/ --job_base ${job_base}_round_${i} --detector_location ${detector_location} --version v03_v2 --inject ${inject} --output ${jobdir} --preselection "${loose_selection}" --method ${method} --select_after_corrections "${tight_selection}" --corrections ${jobdir}/${job_base}_round_${y}/OutputFiles --default_correction
#                   else
#                       python $MomentumValidationDir/Submission/submit_delta_calculation_jobs.py  --file_type ${file_type} --jobdir /project/def-psavard/ladamek/sagittabias_jobdir/ --job_base ${job_base}_round_${i} --detector_location ${detector_location} --version v03_v2 --inject ${inject} --output ${jobdir} --preselection "${loose_selection}" --method ${method} --default_correction  --select_after_corrections="${tight_selection}"
#                   fi
#               done
#               for file_type in MC1516 MC17 MC18 Data1516 Data17 Data18
#               do
#                   job_base=Injection_Mar1_${file_type}_inject_${inject}_method_${method}_region_${detector_location}_loose_preselection_tight_select_after_correction_${selection}_v03_v2
#                   if [ $i -gt 1 ]
#                   then
#                       python $MomentumValidationDir/Submission/submit_delta_calculation_jobs.py  --file_type ${file_type} --jobdir /project/def-psavard/ladamek/sagittabias_jobdir/ --job_base ${job_base}_round_${i} --detector_location ${detector_location} --version v03_v2 --inject ${inject} --output ${jobdir} --preselection "${loose_selection}" --method ${method} --select_after_corrections "${tight_selection}" --corrections ${jobdir}/${job_base}_round_${y}/OutputFiles
#                   else
#                       python $MomentumValidationDir/Submission/submit_delta_calculation_jobs.py  --file_type ${file_type} --jobdir /project/def-psavard/ladamek/sagittabias_jobdir/ --job_base ${job_base}_round_${i} --detector_location ${detector_location} --version v03_v2 --inject ${inject} --output ${jobdir} --preselection "${loose_selection}" --method ${method} --select_after_corrections="${tight_selection}"
#                   fi
#               done
                i=$((i+1))
            done
        done
   done
done
 
