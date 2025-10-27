# implementing: J. Phys. Chem. B 2010, 114, 1954–1958. 
# imports 
import sys
import os
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# names and tags 
'''
tags = [
    'id', 
    'mol', 
    'type', 
    'element', 
    'mass', 
    'v_radius', 
    'x', 
    'y', 
    'z', 
    'vx', 
    'vy', 
    'vz', 
    'fx', 
    'fy', 
    'fz', 
    'q']
names = [
    'atom id', 
    'molecule id', 
    'atom type - O(1)H(2)', 
    'element', 
    'mass (grams/mole)', 
    'radius (Angstroms)', 
    'position x (Angstroms)', 
    'position y (Angstroms)', 
    'position z (Angstroms)', 
    'velocity x (Angstroms/fs)', 
    'velocity y (Angstroms/fs)', 
    'velocity z (Angstroms/fs)', 
    'force x (Kcal/mole-Angstrom)', 
    'force y (Kcal/mole-Angstrom)', 
    'force z (Kcal/mole-Angstrom)', 
    'atomic charge']
'''
# 
filename = sys.argv[1]
timestep = int(os.path.splitext(os.path.basename(filename))[0])
df = pd.read_csv (filename, header=None)
#
mol = df.sort_values(df.columns[2]) # 2 ---> atom type 
#
mol = mol.to_numpy()
xmax, xmin = mol[:,6].max(), mol[:,6].min()
ymax, ymin = mol[:,7].max(), mol[:,7].min()
zmax, zmin = mol[:,8].max(), mol[:,8].min()
mass = mol[:,4].sum()
density = mass / ((xmax - xmin) * (ymax - ymin) * (zmax - zmin))
dummy = np.array([xmin, xmax, ymin, ymax, zmin, zmax, mass, density])
dummy = dummy[np.newaxis, :]
np.savetxt(f'{timestep}'+'_specs.txt', dummy, delimiter=",")
# 
kisi = 2.4 # Angstrom - single water molecule diameter 
c = 0.016 # Angstrom^-3 - one-half the bulk density 
ls = 1 # Angstrom - lattice spacing, R = 3*kisi # Angstrom - max distance of CG 
d = 3 # dimensionality 
R = kisi
#
xgrid = np.arange(xmin, xmax, R)
if not (xmax in xgrid):
    xgrid = np.append(xgrid, xmax)
else: 
    xgrid = np.array([xmin, xmax])
xgrid = xgrid[np.newaxis, :]
ygrid = np.arange(ymin, ymax, R)
if not (ymax in ygrid):
    ygrid = np.append(ygrid, ymax)
else: 
    ygrid = np.array([ymin, ymax])
ygrid = ygrid[np.newaxis, :]
zgrid = np.arange(zmin, zmax, R)
if not (zmax in zgrid):
    zgrid = np.append(zgrid, zmax)
else: 
    zgrid = np.array([zmin, zmax])
zgrid = zgrid[np.newaxis, :]
#
O = np.where(mol[:,2] == 1)
O = O[0]
O = O[np.newaxis, :]
#
Rho = open(f'{timestep}'+'_density.csv', 'a')
IF = open(f'{timestep}'+'_interface.csv', 'a')
cave = open(f'{timestep}'+'_cavity.csv', 'a')
# 3D mesh 
cell = 0
for xlo, xhi in zip(xgrid[0,:-1], xgrid[0,1:]):
    for ylo, yhi in zip(ygrid[0,:-1], ygrid[0,1:]):
        for zlo, zhi in zip(zgrid[0,:-1], zgrid[0,1:]):
            cell += 1
            print('progress (%):', 100*cell/(np.max(xgrid.shape) * np.max(ygrid.shape) * np.max(zgrid.shape)))
            vol = (xhi - xlo) * (yhi - ylo) * (zhi - zlo)
            xcom = (xlo + xhi)/2
            ycom = (ylo + yhi)/2
            zcom = (zlo + zhi)/2
            dx = xcom - mol[O,6]
            dy = ycom - mol[O,7] 
            dz = zcom - mol[O,8] 
            r = (dx*dx + dy*dy + dz*dz)**0.5
            expin = -(r*r)/(2*kisi*kisi)
            sai = (2*math.pi*(kisi*kisi))**(-d/2)*np.exp(expin.astype(float))  
            rho = sai.sum()
            dummy = np.array([cell, xcom, ycom, zcom, vol, rho])
            dummy = dummy[np.newaxis, :]
            np.savetxt(Rho, dummy, delimiter=",")
            if (rho < (1.1*c)) and (rho > (0.9*c)):
                np.savetxt(IF, dummy, delimiter=",")
            if (rho <= (0.9*c)):
                np.savetxt(cave, dummy, delimiter=",")
Rho.close()
IF.close()
cave.close()
#
interface = pd.read_csv (f'{timestep}'+'_interface.csv', header=None)
interface = interface.to_numpy()
density = pd.read_csv (f'{timestep}'+'_density.csv', header=None)
density = density.to_numpy()
cavity = pd.read_csv (f'{timestep}'+'_cavity.csv', header=None)
cavity = cavity.to_numpy()
plt.figure(figsize=(12,7.5))
plt.scatter(density[:,1], density[:,3], c=(density[:,5]), marker='s', s=25, cmap='RdBu', alpha=0.5, label='density map')
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
plt.scatter(cavity[:,1], cavity[:,3], c=(cavity[:,5]), marker='o', s=25, cmap='RdBu', alpha=0.5, label='cavity map')
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