#!/bin/bash
# 
echo processing csv files in all subdirectories and current directory.
echo PWD: $(pwd)
echo processing csv file in current directory
echo PWD: $(pwd)
for file in `ls -f *.csv`
do 
	if test -f $file
	then
		echo processing csv file : $file via python 
		python 20220815_dump2csv_mesh_allocation.py $file 
	fi
done
echo processing csv file in subdirectories of current directory
echo PWD: $(pwd)
for dir in `ls -d */`
do 
	if test -d $dir
	then 
		cd $dir
		echo PWD: $(pwd)
		for file in `ls -f $1.*`
		do 
			if test -f $file
			then
				echo processing csv file : $file via python 
				python ../20220805_dump2csv_proc.py $file 
			fi 
		done
		cd ../
		echo PWD: $(pwd) 
	fi 
done 
echo all done. 
exit 
#1-id 
#2-mol 
#3-type 
#4-element 
#5-mass 
#6-v_radius 
#7-x 
#8-y 
#9-z 
#10-vx 
#11-vy 
#12-vz 
#13-fx 
#14-fy 
#15-fz 
#16-q
# End of file 