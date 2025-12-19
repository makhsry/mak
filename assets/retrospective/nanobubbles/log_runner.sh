#!/bin/bash 
#
for dir in `ls -d */`
do
	cd $dir
	../log_parser.sh < log.lammps&
	cd ../
done
# End of file
