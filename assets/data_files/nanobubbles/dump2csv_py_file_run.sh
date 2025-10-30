#!/bin/bash
# 
echo PWD: $(pwd)
echo processing csv file in current directory
echo PWD: $(pwd)
for file in `ls -f *.csv`
do 
	if test -f $file
	then
		echo processing csv file : $file via python 
		python dump2csv_mesh_allocation.py $file
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