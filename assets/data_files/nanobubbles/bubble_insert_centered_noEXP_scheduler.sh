#!/bin/bash 
#
echo script -scheduler.sh- is open
echo .... bubble-seeded experiments ....
echo .... SINGLE BUBBLE ....
echo .... SEED before EXPANSION ....
N=1
X=0
Y=0
Z=0
echo current directory is $(pwd)
#
#CENTER
#
echo .... CENTERED BUBBLE: x,y,z=0 ....
for RADIUS in `seq 1 1 5`
do
	echo processing for $N bubbles with size R : $RADIUS, positioned at X: $X, Y:$Y, Z:$Z
	echo creating directory b$RADIUS'An'$N'cp'$X$Y$Z
	mkdir b$RADIUS'An'$N'cp'$X$Y$Z
	echo created directory b$RADIUS'An'$N'cp'$X$Y$Z
	echo copying files TIP4P2005.txt, in.lmps and run.pbs to path b$RADIUS'An'$N'cp'$X$Y$Z
	cp TIP4P2005.txt b$RADIUS'An'$N'cp'$X$Y$Z/
	cp in.lmps b$RADIUS'An'$N'cp'$X$Y$Z/
	cp run.pbs b$RADIUS'An'$N'cp'$X$Y$Z/
	echo copied files TIP4P2005.txt, in.lmps and run.pbs to path b$RADIUS'An'$N'cp'$X$Y$Z
	echo enetring directory b$RADIUS'An'$N'cp'$X$Y$Z
	cd b$RADIUS'An'$N'cp'$X$Y$Z/
	echo current directory is $(pwd)
	echo editing jobname in file: run.pbs
	sed -i '4s/.*/#PBS -N ncn1_b'$RADIUS'An'$N'cp'$X$Y$Z'/' run.pbs
	echo Done editing jobname in file: run.pbs
	echo editing bubble in file: in.lmps
	sed -i '244s/.*/variable bubbleR equal '$RADIUS'/' in.lmps
	sed -i '245s/.*/variable XHI equal 0/' in.lmps
	sed -i '246s/.*/variable bubbleX equal 0/' in.lmps
	sed -i '247s/.*/variable bubbleY equal '$Y'/' in.lmps
	sed -i '248s/.*/variable bubbleZ equal '$Z'/' in.lmps
	echo Done editing bubble in file: in.lmps
	echo submiting job ....
	qsub run.pbs
	echo Submitted job 
	echo leaving directory b$RADIUS'An'$N'cp'$X$Y$Z
	cd ../
	echo current directory is $(pwd)	
done
#
#RIGHT
#
for LOCATION in `seq 100 -25 25`
do
	echo .... BUBBLE: x = $LOCATION'xR',y,z=0 ....
	for RADIUS in `seq 1 1 5`
	do
		echo processing for $N bubbles with size R : $RADIUS, positioned at X: $LOCATION'xR', Y:$Y, Z:$Z
		echo creating directory b$RADIUS'An'$N'rp'$LOCATION'xR'$Y$Z
		mkdir b$RADIUS'An'$N'rp'$LOCATION'xR'$Y$Z
		echo created directory b$RADIUS'An'$N'rp'$LOCATION'xR'$Y$Z
		echo copying files TIP4P2005.txt, in.lmps and run.pbs to path b$RADIUS'An'$N'rp'$LOCATION'xR'$Y$Z
		cp TIP4P2005.txt b$RADIUS'An'$N'rp'$LOCATION'xR'$Y$Z/
		cp in.lmps b$RADIUS'An'$N'rp'$LOCATION'xR'$Y$Z/
		cp run.pbs b$RADIUS'An'$N'rp'$LOCATION'xR'$Y$Z/
		echo copied files TIP4P2005.txt, in.lmps and run.pbs to path b$RADIUS'An'$N'rp'$LOCATION'xR'$Y$Z
		echo enetring directory b$RADIUS'An'$N'rp'$LOCATION'xR'$Y$Z
		cd b$RADIUS'An'$N'rp'$LOCATION'xR'$Y$Z/
		echo current directory is $(pwd)
		echo editing jobname in file: run.pbs
		sed -i '4s/.*/#PBS -N ncn1_b'$RADIUS'An'$N'rp'$LOCATION'xR'$Y$Z'/' run.pbs
		echo Done editing jobname in file: run.pbs
		echo editing bubble in file: in.lmps
		sed -i '244s/.*/variable bubbleR equal '$RADIUS'/' in.lmps
		sed -i '245s/.*/variable XHI equal xhi/' in.lmps
		sed -i '246s/.*/variable bubbleX equal '$LOCATION'*0.01*${XHI}''/' in.lmps
		sed -i '247s/.*/variable bubbleY equal '$Y'/' in.lmps
		sed -i '248s/.*/variable bubbleZ equal '$Z'/' in.lmps
		echo Done editing bubble in file: in.lmps
		echo submiting job ....
		qsub run.pbs
		echo Submitted job 
		echo leaving directory b$RADIUS'An'$N'rp'$LOCATION'xR'$Y$Z
		cd ../
		echo current directory is $(pwd)	
	done
done 
#
# LEFT
#
for LOCATION in `seq 100 -25 25`
do
	echo .... BUBBLE: x = $LOCATION'xL',y,z=0 ....
	for RADIUS in `seq 1 1 5`
	do
		echo processing for $N bubbles with size R : $RADIUS, positioned at X: $LOCATION'xL', Y:$Y, Z:$Z
		echo creating directory b$RADIUS'An'$N'lp'$LOCATION'xL'$Y$Z
		mkdir b$RADIUS'An'$N'lp'$LOCATION'xL'$Y$Z
		echo created directory b$RADIUS'An'$N'lp'$LOCATION'xL'$Y$Z
		echo copying files TIP4P2005.txt, in.lmps and run.pbs to path b$RADIUS'An'$N'lp'$LOCATION'xL'$Y$Z
		cp TIP4P2005.txt b$RADIUS'An'$N'lp'$LOCATION'xL'$Y$Z/
		cp in.lmps b$RADIUS'An'$N'lp'$LOCATION'xL'$Y$Z/
		cp run.pbs b$RADIUS'An'$N'lp'$LOCATION'xL'$Y$Z/
		echo copied files TIP4P2005.txt, in.lmps and run.pbs to path b$RADIUS'An'$N'lp'$LOCATION'xL'$Y$Z
		echo enetring directory b$RADIUS'An'$N'lp'$LOCATION'xL'$Y$Z
		cd b$RADIUS'An'$N'lp'$LOCATION'xL'$Y$Z/
		echo current directory is $(pwd)
		echo editing jobname in file: run.pbs
		sed -i '4s/.*/#PBS -N ncn1_b'$RADIUS'An'$N'lp'$LOCATION'xL'$Y$Z'/' run.pbs
		echo Done editing jobname in file: run.pbs
		echo editing bubble in file: in.lmps
		sed -i '244s/.*/variable bubbleR equal '$RADIUS'/' in.lmps
		sed -i '245s/.*/variable XLO equal xlo/' in.lmps
		sed -i '246s/.*/variable bubbleX equal '$LOCATION'*0.01*${XLO}''/' in.lmps
		sed -i '247s/.*/variable bubbleY equal '$Y'/' in.lmps
		sed -i '248s/.*/variable bubbleZ equal '$Z'/' in.lmps
		echo Done editing bubble in file: in.lmps
		echo submiting job ....
		qsub run.pbs
		echo Submitted job 
		echo leaving directory b$RADIUS'An'$N'lp'$LOCATION'xL'$Y$Z
		cd ../
		echo current directory is $(pwd)	
	done
done 
# End of file
