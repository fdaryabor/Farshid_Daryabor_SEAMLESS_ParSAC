import os,sys
import netCDF4 as NC4
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import datetime
from datetime import timedelta


ref = datetime.datetime(2014, 6, 1, 0, 0, 0)

infile='result.nc' 

NCin=NC4.Dataset(infile,"r")

depth=NCin.variables['z'][:,:,0,0].filled()

time=NCin.variables['time'][:].filled()


date_list = []

for myt in time:
    step = datetime.timedelta(seconds=np.int(myt))
    date_list.append(ref + step)

nT=len(date_list)
nZ=depth.shape[1]

#(time, z, lat, lon)
POP=NCin.variables['msi_ergom1_nn'][:,:,0,0].filled()

fig,axs = plt.subplots(1,figsize=(9, 6),gridspec_kw = {'wspace':1.5, 'hspace':1.5})
#fig,axs = plt.subplots(1, gridspec_kw = {'wspace':0.5, 'hspace':0.35})
POPT=np.transpose(POP)
x=np.tile(np.arange(nT),(nZ,1))
y=np.transpose(np.tile(depth[0,:],(nT,1)))
cax=axs.pcolor(x,y,POPT)
#cax=axs.pcolor(x,y,CHLT,norm=LogNorm(vmin=0.1, vmax=CHLT.max()))
tpos=range(0,nT,30)
axs.set_xticks(tpos)
tick_labels=[]
for i in tpos:
   tick_labels.append(date_list[i].strftime("%Y %m"))
axs.set_xticklabels(tick_labels,rotation=90)

axs.set_ylim([-100,0])
axs.set_xlabel('Time')
axs.set_ylabel('Depth [m]')
cbar = fig.colorbar(cax)

fileout='NO3.png'
fig.savefig(fileout, format='png',dpi=150, bbox_inches="tight")

