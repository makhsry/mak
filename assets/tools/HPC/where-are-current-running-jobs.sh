#!/bin/bash
USER="makhsry"
job_ids=$(squeue -u $USER -h -o "%i")
for job_id in $job_ids; do
    job_dir=$(scontrol show job $job_id | grep -oP 'WorkDir=\K\S+')
    echo "Job ID: $job_id - Directory: $job_dir"
done
