import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset as nc

file='result.nc'
data=nc(file,"r")
depth=data.variables['z']
depth=np.squeeze(depth)
for i in range (len(depth[0])):
   print(i, '  ', depth[0,i])
temp=data.variables['temp'][:]
fig = plt.figure()
for i in range (365):
   ax = fig.add_subplot(111)

   ax.plot(temp[i,:,:,:], depth, 'b')
   ax.xaxis.tick_top()

   ax.set_ylabel('depth')
   ax.set_ylim(-50, 0)
   #ax.set_xlim(0, 25)
   ax.set_xlabel('temperature [oC]')

fileout='temp_profile.png'
fig.savefig(fileout, format='png',dpi=150, bbox_inches="tight")

