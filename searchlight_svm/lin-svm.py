import re
import os
import glob
import sys

import numpy as np
import nibabel as nib
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import LeaveOneGroupOut # RepeatedKFold 
from sklearn.svm import LinearSVC

from nilearn.image import concat_imgs
from nibabel import save
from nilearn.decoding import SearchLight
from nilearn.image import load_img

sub = str(sys.argv[1])
phase = str(sys.argv[2])
dimension_list = [[f"positive{phase}", f"negative{phase}"], [f"positive{phase}", f"neutral{phase}"], [f"negative{phase}", f"neutral{phase}"]][int(sys.argv[3])]
permute_bool = False 
sl_radius = 4

scoring = "accuracy" 
print(f"using scoring metric:", scoring)

out_dir = "/home/data/NegativeCueing_RSA/scratch/eventrelated_exp"
betas_dir = f"/home/data/NegativeCueing_RSA/scratch/eventrelated_exp/lss_smoothed-0_mask-gm/sub-{sub}"

# set paths to store output
output_folder = out_dir + f"/lin-svm/sub-{sub}"
if not os.path.exists(output_folder):
    os.makedirs(output_folder, exist_ok=True)

# set file name
dim_ident = dimension_list[0] + "-" + dimension_list[1]
filename =  output_folder + f"/sub-{sub}_dimension-{dim_ident}.nii.gz"
if os.path.isfile(output_folder + filename):
    raise Exception("file already exists, abort mission ...")

# define usefull functions
def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    """
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    """
    return [atoi(c) for c in re.split(r"(\d+)", text)]

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
    img = nib.load(img)
    header = nib.Nifti1Header()
    affine = img.affine
    nii_file = nib.Nifti1Image(scores, affine, header)
    nib.save(nii_file, filename)
    return nii_file

def prepare_data(input_func_dir, sub, dimension_list=None, permute_bool=False):
    combined_global = []
    labels, chunks = [], []
    run_list = ["%.2d" % i for i in range(1, 13)]
    
    for run in run_list:
        print(f"load data for run-{run} ...")
        for dimension in dimension_list:
            func_runs = glob.glob(input_func_dir + f"/sub-{sub}_run-{run}_space-T1w_desc-{dimension}*.nii.gz")
            func_runs.sort(key=natural_keys)
            beta_files = []

            for betas_path in func_runs:
                img_tmp = betas_path
                beta_files.append(img_tmp)
                
                # add number of trials per run to labels & chunks
                labels.append([str(dimension)])
                chunks.append([str(run)])
                combined_img = load_img(beta_files)

            combined_global.append(combined_img)
    
    combined_global = concat_imgs(combined_global)
    labels_global = np.hstack(labels)
    chunks_global = np.hstack(chunks)

    print("labels:\t", labels_global)
    print("chunks:\t", chunks_global)
    print("shape of combined signal:\t", combined_global.shape)
    return combined_global, labels_global, chunks_global

cv = LeaveOneGroupOut()

decoder = Pipeline([
        ("scale", StandardScaler()),
        ("svm", LinearSVC(penalty="l2", dual=True, loss="squared_hinge", max_iter=2000))
])

brain_mask_path = f"/home/data/NegativeCueing_RSA/NegCue_Random/derivatives/fmriprep/sub-{sub}/anat/sub-{sub}_label-GM_prob-0.2.nii.gz"
brain_mask = load_img(brain_mask_path)
combined_global, labels, chunks = prepare_data(input_func_dir=betas_dir, sub=sub, dimension_list=dimension_list, permute_bool=permute_bool)

if not combined_global.shape[3] == labels.shape[0] == chunks.shape[0]:
    raise ValueError("Dimensions do not add up!")

sl = SearchLight(
    mask_img=brain_mask,
    radius=sl_radius,
    estimator=decoder,
    n_jobs=4,
    scoring=scoring,
    cv=cv,
    verbose=True)

# start fitting the searchlight objects
print("starting to fit individual searchlights ...")
sl.fit(imgs=combined_global, y=labels, groups=chunks)

print("saving img ...", filename)
np2nii(brain_mask_path, sl.scores_, filename)