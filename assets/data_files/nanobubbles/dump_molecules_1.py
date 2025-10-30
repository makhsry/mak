# main.py 
import sys
import numpy as np
import math
# 
file = (sys.argv[1])
fp = open(file) # open a file but won't load it to memory, reading line by line
print('processing file: ', file)
line_1 = fp.readline() # label for timestep
line_2 = fp.readline() # time step 
timestep = int(line_2.split()[0]) # conversion to int
line_3 = fp.readline() # label for number of atoms
line_4 = fp.readline() # number of atoms
natoms = int(line_4) # conversion to int
line_5 = fp.readline() # label for box bounds 
line_6 = fp.readline() # box bounds, x 
line_6 = line_6.split()
xlo, xhi = float(line_6[0]), float(line_6[1])
line_7 = fp.readline() # box bounds, y
line_7 = line_7.split()
ylo, yhi = float(line_7[0]), float(line_7[1])
line_8 = fp.readline() # box bounds, z
line_8 = line_8.split()
zlo, zhi = float(line_8[0]), float(line_8[1])
line_9 = fp.readline() # header of tabulated data
line_9 = line_9.split() # id mol type element mass v_radius x y z vx vy vz fx fy fz q
# Populating atoms data 
minz = 0
maxz = 0
ATOMS = {}
for atomi in range(natoms):
  atom = atomi + 1
  ATOMS[atom] = {}
  data = fp.readline().split()
  ATOMS[atom]["id"] = int(data[0])
  ATOMS[atom]["mol"] = int(data[1])
  ATOMS[atom]["type"] = data[2]
  ATOMS[atom]["element"] = data[3]
  ATOMS[atom]["mass"] = float(data[4])
  ATOMS[atom]["radius"] = float(data[5])
  ATOMS[atom]["x"] = float(data[6])
  ATOMS[atom]["y"] = float(data[7])
  ATOMS[atom]["z"] = float(data[8])
  minz = min([minz, ATOMS[atom]["z"]])
  maxz = max([maxz, ATOMS[atom]["z"]])
  ATOMS[atom]["vx"] = float(data[9])
  ATOMS[atom]["vy"] = float(data[10])
  ATOMS[atom]["vz"] = float(data[11])
  ATOMS[atom]["fx"] = float(data[12])
  ATOMS[atom]["fy"] = float(data[13])
  ATOMS[atom]["fz"] = float(data[14])
  ATOMS[atom]["q"] = float(data[15])
fp.close()
# Shuffeling atoms and molecules
MOLECULE = {}
molecules = int(len(ATOMS.keys())/3)
for moleculei in range(molecules):
  print('Populating molecule : ', moleculei, ' , progress (%) : ', 100*moleculei/molecules)
  molecule = moleculei + 1
  MOLECULE[molecule] = {}
  child = 0
  for atom in ATOMS.keys():
    if molecule == ATOMS[atom]["mol"]: 
      child = child + 1
      MOLECULE[molecule][child] = {}
      MOLECULE[molecule][child]['id'] = ATOMS[atom]["id"]
      MOLECULE[molecule][child]["type"] = ATOMS[atom]["type"]
      MOLECULE[molecule][child]["element"] = ATOMS[atom]["element"]
      MOLECULE[molecule][child]["mass"] = ATOMS[atom]["mass"]
      MOLECULE[molecule][child]["radius"] = ATOMS[atom]["radius"]
      MOLECULE[molecule][child]["x"] = ATOMS[atom]["x"]
      MOLECULE[molecule][child]["y"] = ATOMS[atom]["y"]
      MOLECULE[molecule][child]["z"] = ATOMS[atom]["z"]
      MOLECULE[molecule][child]["vx"] = ATOMS[atom]["vx"]
      MOLECULE[molecule][child]["vy"] = ATOMS[atom]["vy"]
      MOLECULE[molecule][child]["vz"] = ATOMS[atom]["vz"]
      MOLECULE[molecule][child]["fx"] = ATOMS[atom]["fx"]
      MOLECULE[molecule][child]["fy"] = ATOMS[atom]["fy"]
      MOLECULE[molecule][child]["fz"] = ATOMS[atom]["fz"]
      MOLECULE[molecule][child]["q"] = ATOMS[atom]["q"]   
# - building bins with different resolutions 
resolutions = np.array([0.1, 1, 5, 10, 15, 25])
BINS = {}
LAYERSx = {}
LAYERSy = {}
LAYERSz = {}
for resolution in resolutions:
    print('Populating with a resolution of: ', resolution, ' *5.1*2.75 --- Navier-Stokes ---')
    BINS[resolution] = {}
    bin = 0
    NS_limit = resolution*np.ceil(5.1 * 2.75) # Navier-Stokes fails bellow: -->5.1 * molecule size<-- - Angstrom
    xgrid = np.arange(xlo, xhi, NS_limit)
    if not (xhi in xgrid):
      xgrid = np.append(xgrid, xhi)
    ygrid = np.arange(ylo, yhi, NS_limit)
    if not (yhi in ygrid):
      ygrid = np.append(ygrid, yhi)
    zgrid = np.arange(zlo, zhi, NS_limit)
    if not (zhi in zgrid):
      zgrid = np.append(zgrid, zhi)
    # defining layers then to pin bins to it 
    for i in range(zgrid.shape[0]-1):
        layer = i + 1
        LAYERSz[layer] = {}
        LAYERSz[layer]['zlo'], LAYERSz[layer]['zhi'] = zgrid[i], zgrid[i+1]
        LAYERSz[layer]['mass'] = 0
        LAYERSz[layer]['VOL'] = abs(zgrid[i] - zgrid[i+1]) * abs(xlo - xhi) * abs(ylo - yhi) 
        LAYERSz[layer]['vol'] = 0
        LAYERSz[layer]['density'] = 0 
        LAYERSz[layer]['binlist'] = [] 
    for i in range(ygrid.shape[0]-1):
        layer = i + 1
        LAYERSy[layer] = {}
        LAYERSy[layer]['ylo'], LAYERSy[layer]['yhi'] = ygrid[i], ygrid[i+1]
        LAYERSy[layer]['mass'] = 0
        LAYERSy[layer]['VOL'] = abs(ygrid[i] - ygrid[i+1]) * abs(xlo - xhi) * abs(zlo - zhi) 
        LAYERSy[layer]['vol'] = 0
        LAYERSy[layer]['density'] = 0 
        LAYERSy[layer]['binlist'] = [] 
    for i in range(xgrid.shape[0]-1):
        layer = i + 1
        LAYERSx[layer] = {}
        LAYERSx[layer]['xlo'], LAYERSx[layer]['xhi'] = xgrid[i], xgrid[i+1]
        LAYERSx[layer]['mass'] = 0
        LAYERSx[layer]['VOL'] = abs(xgrid[i] - xgrid[i+1]) * abs(ylo - yhi) * abs(zlo - zhi) 
        LAYERSx[layer]['vol'] = 0
        LAYERSx[layer]['density'] = 0 
        LAYERSx[layer]['binlist'] = [] 
    # creating bins 
    for i in range(xgrid.shape[0]-1):
        layerx = i + 1
        for j in range(ygrid.shape[0]-1):
            layery = j + 1
            for k in range(zgrid.shape[0]-1):
              layerz = k + 1
              bin += 1
              BINS[resolution][bin] = {}
              BINS[resolution][bin]['xlo'], BINS[resolution][bin]['xhi'] = xgrid[i], xgrid[i+1]
              BINS[resolution][bin]['ylo'], BINS[resolution][bin]['yhi'] = ygrid[j], ygrid[j+1]
              BINS[resolution][bin]['zlo'], BINS[resolution][bin]['zhi'] = zgrid[k], zgrid[k+1]
              BINS[resolution][bin]['VOL'] = abs(BINS[resolution][bin]['xhi'] - BINS[resolution][bin]['xlo']) * abs(BINS[resolution][bin]['yhi'] - BINS[resolution][bin]['ylo']) * abs(BINS[resolution][bin]['zhi'] - BINS[resolution][bin]['zlo'])
              BINS[resolution][bin]['mass'] = 0
              BINS[resolution][bin]['vol'] = 0
              BINS[resolution][bin]['density'] = 0
              if (BINS[resolution][bin]['zlo']>=LAYERSz[layerz]['zlo']) and (BINS[resolution][bin]['zhi'] <=LAYERSz[layerz]['zhi']):
                LAYERSz[layerz]['binlist'].append(bin) 
              if (BINS[resolution][bin]['ylo']>=LAYERSy[layery]['ylo']) and (BINS[resolution][bin]['yhi'] <=LAYERSy[layery]['yhi']):
                LAYERSy[layery]['binlist'].append(bin) 
              if (BINS[resolution][bin]['xlo']>=LAYERSx[layerx]['xlo']) and (BINS[resolution][bin]['xhi'] <=LAYERSx[layerx]['xhi']):
                LAYERSx[layerx]['binlist'].append(bin) 
    # - adding to bins and layers 
    for molecule in MOLECULE.keys():
        for bin in BINS[resolution].keys():
            # in what bin?
            inside = 0
            if ((MOLECULE[molecule][1]["x"] >= BINS[resolution][bin]['xlo']) and (MOLECULE[molecule][1]["x"] <= BINS[resolution][bin]['xhi'])): 
                inside = inside + 1
            if ((MOLECULE[molecule][2]["x"] >= BINS[resolution][bin]['xlo']) and (MOLECULE[molecule][2]["x"] <= BINS[resolution][bin]['xhi'])): 
                inside = inside + 1
            if ((MOLECULE[molecule][3]["x"] >= BINS[resolution][bin]['xlo']) and (MOLECULE[molecule][3]["x"] <= BINS[resolution][bin]['xhi'])): 
                inside = inside + 1
            if ((MOLECULE[molecule][1]["y"] >= BINS[resolution][bin]['ylo']) and (MOLECULE[molecule][1]["y"] <= BINS[resolution][bin]['yhi'])): 
                inside = inside + 1
            if ((MOLECULE[molecule][2]["y"] >= BINS[resolution][bin]['ylo']) and (MOLECULE[molecule][2]["y"] <= BINS[resolution][bin]['yhi'])): 
                inside = inside + 1
            if ((MOLECULE[molecule][3]["y"] >= BINS[resolution][bin]['ylo']) and (MOLECULE[molecule][3]["y"] <= BINS[resolution][bin]['yhi'])): 
                inside = inside + 1
            if ((MOLECULE[molecule][1]["z"] >= BINS[resolution][bin]['zlo']) and (MOLECULE[molecule][1]["z"] <= BINS[resolution][bin]['zhi'])): 
                inside = inside + 1
            if ((MOLECULE[molecule][2]["z"] >= BINS[resolution][bin]['zlo']) and (MOLECULE[molecule][2]["z"] <= BINS[resolution][bin]['zhi'])): 
                inside = inside + 1
            if ((MOLECULE[molecule][3]["z"] >= BINS[resolution][bin]['zlo']) and (MOLECULE[molecule][3]["z"] <= BINS[resolution][bin]['zhi'])): 
                inside = inside + 1
            if inside >=8: 
                BINS[resolution][bin]['mass'] = BINS[resolution][bin]['mass'] + MOLECULE[molecule][1]["mass"] + MOLECULE[molecule][2]["mass"] + MOLECULE[molecule][3]["mass"] 
                dummy1 = (4*math.pi/3) * ((MOLECULE[molecule][1]["radius"]**3) + (MOLECULE[molecule][2]["radius"]**3) + (MOLECULE[molecule][1]["radius"]**3))
                dummy2 = (4*math.pi/3) * (2.75 ** 3)
                vvv = (dummy1 + dummy2) / 2
                BINS[resolution][bin]['vol'] = BINS[resolution][bin]['vol'] + vvv
                BINS[resolution][bin]['density'] = BINS[resolution][bin]['mass'] / BINS[resolution][bin]['vol']
                print('updated bin :', bin, ' - mass: ', BINS[resolution][bin]['mass'], ' - density: ', BINS[resolution][bin]['density'])             
            # in what layer 
            for layerz in LAYERSz.keys():
                if (bin in LAYERSz[layerz]['binlist']):
                    LAYERSz[layerz]['mass'] = LAYERSz[layerz]['mass'] + BINS[resolution][bin]['mass']
                    LAYERSz[layerz]['vol'] = LAYERSz[layerz]['vol'] + BINS[resolution][bin]['vol']
                    LAYERSz[layerz]['density'] = LAYERSz[layerz]['mass'] / LAYERSz[layerz]['vol']
                    print('updated layer z :', layerz, ' - mass: ', LAYERSz[layerz]['mass'], ' - density: ', LAYERSz[layerz]['density']) 
            for layery in LAYERSy.keys():
                if (bin in LAYERSy[layery]['binlist']):
                    LAYERSy[layery]['mass'] = LAYERSy[layery]['mass'] + BINS[resolution][bin]['mass']
                    LAYERSy[layery]['vol'] = LAYERSy[layery]['vol'] + BINS[resolution][bin]['vol']
                    LAYERSy[layery]['density'] = LAYERSy[layery]['mass'] / LAYERSy[layery]['vol']
                    print('updated layer y :', layery, ' - mass: ', LAYERSy[layery]['mass'], ' - density: ', LAYERSy[layery]['density'])    
            for layerx in LAYERSx.keys():
                if (bin in LAYERSx[layerx]['binlist']):
                    LAYERSx[layerx]['mass'] = LAYERSx[layerx]['mass'] + BINS[resolution][bin]['mass']
                    LAYERSx[layerx]['vol'] = LAYERSx[layerx]['vol'] + BINS[resolution][bin]['vol']
                    LAYERSx[layerx]['density'] = LAYERSx[layerx]['mass'] / LAYERSx[layerx]['vol']
                    print('updated layer x :', layerx, ' - mass: ', LAYERSx[layerx]['mass'], ' - density: ', LAYERSx[layerx]['density'])           
    for bin in BINS[resolution].keys():
        if (BINS[resolution][bin]['density'] <= 1e-6): 
            print('nearly empty bin (density <= 1e-6), probabley a nucleation site --> #bin: ', bin)
# - DONE 
fp= open(file+'_done.txt', 'w')
fp.write('dummy file:  done')
fp.close()
# End of file
# Pass86206@