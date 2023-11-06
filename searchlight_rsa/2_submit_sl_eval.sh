logs_dir=/home/data/NegativeCueing_RSA/NegCue_Random/code/logs_eval/
# create the logs dir if it doesn't exist
[ ! -d "$logs_dir" ] && mkdir -p "$logs_dir"

# exclude bad nodes from analysis

printf "# The environment
universe       = vanilla
getenv         = True
request_cpus   = 3
request_memory = 28G
# Execution
initial_dir    = /home/data/NegativeCueing_RSA/NegCue_Random/code/searchlight_rsa/
executable     = 2_rsa.sh
\n"

for sub in 0{1..9} {10..25}; do
    for phase in 0 1; do 
        for hypothesis in {0..2}; do
            printf "arguments = ${sub} ${phase} ${hypothesis}\n"
            printf "log       = ${logs_dir}/sub-${sub}_${phase}_${hypothesis}_\$(Cluster).\$(Process).log\n"
            printf "output    = ${logs_dir}/sub-${sub}_${phase}_${hypothesis}_\$(Cluster).\$(Process).out\n"
            printf "error     = ${logs_dir}/sub-${sub}_${phase}_${hypothesis}_\$(Cluster).\$(Process).err\n"
            printf "Queue\n\n"
        done
    done
done