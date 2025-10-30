#!/bin/bash
for i in `seq 0 100000 5000000`; 
	do 
	cp trjs/trj.$i .; 
done
# End of file 