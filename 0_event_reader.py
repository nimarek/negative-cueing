import numpy as np
import pandas as pd
import glob
import itertools

event_dir_list = glob.glob(
    "/home/data/NegativeCueing_RSA/NegCue_Random/code/events/sub-*/sub-*_task-negativesearch*_run-*_events.tsv"
)
event_dir_list.sort()

for f in event_dir_list:
    sub_id = f[67:69]
    run_id = f[106:108]
    # run_id = int(run_id) # fix wrong BIDS formating
    tmp_file = pd.read_csv(f, sep="\t")
    print(f"working on sub-{sub_id} and run-{run_id} ...")

    # get onsets for cue period and iti
    onset_fixation = tmp_file[tmp_file["event_type"].str.contains("fixation")]["onset"].values
    onset_cue = tmp_file[tmp_file["event_type"].str.contains("cue")]["onset"].values
    onset_delay = tmp_file[tmp_file["event_type"].str.contains("delay")]["onset"].values
    onset_search = tmp_file[tmp_file["event_type"].str.contains("search")]["onset"].values
    onset_iti = tmp_file[tmp_file["event_type"].str.contains("iti")]["onset"].values 
    onsets_all = [x for x in itertools.chain.from_iterable(itertools.zip_longest(onset_fixation, onset_cue, onset_delay, onset_search, onset_iti)) if x]

    # merge cue and delay duration into one
    dur_fixation = tmp_file[tmp_file["event_type"].str.contains("fixation")]["duration"].values
    dur_cue = tmp_file[tmp_file["event_type"].str.contains("cue")]["duration"].values
    dur_delay = tmp_file[tmp_file["event_type"].str.contains("delay")]["duration"].values
    dur_search = tmp_file[tmp_file["event_type"].str.contains("search")]["duration"].values
    dur_iti = tmp_file[tmp_file["event_type"].str.contains("iti")]["duration"].values 
    duration_all = [x for x in itertools.chain.from_iterable(itertools.zip_longest(dur_fixation, dur_cue, dur_delay, dur_search, dur_iti)) if x]
    
    tmp_file = tmp_file[~tmp_file.event_type.str.contains("response")]
    tmp_file["event_type"] = [s.replace("iti", "intertrial") for s in tmp_file["event_type"]]
    trial_type_list = (tmp_file["trial_type"] + tmp_file["event_type"] + tmp_file["cue_type"])
    """
    TR is 2 seconds, add 1 to onsets because of slice timing correction. Check
    https://fmriprep.org/en/stable/outputs.html for more infos.
    """
    onsets_all = [i + 1 for i in onsets_all]

    # create new dataframe from dict to store data
    merged_df = pd.DataFrame(
    {"onset": onsets_all,
     "duration": duration_all,
     "trial_type": trial_type_list
    })

    store_path = f"/home/data/NegativeCueing_RSA/NegCue_Random/sub-{sub_id}/func/sub-{sub_id}_task-negativesearcheventrelated_run-{run_id}_events.tsv"
    merged_df.to_csv(store_path, index=False, sep="\t")