#!/bin/bash

source /home/data/software/experimental/ipsy-env/activate

echo "calling python script with for sub-$1 & run-$2"
python3 /home/data/NegativeCueing_RSA/NegCue_Random/code/searchlight_rsa/1_sl_rdms.py $1 $2 $3
# python3 /home/data/NegativeCueing_RSA/NegCue_Random/code/searchlight_rsa/1_cross-run_sl-rdm.py $1 $2 $3 $4