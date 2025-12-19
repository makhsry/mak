#!/bin/bash
# run as: ./script.sh "last_solution_maxHT_0.25_maxGaps_1_maxCavity_1_maxSample_1_ang_*.mph"
if [ -z "$1" ]; then
    echo "Usage: $0 '<pattern_with_*>'"
    exit 1
fi
# Expand the provided pattern into matching files
files=($1)
# Ensure files exist
if [ ${#files[@]} -eq 0 ]; then
    echo "No files matching the pattern found."
    exit 1
fi
# Extract numbers and find the max
max_num=-1
max_file=""
#
for file in "${files[@]}"; do
    num=$(echo "$file" | grep -oP '(?<=_ang_)\d+(?=\.mph)')
    if [[ "$num" =~ ^[0-9]+$ ]] && (( num > max_num )); then
        max_num=$num
        max_file="$file"
    fi
done
# Delete all except the max
for file in "${files[@]}"; do
    if [[ "$file" != "$max_file" ]]; then
        echo "Deleting: $file"
        rm "$file"
    fi
done
#
echo "Keeping: $max_file"
# End of file