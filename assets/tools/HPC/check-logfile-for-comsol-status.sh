#!/bin/bash
#
for file in */*.log;
do
	echo $file;
	grep 'Opening ' $file;
	grep 'max_mesh_sample ' $file;
	grep 'max_mesh_else ' $file;
	grep 'max_mesh_gaps ' $file;
	grep 'ang = ' $file;
	tail $file;
	grep 'Saving ' $file;
	echo ++++++++++++++++++++;
done
