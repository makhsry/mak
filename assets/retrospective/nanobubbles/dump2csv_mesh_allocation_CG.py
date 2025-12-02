# implementing: J. Phys. Chem. B 2010, 114, 1954–1958. 
# imports 
import sys
import os
import math
import numpy as np
import pandas as pd
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
R = 1
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
#liq = open(f'{timestep}'+'_liquid.csv', 'a')
# 3D mesh 
cell = 0
for xlo, xhi in zip(xgrid[0,:-2], xgrid[0,1:]):
    for ylo, yhi in zip(ygrid[0,:-2], ygrid[0,1:]):
        for zlo, zhi in zip(zgrid[0,:-2], zgrid[0,1:]):
            cell += 1
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
            if (rho < (1.11*c)) and (rho > (0.99*c)):
                np.savetxt(IF, dummy, delimiter=",")
            if (rho <= (0.99*c)):
                np.savetxt(cave, dummy, delimiter=",")
            #if (rho > (0.99*c)):
            #    np.savetxt(liq, dummy, delimiter=",")    
Rho.close()
IF.close()
cave.close()
#liq.close()
# End of file             
