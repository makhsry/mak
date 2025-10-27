# implementing: J. Phys. Chem. B 2010, 114, 1954–1958. 
# imports 
import sys
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
# 
filename = sys.argv[1]
timestep = int(os.path.splitext(os.path.basename(filename))[0])
#
C = 2*0.016
#
###################################################################
# density x-y-z
density = pd.read_csv (f'{timestep}'+'_density.csv', header=None)
density = density.to_numpy()
fig = plt.figure(figsize=(25,15))
ax = fig.add_subplot(projection='3d')
AXS = ax.scatter(density[:,1], density[:,2], density[:,3], c=density[:,5], marker='s', s=50, cmap='rainbow', alpha=0.1, label='density map')
plt.grid(True)
barxy1=plt.colorbar(AXS, ax=ax)
#plt.clim(0, C)
barxy1.set_label('density')
ax.set_xlabel('length - x direction (A)')
ax.set_ylabel('width - y direction (A)')
ax.set_zlabel('height - z direction (A)')
ax.set_title('density map, at time = '+f'{timestep}'+' (fs)')
plt.savefig(f'{timestep}'+'_density_3d.png', dpi=600)
plt.close()
# cavity x-y-z
density = pd.read_csv (f'{timestep}'+'_cavity.csv', header=None)
density = density.to_numpy()
fig = plt.figure(figsize=(25,15))
ax = fig.add_subplot(projection='3d')
AXS = ax.scatter(density[:,1], density[:,2], density[:,3], c=density[:,5], marker='o', cmap='rainbow', alpha=0.1, label='cavity map')
plt.grid(True)
barxy1=plt.colorbar(AXS, ax=ax)
#plt.clim(0, C)
barxy1.set_label('cavity')
ax.set_xlabel('length - x direction (A)')
ax.set_ylabel('width - y direction (A)')
ax.set_zlabel('height - z direction (A)')
ax.set_title('cavity map, at time = '+f'{timestep}'+' (fs)')
plt.savefig(f'{timestep}'+'_cavity_3d.png', dpi=600)
plt.close()
# interface x-y-z
density = pd.read_csv (f'{timestep}'+'_interface.csv', header=None)
density = density.to_numpy()
fig = plt.figure(figsize=(25,15))
ax = fig.add_subplot(projection='3d')
AXS = ax.scatter(density[:,1], density[:,2], density[:,3], c=density[:,5], marker='.', cmap='rainbow', alpha=0.1, label='interface map')
plt.grid(True)
barxy1=plt.colorbar(AXS, ax=ax)
#plt.clim(0, C)
barxy1.set_label('interface')
ax.set_xlabel('length - x direction (A)')
ax.set_ylabel('width - y direction (A)')
ax.set_zlabel('height - z direction (A)')
ax.set_title('cavity map, at time = '+f'{timestep}'+' (fs)')
plt.savefig(f'{timestep}'+'_interface_3d.png', dpi=600)
plt.close()
# End of file             