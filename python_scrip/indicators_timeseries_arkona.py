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
          'chl_max_in_10m_to_45m',
          'depth_of_chl_max_in_10m_to_45m']
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

'''
#    <target name="non-living_particulate_organic_carbon" expression="((1.0e6*(gom_c+pom_c)*h)[:,:].sum(axis=1)/h[:,:].sum(axis=1)).mean(axis=0)" path="result.nc"/>
ind['non-living_particulate_organic_carbon']=(1.0e6*(var['gom_c']+var['pom_c'])*var['h'])[:,:].sum(axis=1)/var['h'][:,:].sum(axis=1)

#    <target name="trophic_efficiency" expression="((zoo_c+mes_c)*h)[:,:].sum(axis=1).mean(axis=0)/((phy_c+dia_c)*h)[:,:].sum(axis=1).mean(axis=0)" path="result.nc"/>
ind['trophic_efficiency']=((var['zoo_c']+var['mes_c'])*var['h'])[:,:].sum(axis=1)/((var['phy_c']+var['dia_c'])*var['h'])[:,:].sum(axis=1)

#    <target name="net_primary_production" expression="(86400.0*1.0e3*12.0*(phy_PPPHY+dia_PPPHY)*h)[:,:].sum(axis=1).mean(axis=0)" path="result.nc"/>
ind['net_primary_production']=(86400.0*1.0e3*12.0*(var['phy_PPPHY']+var['dia_PPPHY'])*var['h'])[:,:].sum(axis=1)

#    <target name="pH" expression="(((carbonate_PH)*h)[:,:].sum(axis=1)/h[:,:].sum(axis=1)).mean(axis=0)" path="result.nc"/>
ind['pH']=(((var['carbonate_PH'])*var['h'])[:,:].sum(axis=1)/var['h'][:,:].sum(axis=1))

#    <target name="O2" expression="((1.0e6*(oxy_O2)*h)[:,:3].sum(axis=1)/h[:,:3].sum(axis=1)).mean(axis=0)" path="result.nc"/>
ind['O2']=((1.0e6*(var['oxy_O2'])*var['h'])[:,:3].sum(axis=1)/var['h'][:,:3].sum(axis=1))

#    <target name="large_over_all_phytoplankton" expression="((dia_c)*h)[:,:].sum(axis=1).mean(axis=0)/((dia_c+phy_c)*h)[:,:].sum(axis=1).mean(axis=0)" path="result.nc"/>
ind['large_over_all_phytoplankton']=((var['dia_c'])*var['h'])[:,:].sum(axis=1)/((var['dia_c']+var['phy_c'])*var['h'])[:,:].sum(axis=1)

#    <target name="chl_max_in_5m" expression="( cumsum (((total_chlorophyll_calculator_result)*h)[:,70:].sum(axis=1)/h[:,70:].sum(axis=1))[3:]/3.0 -  cumsum (((total_chlorophyll_calculator_result)*h)[:,70:].sum(axis=1)/h[:,70:].sum(axis=1))[:-3]/3.0 ).max(axis=0)" path="result.nc"/>
ind['chl_in_5m']=((var['total_chlorophyll_calculator_result'])*var['h'])[:,70:].sum(axis=1)/var['h'][:,70:].sum(axis=1)

#    <target name="chl_max_in_10m_to_150m" expression="(total_chlorophyll_calculator_result)[:,:58].mean(axis=0).max(axis=0)" path="result.nc"/>
ind['chl_max_in_10m_to_50m']=(var['total_chlorophyll_calculator_result'])[:,:58].max(axis=1)

#    <target name="timing_of_chl_max_in_5m" expression="( cumsum (((total_chlorophyll_calculator_result)*h)[:,70:].sum(axis=1)/h[:,70:].sum(axis=1))[3:]/3.0 -  cumsum (((total_chlorophyll_calculator_result)*h)[:,70:].sum(axis=1)/h[:,70:].sum(axis=1))[:-3]/3.0 ).argmax(axis=0)" path="result.nc"/>

#    <target name="depth_of_chl_max_in_10m_to_150m" expression="(total_chlorophyll_calculator_result)[:,:58].mean(axis=0).argmax(axis=0)" path="result.nc"/>
for t,date_time_obj in enumerate(date_list):
    ind['depth_of_chl_max_in_10m_to_50m'][t]=depth[t,int((var['total_chlorophyll_calculator_result'])[t,:58].argmax(axis=0))]
'''

#"non-living_particulate_organic_carbon" expression="(((msi_ergom1_dd)*h)[:,:].sum(axis=1)/h[:,:].sum(axis=1)).mean(axis=0)" path="result.nc"/>
ind['non-living_particulate_organic_carbon']=(12.07*(var['msi_ergom1_dd'])*var['h'])[:,:].sum(axis=1)/var['h'][:,:].sum(axis=1)

# "trophic_efficiency" expression="((msi_ergom1_zz)*h)[:,:].sum(axis=1).mean(axis=0)/((msi_ergom1_pp+msi_ergom1_ff+msi_ergom1_bb)*h)[:,:].sum(axis=1).mean(axis=0)" path="result.nc"/>
ind['trophic_efficiency']=(((var['msi_ergom1_zz']))*var['h'])[:,:].sum(axis=1)/(((var['msi_ergom1_pp']+var['msi_ergom1_ff']+var['msi_ergom1_bb']))*var['h'])[:,:].sum(axis=1)

# "net_primary_production" expression="((msi_ergom1_NPR)*h)[:,:].sum(axis=1).mean(axis=0)" path="result.nc"/>
ind['net_primary_production']=((12.01*9.5*(var['msi_ergom1_NPR']))*var['h'])[:,:].sum(axis=1)

# "pH" expression="(((O3_pH)*h)[:,:].sum(axis=1)/h[:,:].sum(axis=1)).mean(axis=0)" path="result.nc"/>
ind['pH']=(((var['O3_pH'])*var['h'])[:,:].sum(axis=1)/var['h'][:,:].sum(axis=1))

# "O2" expression="(((msi_ergom1_o2)*h)[:,:3].sum(axis=1)/h[:,:3].sum(axis=1)).mean(axis=0)" path="result.nc"/>
#ind['O2']=((1.0e6*(var['msi_ergom1_o2'])*var['h'])[:,:3].sum(axis=1)/var['h'][:,:3].sum(axis=1))
ind['O2']=(((var['msi_ergom1_o2'])*var['h'])[:,:3].sum(axis=1)/var['h'][:,:3].sum(axis=1))

# "large_over_all_phytoplankton" expression="((msi_ergom1_pp)*h)[:,:].sum(axis=1).mean(axis=0)/((msi_ergom1_pp+msi_ergom1_ff+msi_ergom1_bb)*h)[:,:].sum(axis=1).mean(axis=0)" path="result.nc"/>
ind['large_over_all_phytoplankton']=((var['msi_ergom1_pp'])*var['h'])[:,:].sum(axis=1)/((var['msi_ergom1_pp']+var['msi_ergom1_ff']+var['msi_ergom1_bb'])*var['h'])[:,:].sum(axis=1)

# "chl_max_in_5m" expression="( cumsum (((msi_ergom1_pp+msi_ergom1_ff+msi_ergom1_bb)*h)[:,199:].sum(axis=1)/h[:,199:].sum(axis=1))[3:]/3.0 -  cumsum (((msi_ergom1_pp+msi_ergom1_ff+msi_ergom1_bb)*h)[:,199:].sum(axis=1)/h[:,199:].sum(axis=1))[:-3]/3.0 ).max(axis=0)" path="result.nc"/>
ind['chl_in_5m']=(1.1*(var['msi_ergom1_pp']+var['msi_ergom1_ff']+var['msi_ergom1_bb'])*var['h'])[:,51:].sum(axis=1)/var['h'][:,51:].sum(axis=1)

# "chl_max_in_10m_to_50m" expression="(msi_ergom1_pp+msi_ergom1_ff+msi_ergom1_bb)[:,:58].mean(axis=0).max(axis=0)" path="result.nc"/>
ind['chl_max_in_10m_to_45m']=(1.1*(var['msi_ergom1_pp']+var['msi_ergom1_ff']+var['msi_ergom1_bb']))[:,:45].max(axis=1)

# "depth_of_chl_max_in_10m_to_50m" expression="(msi_ergom1_pp+msi_ergom1_ff+msi_ergom1_bb)[:,:58].mean(axis=0).argmax(axis=0)" path="result.nc"/>
for t,date_time_obj in enumerate(date_list):
    ind['depth_of_chl_max_in_10m_to_45m'][t]=depth[t,int(((1.1*(var['msi_ergom1_pp']+var['msi_ergom1_ff']+var['msi_ergom1_bb'])))[t,:45].argmax(axis=0))]



output = MODEL + '_Arkona' + '_ONEYEAR_INDICATORS.txt'
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

