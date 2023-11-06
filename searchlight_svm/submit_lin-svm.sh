logs_dir=/home/data/NegativeCueing_RSA/NegCue_Random/code/logs_sl-svm/
# create the logs dir if it doesn't exist
[ ! -d "$logs_dir" ] && mkdir -p "$logs_dir"

# exclude bad nodes from analysis

printf "# The environment
universe       = vanilla
getenv         = True
request_cpus   = 4
request_memory = 1G
# Execution
initial_dir    = /home/data/NegativeCueing_RSA/NegCue_Random/code/searchlight_svm/
executable     = lin-svm.sh
\n"

for sub in 0{1..9} {10..25}; do
    for phase in "cue" "delay"; do
        for dim in {0..2}; do 
            printf "arguments = ${sub} ${phase} ${dim}\n"
            printf "log       = ${logs_dir}/sub-${sub}_phase-${phase}_dim-${dim}_\$(Cluster).\$(Process).log\n"
            printf "output    = ${logs_dir}/sub-${sub}_phase-${phase}_dim-${dim}_\$(Cluster).\$(Process).out\n"
            printf "error     = ${logs_dir}/sub-${sub}_phase-${phase}_dim-${dim}_\$(Cluster).\$(Process).err\n"
            printf "Queue\n\n"
        done
    done
done