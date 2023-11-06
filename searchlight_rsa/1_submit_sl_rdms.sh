logs_dir=/home/data/NegativeCueing_RSA/NegCue_Random/code/logs_sl-rdm/
# create the logs dir if it doesn't exist
[ ! -d "$logs_dir" ] && mkdir -p "$logs_dir"

# exclude bad nodes from analysis

printf "# The environment
universe       = vanilla
getenv         = True
request_cpus   = 1
request_memory = 40G
# Execution
initial_dir    = /home/data/NegativeCueing_RSA/NegCue_Random/code/
executable     = 1_sl-rdm.sh
\n"

for sub in 0{1..9} {10..25}; do
    for phase in 0 1; do
        printf "arguments = ${sub} ${phase}\n"
        printf "log       = ${logs_dir}/sub-${sub}_phase-${phase}_\$(Cluster).\$(Process).log\n"
        printf "output    = ${logs_dir}/sub-${sub}_phase-${phase}_\$(Cluster).\$(Process).out\n"
        printf "error     = ${logs_dir}/sub-${sub}_phase-${phase}_\$(Cluster).\$(Process).err\n"
        printf "Queue\n\n"
    done
done