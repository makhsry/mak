# imports 
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.ndimage.filters import uniform_filter1d
# names and tags 
tags = [
    'Temp', 
    'Press', 
    'Density', 
    'Volume', 
    'PotEng', 
    'KinEng', 
    'TotEng', 
    'Enthalpy', 
    'E_vdwl', 
    'E_tail', 
    'E_coul', 
    'E_pair', 
    'E_mol', 
    'E_long', 
    'boxXYZ', 
    'boxAng', 
    'boxABC', 
    'Pxx', 
    'Pyy', 
    'Pzz', 
    'Pxy', 
    'Pxz', 
    'Pyz', 
    'Fmax', 
    'Fnorm']
names = [
    'temperature (K)', 
    'pressure (atm)', 
    'density (gram/cm^3)', 
    'volume (Angstroms^3)', 
    'potential energy (Kcal/mol)', 
    'kinetic energy (Kcal/mol)', 
    'total energy (Kcal/mol)', 
    'enthalpy (Kcal/mol)', 
    'van der Waals pairwise energy (includes etail) (Kcal/mol)', 
    'van der Waals energy long-range tail correction energy (Kcal/mol)', 
    'coulombic pairwise energy (Kcal/mol)', 
    'pairwise energy (evdwl + ecoul + elong) (Kcal/mol)', 
    'molecular energy (ebond + eangle + edihed + eimp) (Kcal/mol)', 
    'long-range kspace energy (Kcal/mol)', 
    'box dimensions (Angstroms)', 
    'periodic cell angles', 
    'periodic cell lattice constants', 
    'pressure tensor - pxx', 
    'pressure tensor - pyy',
    'pressure tensor - pzz', 
    'pressure tensor - pxy',
    'pressure tensor - pxz',
    'pressure tensor - pyz', 
    'max component of force on any atom in any dimension', 
    'length of force vector for all atoms']
# loading 
df = pd.read_csv ('20220623_channel_expansion_by_fixdeform_no_remap_log.csv', header=None)
data = df.to_numpy()
# 
col = 1
for name, tag in zip(names, tags): 
    trim = 100
    window = 10
    col += 1
    plt.figure(figsize=(12,7.5))
    if tag == 'boxXYZ':
        plt.plot(data[:,0], data[:,col], color='black', linestyle='solid', label="xlo")
        col += 1
        plt.plot(data[:,0], data[:,col], color='black', linestyle='dotted', label="xhi")
        col += 1
        plt.plot(data[:,0], data[:,col], color='red', linestyle='solid', label="ylo")
        col += 1
        plt.plot(data[:,0], data[:,col], color='red', linestyle='dashed', label="yhi")
        col += 1
        plt.plot(data[:,0], data[:,col], color='blue', linestyle='solid', label="zlo")
        col += 1
        plt.plot(data[:,0], data[:,col], color='blue', linestyle='dashed', label="zhi")
        plt.xlabel('timestep (fs)')
        plt.ylabel(name)
        plt.xlim([0, data[:,0].max()])
        plt.legend(loc="best") 
        continue
    if tag == 'boxAng':
        plt.plot(data[:,0], data[:,col], color='black', linestyle='dotted', label="alpha")
        col += 1
        plt.plot(data[:,0], data[:,col], color='black', linestyle='dotted', label="betta")
        col += 1
        plt.plot(data[:,0], data[:,col], color='red', linestyle='dotted', label="gamma")
        plt.xlabel('timestep (fs)')
        plt.ylabel(name)
        plt.xlim([0, data[:,0].max()])
        plt.legend(loc="best")
        plt.savefig(tag+'.png')
        continue
    if tag == 'boxABC':
        plt.plot(data[:,0], data[:,col], color='red', linestyle='dotted', label="a")
        col += 1
        plt.plot(data[:,0], data[:,col], color='blue', linestyle='dotted', label="b")
        col += 1
        plt.plot(data[:,0], data[:,col], color='blue', linestyle='dotted', label="c")
        plt.xlabel('timestep (fs)')
        plt.ylabel(name)
        plt.xlim([0, data[:,0].max()])
        plt.legend(loc="best")
        plt.savefig(tag+'.png')
        continue
    # none of above 
    plt.plot(data[:,0], data[:,col], color='blue', linestyle='dotted', label="current")
    i = 0
    arr = data[:,col]
    moving_averages = []
    timesteps = []
    while i < len(arr) - window + 1:
        window_average = round(np.sum(arr[i:i+window]) / window, 2)
        timesteps.append(data[i,0])
        moving_averages.append(window_average)
        i += 1
    plt.plot(timesteps, moving_averages, color='red', linestyle='dotted', label="moving average")
    if tag == 'Temp':
        plt.plot(data[:,0], np.ones(data[:,0].shape)*300, color='green', linestyle='solid', label="target")
    plt.xlabel('timestep (fs)')
    plt.ylabel(name)
    plt.ylim([arr[trim:].min(), arr[trim:].max()])
    plt.xlim([0, data[:,0].max()])
    plt.legend(loc="best")
    plt.savefig(tag+'.png')
    plt.close()