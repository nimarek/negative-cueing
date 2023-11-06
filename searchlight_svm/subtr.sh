#!/bin/bash

hypothesis_list=("positive-negative")

for sub in 0{1..9} {10..25}; do
    echo working on ${sub} ...
    for hypothesis in ${hypothesis_list[@]}; do
        fslmaths /home/data/NegativeCueing_RSA/scratch/eventrelated_exp/lin-svm/sub-${sub}/sub-${sub}_space-MNI152_dimension-${hypothesis}_sl-radius-5.nii.gz \
        -sub 0.5 \
        -mas /usr/share/fsl/data/standard/MNI152_T1_2mm_brain_mask.nii.gz \
        /home/data/NegativeCueing_RSA/NegCue_Random/derivatives/sl-svm_mni/sub-${sub}/sub-${sub}_space-MNI152_dimension-${hypothesis}_sl-radius-5_minus-chance.nii.gz
    done
done

for sub in 0{1..9} {10..25}; do
    echo working on ${sub} ...
    for hypothesis in ${hypothesis_list[@]}; do
        fslmaths /home/data/NegativeCueing_RSA/NegCue_Random/derivatives/sl-svm_mni/sub-${sub}/sub-${sub}_space-MNI152_dimension-${hypothesis}_sl-radius-5_minus-chance.nii.gz \
        -thr 0 \
        /home/data/NegativeCueing_RSA/NegCue_Random/derivatives/sl-svm_mni/sub-${sub}/sub-${sub}_space-MNI152_dimension-${hypothesis}_sl-radius-5_minus-chance.nii.gz
    done
done