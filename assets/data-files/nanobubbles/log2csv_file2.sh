#!/bin/bash
awk '{print $1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17,$18,$19,$20,$21,$22,$23,$24,$25,$26,$27,$28,$29,$30}' OFS=',' log.lammps | awk '/^Step,Temp,Press/{flag=1;next}/^Loop,time/{flag=0}flag' > log.csv
#cat log.lammps| awk '{print $1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17,$18,$19,$20,$21,$22,$23,$24,$25,$26,$27,$28,$29,$30,$31,$32,$33,$34,$35,$36}' | awk '/^Step Elaplong Temp/{flag=1;next}/^Loop time/{flag=0}flag' | awk '{for(i=1;i<=NF-1;i++) printf $i" "; print ""}' OFS=',' > log2.csv
echo all done. 
# End of file 





  
