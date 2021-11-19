import pickle as pkl
import numpy as np
import netCDF4 as NC4

INDIR="/g100_work/tra21_seamless/RESULTS_OBSERVABILITY/"
OUTDIR="/g100_work/tra21_seamless/RESULTS_OBSERVABILITY/"

MODEL_list=['ERGOM']
SITE_list=['BATS']
PERIOD_list=['JAN', 'JUN']
OBSERVABLE_list=['OC', 'ARGO_CHL', 'ARGO_NO3', 'ARGO_O2', 'ARGO_DIC', 'ARGO_PO4', 'ARGO_POC']
INDICATOR_list=['non-living_particulate_organic_carbon', 'trophic_efficiency', 'net_primary_production', 'pH', 'O2', 'large_over_all_phytoplankton', 'chl_max_in_5m', 'chl_max_in_10m_to_150m', 'timing_of_chl_max_in_5m', 'depth_of_chl_max_in_10m_to_150m']

Nmodel=len(MODEL_list)
Nsite=len(SITE_list)
Nperiod=len(PERIOD_list)
Nobservable=len(OBSERVABLE_list)
Nindicator=len(INDICATOR_list)

observability_array=np.zeros([Nmodel,Nsite,Nperiod,Nobservable,Nindicator])

for m,model in enumerate(MODEL_list):
    for s,site in enumerate(SITE_list):
        for p,period in enumerate(PERIOD_list):
            for o,observable in enumerate(OBSERVABLE_list):
                filein=INDIR+model+'/'+ model+'_' + site+'_observability_'+observable+'_'+period+'.analyze.pickle'
                fid=open(filein,"rb")
                indata=pkl.load(fid)
                fid.close()
                for i,indicator in enumerate(INDICATOR_list):
                    observability_array[m,s,p,o,i]=indata[indicator]['cv'][0]

output="results_observability.txt"
fid = open(output,'w')
header='MODEL\tSITE\tPERIOD\tOBSERVABLE'
for i,indicator in enumerate(INDICATOR_list):
    header += '\t' + indicator

fid.write(header)
fid.write("\n")


for m,model in enumerate(MODEL_list):
    for s,site in enumerate(SITE_list):
        for p,period in enumerate(PERIOD_list):
            for o,observable in enumerate(OBSERVABLE_list):
               fid.write(model)
               fid.write('\t')
               fid.write(site)
               fid.write('\t')
               fid.write(period)
               fid.write('\t')
               fid.write(observable)
               for i,indicator in enumerate(INDICATOR_list):
                   fid.write('\t')
                   fid.write(str(observability_array[m,s,p,o,i]))
               fid.write('\n')
fid.close()
		    	 

output="results_observability.nc"
ncOUT = NC4.Dataset(output,'w')
ncOUT.createDimension('model',Nmodel)
ncOUT.createDimension('site',Nsite)
ncOUT.createDimension('period',Nperiod)
ncOUT.createDimension('observable',Nobservable)
ncOUT.createDimension('indicator',Nindicator)
ncvar = ncOUT.createVariable('observability_result','f',('model','site','period','observable','indicator'))
ncvar[:]=observability_array
setattr(ncOUT, 'MODEL_list', MODEL_list)
setattr(ncOUT, 'SITE_list' , SITE_list)
setattr(ncOUT, 'PERIOD_list' ,PERIOD_list)
setattr(ncOUT, 'OBSERVABLE_list' ,OBSERVABLE_list)
setattr(ncOUT, 'INDICATOR_list' ,INDICATOR_list)
ncOUT.close()
