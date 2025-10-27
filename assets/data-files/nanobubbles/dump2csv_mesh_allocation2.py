# imports 
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.ndimage.filters import uniform_filter1d
# names and tags 
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
# 
filename = sys.argv[1]
timestep = int(os.path.splitext(os.path.basename(filename))[0])
df = pd.read_csv (filename, header=None)
#
mol = df.sort_values(df.columns[1]) # 1 ---> molecule id
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
limit = 2.75 #Angstrom - single water molecule diameter 
binsizes = np.ceil(np.array([1, 2, 3, 4, 5, 7.5, 10]) * limit) # times limit - nominal bubble/cavity size 
binned = np.zeros([1,11]) # [0-binsize, 1-xlo, 2-xhi, 3-ylo, 4-yhi, 5-zlo, 6-zhi, 7-vol, 8-natom, 9-mass, 10-density]
xlayer = np.zeros([1,8]) # [0-binsize, 1-layerx, 2-xlo, 3-xhi, 4-xvol, 5-xnatom, 6-xmass, 7-xdensity]
ylayer = np.zeros([1,8])
zlayer = np.zeros([1,8])
for binsize in binsizes:
    # grid 
    if (binsize < (xmax - xmin)): 
        xgrid = np.arange(xmin, xmax, binsize)
        if not (xmax in xgrid):
            xgrid = np.append(xgrid, xmax)
    else: 
        xgrid = np.array([xmin, xmax])
    xgrid = xgrid[np.newaxis, :]
    if (binsize < (ymax - ymin)):
        ygrid = np.arange(ymin, ymax, binsize)
        if not (ymax in ygrid):
            ygrid = np.append(ygrid, ymax)
    else: 
        ygrid = np.array([ymin, ymax])
    ygrid = ygrid[np.newaxis, :]
    if (binsize < (zmax - zmin)):
        zgrid = np.arange(zmin, zmax, binsize)
        if not (zmax in zgrid):
            zgrid = np.append(zgrid, zmax)
    else: 
        zgrid = np.array([zmin, zmax])
    zgrid = zgrid[np.newaxis, :]
    # layer X
    layerx = 0
    for xlo, xhi in zip(xgrid[0,:-1], xgrid[0,1:]):
        xin = np.where((mol[:,6] >= xlo) & (mol[:,6] <= xhi))
        xin = xin[0]
        xin = xin[np.newaxis, :]
        if (xin.size != 0): 
            layerx += 1
            xvol = (xhi - xlo) * (ymax - ymin) * (zmax - zmin)
            xnatom = 0
            xmass = 0
            for x in xin[0,:]:
                xnatom += 1
                xmass += mol[x,4]
                xdensity = xmass/xvol
            xdummy = np.array([binsize, layerx, xlo, xhi, xvol, xnatom, xmass, xdensity])
            xdummy = xdummy[np.newaxis, :]
            if layerx == 1:
                xlayer[0,:] = xdummy
            else:
                xlayer = np.concatenate((xlayer, xdummy), axis=0)
    # layer Y
    layery = 0
    for ylo, yhi in zip(ygrid[0,:-1], ygrid[0,1:]):
        yin = np.where((mol[:,7] >= ylo) & (mol[:,7] <= yhi))
        yin = yin[0]
        yin = yin[np.newaxis, :]
        if (yin.size != 0): 
            layery += 1
            yvol = (xmax - xmin) * (yhi - ylo) * (zmax - zmin)
            ynatom = 0
            ymass = 0
            for y in yin[0,:]:
                ynatom += 1
                ymass += mol[y,4]
                ydensity = ymass/yvol
            ydummy = np.array([binsize, layery, ylo, yhi, yvol, ynatom, ymass, ydensity])
            ydummy = ydummy[np.newaxis, :]
            if layery == 1:
                ylayer[0,:] = ydummy 
            else:
                ylayer = np.concatenate((ylayer, ydummy), axis=0)
    # layer Z
    layerz = 0
    for zlo, zhi in zip(zgrid[0,:-1], zgrid[0,1:]):
        zin = np.where((mol[:,8] >= zlo) & (mol[:,8] <= zhi))
        zin = zin[0]
        zin = zin[np.newaxis, :]
        if (zin.size != 0): 
            layerz += 1
            zvol = (xmax - xmin) * (ymax- ymin) * (zhi - zlo)
            znatom = 0
            zmass = 0
            for z in zin[0,:]:
                znatom += 1
                zmass += mol[y,4]
                zdensity = zmass/zvol
            zdummy = np.array([binsize, layerz, zlo, zhi, zvol, znatom, zmass, zdensity])
            zdummy = zdummy[np.newaxis, :]
            if layerz == 1:
                zlayer[0,:] = zdummy 
            else:
                zlayer = np.concatenate((zlayer, zdummy), axis=0)
    # 3D mesh 
    cell = 0
    for xlo, xhi in zip(xgrid[0,:-1], xgrid[0,1:]):
        xin = np.where((mol[:,6] >= xlo) & (mol[:,6] <= xhi))
        for ylo, yhi in zip(ygrid[0,:-1], ygrid[0,1:]):
            yin = np.where((mol[:,7] >= ylo) & (mol[:,7] <= yhi))
            for zlo, zhi in zip(zgrid[0,:-1], zgrid[0,1:]):
                zin = np.where((mol[:,8] >= zlo) & (mol[:,8] <= zhi))
                cell += 1
                mass = 0
                natom = 0
                density = 0
                vol = (xhi - xlo) * (yhi - ylo) * (zhi - zlo)
                xin = xin[0]
                yin = yin[0]
                zin = zin[0]
                xin = xin[np.newaxis, :]
                yin = yin[np.newaxis, :]
                zin = zin[np.newaxis, :]
                if ((xin.size != 0) and (yin.size != 0) and (zin.size != 0)):
                    common = xin[0,np.in1d(xin, yin)]
                    common = common[np.in1d(common, zin)]
                    for particle in common: 
                        natom += 1
                        mass += mol[particle,4]
                        density = mass/vol
                #else it remains empty
                dummy = np.array([binsize, xlo, xhi, ylo, yhi, zlo, zhi, vol, natom, mass, density])
                dummy = dummy[np.newaxis, :]
                if cell == 1:
                    binned[0,:] = dummy
                else:
                    binned = np.concatenate((binned, dummy), axis=0)
np.savetxt(f'{timestep}'+'_3Dmesh.txt', binned, delimiter=",")
np.savetxt(f'{timestep}'+'_layerx.txt', xlayer, delimiter=",")
np.savetxt(f'{timestep}'+'_layery.txt', ylayer, delimiter=",")
np.savetxt(f'{timestep}'+'_layerz.txt', zlayer, delimiter=",")
# End of file             