jobdir=/project/def-psavard/ladamek/sagittabias_matrices
tight_selection_nom="( abs(Pair_{}_Mass - 91.2) < 12) and (Pos_{}_Pt < 100) and (Neg_{}_Pt < 100) and ((Pos_CB_Pt > 6.25) or (Neg_CB_Pt > 6.25)) and (Pair_IsOppCharge > 0.5)"
tight_selection_up="( abs(Pair_{}_Mass - 91.2) < 9) and (Pos_{}_Pt < 90) and (Neg_{}_Pt < 90) and ((Pos_CB_Pt > 6.25) or (Neg_CB_Pt > 6.25)) and (Pair_IsOppCharge > 0.5)"
tight_selection_down="( abs(Pair_{}_Mass - 91.2) < 15) and (Pos_{}_Pt < 110) and (Neg_{}_Pt < 110) and ((Pos_CB_Pt > 6.25) or (Neg_CB_Pt > 6.25)) and (Pair_IsOppCharge > 0.5)"
#tight_selection="( abs(Pair_{}_Mass - 91.2) < 12) and (Pos_{}_Pt < 100) and (Neg_{}_Pt < 100) and (Pair_IsOppCharge > 0.5)"
#tight_selection_up="( abs(Pair_{}_Mass - 91.2) < 9) and (Pos_{}_Pt < 90) and (Neg_{}_Pt < 90) and (Pair_IsOppCharge > 0.5)"
#tight_selection_down="( abs(Pair_{}_Mass - 91.2) < 15) and (Pos_{}_Pt < 110) and (Neg_{}_Pt < 110) and (Pair_IsOppCharge > 0.5)"
loose_selection="( abs(Pair_{}_Mass - 91.2) < 40) and (Pos_{}_Pt < 500) and (Neg_{}_Pt < 500)"
inject=None
date="July10"
bootstrap=0

#    if selection == "": selection = "((Pos_CB_Pt > 6.25) or (Neg_CB_Pt > 6.25))"
#    else: selection += " and ((Pos_CB_Pt > 6.25) or (Neg_CB_Pt > 6.25))"
#    selection += " and (Pair_IsOppCharge > 0.5)"

for method in matrix # delta_qm
do
    if [ "$method" = "matrix" ]
    then
        max_iter=6
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
        for detector_location in CB ID ME
        do
            #for filebase in 1516 17 18
            #do
            #   file_type=MC${filebase}
            #   thisinject=ResbiasData${filebase}
            #   job_base=ResbiasInjection_${file_type}_inject_${thisinject}_method_${method}_region_${detector_location}_loose_preselection_tight_select_after_correction_${selection}
            #   python $MomentumValidationDir/Submission/submit_delta_calculation_jobs.py --test --file_type ${file_type} --jobdir /project/def-psavard/ladamek/sagittabias_jobdir/ --job_base ${job_base} --detector_location ${detector_location} --version v05 --inject ${thisinject} --output ${jobdir} --preselection "${loose_selection}" --method ${method} --select_after_corrections "${tight_selection}" 
            #done

            i=0
            until [ $i -eq $max_iter ]
            do
                #if it's the first iteration, do 100 bootstraps to estimate the sagitta bias uncertainty
                if [ $i -eq 0 ] 
                then
                    if [ $bootstrap -eq 1 ]
                    then
                       job_base=Injection_${date}_${file_type}_inject_${inject}_method_${method}_region_${detector_location}_loose_preselection_tight_select_after_correction_${selection}_boostraps
                       python $MomentumValidationDir/Submission/submit_delta_calculation_jobs.py --test --file_type ${file_type} --jobdir /project/def-psavard/ladamek/sagittabias_jobdir/ --job_base ${job_base}_round_${i} --detector_location ${detector_location} --version v05 --inject ${inject} --output ${jobdir} --preselection "${loose_selection}" --method ${method} --select_after_corrections "${tight_selection}" --bootstrap 100
                    fi
                fi

                if [ $bootstrap -ne 1 ]
                then
                   y=$((i-1))
                   #estimate the sagitta bias in data and the simulation
                   for file_type in Data1516 Data17 Data18 MC1516 MC17 MC18
                   do
                       job_base=Injection_${date}_${file_type}_inject_${inject}_method_${method}_region_${detector_location}_loose_preselection_tight_select_after_correction_${selection}
                       if [ $i -gt 0 ]
                       then
                           python $MomentumValidationDir/Submission/submit_delta_calculation_jobs.py --test --file_type ${file_type} --jobdir /project/def-psavard/ladamek/sagittabias_jobdir/ --job_base ${job_base}_round_${i} --detector_location ${detector_location} --version v05 --inject ${inject} --output ${jobdir} --preselection "${loose_selection}" --method ${method} --select_after_corrections "${tight_selection}" --corrections ${jobdir}/${job_base}_round_${y}/OutputFiles 
                       else
                           python $MomentumValidationDir/Submission/submit_delta_calculation_jobs.py --test --file_type ${file_type} --jobdir /project/def-psavard/ladamek/sagittabias_jobdir/ --job_base ${job_base}_round_${i} --detector_location ${detector_location} --version v05 --inject ${inject} --output ${jobdir} --preselection "${loose_selection}" --method ${method} --select_after_corrections "${tight_selection}" 
                       fi
                   done

                   #estimate the sagitta bias in different MC samples
                   for file_type in MCSherpa MCMadGraph MC
                   do
                       job_base=Injection_${date}_${file_type}_inject_${inject}_method_${method}_region_${detector_location}_loose_preselection_tight_select_after_correction_${selection}
                       if [ $i -gt 0 ]
                       then
                           python $MomentumValidationDir/Submission/submit_delta_calculation_jobs.py --test --file_type ${file_type} --jobdir /project/def-psavard/ladamek/sagittabias_jobdir/ --job_base ${job_base}_round_${i} --detector_location ${detector_location} --version v05 --inject ${inject} --output ${jobdir} --preselection "${loose_selection}" --method ${method} --select_after_corrections "${tight_selection}" --corrections ${jobdir}/${job_base}_round_${y}/OutputFiles --coarse_binning
                       else
                           python $MomentumValidationDir/Submission/submit_delta_calculation_jobs.py --test --file_type ${file_type} --jobdir /project/def-psavard/ladamek/sagittabias_jobdir/ --job_base ${job_base}_round_${i} --detector_location ${detector_location} --version v05 --inject ${inject} --output ${jobdir} --preselection "${loose_selection}" --method ${method} --select_after_corrections "${tight_selection}"  --coarse_binning 
                       fi
                    done
                fi

                i=$((i+1))
#               for file_type in MC1516 MC17 MC18 
#               do
#                   job_base=Injection_Mar17_${file_type}_inject_${inject}_method_${method}_region_${detector_location}_loose_preselection_tight_select_after_correction_${selection}_v03_v2_default_corr
#                   if [ $i -gt 1 ]
#                   then
#                       python $MomentumValidationDir/Submission/submit_delta_calculation_jobs.py --test --file_type ${file_type} --jobdir /project/def-psavard/ladamek/sagittabias_jobdir/ --job_base ${job_base}_round_${i} --detector_location ${detector_location} --version v03_v2 --inject ${inject} --output ${jobdir} --preselection "${loose_selection}" --method ${method} --select_after_corrections "${tight_selection}" --corrections ${jobdir}/${job_base}_round_${y}/OutputFiles --default_correction
#                   else
#                       python $MomentumValidationDir/Submission/submit_delta_calculation_jobs.py --test --file_type ${file_type} --jobdir /project/def-psavard/ladamek/sagittabias_jobdir/ --job_base ${job_base}_round_${i} --detector_location ${detector_location} --version v03_v2 --inject ${inject} --output ${jobdir} --preselection "${loose_selection}" --method ${method} --default_correction  --select_after_corrections="${tight_selection}"
#                   fi
#               done
#               for file_type in MC1516 MC17 MC18 Data1516 Data17 Data18
#               do
#                   job_base=Injection_Mar17_${file_type}_inject_${inject}_method_${method}_region_${detector_location}_loose_preselection_tight_select_after_correction_${selection}_v03_v2
#                   if [ $i -gt 1 ]
#                   then
#                       python $MomentumValidationDir/Submission/submit_delta_calculation_jobs.py --test --file_type ${file_type} --jobdir /project/def-psavard/ladamek/sagittabias_jobdir/ --job_base ${job_base}_round_${i} --detector_location ${detector_location} --version v03_v2 --inject ${inject} --output ${jobdir} --preselection "${loose_selection}" --method ${method} --select_after_corrections "${tight_selection}" --corrections ${jobdir}/${job_base}_round_${y}/OutputFiles
#                   else
#                       python $MomentumValidationDir/Submission/submit_delta_calculation_jobs.py --test --file_type ${file_type} --jobdir /project/def-psavard/ladamek/sagittabias_jobdir/ --job_base ${job_base}_round_${i} --detector_location ${detector_location} --version v03_v2 --inject ${inject} --output ${jobdir} --preselection "${loose_selection}" --method ${method} --select_after_corrections="${tight_selection}"
#                   fi
#               done
            done
        done
   done
done
 
