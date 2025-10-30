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
plt.scatter(interface[:,1], interface[:,3], c=interface[:,5], marker='s', s=25, cmap='rainbow', alpha=0.5, label='interface locus')
plt.scatter(density[:,1], density[:,3], c=density[:,5], marker='+', s=25, cmap='rainbow', alpha=0.5, label='density map')
plt.scatter(cavity[:,1], cavity[:,3], c=cavity[:,5], marker='o', s=25, cmap='rainbow', alpha=0.5, label='cavity map')
plt.grid(True)
plt.colorbar()
plt.xlabel('x direction (A)')
plt.ylabel('z direction (A)')
plt.legend()
plt.savefig(f'{timestep}'+'_cavities.png', dpi=600)
plt.close()
# End of file             