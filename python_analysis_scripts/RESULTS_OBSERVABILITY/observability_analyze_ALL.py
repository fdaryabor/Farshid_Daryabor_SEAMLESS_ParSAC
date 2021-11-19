import pickle as pkl
import numpy as np
import netCDF4 as NC4

INDIR="/g100_work/tra21_seamless/RESULTS_OBSERVABILITY/"
OUTDIR="/g100_work/tra21_seamless/RESULTS_OBSERVABILITY/"

MODEL_list=['PISCES','ECOSMO','ERGOM','BFM','ERSEM']
SITE_list=['BATS','L4']
PERIOD_listBATS=['JAN', 'JUN']
PERIOD_listL4=['NOV', 'JUN']
OBSERVABLE_list=['ARGO_NO3', 'ARGO_PO4','OC', 'ARGO_CHL', 'ARGO_POC', 'ARGO_O2', 'ARGO_DIC']
INDICATOR_list=['chl_max_in_5m', 'chl_max_in_10m_to_150m', 'depth_of_chl_max_in_10m_to_150m','timing_of_chl_max_in_5m','net_primary_production','large_over_all_phytoplankton','trophic_efficiency','non-living_particulate_organic_carbon','O2','pH' ]


Nmodel=len(MODEL_list)
Nsite=len(SITE_list)
Nperiod=len(PERIOD_listBATS)
Nobservable=len(OBSERVABLE_list)
Nindicator=len(INDICATOR_list)

observability_array=np.zeros([Nmodel,Nsite,Nperiod,Nobservable,Nindicator])

for m,model in enumerate(MODEL_list):
    for s,site in enumerate(SITE_list):
        if site == 'BATS': 
          PERIOD_list= PERIOD_listBATS
        elif site == 'L4':
          PERIOD_list= PERIOD_listL4
        for p,period in enumerate(PERIOD_list):
            for o,observable in enumerate(OBSERVABLE_list):
                filein=INDIR+model+'/'+ model+'_' + site+'_observability_'+observable+'_'+period+'.analyze.pickle'
                fid=open(filein,"rb")
                indata=pkl.load(fid)
                fid.close()
                for i,indicator in enumerate(INDICATOR_list):
                    observability_array[m,s,p,o,i]=indata[indicator]['cv'][0]

output="results_observability_ALL.txt"
fid = open(output,'w')
header='MODEL\tSITE\tPERIOD\tOBSERVABLE'
for i,indicator in enumerate(INDICATOR_list):
    header += '\t' + indicator

fid.write(header)
fid.write("\n")


for m,model in enumerate(MODEL_list):
    for s,site in enumerate(SITE_list):
        if site == 'BATS': 
          PERIOD_list= PERIOD_listBATS
        elif site == 'L4':
          PERIOD_list= PERIOD_listL4
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
		    	 

output="results_observability_ALL.nc"
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
