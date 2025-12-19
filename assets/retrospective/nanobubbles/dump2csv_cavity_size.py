# imports 
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.ndimage.filters import uniform_filter1d
# 
limit = 2.75 #Angstrom - single water molecule diameter 
binsizes = np.ceil(np.array([1, 2, 3, 4, 5, 7.5, 10]) * limit) # times limit - nominal bubble/cavity size 
timestep = sys.argv[1]
#timestep = int(os.path.splitext(os.path.basename(filename))[0])
mesh3d = np.loadtxt(f'{timestep}'+'_3Dmesh.txt', delimiter=",")
#  np.array([binsize, xlo, xhi, ylo, yhi, zlo, zhi, vol, natom, mass, density])
#layerx = np.loadtxt(f'{timestep}'+'_layerx.txt', delimiter=",")
# np.array([binsize, layerx, xlo, xhi, xvol, xnatom, xmass, xdensity])
#layery = np.loadtxt(f'{timestep}'+'_layery.txt', delimiter=",")
#layerz = np.loadtxt(f'{timestep}'+'_layerz.txt', delimiter=",")
# 
bubble_min = 0.0 
bubble_max = 0.0001 # vapor density 
# 
mesh3d_indx = np.where((mesh3d[:,-1] <= bubble_max) & (mesh3d[:,-1] >= bubble_min))
#layerx_indx = np.where((layerx[:,-1] <= bubble_max) & (layerx[:,-1] >= bubble_min))
#layery_indx = np.where((layery[:,-1] <= bubble_max) & (layery[:,-1] >= bubble_min))
#layerz_indx = np.where((layerz[:,-1] <= bubble_max) & (layerz[:,-1] >= bubble_min))
# 
count = 0
for bin in binsizes:
    bin_indx = np.where(mesh3d[mesh3d_indx,0] == bin)
    if count == 0: 
        dummy = np.array([bin, np.max(bin_indx[0].shape)])
        dummy = dummy[np.newaxis, :]
    else: 
        dummy2 = np.array([bin, np.max(bin_indx[0].shape)])
        dummy2 = dummy2[np.newaxis, :]
        dummy = np.concatenate((dummy, dummy2), axis=0)
    count += 1
    #print('binsize:', bin ,', # bubbles: ', np.max(bin_indx[0].shape))   
np.savetxt(f'{timestep}'+'_cavity_size.txt', dummy, delimiter=",")
#print('mesh index: ', mesh3d_indx)
#print('mesh value: ', mesh3d[mesh3d_indx, :])
#print('layerx index: ', layerx_indx)
#print('layerx value: ', layerx[layerx_indx, :])
#print('layery index: ', layery_indx)
#print('layery value: ', layery[layery_indx, :])
#print('layerz index: ', layerz_indx)
#print('layerz value: ', layerz[layerz_indx, :])
#print('# bubbles: ', np.max(mesh3d_indx[0].shape))
#print('dummy: ', dummy)
#np.savetxt(f'{timestep}'+'_3Dmesh.txt', binned, delimiter=",")
#np.savetxt(f'{timestep}'+'_layerx.txt', xlayer, delimiter=",")
#np.savetxt(f'{timestep}'+'_layery.txt', ylayer, delimiter=",")
#np.savetxt(f'{timestep}'+'_layerz.txt', zlayer, delimiter=",")
# End of file             