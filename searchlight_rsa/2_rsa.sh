#!/bin/bash

source /home/data/software/experimental/ipsy-env/activate

echo "calling python script with for sub-$1"
python3 /home/data/NegativeCueing_RSA/NegCue_Random/code/searchlight_rsa/2_eval_model.py $1 $2 $3 