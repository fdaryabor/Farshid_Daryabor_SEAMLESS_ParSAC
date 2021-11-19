import argparse
def argument():
    parser = argparse.ArgumentParser(description = '''
    Prepare .txt table of indicator time series based on results.nc from gotm
    ''',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(   '--infile', '-i',
                                type = str,
                                required = True,
                                help = ''' result. nc file from gotm '''

                                )

    parser.add_argument(   '--model', '-m',
                                type = str,
                                required = True,
                                help = ''' model used for simulation (e.g., BFM, ERSEM, PISCES) '''

                                )

    return parser.parse_args()

args = argument()



import os,sys
import netCDF4 as NC4
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import datetime
from datetime import timedelta



infile = args.infile
MODEL = args.model


NCin=NC4.Dataset(infile,"r")

depth=NCin.variables['z'][:,:,0,0].filled()

time=NCin.variables['time'][:].filled()

ref = datetime.datetime.strptime(NCin.variables['time'].units[-19:-9],'%Y-%m-%d')


date_list = []


for myt in time:
    step = datetime.timedelta(seconds=int(myt))
    date_list.append(ref + step)

nT=len(date_list)
nZ=depth.shape[1]

#(time, z, lat, lon)
# list_var=['h','gom_c','pom_c','mes_c','zoo_c','dia_c','phy_c','no3_c','po4_c','oxy_O2','carbonate_DIC','carbonate_PH','phy_PPPHY','dia_PPPHY','total_chlorophyll_calculator_result']
list_var=['h','msi_ergom1_dd','msi_ergom1_zz','msi_ergom1_pp','msi_ergom1_ff','msi_ergom1_bb','msi_ergom1_NPR','O3_pH','msi_ergom1_o2',]
list_ind=['non-living_particulate_organic_carbon',
          'trophic_efficiency',
          'net_primary_production',
          'pH',
          'O2',
          'large_over_all_phytoplankton',
          'chl_in_5m',
          'chl_max_in_10m_to_150m',
          'depth_of_chl_max_in_10m_to_150m']
var={}

for vv in list_var:
    print(vv)
    var[vv]=NCin.variables[vv][:,:,0,0].filled()

ind={}

for i in list_ind:
    print(i)
    ind[i]=np.zeros(nT)

NCin.close()

#indicators


#"non-living_particulate_organic_carbon" expression="(((msi_ergom1_dd)*h)[:,145:].sum(axis=1)/h[:,145:].sum(axis=1)).mean(axis=0)" path="result.nc"/>
ind['non-living_particulate_organic_carbon']=(12.07*(var['msi_ergom1_dd'])*var['h'])[:,145:].sum(axis=1)/var['h'][:,145:].sum(axis=1)

# "trophic_efficiency" expression="((msi_ergom1_zz)*h)[:,145:].sum(axis=1).mean(axis=0)/((msi_ergom1_pp+msi_ergom1_ff+msi_ergom1_bb)*h)[:,145:].sum(axis=1).mean(axis=0)" path="result.nc"/>
ind['trophic_efficiency']=((var['msi_ergom1_zz'])*var['h'])[:,145:].sum(axis=1)/((var['msi_ergom1_pp']+var['msi_ergom1_ff']+var['msi_ergom1_bb'])*var['h'])[:,145:].sum(axis=1)

# "net_primary_production" expression="((msi_ergom1_NPR)*h)[:,145:].sum(axis=1).mean(axis=0)" path="result.nc"/>
ind['net_primary_production']=(12.07*(var['msi_ergom1_NPR'])*var['h'])[:,145:].sum(axis=1)

# "pH" expression="(((O3_pH)*h)[:,145:].sum(axis=1)/h[:,145:].sum(axis=1)).mean(axis=0)" path="result.nc"/>
ind['pH']=(((var['O3_pH'])*var['h'])[:,145:].sum(axis=1)/var['h'][:,145:].sum(axis=1))

# "O2" expression="(((msi_ergom1_o2)*h)[:,145:160].sum(axis=1)/h[:,145:160].sum(axis=1)).mean(axis=0)" path="result.nc"/>
#ind['O2']=((1.0e6*(var['msi_ergom1_o2'])*var['h'])[:,145:160].sum(axis=1)/var['h'][:,145:160].sum(axis=1))
ind['O2']=(((var['msi_ergom1_o2'])*var['h'])[:,145:160].sum(axis=1)/var['h'][:,145:160].sum(axis=1))
# "large_over_all_phytoplankton" expression="((msi_ergom1_pp)*h)[:,145:].sum(axis=1).mean(axis=0)/((msi_ergom1_pp+msi_ergom1_ff+msi_ergom1_bb)*h)[:,145:].sum(axis=1).mean(axis=0)" path="result.nc"/>
ind['large_over_all_phytoplankton']=((var['msi_ergom1_pp'])*var['h'])[:,145:].sum(axis=1)/((var['msi_ergom1_pp']+var['msi_ergom1_ff']+var['msi_ergom1_bb'])*var['h'])[:,145:].sum(axis=1)

# "chl_max_in_5m" expression="( cumsum (((msi_ergom1_pp+msi_ergom1_ff+msi_ergom1_bb)*h)[:,199:].sum(axis=1)/h[:,199:].sum(axis=1))[3:]/3.0 -  cumsum (((msi_ergom1_pp+msi_ergom1_ff+msi_ergom1_bb)*h)[:,199:].sum(axis=1)/h[:,199:].sum(axis=1))[:-3]/3.0 ).max(axis=0)" path="result.nc"/>
ind['chl_in_5m']=(1.1*(var['msi_ergom1_pp']+var['msi_ergom1_ff']+var['msi_ergom1_bb'])*var['h'])[:,199:].sum(axis=1)/var['h'][:,199:].sum(axis=1)

# "chl_max_in_10m_to_150m" expression="(msi_ergom1_pp+msi_ergom1_ff+msi_ergom1_bb)[:,152:192].mean(axis=0).max(axis=0)" path="result.nc"/>
ind['chl_max_in_10m_to_150m']=(1.1*(var['msi_ergom1_pp']+var['msi_ergom1_ff']+var['msi_ergom1_bb']))[:,152:192].max(axis=1)

# "depth_of_chl_max_in_10m_to_150m" expression="(msi_ergom1_pp+msi_ergom1_ff+msi_ergom1_bb)[:,152:192].mean(axis=0).argmax(axis=0)" path="result.nc"/>
for t,date_time_obj in enumerate(date_list):
    ind['depth_of_chl_max_in_10m_to_150m'][t]=depth[t,int(1.1*((var['msi_ergom1_pp']+var['msi_ergom1_ff']+var['msi_ergom1_bb']))[t,152:192].argmax(axis=0))+152]



output = MODEL + '_BATS' + '_ONEYEAR_INDICATORS.txt'
fid = open(output,'w')
header='DATE'
for i,indicator in enumerate(list_ind):
    header += '\t' + indicator

fid.write(header)
fid.write("\n")


for t,date_time_obj in enumerate(date_list):
     fid.write(date_time_obj.strftime("%Y-%m-%d 12:00:00"))
     for i,indicator in enumerate(list_ind):
         fid.write('\t')
         fid.write(str(ind[indicator][t]))
     fid.write('\n')
fid.close()

