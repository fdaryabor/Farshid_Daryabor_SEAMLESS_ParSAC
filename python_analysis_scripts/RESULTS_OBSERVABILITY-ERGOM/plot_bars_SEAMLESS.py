from matplotlib import pyplot as plt
import pickle as pkl
import numpy as np
import netCDF4 as NC4

INDIR="/g100_work/tra21_seamless/RESULTS_OBSERVABILITY/"
#OUTDIR="/g100_work/tra21_seamless/RESULTS_OBSERVABILITY/"

MODEL_list=['ERGOM']
SITE_list=['Arkona']
PERIOD_list=['JAN', 'JUN']
OBSERVABLE_list=['OC', 'ARGO_CHL', 'ARGO_NO3', 'ARGO_O2', 'ARGO_DIC', 'ARGO_PO4', 'ARGO_POC']
INDICATOR_list=['non-living_particulate_organic_carbon', 'trophic_efficiency', 'net_primary_production', 'pH', 'O2', 'large_over_all_phytoplankton', 'chl_max_in_5m', 'chl_max_in_10m_to_150m', 'timing_of_chl_max_in_5m', 'depth_of_chl_max_in_10m_to_150m']

Nmodel=len(MODEL_list)
Nsite=len(SITE_list)
Nperiod=len(PERIOD_list)
Nobservable=len(OBSERVABLE_list)
Nindicator=len(INDICATOR_list)

output_dir="./output_plots/Arkona/barplots/"

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





X = np.arange(7)

ind=0

font=8

for indicator in INDICATOR_list:

    print(indicator)

    fig, ax = plt.subplots(figsize=(8, 5))
#    ax = fig.add_axes([0,0,1,1])
    ax.set_title(indicator)
    ax.bar(X + 0.00, observability_array[0,0,0,:,ind], color = 'b', width = 0.25, label="JAN")
    ax.bar(X + 0.25, observability_array[0,0,1,:,ind], color = 'g', width = 0.25, label="JUN")
    ax.set_xticks([0., 1., 2., 3., 4., 5., 6.])
    ax.set_xticklabels(OBSERVABLE_list, fontsize=font)
    plt.legend()
    fig.savefig(output_dir + indicator + ".png", dpi=150)

    ind+=1
