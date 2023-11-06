import sys
import os
import glob
import numpy as np
import pandas as pd
from nilearn.image import threshold_img
from nilearn.glm.second_level import non_parametric_inference

phase = str(sys.argv[1])
hypothesis = str(sys.argv[2])

def group_lvl(phase, hypothesis, fwhm, out_dir=None): 
    map_paths = glob.glob("/home/data/NegativeCueing_RSA/scratch/eventrelated_exp" + f"/corr-maps_phase-{phase}_mni/sub-*_{hypothesis}_mni.nii.gz")
    if not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)
        
    condition_effect = ([1] * len(map_paths))
    design_matrix = pd.DataFrame(condition_effect, columns=["intercept"])
    neg_log_pvals_permuted_ols_unmasked = \
        non_parametric_inference(map_paths,
                                design_matrix=design_matrix,
                                model_intercept=True, 
                                mask="/home/data/NegativeCueing_RSA/NegCue_Random/code/masks/resampled_mni_gm.nii.gz", 
                                n_perm=5000,
                                two_sided_test=True,
                                smoothing_fwhm=fwhm, 
                                n_jobs=6,
                                verbose=2, 
                                tfce=True)
    
    neg_log_pvals_permuted_ols_unmasked["t"].to_filename(out_dir + f"/phase-{phase}_hypothesis-{hypothesis}_tstat.nii")
    neg_log_pvals_permuted_ols_unmasked["logp_max_t"].to_filename(out_dir + f"/phase-{phase}_hypothesis-{hypothesis}_max-t.nii")
    neg_log_pvals_permuted_ols_unmasked["tfce"].to_filename(out_dir + f"/phase-{phase}_hypothesis-{hypothesis}_tfce.nii")
    neg_log_pvals_permuted_ols_unmasked["logp_max_tfce"].to_filename(out_dir + f"/phase-{phase}_hypothesis-{hypothesis}_logp_max_tfce.nii")
    return None

# set paths to store output
output_folder = f"/home/data/NegativeCueing_RSA/scratch/eventrelated_exp/permutation_results_two-sided/phase-{phase}_hypothesis-{hypothesis}"
if not os.path.exists(output_folder):
    os.makedirs(output_folder, exist_ok=True)

print(f"working phase-{phase}, hypothesis-{hypothesis}")
group_lvl(phase=phase, 
        hypothesis=hypothesis, 
        fwhm=5., 
        out_dir=output_folder)