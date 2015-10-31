#!/bin/bash
export PYTHONPATH=/kb/dev_container/modules/msa_muscle/lib:$PATH:$PYTHONPATH
python /kb/dev_container/modules/msa_muscle/lib/msa_muscle/msa_muscleServer.py $1 $2 $3
