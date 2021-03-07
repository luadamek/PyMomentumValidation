#python Submission/prepare_submission.py --tree_name MuonMomentumCalibrationTree --n_jobs 100 --job_name Mar7_${version}_nocalib --queue_flavour 00\:15:\00 --file_flavour ${version} --filling_script Macros\/filling_script.py 
#python Submission/prepare_submission.py --tree_name MuonMomentumCalibrationTree --n_jobs 100 --job_name Mar7_${version}_matrix_calib_7 --queue_flavour 00\:15:\00 --file_flavour ${version} --filling_script Macros\/filling_script.py  --load_calibrations /scratch/ladamek/sagittabias_matrices/Injection_Dec17_Data_inject_None_region_ID_tight_select_after_correction_round_7/OutputFiles/,/scratch/ladamek/sagittabias_matrices/Injection_Dec17_Data_inject_None_region_ME_tight_select_after_correction_round_7/OutputFiles/ --load_subtractions /scratch/ladamek/sagittabias_matrices/Injection_Dec17_inject_None_region_ID_loose_preselection_tight_select_after_correction_round_7/OutputFiles/,/scratch/ladamek/sagittabias_matrices/Injection_Dec17_inject_None_region_ME_loose_preselection_tight_select_after_correction_round_7/OutputFiles/
version=v03_v2
python Submission/prepare_submission.py --tree_name MuonMomentumCalibrationTree --n_jobs 100 --job_name Mar7_${version}_nocalib --queue_flavour 00\:15:\00 --file_flavour ${version} --filling_script Macros\/filling_script.py 
python Submission/prepare_submission.py --tree_name MuonMomentumCalibrationTree --n_jobs 100 --job_name Mar7_${version}_matrix_calib_7 --queue_flavour 00\:15:\00 --file_flavour ${version} --filling_script Macros\/filling_script.py  --load_calibrations default_matrix 
python Submission/prepare_submission.py --tree_name MuonMomentumCalibrationTree --n_jobs 100 --job_name Mar7_${version}_deltaqm_calib_21 --queue_flavour 00\:15:\00 --file_flavour ${version} --filling_script Macros\/filling_script.py  --load_calibrations default_deltaqm 
#python Submission/prepare_submission.py --tree_name MuonMomentumCalibrationTree --n_jobs 100 --job_name Mar7_${version}_matrix_mconly_calib_7 --queue_flavour 00\:15:\00 --file_flavour ${version} --filling_script Macros\/filling_script.py  --load_calibrations mconly_matrix 
#python Submission/prepare_submission.py --tree_name MuonMomentumCalibrationTree --n_jobs 100 --job_name Mar7_${version}_matrix_uncorr_calib_7 --queue_flavour 00\:15:\00 --file_flavour ${version} --filling_script Macros\/filling_script.py  --load_calibrations uncorr_matrix 
#python Submission/prepare_submission.py --tree_name MuonMomentumCalibrationTree --n_jobs 100 --job_name Mar7_${version}_deltaqm_calib_21 --queue_flavour 00\:15:\00 --file_flavour ${version} --filling_script Macros\/filling_script.py  --load_calibrations default_deltaqm 
#python Submission/prepare_submission.py --tree_name MuonMomentumCalibrationTree --n_jobs 100 --job_name Mar7_${version}_deltaqm_mconly_calib_21 --queue_flavour 00\:15:\00 --file_flavour ${version} --filling_script Macros\/filling_script.py  --load_calibrations mconly_deltaqm 
#python Submission/prepare_submission.py --tree_name MuonMomentumCalibrationTree --n_jobs 100 --job_name Mar7_${version}_deltaqm_uncorr_calib_21 --queue_flavour 00\:15:\00 --file_flavour ${version} --filling_script Macros\/filling_script.py  --load_calibrations uncorr_deltaqm 
