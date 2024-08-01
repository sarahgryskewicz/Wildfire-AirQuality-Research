#!/usr/bin/env python
# coding: utf-8

# # Using Multiple sites to make Boxplots for Daily Aerosol Concentrations, Monthly Averages, and NE Site Locations
# ### CSU REU Summer 2024 - by Sarah Gryskewicz
# *This notebook will be essential to discovering various IMPROVE sites' daily concentrations and monthly averages of these observed aerosol species*
# *over a timeframe of interest. These plots will be printed both individually and on one figure. Additionally, mapping of the site location will be included to give others perspective on where these IMPROVE sites are located.* </p>
# ***

# *In the following cell, we will import a series of environments and packages that will allow us to interact with the collected data.*

# In[1]:


import pandas as pd
import pylab as pl 
import numpy as np
import matplotlib as mplt
import matplotlib.pyplot as plt
from metpy.plots import USCOUNTIES
import matplotlib.ticker as mticker
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


# * Now, the directory will be read to access the data.

# In[3]:


df = pd.read_csv(r"C:\Users\C837388336\Desktop\REU\Data files\Massive Files\2018_2023_df_NEW.txt")
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


# ## One figure, subplots
# * Now it is time to make a few plots on one figure using subplots

# In[4]:


dates = df_2023['Date'].unique()
dates
sitenames


# In[33]:


fig, axs = plt.subplots(ncols=1,nrows=len(sitenames), figsize=(10,70))
fig.set_facecolor("whitesmoke")
axs=axs.flatten()

start_date = pd.to_datetime('2023-07-13')
end_date = pd.to_datetime('2023-07-18')

for j, sitename in enumerate(sitenames):
    
    #df_2023.dropna(axis=0,how='any',inplace=True,ignore_index=True)
     # Filter data for the current sitename
    data = df_2023.loc[df_2023.SiteCode == sitename]
    
    # Calculate cumulative heights for stacking bars
    ammSO4f = data['ammSO4f_Val'].values
    ammNO3f = data['ammNO3f_Val'].values
    OMCf = data['OMCf_Val'].values
    ECf = data['ECf_Val'].values
    soilf = data['SOILf_Val'].values
    state = data['State'].iloc[0] 
    
    axs[j].set_facecolor('snow')
    axs[j].bar(data['Date'], data['ammSO4f_Val'], width = 2.9, color='yellow', label='Ammonium Sulfate')
    axs[j].bar(data['Date'], data['ammNO3f_Val'], width = 2.9, color='red', label='Ammonium Nitrate', bottom=ammSO4f)
    axs[j].bar(data['Date'], data['OMCf_Val'],width = 2.9, color='green', label='Organic Mass', bottom=ammSO4f + ammNO3f)
    axs[j].bar(data['Date'], data['ECf_Val'],width = 2.9, color='black', label='Elemental Carbon', bottom=ammSO4f + ammNO3f + OMCf)
    axs[j].bar(data['Date'], data['SOILf_Val'], width = 2.9,color='brown', label='Dust', bottom=ammSO4f + ammNO3f + OMCf + ECf)
    axs[j].bar(data['Date'], data['SeaSaltf_Val'], width = 2.9,color='blue', label='Sea Salt', bottom=ammSO4f + ammNO3f + OMCf + ECf + soilf)
    axs[j].legend(loc='upper left')
    axs[j].set_ylabel('μg m$^{-3}$', fontsize = 20, rotation = 0, labelpad = 40)
    axs[j].set_xlabel('Date', fontsize = 20)
    axs[j].set_title('14-17 July 2023 Species Composition at %s, %s' % (sitename,state), fontsize=25)
    axs[j].set_xticks(dates)  # Set the positions of the x ticks
    axs[j].set_xlim(start_date, end_date)  # Set the limits of the x axis
    axs[j].tick_params(axis='x', labelsize=15)  # Set the font size of x tick labels
    axs[j].tick_params(axis='y', labelsize=15)  # Set the font size of y tick labels
    axs[j].set_ylim(0,20)

plt.tight_layout()
plt.show()


# ## Monthly Averages
# * Now it is time to plot the average concentrations for these months at these sites.

# In[115]:


fig, axs = plt.subplots(ncols=1,nrows=len(sitenames), figsize=(15,85))
fig.set_facecolor("whitesmoke")
axs=axs.flatten()
plt.subplots_adjust(hspace=0.35)
df_monthmean=df_2023.groupby(['SiteCode','State','month']).mean(numeric_only=True)
df_monthmean.reset_index(inplace=True)

for j, sitename in enumerate(sitenames):
    df['month']=None
    df['Date'] = pd.to_datetime(df.Date).copy()  
    df['month']=df['Date'].dt.month

    data = df_monthmean.loc[df_monthmean.SiteCode == sitename]
    SO4f = data['ammSO4f_Val'].values
    NO3f = data['ammNO3f_Val'].values
    O = data['OMCf_Val'].values
    E = data['ECf_Val'].values
    soil = data['SOILf_Val'].values
    month = data['month'].unique()
    state = data['State'].iloc[0]
    axs[j].set_facecolor('snow')
    axs[j].bar(data['month'], data['ammSO4f_Val'], color = 'yellow',  label = 'Ammonium Sulfate')
    axs[j].bar(data['month'], data['ammNO3f_Val'], color = 'red',  label = 'Ammonium Nitrate', bottom=SO4f)
    axs[j].bar(data['month'], data['OMCf_Val'], color = 'green', label = 'Organic Mass', bottom=(SO4f + NO3f))
    axs[j].bar(data['month'], data['ECf_Val'], color = 'black',  label = 'Elemental Carbon', bottom=(SO4f + NO3f + O))
    axs[j].bar(data['month'], data['SOILf_Val'], color = 'brown', label = 'Dust', bottom=(SO4f + NO3f + O + E))
    axs[j].bar(data['month'], data['SeaSaltf_Val'], color = 'blue',  label = 'Sea Salt', bottom=(SO4f + NO3f + O + E + soil))
    #plt.xticks(rotation=-37)
    axs[j].set_title('JJA 2023 Average Species Composition at %s, %s' % (sitename, state), fontsize = 15)    
    axs[j].legend(loc='upper right')
    axs[j].set_ylabel('μg m$^{-3}$', fontsize = 15)
    axs[j].set_xlabel('Month', fontsize =15)
    axs[j].set_xticks(month)
    axs[j].set_xticklabels(['June','July','August'])
    fig.savefig('/Users/C837388336/Desktop/REU/Data files/Saved Plots/Using_Multiple_Sites_Average.png')


# ## Average NE Concentrations

# In[92]:


df_regional_avg = df_others.groupby(['month']).mean(numeric_only=True)
df_regional_avg.reset_index(inplace=True)
df_regional_avg


# In[107]:


months = df_regional_avg['month'].unique()

fig = plt.figure(figsize=(5,3))
fig.set_facecolor("whitesmoke")

SO4f = df_regional_avg['ammSO4f_Val'].values
NO3f = df_regional_avg['ammNO3f_Val'].values
O = df_regional_avg['OMCf_Val'].values
E = df_regional_avg['ECf_Val'].values
soil = df_regional_avg['SOILf_Val'].values

plt.bar(df_regional_avg['month'], df_regional_avg['ammSO4f_Val'], color = 'yellow',  label = 'Ammonium Sulfate')
plt.bar(df_regional_avg['month'], df_regional_avg['ammNO3f_Val'], color = 'red',  label = 'Ammonium Nitrate', bottom=SO4f)
plt.bar(df_regional_avg['month'], df_regional_avg['OMCf_Val'], color = 'green', label = 'Organic Mass', bottom=(SO4f + NO3f))
plt.bar(df_regional_avg['month'], df_regional_avg['ECf_Val'], color = 'black',  label = 'Elemental Carbon', bottom=(SO4f + NO3f + O))
plt.bar(df_regional_avg['month'], df_regional_avg['SOILf_Val'], color = 'brown', label = 'Dust', bottom=(SO4f + NO3f + O + E))
plt.bar(df_regional_avg['month'], df_regional_avg['SeaSaltf_Val'], color = 'blue',  label = 'Sea Salt', bottom=(SO4f + NO3f + O + E + soil))

plt.title('Northeast 2023 JJA Average Species Concentrations', fontsize=13)
plt.ylabel('μg m$^{-3}$', fontsize = 10, rotation = 0, labelpad=20)
plt.xticks(months,['June','July','August'], fontsize=10)
fig.savefig('/Users/C837388336/Desktop/REU/Data files/Saved Plots/Concentrations/Northeast_JJA_Avg.png')


# ## 2022 Vs 2023

# In[95]:


fig, axs = plt.subplots(nrows=1,ncols=2, figsize=(10,5))

fig.set_facecolor('whitesmoke')
#subplot_titles=['AOD 550 Land Mean', 'AOD 550 Max','AOD 550 Min', 'AOD STD', 'Angstrom Exponent','Angstrom Exp Land Mean','Angstrom Exponent STD']
axs=axs.flatten()
# Loop over the figures
for i in range (0,2):
        if (i==0):
            df_other = df.loc[df.year == 2022].copy()
            df_ot = df_other.groupby(['SiteCode','Date','State']).mean(numeric_only=True)
            df_ot.reset_index(inplace = True)
            
            df_w = df_ot.groupby(['month']).mean(numeric_only=True)
            df_w.reset_index(inplace=True)
            df_w
            
            months = df_w['month'].unique()
                        
            SO4f = df_w['ammSO4f_Val'].values
            NO3f = df_w['ammNO3f_Val'].values
            O = df_w['OMCf_Val'].values
            E = df_w['ECf_Val'].values
            soil = df_w['SOILf_Val'].values
            ax=axs[i]
            ax.bar(df_w['month'], df_w['ammSO4f_Val'], color = 'yellow',  label = 'Ammonium Sulfate')
            ax.bar(df_w['month'], df_w['ammNO3f_Val'], color = 'red',  label = 'Ammonium Nitrate', bottom=SO4f)
            ax.bar(df_w['month'], df_w['OMCf_Val'], color = 'green', label = 'Organic Mass', bottom=(SO4f + NO3f))
            ax.bar(df_w['month'], df_w['ECf_Val'], color = 'black',  label = 'Elemental Carbon', bottom=(SO4f + NO3f + O))
            ax.bar(df_w['month'], df_w['SOILf_Val'], color = 'brown', label = 'Dust', bottom=(SO4f + NO3f + O + E))
            ax.bar(df_w['month'], df_w['SeaSaltf_Val'], color = 'blue',  label = 'Sea Salt', bottom=(SO4f + NO3f + O + E + soil))
            
            ax.set_title('Northeast 2022 JJA Average Species Concentrations', fontsize=12)
            ax.set_ylabel('μg m$^{-3}$', fontsize = 10)
            ax.set_xticks(months,['June','July','August'], fontsize=10) 
            ax.set_ylim(0,7.5)
        elif (i==1):
            months = df_regional_avg['month'].unique()
                        
            SO4f = df_regional_avg['ammSO4f_Val'].values
            NO3f = df_regional_avg['ammNO3f_Val'].values
            O = df_regional_avg['OMCf_Val'].values
            E = df_regional_avg['ECf_Val'].values
            soil = df_regional_avg['SOILf_Val'].values
            ax=axs[i]
            ax.bar(df_regional_avg['month'], df_regional_avg['ammSO4f_Val'], color = 'yellow',  label = 'Ammonium Sulfate')
            ax.bar(df_regional_avg['month'], df_regional_avg['ammNO3f_Val'], color = 'red',  label = 'Ammonium Nitrate', bottom=SO4f)
            ax.bar(df_regional_avg['month'], df_regional_avg['OMCf_Val'], color = 'green', label = 'Organic Mass', bottom=(SO4f + NO3f))
            ax.bar(df_regional_avg['month'], df_regional_avg['ECf_Val'], color = 'black',  label = 'Elemental Carbon', bottom=(SO4f + NO3f + O))
            ax.bar(df_regional_avg['month'], df_regional_avg['SOILf_Val'], color = 'brown', label = 'Dust', bottom=(SO4f + NO3f + O + E))
            ax.bar(df_regional_avg['month'], df_regional_avg['SeaSaltf_Val'], color = 'blue',  label = 'Sea Salt', bottom=(SO4f + NO3f + O + E + soil))
            
            ax.set_title('Northeast 2023 JJA Average Species Concentrations', fontsize=12)
            ax.set_ylabel('μg m$^{-3}$', fontsize = 10)
            ax.set_xticks(months,['June','July','August'], fontsize=10)
            ax.set_ylim(0,7.5)


# ## Make time series

# In[99]:


df_non = df.loc[df.year != 2023].copy()
df_5 = df_non.groupby(['month']).mean(numeric_only=True)
df_5.reset_index(inplace=True)
df_5


# In[103]:


fig, axs = plt.subplots(ncols=1,nrows=1,figsize=(10,5))
fig.set_facecolor('whitesmoke')
axs.plot(df_5['month'], df_5['OMCf_Val'], color = 'g', linestyle='--', alpha=0.5, marker='.',label = '2018-2022')
axs.set_ylim(1,6)
axs.set_xticks(months)
axs.set_facecolor('snow')
axs.set_xticklabels(['June','July','August'])
axs.set_title('Northeast 2018-2022 vs 2023 Average OM Concentrations',fontsize=14)
ax = axs.twinx()
ax.plot(df_regional_avg['month'], df_regional_avg['OMCf_Val'], color = 'b',  marker ='.', label = '2023')
ax.set_ylim(1,6)
ax.set_ylabel('μg m$^{-3}$', fontsize = 12)
axs.set_ylabel('μg m$^{-3}$', fontsize = 12, rotation = 0, labelpad = 30)

ax.grid(True, color='gainsboro')
lines, labels = axs.get_legend_handles_labels()
lines2, labels2 = ax.get_legend_handles_labels()
ax.legend(lines + lines2, labels + labels2, loc='upper right')


# In[25]:


dfts = df.loc[df.month != 8].copy()
dfts.reset_index(inplace=True)
dfts


# In[27]:


ts = dfts.groupby(['year']).mean(numeric_only=True)
ts.reset_index(inplace=True)
ts['OMCf_Val']


# In[29]:


fig = plt.figure(figsize=(10,4), dpi=500)
plt.plot(ts['year'], ts['OMCf_Val'],color='g', marker='.',label='Average OM 2018-2023')
fig.set_facecolor('whitesmoke')
plt.grid(True, color='gainsboro')
plt.ylabel('OM (μg m$^{-3}$)', fontsize = 12, rotation = 0, labelpad = 35)
plt.xlabel('Year', fontsize=12)
plt.ylim(2,5.5)
years = ts['year'].unique()
plt.xticks(years)
plt.legend(loc='upper left')
plt.title('Yearly June & July Northeast Average Organic Mass from 2018 - 2023', fontsize = 14)
fig.savefig('/Users/C837388336/Desktop/REU/Data files/Saved Plots/Concentrations/Northeast_JJ_yearly_Avg.png')


# ## How much of air was OM compared to other species

# In[36]:


df_totalOM = df_2023.groupby(['SiteCode','Date', 'OMCf_Val', 'ECf_Val', 'ammNO3f_Val', 'SOILf_Val','SeaSaltf_Val', 'RCFM_Val']).mean(numeric_only=True).copy()
df_totalOM.reset_index(inplace=True)
df_totalOM = df_totalOM[df_totalOM.month != 8]

df_totalOM['OM'] = (df_totalOM['OMCf_Val']/df_totalOM['RCFM_Val']) 
df_totalOM['EC'] = (df_totalOM['ECf_Val']/df_totalOM['RCFM_Val']) 
df_totalOM['AS'] = (df_totalOM['ammSO4f_Val']/df_totalOM['RCFM_Val']) 
df_totalOM['AN'] = (df_totalOM['ammNO3f_Val']/df_totalOM['RCFM_Val']) 
df_totalOM['SS'] = (df_totalOM['SeaSaltf_Val']/df_totalOM['RCFM_Val']) 
df_totalOM['SOIL'] = (df_totalOM['SOILf_Val']/df_totalOM['RCFM_Val']) 

df_totalOM


# In[38]:


df_totalOM['SiteCode'].unique()


# In[40]:


d = df_totalOM.groupby(['Date']).mean(numeric_only=True)
d.reset_index(inplace=True)
d


# In[64]:


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
#fig.savefig('/Users/C837388336/Desktop/REU/Data files/Saved Plots/Concentrations/impactsites_loadings_17july.png')


# In[62]:


d.loc[d.Date == '2023-06-08']['OM']


# In[ ]:





# In[39]:


fig = plt.figure(figsize=(20,10))
fig.set_facecolor("whitesmoke")

start_date = pd.to_datetime('2023-07-13')
end_date = pd.to_datetime('2023-07-18')
data = df_2023.loc[df_2023.SiteCode == 'MOMO1']
dates = df_2023.loc[df_2023.month !=8]
dates = df_2023['Date'].unique()
# Calculate cumulative heights for stacking bars
ammSO4f = data['ammSO4f_Val'].values
ammNO3f = data['ammNO3f_Val'].values
OMCf = data['OMCf_Val'].values
ECf = data['ECf_Val'].values
soilf = data['SOILf_Val'].values
state = data['State'].iloc[0] 

plt.bar(data['Date'], data['ammSO4f_Val'], width = 2.9, color='yellow', label='Ammonium Sulfate')
plt.bar(data['Date'], data['ammNO3f_Val'], width = 2.9, color='red', label='Ammonium Nitrate', bottom=ammSO4f)
plt.bar(data['Date'], data['OMCf_Val'],width = 2.9, color='green', label='Organic Mass', bottom=ammSO4f + ammNO3f)
plt.bar(data['Date'], data['ECf_Val'],width = 2.9, color='black', label='Elemental Carbon', bottom=ammSO4f + ammNO3f + OMCf)
plt.bar(data['Date'], data['SOILf_Val'], width = 2.9,color='brown', label='Dust', bottom=ammSO4f + ammNO3f + OMCf + ECf)
plt.bar(data['Date'], data['SeaSaltf_Val'], width = 2.9,color='blue', label='Sea Salt', bottom=ammSO4f + ammNO3f + OMCf + ECf + soilf)
#plt.plot(data['Date'], data['RCFM_Val'], color = 'purple',label='RCFM', linestyle = '--', linewidth=6)
plt.legend(loc='upper left', fontsize=20)
plt.ylabel('μg m$^{-3}$', fontsize = 35, rotation = 0, labelpad = 75)
plt.xlabel('Date', fontsize = 35)
plt.title('July 2023 Species Composition at MOMO1, CT', fontsize=45)
plt.xticks(dates,fontsize=30)
plt.yticks(fontsize=30)
plt.xlim(start_date,end_date)
#axs[j].set_ylim(0,35)

plt.tight_layout()
plt.show()


# In[ ]:





# In[ ]:




