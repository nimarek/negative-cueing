import os
import re
import sys
import glob

import numpy as np
import nibabel as nib
from nilearn.image import mean_img, binarize_img, math_img
from rsatoolbox.rdm.rdms import RDMs
from rsatoolbox.util.searchlight import (
    get_volume_searchlight,
    get_searchlight_RDMs,
)

phase_list = ["cue", "delay"]

sub = str(sys.argv[1])
run = "*"
phase = phase_list[int(sys.argv[2])]

bids_dir = "/home/data/NegativeCueing_RSA/NegCue_Random"
beta_dir = "/home/data/NegativeCueing_RSA/scratch/eventrelated_exp/lss_smoothed-2_mask-full"
# beta_dir = "/home/data/NegativeCueing_RSA/NegCue_Random/derivatives/nibetaseries"
out_dir = "/home/data/NegativeCueing_RSA/scratch/eventrelated_exp"

# analysis hyperparameters
radius = 4
distance_metric = "correlation"

# set paths to store output
output_folder = out_dir + f"/neural-rdms_phase-{phase}_lss/sub-{sub}/"
if not os.path.exists(output_folder):
    os.makedirs(output_folder, exist_ok=True)

# set file name
filename = f"/sub-{sub}_task-negativesearcheventrelated"

if os.path.isfile(output_folder + filename):
    raise Exception("file already exists, abort mission ...")

print(f"working on sub-{sub} phase-{phase}")

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    '''
    return [atoi(c) for c in re.split(r'(\d+)', text)]

def set_paths(sub=None, run=None, phase=None, beta_dir=None):
    image_paths = glob.glob(beta_dir + f"/sub-{sub}/sub-{sub}_run-{run}_space-T1w_desc-*{phase}*.nii.gz")   
    # image_paths = glob.glob(beta_dir + f"/sub-{sub}/func/sub-{sub}_task-negativesearcheventrelated_run-{run}_space-T1w_desc-*{phase}*_betaseries.nii.gz")
    image_paths.sort(key=natural_keys)
    return image_paths

def create_dataset(image_paths):
    labels = []

    # load data with only one time point
    reference_img = nib.load(image_paths[0])
    x, y, z, = reference_img.get_fdata().shape

    # create dummy df according to coordinates
    data = np.zeros((len(image_paths), x, y, z))

    for x, im in enumerate(image_paths):
        print("contrast loaded:\t", im)
        labels.append(im)
        data[x] = nib.load(im).get_fdata()
    return data, labels

def merge_masks(input_path):
    return binarize_img(mean_img(glob.glob(input_path)))

# load mask
mask_img = merge_masks(f"/home/data/NegativeCueing_RSA/NegCue_Random/derivatives/fmriprep/sub-{sub}/func/sub-{sub}_task-negativesearcheventrelated_run-*_space-T1w_desc-brain_mask.nii.gz")
mask_data = mask_img.get_fdata()
x, y, z = mask_data.shape

print(f"shape of the mask:\t {mask_data.shape}")

# create dataset
image_paths = set_paths(sub=sub, run=run, phase=phase, beta_dir=beta_dir)

# remove a condition from input list
image_paths = [x for x in image_paths if "neutral" not in x]
# image_paths = [x for x in image_paths if "residuals_bold" not in x]
data, labels = create_dataset(image_paths)

# reshape data so we have n_observastions x n_voxels
data_2d = data.reshape([data.shape[0], -1])
mask_2d = ~np.all(data_2d==0, axis=0)
mask_3d = mask_2d.reshape(x, y, z)
print("shape of 2d data ...\t", data_2d.shape)

centers, neighbors = get_volume_searchlight(mask_data, radius=radius, threshold=0.5)
sl_rdms = get_searchlight_RDMs(data_2d, centers, neighbors, labels, method=distance_metric)

# save output as .hdf5
sl_rdms.save(output_folder + filename, file_type="hdf5", overwrite=True)