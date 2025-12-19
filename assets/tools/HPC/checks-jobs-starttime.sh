#!/bin/bash
#
duration=$((24 * 60 * 60))
#
start_time=$(date +%s)
#
while [ $(($(date +%s) - start_time)) -lt $duration ];
do
    #
    squeue -u makhsry -l --start | awk 'NR>1 && $1 ~ /^[0-9]/ {print $1, $6}' | while read -r JOBID START_TIME; 
	do
        if [ "$START_TIME" != "N/A" ]; then
            unix_time=$(date -d "${START_TIME//T/ }" +%s 2>/dev/null)
            if [ $? -eq 0 ]; then
                echo "$unix_time $START_TIME" >> "${JOBID}.starttime"
            else
                echo "Error converting START_TIME for JOBID $JOBID: $START_TIME"
            fi
        fi
    	done
    	sleep 60
done
# 
#gnuplot plot_with.gnuplot
