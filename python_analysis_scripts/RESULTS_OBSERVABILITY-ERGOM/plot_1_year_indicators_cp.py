from netCDF4 import Dataset, num2date
import numpy as np
from matplotlib import pyplot as plt
import os
import sys, time

def plot_var(var, var_name, units, output_dir):

    fig, ax = plt.subplots(figsize=(8, 5))
#    perc = np.percentile(var, (25, 50, 75), axis=0)
#    ax.fill_between(time, var.min(axis=0), var.max(axis=0), color='C0', alpha=.5)
#    ax.fill_between(time, perc[0, :], perc[-1, :], color='C0')
    ax.plot(time, var[0,:], '-k')
    ax.set_ylabel('%s (%s)' % (var_name, units))
    ax.grid()
    fig.savefig(output_dir + var_name+".png", dpi=150)


##for i,arg in enumerate(sys.argv[1:]):
##    if i == 0:
##        path_out = arg

path_out="/g100_work/tra21_seamless/RESULTS_OBSERVABILITY/ERGOM/output_plots/L4/1-year_runs/"
#path_base= ""

n_ensemble = 1
n_days = 365

detritus = np.zeros((n_ensemble, n_days))
trophic_efficiency = np.zeros((n_ensemble, n_days))
NetPP = np.zeros((n_ensemble, n_days))
pH = np.zeros((n_ensemble, n_days))
O2 = np.zeros((n_ensemble, n_days))
Large_to_All_Phyto = np.zeros((n_ensemble, n_days))

#dirs = os.listdir(path_base)

ensmem = 0

#for subdir in dirs:

#    print("Working on ", subdir)

inp = Dataset("result.nc")

#if ensmem == 0:
nctime = inp.variables['time']
time = num2date(nctime[:], units=nctime.units, only_use_cftime_datetimes=False)
 

depth = inp.variables["z"][:,:,0,0].filled()

detritus[ensmem,:] = ((inp.variables["msi_ergom1_dd"][:,:,0,0].filled())*depth[:,:]).sum(axis=1)/depth[:,:].sum(axis=1)

trophic_efficiency[ensmem,:] = ((inp.variables["msi_ergom1_zz"][:,:,0,0].filled())*depth[:,:]).sum(axis=1)/((inp.variables["msi_ergom1_pp"][:,:,0,0].filled() + inp.variables["msi_ergom1_ff"][:,:,0,0].filled() + inp.variables["msi_ergom1_bb"][:,:,0,0].filled())*depth[:,:]).sum(axis=1)

NetPP[ensmem,:] = ((inp.variables["msi_ergom1_NPR"][:,:,0,0].filled())*depth[:,:]).sum(axis=1)

pH[ensmem,:] = (inp.variables["O3_pH"][:,:,0,0].filled()*depth[:,:]).sum(axis=1)/depth[:,:].sum(axis=1)

O2[ensmem,:] = (inp.variables["msi_ergom1_o2"][:,:3,0,0].filled()*depth[:,:3]).sum(axis=1)/depth[:,:3].sum(axis=1)

Large_to_All_Phyto[ensmem,:] = ((inp.variables["msi_ergom1_pp"][:,:,0,0].filled())*depth[:,:]).sum(axis=1)/((inp.variables["msi_ergom1_pp"][:,:,0,0].filled() + inp.variables["msi_ergom1_ff"][:,:,0,0].filled() + inp.variables["msi_ergom1_bb"][:,:,0,0].filled())*depth[:,:]).sum(axis=1)


#ensmem += 1




plot_var(detritus, "nlpoc", "mmolC/m$^{3}$", path_out)
plot_var(trophic_efficiency, "troph", "1", path_out)
plot_var(NetPP, "npp", "mmolC/(m$^{2}$d)", path_out)
plot_var(pH, "pH", "1", path_out)
plot_var(O2, "O2", "mmolO2/m$^{3}$", path_out)
plot_var(Large_to_All_Phyto, "lpr", "1", path_out)


out=Dataset(path_out+"1_year_simulation.nc", "w", format="NETCDF4_CLASSIC")

out.createDimension("time", n_days)

var1 = out.createVariable("nlpoc", np.float32, ("time"))
var1[:] = detritus[0,:]

var1 = out.createVariable("troph", np.float32, ("time"))
var1[:] = trophic_efficiency[0,:]

var1 = out.createVariable("npp", np.float32, ("time"))
var1[:] = NetPP[0,:]

var1 = out.createVariable("pH", np.float32, ("time"))
var1[:] = pH[0,:]

var1 = out.createVariable("O2", np.float32, ("time"))
var1[:] = O2[0,:]

var1 = out.createVariable("lpr", np.float32, ("time"))
var1[:] = Large_to_All_Phyto[0,:]

out.close()


