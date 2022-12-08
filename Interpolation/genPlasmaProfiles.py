import os
import netCDF4 as nc
import torch
import numpy as np
from enum import Enum, IntEnum
import collections

def function(model,r,z):
    
    Inputs = collections.namedtuple('SOLEDGE', 'R Z')
    L=[]
    for ir in r:
        val =[]
        for jz in z:
            [b_phi,b_r,b_z,T_e,n_e,v_e,t_i,n_i,v_i]=[model(Inputs(ir, jz))[0][i] for i in range(9)]
            val.append([b_phi,b_r,b_z,T_e,n_e,v_e,t_i,n_i,v_i])
        L.append(val)
    
    return np.asarray(L)
 
# Load in the interpolated torch model
model=torch.load("data.pt")

# Set grid points
nR,nZ=5,10
r_=np.linspace(1.8,3.5,nR)
z_=np.linspace(-1,1,nZ)

# Get plasma data
[b_phi,b_r,b_z,t_e,n_e,v_e,t_i,n_i,v_i]=[function(model,r_,z_)[:,:,i] for i in range(9)]


#writeGITRplasmaProfile
profiles_filename = "profiles.nc"

if os.path.exists(profiles_filename):
    os.remove(profiles_filename)

rootgrp = nc.Dataset(profiles_filename, "w", format="NETCDF4")

nr = rootgrp.createDimension("nR", nR)
nz = rootgrp.createDimension("nZ", nZ)

r = rootgrp.createVariable("gridR", "f8", ("nR"))
z = rootgrp.createVariable("gridZ", "f8", ("nZ"))

ne = rootgrp.createVariable("ne", "f8", ("nZ", "nR"))
te = rootgrp.createVariable("te", "f8", ("nZ", "nR"))

ni = rootgrp.createVariable("ni", "f8", ("nZ", "nR"))
ti = rootgrp.createVariable("ti", "f8", ("nZ", "nR"))

vpar = rootgrp.createVariable("Vpara", "f8", ("nZ", "nR"))

br = rootgrp.createVariable("br", "f8", ("nZ", "nR"))
bt = rootgrp.createVariable("bt", "f8", ("nZ", "nR"))
bz = rootgrp.createVariable("bz", "f8", ("nZ", "nR"))

r[:] = r_
z[:] = z_

ne[:] = n_e.T
te[:] = t_e.T

ni[:] = n_i.T
ti[:] = t_i.T

###
rootgrp.close()
