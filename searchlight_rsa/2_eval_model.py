import os
import glob
import sys

import numpy as np
import nibabel as nib
from rsatoolbox.rdm.rdms import load_rdm
from rsatoolbox.model import ModelFixed
from rsatoolbox.inference import eval_fixed
from rsatoolbox.util.searchlight import evaluate_models_searchlight

import matplotlib.pyplot as plt
import seaborn as sns

phase_list = ["cue", "delay"]
hypothesis_list = ["cue-item-indep", "cue-attent", "cue-inhibition"]

sub = str(sys.argv[1])
phase, hypothesis = phase_list[int(sys.argv[2])], hypothesis_list[int(sys.argv[3])]
distance = "spearman"

in_dir = f"/home/data/NegativeCueing_RSA/scratch/eventrelated_exp/neural-rdms_phase-{phase}_lss" 
out_dir = "/home/data/NegativeCueing_RSA/scratch/eventrelated_exp"

# save image
sub_folder_save = out_dir + f"/corr-maps_phase-{phase}_lss/sub-{sub}"
if not os.path.exists(sub_folder_save):
    os.makedirs(sub_folder_save, exist_ok=True)
filename_save = f"/sub-{sub}_task-negativesearcheventrelated_hypothesis-{hypothesis}.nii.gz"

if os.path.isfile(sub_folder_save + filename_save):
    raise Exception("file already exists, abort mission ...")

def upper_tri(RDM):
    m = RDM.shape[0]
    r, c = np.triu_indices(m, 1)
    return RDM[r, c]

def np2nii(img, scores, filename):
    """
    It saves data into a nifti file
    by leveraging on another image
    of the same size.
    Parameters
    ----------
    img : nifti file (e.g a mask)
    scores : numpy array containing decoding scores
    filename : string name of the new nifti file
    Returns
    -------
    nii_file : Nifti1Image
    """
    header = nib.Nifti1Header()
    affine = img.affine
    nii_file = nib.Nifti1Image(scores, affine, header)
    nib.save(nii_file, filename)
    return nii_file

def fisher_r_to_z(x):
    """    
    correct any rounding errors
    correlations cannot be greater than 1.
    """
    x = np.clip(x, -1, 1)
    return np.arctanh(x)

def merge_masks(input_path):
    return binarize_img(mean_img(glob.glob(input_path)))

# load model rdm containing specific hypothesis about relationships
if hypothesis == "cue-item-indep":
    neg_cue_matrix = np.loadtxt(
        os.getcwd() + "/hypothesis_rdms/" + "rdm-matrix_cue-item-indep.csv", delimiter=","
    )
elif hypothesis == "cue-attent":
    neg_cue_matrix = np.loadtxt(
        os.getcwd() + "/hypothesis_rdms/" + "rdm-matrix_cue-attent.csv", delimiter=","
    )
elif hypothesis == "cue-inhibition":
    neg_cue_matrix = np.loadtxt(
        os.getcwd() + "/hypothesis_rdms/" + "rdm-matrix_cue-inhibition.csv", delimiter=","
    )

neg_cue_matrix = np.tile(neg_cue_matrix, (12, 12))
eval_model = ModelFixed("Negatice Cue RDM", upper_tri(neg_cue_matrix))

# load sl rdms for each voxel
sub_neural_path = (in_dir + f"/sub-{sub}")
filename_hdf = f"/sub-{sub}_task-negativesearcheventrelated"

rdm = load_rdm(sub_neural_path + filename_hdf, file_type="hdf5")

print(f"working on sub-{sub}. Shape of the model rdm: {neg_cue_matrix.shape}, shape of the neural rdm: {rdm.dissimilarities.shape}")

# evaluate each voxel RDM with a fixed effects model
eval_results = evaluate_models_searchlight(
    sl_RDM=rdm,
    models=eval_model,
    eval_function=eval_fixed,
    method=distance,
    n_jobs=4,
)
eval_score = [np.float(e.evaluations) for e in eval_results]
eval_score = fisher_r_to_z(eval_score)

sns.distplot(eval_score)
plt.title(f"sub-{sub} hypothesis-{hypothesis}", size=14)
plt.ylabel("Occurance", size=18)
plt.xlabel(f"{distance}", size=18)
sns.despine()

# load mask
mask_img = nib.load(f"/home/data/NegativeCueing_RSA/NegCue_Random/derivatives/fmriprep/sub-{sub}/anat/sub-{sub}_complete-mask.nii.gz")
mask_data = mask_img.get_fdata()
x, y, z = mask_data.shape

RDM_brain = np.zeros([x * y * z])
RDM_brain[list(rdm.rdm_descriptors["voxel_index"])] = list(eval_score)
RDM_brain = RDM_brain.reshape([x, y, z])

plt.savefig(sub_folder_save + f"/sub-{sub}_{hypothesis}.png")
plt.close()

print(f"saving file to: {sub_folder_save + filename_save} ...")
np2nii(mask_img, RDM_brain, sub_folder_save + filename_save)