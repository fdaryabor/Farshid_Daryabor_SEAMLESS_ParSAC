import netCDF4
from netCDF4 import Dataset
import numpy as np
import tkinter
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import datetime
import matplotlib.dates as mdates

myfile = 'result.nc'
fh = Dataset(myfile, mode = 'r')
time  = np.transpose(np.squeeze(fh.variables['time'][:]))
dept  = np.transpose(np.squeeze(fh.variables['z'][:]))
#oxyg  = np.transpose(np.squeeze(fh.variables['msi_ergom1_o2'][:]))
phos  = np.transpose(np.squeeze(fh.variables['msi_ergom1_po'][:]))
fh.close()
dept_25 = dept[33:]
#oxyg_25 = oxyg[33:,:]
phos_25 = phos[33:,:]

plt.rcParams["figure.figsize"] = (7,3) 

xticks = np.arange(15*24*3600,365*24*3600,30*24*3600)
xticklabels = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D']
#plt.pcolor(time,depth, oxy, shading='auto', cmap='YlGn')
#plt.colorbar()
ax = plt.gca()
pcolorplot = ax.pcolor(time,dept_25, phos_25, shading='auto', cmap='jet' ) #, cmap='YlGn'
cb = plt.colorbar(pcolorplot, ax=ax, orientation="vertical", pad=0.01)
cb.set_label('$mmol p/m^3$')
#pcolorplot.set_clim([0.2,0.7])
ax.set_xticks(xticks)
ax.set_xticklabels(xticklabels)
ax.set_xlabel('Month')
ax.set_ylabel('depth (m)')
#plt.show()
fileout='pho_model.png'
plt.savefig(fileout, format='png',dpi=150, bbox_inches="tight")







