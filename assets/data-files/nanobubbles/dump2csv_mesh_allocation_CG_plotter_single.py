# implementing: J. Phys. Chem. B 2010, 114, 1954–1958. 
# imports 
from cProfile import label
import sys
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
# 
filename = sys.argv[1]
timestep = int(os.path.splitext(os.path.basename(filename))[0])
#
interface = pd.read_csv (f'{timestep}'+'_interface.csv', header=None)
interface = interface.to_numpy()
density = pd.read_csv (f'{timestep}'+'_density.csv', header=None)
density = density.to_numpy()
cavity = pd.read_csv (f'{timestep}'+'_cavity.csv', header=None)
cavity = cavity.to_numpy()
plt.figure(figsize=(12,7.5))
plt.scatter(density[:,1], density[:,3], c=(density[:,5]), marker='s', s=25, cmap='RdBu', alpha=0.5, label='density map')
#plt.scatter(cavity[:,1], cavity[:,3], c=(cavity[:,5]/(density[:,5].max())), marker='o', s=25, cmap='RdBu', alpha=0.5, label='cavity map')
#plt.scatter(interface[:,1], interface[:,3], c=(interface[:,5]/(density[:,5].max())), marker='+', s=25, cmap='RdBu', alpha=0.5, label='interface locus')
plt.grid(True)
bar=plt.colorbar()
#plt.colorbar(extend='both')
#plt.clim(0, 1)
bar.set_label('density')
plt.xlabel('x direction (A)')
plt.ylabel('z direction (A)')
plt.title('density map, at time = '+f'{timestep}'+' (fs)')
#plt.legend()
plt.savefig(f'{timestep}'+'_density.png', dpi=600)
plt.close()
#plt.scatter(density[:,1], density[:,3], c=(density[:,5]/(density[:,5].max())), marker='s', s=25, cmap='RdBu', alpha=0.5, label='density map')
plt.scatter(cavity[:,1], cavity[:,3], c=(cavity[:,5]), marker='o', s=25, cmap='RdBu', alpha=0.5, label='cavity map')
#plt.scatter(interface[:,1], interface[:,3], c=(interface[:,5]/(density[:,5].max())), marker='+', s=25, cmap='RdBu', alpha=0.5, label='interface locus')
plt.grid(True)
bar=plt.colorbar()
#plt.colorbar(extend='both')
#plt.clim(0, 1)
bar.set_label('density')
plt.xlabel('x direction (A)')
plt.ylabel('z direction (A)')
plt.title('cavities, at time = '+f'{timestep}'+' (fs)')
#plt.legend()
plt.savefig(f'{timestep}'+'_cavities.png', dpi=600)
plt.close()
#plt.scatter(density[:,1], density[:,3], c=(density[:,5]/(density[:,5].max())), marker='s', s=25, cmap='RdBu', alpha=0.5, label='density map')
#plt.scatter(cavity[:,1], cavity[:,3], c=(cavity[:,5]/(density[:,5].max())), marker='o', s=25, cmap='RdBu', alpha=0.5, label='cavity map')
plt.scatter(interface[:,1], interface[:,3], c=(interface[:,5]), marker='+', s=25, cmap='RdBu', alpha=0.5, label='interface locus')
plt.grid(True)
bar=plt.colorbar()
#plt.colorbar(extend='both')
#plt.clim(0, 1)
bar.set_label('density')
plt.xlabel('x direction (A)')
plt.ylabel('z direction (A)')
plt.title('interface, at time = '+f'{timestep}'+' (fs)')
#plt.legend()
plt.savefig(f'{timestep}'+'_interface.png', dpi=600)
plt.close()
# End of file             