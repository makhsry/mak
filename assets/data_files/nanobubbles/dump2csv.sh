#!/bin/bash
# exec as: dump2csv.sh 0/1 namestyle1 namestyle2 namestyle3 ....
# 1 - do for subdirectories, and current directory  
# 0 - current directory only 
types=$#
#types=$((types - 1))
n=$((types-1))
mode=$1
shift 1
if (( $mode == 0 ))
then 
	echo processing dump files in current directory only. 
	echo PWD: $(pwd)
	i=0
	while (($i < $n))
	do
		i=$((i + 1)); 
		echo step $i / $n
		for file in `ls -f $1.*`
		do 
			if test -f $file
			then
				echo converting file : $file 
				timestep=`echo "${file##*.}"`
				filename=`echo "${file%%.*}"`
				awk '{print $1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16}' OFS=',' $file |&
				awk '/^ITEM:,ATOMS/{flag=1;next}flag' > $timestep'.csv'
			fi
		done
		shift 1
	done 
else 
	echo processing dump files in all subdirectories and current directory.
	echo PWD: $(pwd)
		i=0
		while (($i < $n))
		do
			i=$((i + 1)); 
			echo step $i / $n
			echo processing dump style : $1 in current directory
			echo PWD: $(pwd)
			for file in `ls -f $1.*`
			do 
				if test -f $file
				then
					echo converting file : $file 
					timestep=`echo "${file##*.}"`
					filename=`echo "${file%%.*}"`
					awk '{print $1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16}' OFS=',' $file |&
					awk '/^ITEM:,ATOMS/{flag=1;next}flag' > $timestep'.csv'
				fi
			done
			echo processing dump style : $1 in subdirectories of current directory
			echo PWD: $(pwd)
			for dir in `ls -d */`
			do 
				cd $dir
				echo PWD: $(pwd)
				for file in `ls -f $1.*`
				do 
					if test -f $file
					then
						echo converting file : $file 
						timestep=`echo "${file##*.}"`
						filename=`echo "${file%%.*}"`
						awk '{print $1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16}' OFS=',' $file |&
						awk '/^ITEM:,ATOMS/{flag=1;next}flag' > $timestep'.csv'
					fi 
				done
				cd ../
				echo PWD: $(pwd) 
			done 
			shift 1
		done
fi 
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