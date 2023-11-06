from nilearn import image
from templateflow import api as tflow

func_ref_path = "/home/data/NegativeCueing_RSA/scratch/eventrelated_exp/corr-maps_phase-cue_smoothed-6_mni/sub-01_cue-attent_mni.nii.gz"

mni_gm = tflow.get("MNI152NLin2009cAsym", desc=None, label="GM", resolution=2, suffix="probseg", extension="nii.gz")
gray_matter_binary = image.math_img("i1 > 0.50", i1=image.load_img(mni_gm))
gray_matter_binary.to_filename("source_mni_gm.nii.gz")

image.resample_to_img("source_mni_gm.nii.gz", func_ref_path, interpolation="nearest").to_filename("resampled_mni_gm.nii.gz")