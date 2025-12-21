#!/bin/bash

for file in *-*; do
    # The [ -e "$file" ] check prevents errors if no files match
    [ -e "$file" ] || continue

    mv -v -- "$file" "${file//-/_}"
done

echo "Renaming complete!"
