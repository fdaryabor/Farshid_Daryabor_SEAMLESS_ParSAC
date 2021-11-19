import argparse
def argument():
    parser = argparse.ArgumentParser(description = '''
    Prepare .txt table of indicator time series based on results.nc from gotm
    ''',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(   '--site', '-s',
                                type = str,
                                required = True,
                                help = ''' name of the site (e.g. BATS, L4) '''

                                )

    parser.add_argument(   '--indir', '-i',
                                type = str,
                                required = True,
                                help = ''' indir with .txt file '''

                                )

    return parser.parse_args()

args = argument()


import os,sys
import netCDF4 as NC4
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import matplotlib.dates as mdates
import datetime 
import pandas as pd

SITE = args.site
MODEL_list = ['BFM','PISCES','ERGOM','ERSEM']#,'ECOSMO']
MODEL_list = ['BFM','PISCES','ERGOM','ERSEM','ECOSMO']
INDIR = args.indir


DICTind = {
    'BATS': [#'non-living_particulate_organic_carbon',
          'trophic_efficiency',
#          'net_primary_production',
          'pH',
          'O2',
          'large_over_all_phytoplankton',
#          'chl_in_5m',
#          'chl_max_in_10m_to_150m',
          'depth_of_chl_max_in_10m_to_150m'],
    'L4':  [#'non-living_particulate_organic_carbon',
          'trophic_efficiency',
#          'net_primary_production',
          'pH',
          'O2',
          'large_over_all_phytoplankton',
#          'chl_in_5m',
#          'chl_max_in_10m_to_50m',
          'depth_of_chl_max_in_10m_to_50m']
}


list_ind = DICTind[SITE]

DICTunits = {
    'non-living_particulate_organic_carbon': '[$mgC/m^3$]',
    'trophic_efficiency'                   : '[]',
    'net_primary_production'               : '[$mgC/m^2/d$]',
    'pH'                                   : '[$total scale$]',
    'O2'                                   : '[$mmolO2/m^3$]',
    'large_over_all_phytoplankton'         : '[]',
    'chl_in_5m'                            : '[$mgChl/m^3$]',
    'chl_max_in_10m_to_150m'               : '[$mgChl/m^3$]',
    'chl_max_in_10m_to_50m'                : '[$mgChl/m^3$]',
    'depth_of_chl_max_in_10m_to_150m'      : '[$m$]',
    'depth_of_chl_max_in_10m_to_50m'       : '[$m$]',
}


plt.close('All')


for MODEL in MODEL_list:
    infile = INDIR + '/' + MODEL +'/' + MODEL + '_' + SITE + '_ONEYEAR_INDICATORS.txt'
    df = pd.read_csv(infile, delimiter="\t",skiprows = 0, engine='python')
    df['model']=MODEL
    
    if MODEL == MODEL_list[0]:
        dfall = df
    else:
        dfall = pd.concat([dfall,df])
    df=dfall


years = mdates.YearLocator()   # every year
months = mdates.MonthLocator()  # every month
yearsFmt = mdates.DateFormatter('%Y')
monthsFmt = mdates.DateFormatter('%Y %m')

for i,ind in enumerate(list_ind):
    fig,ax = plt.subplots(1,1)
    fig.set_size_inches(10,10)

    for MODEL in MODEL_list:
        
        print(MODEL)
        dfmod=df[df['model']==MODEL]

        dates=dfmod['DATE'].values
        yyyymmdd=[]
        for datestr in dates :
            yyyymmdd.append(datetime.datetime.strptime(datestr, "%Y-%m-%d %H:%M:%S"))
        print(len(dates))

        y=dfmod[ind].values
        ax.plot( yyyymmdd,y, label=MODEL)

    plt.legend()
    ax.set_title(ind + ' ALL ' + SITE +' ' + DICTunits[ind])


    # format the ticks
    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_major_formatter(monthsFmt)
#   ax.xaxis.set_minor_locator(months)

    datemin = yyyymmdd[0]
    datemax = yyyymmdd[-1]
    ax.set_xlim(datemin, datemax)
    ax.grid('both')
    fig.autofmt_xdate()


    fileout = 'ALL' + '_' + SITE + '_oneyear_' + ind +'.png'
    fig.savefig(fileout, format='png',dpi=150)
