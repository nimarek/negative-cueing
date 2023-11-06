logs_dir=/home/data/NegativeCueing_RSA/NegCue_Random/code/logs_group-lvl/
# create the logs dir if it doesn't exist
[ ! -d "$logs_dir" ] && mkdir -p "$logs_dir"

# exclude bad nodes from analysis

printf "# The environment
universe       = vanilla
getenv         = True
request_cpus   = 6
request_memory = 15G
# Execution
initial_dir    = /home/data/NegativeCueing_RSA/NegCue_Random/code/searchlight_rsa/
executable     = 3_permute.sh
\n"


for phase in "cue" "delay"; do 
    for hypothesis in "cue-attent" "cue-inhibition" "cue-item-indep"; do
        printf "arguments = ${phase} ${hypothesis}\n"
        printf "log       = ${logs_dir}/${phase}_${hypothesis}_\$(Cluster).\$(Process).log\n"
        printf "output    = ${logs_dir}/${phase}_${hypothesis}_\$(Cluster).\$(Process).out\n"
        printf "error     = ${logs_dir}/${phase}_${hypothesis}_\$(Cluster).\$(Process).err\n"
        printf "Queue\n\n"
    done
done
