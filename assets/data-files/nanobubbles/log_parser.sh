#!/bin/bash
# processing LAMMPS log file 
i=0
data_idx=`grep -n '   Step      Elaplong' log.lammps | cut -f1 -d:` # 
for data_i in $data_idx; do
    i=$(($i + 1));
    reading_starts=$(($data_i + 1));
    run_idx=`grep -n 'Loop time of ' log.lammps | cut -f1 -d:` # length = data_idx + 1
    j=-1
    for dummy in $run_idx; do 
        j=$(($j + 1));
        if [ "$i" -eq "$j" ]; then
            reading_stops=$(($dummy - 1));
            for L in `seq $reading_starts $reading_stops`; do
                data=`sed -n ${L}p log.lammps`;
                echo  $data >> dummy.csv;
            done
        fi
    done 
done
sed '${/^[[:space:]]*$/d}' dummy.csv > OUT.csv;
rm dummy.csv
# ----
exit
###########################################################
# backups 
###########################################################
#!/bin/bash
# processing LAMMPS log file 
i=0
data_idx=`grep -n '   Step      Elaplong' log.lammps | cut -f1 -d:` # 
for data_i in $data_idx; do
    i=$(($i + 1));
    reading_starts=$(($data_i + 1));
    run_idx=`grep -n 'Loop time of ' log.lammps | cut -f1 -d:` # length = data_idx + 1
    j=-1
    for dummy in $run_idx; do 
        j=$(($j + 1));
        if [ "$i" -eq "$j" ]; then
            reading_stops=$(($dummy - 1));
			line=0
			while read Step Elaplong Temp Press Density Volume PotEng KinEng TotEng Enthalpy E_vdwl E_tail E_coul E_pair E_mol E_long Xlo Xhi Ylo Yhi Zlo Zhi CellAlpha CellBeta CellGamma Cella Cellb Cellc Pxx Pyy Pzz Pxy Pxz Pyz Fmax Fnorm; do
				line=$(($line + 1));
				if [ "$line" -lt "$reading_stops" ] && [ "$line" -gt "$reading_starts" ]; then
					echo $Step >> Step.out
					echo $Elaplong  >> Elaplong.out
					echo $Temp >>  Temp.out
					echo $Press >>  Press.out
					echo $Density >>  Density.out
					echo $Volume >>  Volume.out
					echo $PotEng >>  PotEng.out
					echo $KinEng >>  KinEng.out
					echo $TotEng >>  TotEng.out
					echo $Enthalpy >>  Enthalpy.out
					echo $E_vdwl >>  E_vdwl.out
					echo $E_tail >>  E_tail.out
					echo $E_coul >>  E_coul.out
					echo $E_pair >> E_pair.out
					echo $E_mol >>  E_mol.out
					echo $E_long >> E_long.out
					echo $Xlo >> Xlo.out
					echo $Xhi >>  Xhi.out
					echo $Ylo >>  Ylo.out
					echo $Yhi >>  Yhi.out
					echo $Zlo >>  Zlo.out
					echo $Zhi >>  Zhi.out
					echo $CellAlpha >> CellAlpha.out
					echo $CellBeta >> CellBeta.out
					echo $CellGamma >> CellGamma.out
					echo $Cella >>  Cella.out
					echo $Cellb >>  Cellb.out
					echo $Cellc >>  Cellc.out
					echo $Pxx >>  Pxx.out
					echo $Pyy >>  Pyy.out
					echo $Pzz >>  Pzz.out
					echo $Pxy >>  Pxy.out
					echo $Pxz >>  Pxz.out
					echo $Pyz >>  Pyz.out
					echo $Fmax >>  Fmax.out
					echo $Fnorm >>  Fnorm.out
				fi
			done < log.lammps
        fi
    done 
done
# --------------------------------

# End of file