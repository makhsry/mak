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
density = pd.read_csv (f'{timestep}'+'_density.csv', header=None)
density = density.to_numpy()
# x-y
plt.figure(figsize=(12,7.5))
plt.scatter(density[:,1], density[:,2], c=density[:,5], marker='s', s=15, cmap='rainbow', alpha=0.01, label='density map')
plt.grid(True)
barxy1=plt.colorbar()
#plt.clim(0, C)
barxy1.set_label('density')
plt.xlabel('x direction (A)')
plt.ylabel('y direction (A)')
plt.title('density map, at time = '+f'{timestep}'+' (fs)')
plt.savefig(f'{timestep}'+'_density_xy.png', dpi=600)
plt.close()
# x-z
plt.figure(figsize=(12,7.5))
plt.scatter(density[:,1], density[:,3], c=density[:,5], marker='s', s=15, cmap='rainbow', alpha=0.01, label='density map')
plt.grid(True)
barxz1=plt.colorbar()
#plt.clim(0, C)
barxz1.set_label('density')
plt.xlabel('x direction (A)')
plt.ylabel('z direction (A)')
plt.title('density map, at time = '+f'{timestep}'+' (fs)')
plt.savefig(f'{timestep}'+'_density_xz.png', dpi=600)
plt.close()
# y-z
plt.figure(figsize=(12,7.5))
plt.scatter(density[:,2], density[:,3], c=density[:,5], marker='s', s=15, cmap='rainbow', alpha=0.01, label='density map')
plt.grid(True)
baryz1=plt.colorbar()
#plt.clim(0, C)
baryz1.set_label('density')
plt.xlabel('y direction (A)')
plt.ylabel('z direction (A)')
plt.title('density map, at time = '+f'{timestep}'+' (fs)')
plt.savefig(f'{timestep}'+'_density_yz.png', dpi=600)
plt.close()
###################################################################
cavity = pd.read_csv (f'{timestep}'+'_cavity.csv', header=None)
cavity = cavity.to_numpy()
# x-y
plt.figure(figsize=(12,7.5))
plt.scatter(cavity[:,1], cavity[:,2], c=cavity[:,5], marker='s', s=15, cmap='rainbow', alpha=0.01, label='cavity map')
plt.grid(True)
barxy2=plt.colorbar()
#plt.clim(0, C)
barxy2.set_label('cavity')
plt.xlabel('x direction (A)')
plt.ylabel('y direction (A)')
plt.title('cavity map, at time = '+f'{timestep}'+' (fs)')
plt.savefig(f'{timestep}'+'_cavity_xy.png', dpi=600)
plt.close()
# x-z
plt.figure(figsize=(12,7.5))
plt.scatter(cavity[:,1], cavity[:,3], c=cavity[:,5], marker='s', s=15, cmap='rainbow', alpha=0.01, label='cavity map')
plt.grid(True)
barxz2=plt.colorbar()
#plt.clim(0, C)
barxz2.set_label('cavity')
plt.xlabel('x direction (A)')
plt.ylabel('z direction (A)')
plt.title('cavity map, at time = '+f'{timestep}'+' (fs)')
plt.savefig(f'{timestep}'+'_cavity_xz.png', dpi=600)
plt.close()
# y-z
plt.figure(figsize=(12,7.5))
plt.scatter(cavity[:,2], cavity[:,3], c=cavity[:,5], marker='s', s=15, cmap='rainbow', alpha=0.01, label='density map')
plt.grid(True)
baryz2=plt.colorbar()
#plt.clim(0, C)
baryz2.set_label('density')
plt.xlabel('y direction (A)')
plt.ylabel('z direction (A)')
plt.title('cavity map, at time = '+f'{timestep}'+' (fs)')
plt.savefig(f'{timestep}'+'_cavity_yz.png', dpi=600)
plt.close()
###################################################################
interface = pd.read_csv (f'{timestep}'+'_interface.csv', header=None)
interface = interface.to_numpy()
# x-y
plt.figure(figsize=(12,7.5))
plt.scatter(interface[:,1], interface[:,2], c=interface[:,5], marker='s', s=15, cmap='rainbow', alpha=0.01, label='interface map')
plt.grid(True)
barxy3=plt.colorbar()
#plt.clim(0, C)
barxy3.set_label('interface')
plt.xlabel('x direction (A)')
plt.ylabel('y direction (A)')
plt.title('interface map, at time = '+f'{timestep}'+' (fs)')
plt.savefig(f'{timestep}'+'_interface_xy.png', dpi=600)
plt.close()
# x-z
plt.figure(figsize=(12,7.5))
plt.scatter(interface[:,1], interface[:,3], c=interface[:,5], marker='s', s=15, cmap='rainbow', alpha=0.01, label='interface map')
plt.grid(True)
barxz3=plt.colorbar()
#plt.clim(0, C)
barxz3.set_label('interface')
plt.xlabel('x direction (A)')
plt.ylabel('z direction (A)')
plt.title('interface map, at time = '+f'{timestep}'+' (fs)')
plt.savefig(f'{timestep}'+'_interface_xz.png', dpi=600)
plt.close()
# y-z
plt.figure(figsize=(12,7.5))
plt.scatter(interface[:,2], interface[:,3], c=interface[:,5], marker='s', s=15, cmap='rainbow', alpha=0.01, label='interface map')
plt.grid(True)
baryz3=plt.colorbar()
#plt.clim(0, C)
baryz3.set_label('interface')
plt.xlabel('y direction (A)')
plt.ylabel('z direction (A)')
plt.title('interface map, at time = '+f'{timestep}'+' (fs)')
plt.savefig(f'{timestep}'+'_interface_yz.png', dpi=600)
plt.close()
###################################################################
###################################################################
###################################################################
###################################################################
###################################################################
###################################################################
###################################################################
###################################################################
###################################################################
###################################################################
# x-y
fig = plt.figure(figsize=(12,7.5))
ax = fig.add_subplot(projection='3d')
AXS = ax.scatter(density[:,1], density[:,2], c=density[:,5], marker='s', s=15, cmap='rainbow', alpha=0.01, label='density map')
plt.grid(True)
barxy1=plt.colorbar(AXS)
#plt.clim(0, C)
barxy1.set_label('density')
ax.set_xlabel('x direction (A)')
ax.set_ylabel('y direction (A)')
ax.set_title('density map, at time = '+f'{timestep}'+' (fs)')
plt.savefig(f'{timestep}'+'_density_xy.png', dpi=600)
plt.close()
# x-z
plt.figure(figsize=(12,7.5))
plt.scatter(density[:,1], density[:,3], c=density[:,5], marker='s', s=15, cmap='rainbow', alpha=0.01, label='density map')
plt.grid(True)
barxz1=plt.colorbar()
#plt.clim(0, C)
barxz1.set_label('density')
plt.xlabel('x direction (A)')
plt.ylabel('z direction (A)')
plt.title('density map, at time = '+f'{timestep}'+' (fs)')
plt.savefig(f'{timestep}'+'_density_xz.png', dpi=600)
plt.close()
# y-z
plt.figure(figsize=(12,7.5))
plt.scatter(density[:,2], density[:,3], c=density[:,5], marker='s', s=15, cmap='rainbow', alpha=0.01, label='density map')
plt.grid(True)
baryz1=plt.colorbar()
#plt.clim(0, C)
baryz1.set_label('density')
plt.xlabel('y direction (A)')
plt.ylabel('z direction (A)')
plt.title('density map, at time = '+f'{timestep}'+' (fs)')
plt.savefig(f'{timestep}'+'_density_yz.png', dpi=600)
plt.close()
###################################################################
cavity = pd.read_csv (f'{timestep}'+'_cavity.csv', header=None)
cavity = cavity.to_numpy()
# x-y
plt.figure(figsize=(12,7.5))
plt.scatter(cavity[:,1], cavity[:,2], c=cavity[:,5], marker='s', s=15, cmap='rainbow', alpha=0.01, label='cavity map')
plt.grid(True)
barxy2=plt.colorbar()
#plt.clim(0, C)
barxy2.set_label('cavity')
plt.xlabel('x direction (A)')
plt.ylabel('y direction (A)')
plt.title('cavity map, at time = '+f'{timestep}'+' (fs)')
plt.savefig(f'{timestep}'+'_cavity_xy.png', dpi=600)
plt.close()
# x-z
plt.figure(figsize=(12,7.5))
plt.scatter(cavity[:,1], cavity[:,3], c=cavity[:,5], marker='s', s=15, cmap='rainbow', alpha=0.01, label='cavity map')
plt.grid(True)
barxz2=plt.colorbar()
#plt.clim(0, C)
barxz2.set_label('cavity')
plt.xlabel('x direction (A)')
plt.ylabel('z direction (A)')
plt.title('cavity map, at time = '+f'{timestep}'+' (fs)')
plt.savefig(f'{timestep}'+'_cavity_xz.png', dpi=600)
plt.close()
# y-z
plt.figure(figsize=(12,7.5))
plt.scatter(cavity[:,2], cavity[:,3], c=cavity[:,5], marker='s', s=15, cmap='rainbow', alpha=0.01, label='density map')
plt.grid(True)
baryz2=plt.colorbar()
#plt.clim(0, C)
baryz2.set_label('density')
plt.xlabel('y direction (A)')
plt.ylabel('z direction (A)')
plt.title('cavity map, at time = '+f'{timestep}'+' (fs)')
plt.savefig(f'{timestep}'+'_cavity_yz.png', dpi=600)
plt.close()
###################################################################
interface = pd.read_csv (f'{timestep}'+'_interface.csv', header=None)
interface = interface.to_numpy()
# x-y
plt.figure(figsize=(12,7.5))
plt.scatter(interface[:,1], interface[:,2], c=interface[:,5], marker='s', s=15, cmap='rainbow', alpha=0.01, label='interface map')
plt.grid(True)
barxy3=plt.colorbar()
#plt.clim(0, C)
barxy3.set_label('interface')
plt.xlabel('x direction (A)')
plt.ylabel('y direction (A)')
plt.title('interface map, at time = '+f'{timestep}'+' (fs)')
plt.savefig(f'{timestep}'+'_interface_xy.png', dpi=600)
plt.close()
# x-z
plt.figure(figsize=(12,7.5))
plt.scatter(interface[:,1], interface[:,3], c=interface[:,5], marker='s', s=15, cmap='rainbow', alpha=0.01, label='interface map')
plt.grid(True)
barxz3=plt.colorbar()
#plt.clim(0, C)
barxz3.set_label('interface')
plt.xlabel('x direction (A)')
plt.ylabel('z direction (A)')
plt.title('interface map, at time = '+f'{timestep}'+' (fs)')
plt.savefig(f'{timestep}'+'_interface_xz.png', dpi=600)
plt.close()
# y-z
plt.figure(figsize=(12,7.5))
plt.scatter(interface[:,2], interface[:,3], c=interface[:,5], marker='s', s=15, cmap='rainbow', alpha=0.01, label='interface map')
plt.grid(True)
baryz3=plt.colorbar()
#plt.clim(0, C)
baryz3.set_label('interface')
plt.xlabel('y direction (A)')
plt.ylabel('z direction (A)')
plt.title('interface map, at time = '+f'{timestep}'+' (fs)')
plt.savefig(f'{timestep}'+'_interface_yz.png', dpi=600)
plt.close()











# End of file             