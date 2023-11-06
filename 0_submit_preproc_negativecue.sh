#!/bin/bash

logs_dir=/home/data/NegativeCueing_RSA/NegCue_Random/code/logs_fmriprep/
# create the logs dir if it doesn't exist
[ ! -d "$logs_dir" ] && mkdir -p "$logs_dir"

printf "# The environment
universe       = vanilla
getenv         = True
request_cpus   = 8
request_memory = 16GB

# Execution
initial_dir    = /home/data/NegativeCueing_RSA/NegCue_Random/code/
executable     = 0_preproc_negativecue.sh
\n"

for sub in 0{1..9} {10..25}; do
    printf "arguments = ${sub}\n"
    printf "log       = ${logs_dir}/sub-${sub}_\$(Cluster).\$(Process).log\n"
    printf "output    = ${logs_dir}/sub-${sub}_\$(Cluster).\$(Process).out\n"
    printf "error     = ${logs_dir}/sub-${sub}_\$(Cluster).\$(Process).err\n"
    printf "Queue\n\n"
done