#!/bin/bash
export KB_DEPLOYMENT_CONFIG=/kb/dev_container/modules/msa_muscle/deploy.cfg
export PYTHONPATH=/kb/dev_container/modules/msa_muscle/lib:$PATH:$PYTHONPATH
uwsgi --master --processes 5 --threads 5 --http :5000 --wsgi-file /kb/dev_container/modules/msa_muscle/lib/msa_muscle/msa_muscleServer.py
