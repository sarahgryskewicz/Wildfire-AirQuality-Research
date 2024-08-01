#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import pylab as pl 
import numpy as np
import matplotlib as mplt
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib import rc
rc('mathtext', default='regular') 
rcParams['font.family'] = 'Tahoma'
rcParams['mathtext.fontset'] = 'cm'
rcParams['mathtext.rm'] = 'Tahoma'

df = pd.read_csv(r"C:\Users\C837388336\Desktop\REU\Data files\Massive Files\2018_2023_df.txt")
df['month']=None
df['year']=None
df['Date']=pd.to_datetime(df.Date).copy()
df['month'] = df['Date'].dt.month
df['year'] = df['Date'].dt.year
sitenames=df['SiteCode'].unique()

df.loc[df.OMCf_Val < 0, 'OMCf_Val']=np.nan
df.loc[df.ECf_Val < 0, 'ECf_Val']=np.nan
df.loc[df.ammSO4f_Val < 0, 'ammSO4f_Val']=np.nan
df.loc[df.SOILf_Val < 0, 'SOILf_Val']=np.nan
df.loc[df.SeaSaltf_Val < 0, 'SeaSaltf_Val']=np.nan
df.loc[df.ammNO3f_Val < 0, 'ammNO3f_Val']=np.nan
df.dropna(axis=0,how='any',inplace=True,ignore_index=True)


df_others = df.loc[df.year == 2023].copy()
df_2023 = df_others.groupby(['SiteCode','Date','State']).mean(numeric_only=True)
df_2023.reset_index(inplace = True)
df_2023

###########
# Mass fractions: How much of air was OM compared to other species?
df_totalOM = df_2023.groupby(['SiteCode','Date', 'OMCf_Val', 'ECf_Val', 'ammNO3f_Val', 'SOILf_Val','SeaSaltf_Val', 'RCFM_Val']).mean(numeric_only=True).copy()
df_totalOM.reset_index(inplace=True)
df_totalOM = df_totalOM[df_totalOM.month != 8]

# Get mass fractions
df_totalOM['OM'] = (df_totalOM['OMCf_Val']/df_totalOM['RCFM_Val']) 
df_totalOM['EC'] = (df_totalOM['ECf_Val']/df_totalOM['RCFM_Val']) 
df_totalOM['AS'] = (df_totalOM['ammSO4f_Val']/df_totalOM['RCFM_Val']) 
df_totalOM['AN'] = (df_totalOM['ammNO3f_Val']/df_totalOM['RCFM_Val']) 
df_totalOM['SS'] = (df_totalOM['SeaSaltf_Val']/df_totalOM['RCFM_Val']) 
df_totalOM['SOIL'] = (df_totalOM['SOILf_Val']/df_totalOM['RCFM_Val']) 

d = df_totalOM.groupby(['Date']).mean(numeric_only=True)
d.reset_index(inplace=True)
# Example: How much was OM attributable to in the RCFM?
d.loc[d.Date == '2023-06-08']['OM']

fig = plt.figure(figsize = (10,5))
fig.set_facecolor('whitesmoke')

start = pd.to_datetime('2023-07-13')
end = pd.to_datetime('2023-07-18')
plt.bar(d['Date'], d['AS'], width = 2, color='yellow', label='Ammonium Sulfate')
plt.bar(d['Date'],  d['AN'], width = 2, color='red', label='Ammonium Nitrate', bottom=d['AS'])
plt.bar(d['Date'],  d['OM'],width = 2, color='green', label='Organic Mass', bottom=d['AS'] + d['AN'])
plt.bar(d['Date'],  d['EC'],width = 2, color='black', label='Elemental Carbon', bottom=d['AS'] + d['AN'] + d['OM'])
plt.bar(d['Date'], d['SOIL'], width =2,color='brown', label='Dust', bottom=d['AS'] + d['AN'] + d['OM'] + d['EC'])
plt.bar(d['Date'],  d['SS'], width = 2,color='blue', label='Sea Salt', bottom=d['AS'] + d['AN'] + d['OM'] + d['EC'] + d['SOIL'])

plt.xticks(d['Date'], fontsize=13)
plt.xlim(start,end)
plt.ylabel('Mass Fraction', fontsize = 15, rotation = 0, labelpad=40)
plt.xlabel('Date', fontsize = 15)
plt.title('14-17 July 2023 PM$_{2.5}$ Mass Fractions Across the Northeast', fontsize=20)
#plt.title('17 July 2023 Species Loadings Across the Northeast', fontsize=15)
#fig.savefig('/Users/Desktop/REU/Saved Plots/Concentrations/impactsites_loadings_17july.png')


# In[ ]:




