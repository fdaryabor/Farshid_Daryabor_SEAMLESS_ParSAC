#!/usr/bin/env python3
import pandas as pd
##LIST_PERIOD= 'JAN JUN'
##LIST_OBSERVABLE=' OC ARGO_CHL ARGO_NO3 ARGO_O2 ARGO_DIC ARGO_PO4 ARGO_POC '
df = pd.read_table('results_observability.txt', sep='\t') 
df.to_excel('results_observability.xlsx', 'Sheet1', index=False)
  
