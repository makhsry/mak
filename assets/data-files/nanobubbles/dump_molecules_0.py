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
# - building bins with different resolutions 
resolutions = np.array([1, 10])
BINS = {}
LAYERSx = {}
LAYERSy = {}
LAYERSz = {}
for resolution in resolutions:
    print('populating with a resolution of: ', resolution, ' *5.1*2.75 --- Navier-Stokes ---')
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
        LAYERSz[layer]["zlo"], LAYERSz[layer]["zhi"] = zgrid[i], zgrid[i+1]
        LAYERSz[layer]["mass"] = 0
        LAYERSz[layer]["VOL"] = abs(zgrid[i] - zgrid[i+1]) * abs(xlo - xhi) * abs(ylo - yhi) 
        LAYERSz[layer]["vol"] = 0
        LAYERSz[layer]["density"] = 0 
        LAYERSz[layer]["binlist"] = [] 
    for i in range(ygrid.shape[0]-1):
        layer = i + 1
        LAYERSy[layer] = {}
        LAYERSy[layer]["ylo"], LAYERSy[layer]["yhi"] = ygrid[i], ygrid[i+1]
        LAYERSy[layer]["mass"] = 0
        LAYERSy[layer]["VOL"] = abs(ygrid[i] - ygrid[i+1]) * abs(xlo - xhi) * abs(zlo - zhi) 
        LAYERSy[layer]["vol"] = 0
        LAYERSy[layer]["density"] = 0 
        LAYERSy[layer]["binlist"] = [] 
    for i in range(xgrid.shape[0]-1):
        layer = i + 1
        LAYERSx[layer] = {}
        LAYERSx[layer]["xlo"], LAYERSx[layer]["xhi"] = xgrid[i], xgrid[i+1]
        LAYERSx[layer]["mass"] = 0
        LAYERSx[layer]["VOL"] = abs(xgrid[i] - xgrid[i+1]) * abs(ylo - yhi) * abs(zlo - zhi) 
        LAYERSx[layer]["vol"] = 0
        LAYERSx[layer]["density"] = 0 
        LAYERSx[layer]["binlist"] = [] 
    # creating bins 
    for i in range(xgrid.shape[0]-1):
        layerx = i + 1
        for j in range(ygrid.shape[0]-1):
            layery = j + 1
            for k in range(zgrid.shape[0]-1):
              layerz = k + 1
              bin += 1
              BINS[resolution][bin] = {}
              BINS[resolution][bin]["xlo"], BINS[resolution][bin]["xhi"] = xgrid[i], xgrid[i+1]
              BINS[resolution][bin]["ylo"], BINS[resolution][bin]["yhi"] = ygrid[j], ygrid[j+1]
              BINS[resolution][bin]["zlo"], BINS[resolution][bin]["zhi"] = zgrid[k], zgrid[k+1]
              BINS[resolution][bin]["VOL"] = abs(BINS[resolution][bin]["xhi"] - BINS[resolution][bin]["xlo"]) * abs(BINS[resolution][bin]["yhi"] - BINS[resolution][bin]["ylo"]) * abs(BINS[resolution][bin]["zhi"] - BINS[resolution][bin]["zlo"])
              BINS[resolution][bin]["mass"] = 0
              BINS[resolution][bin]["vol"] = 0
              BINS[resolution][bin]["density"] = 0
              if (BINS[resolution][bin]["zlo"]>=LAYERSz[layerz]["zlo"]) and (BINS[resolution][bin]["zhi"] <=LAYERSz[layerz]["zhi"]):
                LAYERSz[layerz]["binlist"].append(bin) 
              if (BINS[resolution][bin]["ylo"]>=LAYERSy[layery]["ylo"]) and (BINS[resolution][bin]["yhi"] <=LAYERSy[layery]["yhi"]):
                LAYERSy[layery]["binlist"].append(bin) 
              if (BINS[resolution][bin]["xlo"]>=LAYERSx[layerx]["xlo"]) and (BINS[resolution][bin]["xhi"] <=LAYERSx[layerx]["xhi"]):
                LAYERSx[layerx]["binlist"].append(bin) 
    # - adding to bins and layers 
    for atom in ATOMS.keys():
        for bin in BINS[resolution].keys():
            # in what bin?
            inside = 0
            if ((ATOMS[atom]["x"] >= BINS[resolution][bin]["xlo"]) and (ATOMS[atom]["x"] <= BINS[resolution][bin]["xhi"])): 
                inside = inside + 1
            if ((ATOMS[atom]["y"] >= BINS[resolution][bin]["ylo"]) and (ATOMS[atom]["y"] <= BINS[resolution][bin]["yhi"])): 
                inside = inside + 1
            if ((ATOMS[atom]["z"] >= BINS[resolution][bin]["zlo"]) and (ATOMS[atom]["z"] <= BINS[resolution][bin]["zhi"])): 
                inside = inside + 1
            if inside == 3: 
                BINS[resolution][bin]["mass"] = BINS[resolution][bin]["mass"] + ATOMS[atom]["mass"] 
                BINS[resolution][bin]["vol"] = BINS[resolution][bin]["vol"] + (4*math.pi/3) * (ATOMS[atom]["radius"]**3)
                BINS[resolution][bin]["density"] = BINS[resolution][bin]["mass"] / BINS[resolution][bin]["VOL"]
                print('updated bin: ', bin, ' - density: ', BINS[resolution][bin]["density"])
        # in what layer?
        for layerx in LAYERSx.keys():
            if ((ATOMS[atom]["x"] >= LAYERSx[layerx]["xlo"]) and (ATOMS[atom]["x"] <= LAYERSx[layerx]["xhi"])): 
                LAYERSx[layerx]["mass"] = LAYERSx[layerx]["mass"] + ATOMS[atom]["mass"]
                LAYERSx[layerx]["vol"] = LAYERSx[layerx]["vol"] + (4*math.pi/3) * (ATOMS[atom]["radius"]**3)
                LAYERSx[layerx]["density"] = LAYERSx[layerx]["mass"] / LAYERSx[layerx]["VOL"]
                print('updated layerx: ', layerx, ' - density: ', LAYERSx[layerx]["density"])
        for layery in LAYERSy.keys():
            if ((ATOMS[atom]["y"] >= LAYERSy[layery]["ylo"]) and (ATOMS[atom]["y"] <= LAYERSy[layery]["yhi"])): 
                LAYERSy[layery]["mass"] = LAYERSy[layery]["mass"] + ATOMS[atom]["mass"]
                LAYERSy[layery]["vol"] = LAYERSy[layery]["vol"] + (4*math.pi/3) * (ATOMS[atom]["radius"]**3)
                LAYERSy[layery]["density"] = LAYERSy[layery]["mass"] / LAYERSy[layery]["VOL"]
                print('updated layery: ', layery, ' - density: ', LAYERSy[layery]["density"])
        for layerz in LAYERSz.keys():
            if ((ATOMS[atom]["z"] >= LAYERSz[layerz]["zlo"]) and (ATOMS[atom]["z"] <= LAYERSz[layerz]["zhi"])): 
                LAYERSz[layerz]["mass"] = LAYERSz[layerz]["mass"] + ATOMS[atom]["mass"]
                LAYERSz[layerz]["vol"] = LAYERSz[layerz]["vol"] + (4*math.pi/3) * (ATOMS[atom]["radius"]**3)
                LAYERSz[layerz]["density"] = LAYERSz[layerz]["mass"] / LAYERSz[layerz]["VOL"]  
                print('updated layerz: ', layerz, ' - density: ', LAYERSz[layerz]["density"])
    # empty bins - nucleation sites ....         
    for bin in BINS[resolution].keys():
        if (BINS[resolution][bin]["density"] <= 1e-6): 
            print('nearly empty bin (density <= 1e-6), probabley a nucleation site --> #bin: ', bin)
# - DONE 
fp= open(file+'_done.txt', 'w')
fp.write('dummy file:  done')
fp.close()
# End of file
# Pass86206@