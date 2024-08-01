#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib as mplt
import matplotlib.pyplot as plt
from metpy.plots import USCOUNTIES
import matplotlib.ticker as mticker
from windrose import WindroseAxes
import cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.mpl.gridliner 
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import os, sys, glob, os.path
from matplotlib import rcParams
from matplotlib import rc
rc('mathtext', default='regular') 
rcParams['font.family'] = 'Tahoma'
rcParams['mathtext.fontset'] = 'cm'
rcParams['mathtext.rm'] = 'Tahoma'
# Tahoma, serif, Verdana


# In[4]:


df = pd.read_csv(r"C:\Users\C837388336\Desktop\REU\Data files\Massive Files\2018_2023_df.txt")
print(df.columns)


# In[6]:


df.loc[df['MF_Val'] < 0, 'MF_Val'] = np.nan
df.loc[df['CM_calculated_Val'] < 0, 'CM_calculated_Val'] = np.nan
df.loc[df['RCFM_Val'] < 0, 'RCFM_Val'] = np.nan

df.dropna(axis=0,how='any',inplace=True,ignore_index=True)

df['month']=None
df['year']=None
df['Date']=pd.to_datetime(df.Date).copy()
df['month'] = df['Date'].dt.month
df['year'] = df['Date'].dt.year

sitenames = df['SiteCode'].unique()
years = df['year'].unique()
months = df['month'].unique()
df_year = df.loc[df.year == 2023].copy()
df_2023 = df_year.groupby(['SiteCode', 'month', 'State']).mean(numeric_only=True)
df_2023.reset_index(inplace=True)
MF = df_2023['MF_Val'].copy()
CM = df_2023['CM_calculated_Val'].copy()
df_2023


# In[34]:


fig, axs = plt.subplots(ncols = 1, nrows = len(sitenames), figsize=(10,50))
axs = axs.flatten()
for i, sitename in enumerate(sitenames):
    ax=axs[i]
    ax.plot(months, df_2023.loc[df_2023.SiteCode == sitename]['MF_Val'], label = 'MF', marker = 'o', linestyle = '--')
    ax.set_xlabel('Month', fontsize = 10)
    ax.set_ylabel('MF (μg m$^{-3}$)', fontsize = 10)
    ax.set_xticks(months)
    ax.set_xticklabels(['June', 'July', 'August'], fontsize = 9)
    ax.grid(True)
    state = df_2023.loc[df_2023.SiteCode == sitename].iloc[0]
    ax.set_title('2023 JJA MF vs CM at %s' % sitename+ ' %s' % state['State'], fontsize=11)
    
    ax2 = ax.twinx()
    ax2.plot(months, df_2023.loc[df_2023.SiteCode == sitename]['CM_calculated_Val'], label = 'CM', marker = '<', color = 'r')
    ax2.set_ylabel('CM (μg m$^{-3}$)', fontsize = 10)
    ax2.set_ylim(1,30)
    ax.set_ylim(1,30)
 # Add legend
    lines, labels = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc='upper right')
    
plt.tight_layout()
plt.show()


# In[9]:


df_2023_new = df_2023.groupby(['month']).mean(numeric_only=True)
df_2023_new.reset_index(inplace=True)
df_2023_new


# In[12]:


fig,ax = plt.subplots(ncols=1, nrows=1, figsize=(8,4))
fig.set_facecolor('whitesmoke')

ax.plot(months, df_2023_new['MF_Val'], label = 'Fine Mass', marker = 'o', linestyle = '--')
ax.set_xlabel('Month', fontsize = 10)
ax.set_ylabel('Fine Particulate Mass (μg m$^{-3}$)', fontsize = 10)
ax.set_xticks(months, ['June', 'July', 'August'], fontsize = 9)
#plt.xticklabels(['June', 'July', 'August'], fontsize = 9)
ax.grid(True, color ='gainsboro')
ax.set_ylim(3,10)
#state = df_2023.loc[df_2023.SiteCode == sitename].iloc[0]
ax.set_title('Northeast 2023 Average JJA Fine vs Coarse Particulate Mass', fontsize=12)

ax2 = ax.twinx()
ax2.plot(months, df_2023_new['CM_calculated_Val'], label = 'Coarse Mass', marker = 'x', color = 'r')
ax2.set_ylabel('Coarse Particulate Mass (μg m$^{-3}$)', fontsize = 10)
ax2.set_ylim(3,10)
# Add legend
lines, labels = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper right')


plt.tight_layout()
plt.show()


# ## MF vs RCFM

# In[4]:


dates = df['Date'].unique()
start_date = pd.to_datetime('2023-06-05')
end_date = pd.to_datetime('2023-06-11')
x = '2023-06-06'
y = '2023-06-09'
#June: 
sites_non = ['PACK1', 'LYEB1', 'LOND1', 'GRGU1', 'CABA1', 'MOOS1', 'PRIS1', 'PENO1', 'ACAD1']
# July:
#sites_non = ['BRIG1', 'LOND1', 'MOOS1', 'PRIS1', 'PENO1', 'ACAD1', 'EGBE1']

# Filtering out rows where SiteCode is in sites_non
df = df[~df['SiteCode'].isin(sites_non)]
sitenames = df['SiteCode'].unique()
# 30,13 (june)
# 15,13 (july)
fig, axs = plt.subplots(ncols = 2, nrows = ((len(sitenames)+1)//2), figsize=(15,13))
fig.set_facecolor("whitesmoke")
axs=axs.flatten()
for j, sitename in enumerate(sitenames):
    data = df.loc[df.SiteCode == sitename]
    
    # Calculate cumulative heights for stacking bars
    MF = data['MF_Val'].values
    RCFM = data['RCFM_Val'].values
    state = data['State'].iloc[0]
    
    #axs[j].set_facecolor('snow')
    axs[j].plot(data['Date'], data['MF_Val'], label='MF', color='purple', alpha=0.6)
    axs[j].plot(data['Date'], data['RCFM_Val'], label='RCFM', linestyle = '--')
   
    axs[j].legend(loc='upper left')
    axs[j].set_ylabel('μg m$^{-3}$', fontsize = 10, rotation = 0, labelpad = 15)
    axs[j].set_xlabel('Date', fontsize = 10)
    axs[j].set_xticks(dates)
    axs[j].set_xlim(start_date,end_date)
    axs[j].set_title('5-11 June 2023 Species Composition at %s, %s' % (sitename,state), fontsize=20)
    axs[j].set_xlim(start_date,end_date)
    axs[j].axvspan(x, y, facecolor='slategrey', alpha=0.3)

plt.tight_layout()
plt.show()
fig.savefig('/Users/C837388336/Desktop/REU/Data files/Saved Plots/MF vs RCFM (june).png')


# In[ ]:





# In[ ]:




