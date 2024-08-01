# # Using Multiple sites to make Boxplots for Daily Aerosol Concentrations, Monthly Averages, and NE Site Locations

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

# Read in data
df = pd.read_csv(r"C:\Users\Desktop\REU\Data\2018_2023_df_NEW.txt")
df['month']=None
df['year']=None
df['Date']=pd.to_datetime(df.Date).copy()
df['month'] = df['Date'].dt.month
df['year'] = df['Date'].dt.year
sitenames=df['SiteCode'].unique()

# Find where species are less than 0 in value (not valid data) and drop the sample day that has this data (not a valid sample day)
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

######################
# Plot on one figure: Subplots
dates = df_2023['Date'].unique()

fig, axs = plt.subplots(ncols=1,nrows=len(sitenames), figsize=(10,70))
fig.set_facecolor("whitesmoke")
axs=axs.flatten()

start_date = pd.to_datetime('2023-07-13')
end_date = pd.to_datetime('2023-07-18')

for j, sitename in enumerate(sitenames):
     # Filter data for the current sitename
    data = df_2023.loc[df_2023.SiteCode == sitename]
    
    # Get species for plot
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


######################
# Monthly averages: Now it is time to plot the average concentrations for these months at these sites.
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
    fig.savefig('/Users/Desktop/REU/Data/Saved Plots/Using_Multiple_Sites_Average.png')

######################
# Plot the average Northeast concentrations during JJA
df_regional_avg = df_others.groupby(['month']).mean(numeric_only=True)
df_regional_avg.reset_index(inplace=True)
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
fig.savefig('/Users/Desktop/REU/Saved Plots/Concentrations/Northeast_JJA_Avg.png')



######################
# Make time series of average OM over JJA
df_non = df.loc[df.year != 2023].copy()
df_5 = df_non.groupby(['month']).mean(numeric_only=True)
df_5.reset_index(inplace=True)
df_5

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

# USE the above code to now plot June & July averages for each year in the dataframe
dfts = df.loc[df.month != 8].copy()
dfts.reset_index(inplace=True)

ts = dfts.groupby(['year']).mean(numeric_only=True)
ts.reset_index(inplace=True)


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




