import os
import glob
import numpy as np
import nibabel as nib
from nilearn.image import binarize_img, math_img, resample_to_img, mean_img

sub_list = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25"]

prob=.20

def gm_mask_prob(mask_path, func_ref_path, prob=.5):
    return resample_to_img(
        binarize_img(
            math_img(f"img>={prob}", img=mask_path), 
        threshold=prob), 
    func_ref_path, interpolation="nearest")

def merge_masks(input_path):
    return binarize_img(mean_img(glob.glob(input_path)))

for sub in sub_list:
    print(f"segmenting subject-{sub}")
    anat_dir = f"/home/data/NegativeCueing_RSA/NegCue_Random/derivatives/fmriprep/sub-{sub}/anat"
    func_dir = f"/home/data/NegativeCueing_RSA/NegCue_Random/derivatives/fmriprep/sub-{sub}/func"
    sub_path = anat_dir + f"/sub-{sub}_label-GM_probseg.nii.gz"
    sub_func_path = func_dir + f"/sub-{sub}_task-negativesearcheventrelated_run-01_space-T1w_desc-preproc_bold.nii.gz"
    
    # create gm mask
    gm_mask = gm_mask_prob(mask_path=sub_path, prob=prob, func_ref_path=sub_func_path)
    nib.save(gm_mask, anat_dir + f"/sub-{sub}_label-GM_prob-{prob}.nii.gz")
    
    # create mask from different runs
    func_mask = merge_masks(f"/home/data/NegativeCueing_RSA/NegCue_Random/derivatives/fmriprep/sub-{sub}/func/sub-{sub}_task-negativesearcheventrelated_run-*_space-T1w_desc-brain_mask.nii.gz")
    nib.save(func_mask, anat_dir + f"/sub-{sub}_complete-mask.nii.gz")
