import numpy as np
import matplotlib.pyplot as plt

def str2num_noneg(str_in):
    num = float(str_in)
    return num

lines = []
with open('no3.txt') as f:
    for line in f:
        lines.append(line)
f.close()
datalines = lines[1: -1]

depth = np.zeros(len(datalines))
no3 = np.zeros([len(datalines),12])
i = 0
for line in datalines:
    # convert each line to to charecter array
    textarray = line.split()
    dth = str2num_noneg(textarray[0])
    depth[i] = dth
    for j in range(12):
        value = textarray[j+1]
        no3[i,j] = value
    i+=1
time = np.arange(1,13)

plt.rcParams["figure.figsize"] = (7,3)
xticks = np.arange(1,13)
xticklabels = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D']
#plt.pcolor(time,depth, no3, shading='auto', cmap='YlGn')
#plt.colorbar()
ax = plt.gca()
pcolorplot = ax.pcolor(time,depth, no3, shading='auto', cmap='jet') #, cmap='YlGn'
cb = plt.colorbar(pcolorplot, ax=ax, orientation="vertical", pad=0.01)
cb.set_label('$mmoln/m^3$')
pcolorplot.set_clim([0,6])
ax.set_xticks(xticks)
ax.set_xticklabels(xticklabels)
ax.set_xlabel('Month')
ax.set_ylabel('depth (m)')
plt.show()
fileout='no3_obs.png'
plt.savefig(fileout, format='png',dpi=150, bbox_inches="tight")

