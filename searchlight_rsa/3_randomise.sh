#!/bin/bash

threshold=0.95
permutations=5000
phase=${1}
hypothesis=${2}
output_path="/home/data/NegativeCueing_RSA/scratch/eventrelated_exp/permutation_results/phase-${phase}_hypothesis-${hypothesis}"

echo starting group-lvl for phase-${phase} hypothesis-${hypothesis}

echo creating folders ...
mkdir -p ${output_path}

echo merging input files ...
fslmerge -t ${output_path}/output_complete `ls /home/data/NegativeCueing_RSA/scratch/eventrelated_exp/corr-maps_phase-${phase}_mni/*${hypothesis}*.nii.gz`

# echo calculating negative correlation values ...
# fslmaths ${output_path}/output_complete -mul -1 ${output_path}/output_complete

echo starting permutation-test ...
randomise -i ${output_path}/output_complete -o ${output_path}/perm_hypothesis-${hypothesis} -1 -T -v 0 -n ${permutations} -m /home/data/NegativeCueing_RSA/NegCue_Random/code/masks/resampled_mni_gm.nii.gz

echo combining maps ...
fslmaths ${output_path}/perm_hypothesis-${hypothesis}_tfce_corrp_tstat1.nii.gz -thr ${threshold} -bin -mul ${output_path}/perm_hypothesis-${hypothesis}_tstat1.nii.gz ${output_path}/results-${hypothesis}_output_complete

echo extracting cluster information ...
cluster --in=${output_path}/results-${hypothesis}_output_complete --thresh=0.0001 --oindex=${output_path}/results-${hypothesis}_output_complete_cluster_index --olmax=${output_path}/results-${hypothesis}_output_complete_lmax.txt --osize=${output_path}/results-${hypothesis}_output_complete_cluster_size

echo removing smoothed files and marged input file
rm ${output_path}/output_complete.nii.gz