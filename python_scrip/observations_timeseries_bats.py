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
# list_var=['h','gom_c','pom_c','mes_c','zoo_c','dia_c','phy_c','no3_c','po4_c','oxy_O2','carbonate_DIC','carbonate_PH','phy_PPPHY','dia_PPPHY','total_chlorophyll_calculator_result']#,'carbonate_pCO2']
list_var=['h','msi_ergom1_dd','msi_ergom1_zz','msi_ergom1_pp','msi_ergom1_ff','msi_ergom1_bb','msi_ergom1_NPR','O3_pH','msi_ergom1_o2','msi_ergom1_nn','msi_ergom1_po','O3_c']
list_ind=['ocean_colour',
          'BGC_Argo_chl_0m_to_300m',
          'BGC_Argo_no3_0m_to_300m',
          'BGC_Argo_po4_0m_to_300m',
          'BGC_Argo_POC_0m_to_300m',
          'BGC_Argo_POC_300m_to_1000m',
          'BGC_Argo_o2_0m_to_300m',
          'BGC_Argo_o2_300m_to_1000m',
          'BGC_Argo_DIC_0m_to_300m',
          'BGC_Argo_DIC_300m_to_1000m',
          'BGC_Argo_pH_0m_to_300m',
          'BGC_Argo_pH_300m_to_1000m',
#          'BGC_Argo_pCO2_0m_to_300m',
#          'BGC_Argo_pCO2_300m_to_1000m',
]

var={}

for vv in list_var:
    print(vv)
    var[vv]=NCin.variables[vv][:,:,0,0].filled()

ind={}

for i in list_ind:
    print(i)
    ind[i]=np.zeros(nT)


#indicator

# ocean_colour=(((P1_Chl+P2_Chl+P3_Chl+P4_Chl)*h)[:,192:].sum(axis=1)/h[:,192:].sum(axis=1)).mean(axis=0)
ind['ocean_colour']=(((var['msi_ergom1_pp']+var['msi_ergom1_ff']+var['msi_ergom1_bb'])*var['h'])[:,192:].sum(axis=1)/var['h'][:,192:].sum(axis=1))
# BGC_Argo_chl_0m_to_300m=(((P1_Chl+P2_Chl+P3_Chl+P4_Chl)*h)[:,138:].sum(axis=1)/h[:,138:].sum(axis=1)).mean(axis=0)
ind['BGC_Argo_chl_0m_to_300m']=((1.1*(var['msi_ergom1_pp']+var['msi_ergom1_ff']+var['msi_ergom1_bb'])*var['h'])[:,138:].sum(axis=1)/var['h'][:,138:].sum(axis=1))
# BGC_Argo_no3_0m_to_300m=(((N3_n)*h)[:,138:].sum(axis=1)/h[:,138:].sum(axis=1)).mean(axis=0)
ind['BGC_Argo_no3_0m_to_300m']=(((var['msi_ergom1_nn'])*var['h'])[:,138:].sum(axis=1)/var['h'][:,138:].sum(axis=1))
# BGC_Argo_POC_0m_to_300m=(((R6_c+P2_c+P3_c+Z6_c+B1_c)*h)[:,138:].sum(axis=1)/h[:,138:].sum(axis=1)).mean(axis=0)
ind['BGC_Argo_po4_0m_to_300m']=(((var['msi_ergom1_po'])*var['h'])[:,138:].sum(axis=1)/var['h'][:,138:].sum(axis=1))
# BGC_Argo_POC_0m_to_300m=(((R6_c+P2_c+P3_c+Z6_c+B1_c)*h)[:,138:].sum(axis=1)/h[:,138:].sum(axis=1)).mean(axis=0)
ind['BGC_Argo_POC_0m_to_300m']=(((var['msi_ergom1_dd']+var['msi_ergom1_ff']+var['msi_ergom1_bb'])*var['h'])[:,138:].sum(axis=1)/var['h'][:,138:].sum(axis=1))
# BGC_Argo_POC_300m_to_1000m=(((R6_c+P2_c+P3_c+Z6_c+B1_c)*h)[:,124:138].sum(axis=1)/h[:,124:138].sum(axis=1)).mean(axis=0)
ind['BGC_Argo_POC_300m_to_1000m']=(((var['msi_ergom1_dd']+var['msi_ergom1_ff']+var['msi_ergom1_bb'])*var['h'])[:,124:138].sum(axis=1))/var['h'][:,124:138].sum(axis=1)
# BGC_Argo_o2_0m_to_300m=(((O2_o)*h)[:,138:].sum(axis=1)/h[:,138:].sum(axis=1)).mean(axis=0)
ind['BGC_Argo_o2_0m_to_300m']=(((var['msi_ergom1_o2'])*var['h'])[:,138:].sum(axis=1)/var['h'][:,138:].sum(axis=1))
# BGC_Argo_o2_300m_to_1000m=(((O2_o)*h)[:,124:138].sum(axis=1)/h[:,124:138].sum(axis=1)).mean(axis=0)
ind['BGC_Argo_o2_300m_to_1000m']=(((var['msi_ergom1_o2'])*var['h'])[:,124:138].sum(axis=1)/var['h'][:,124:138].sum(axis=1))
# BGC_Argo_DIC_0m_to_300m=(((O3_c)*h)[:,138:].sum(axis=1)/h[:,138:].sum(axis=1)).mean(axis=0)
ind['BGC_Argo_DIC_0m_to_300m']=(((var['O3_c'])*var['h'])[:,138:].sum(axis=1)/var['h'][:,138:].sum(axis=1))
# BGC_Argo_DIC_300m_to_1000m=(((O3_c)*h)[:,124:138].sum(axis=1)/h[:,124:138].sum(axis=1)).mean(axis=0)
ind['BGC_Argo_DIC_300m_to_1000m']=((12.07*(var['O3_c'])*var['h'])[:,124:138].sum(axis=1)/var['h'][:,124:138].sum(axis=1))
# BGC_Argo_pH_0m_to_300m=(((O3_pH)*h)[:,138:].sum(axis=1)/h[:,138:].sum(axis=1)).mean(axis=0)
ind['BGC_Argo_pH_0m_to_300m']=(((var['O3_pH'])*var['h'])[:,138:].sum(axis=1)/var['h'][:,138:].sum(axis=1))
# BGC_Argo_pH_300m_to_1000m=(((O3_pH)*h)[:,124:138].sum(axis=1)/h[:,124:138].sum(axis=1)).mean(axis=0)
ind['BGC_Argo_pH_300m_to_1000m']=(((var['O3_pH'])*var['h'])[:,124:138].sum(axis=1)/var['h'][:,124:138].sum(axis=1))
## BGC_Argo_pCO2_0m_to_300m=(((O3_pCO2)*h)[:,138:].sum(axis=1)/h[:,138:].sum(axis=1)).mean(axis=0)
#ind['BGC_Argo_pCO2_0m_to_300m']=(((var['carbonate_pCO2'])*var['h'])[:,138:].sum(axis=1)/var['h'][:,138:].sum(axis=1))
## BGC_Argo_pCO2_300m_to_1000m=(((O3_pCO2)*h)[:,124:138].sum(axis=1)/h[:,124:138].sum(axis=1)).mean(axis=0)
#ind['BGC_Argo_pCO2_300m_to_1000m']=(((var['carbonate_pCO2'])*var['h'])[:,124:138].sum(axis=1)/var['h'][:,124:138].sum(axis=1))



output=MODEL + "_BATS_ONEYEAR_OBSERVATIONS.txt"
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

