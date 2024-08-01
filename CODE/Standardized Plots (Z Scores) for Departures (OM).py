#!/usr/bin/env python
# coding: utf-8

# ## Make Standardized Maps (Z Scores)
# ### CSU REU Summer 2024 - Sarah Gryskewicz
# These will make data easier to read. </p>
# Note: A standardized anomaly, often referred to simply as a standard anomaly, is a statistical term used to express how much a particular observation deviates from the mean (average) of a dataset, in units of standard deviation. It is calculated by subtracting the mean of the dataset from the observation, and then dividing the result by the standard deviation of the dataset. </p>
# **Standard Deviation (Z-score of ±1):Indicates a typical or normal fluctuation.** </p>
# 
# **Standard Deviations (Z-score of ±2): Indicates that the observation is relatively rare compared to the normal distribution of the data.** </p>
# 
# **Standard Deviations (Z-score of ±3): Indicates that the observation is rare and may indicate outliers or events that are far outside the norm.** </p>
# ****

# In[2]:


import io
import requests
import shapefile
import shapely
import cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
import matplotlib as mplt
import matplotlib.pyplot as plt
import cartopy.io.img_tiles as cimgt
from urllib.request import urlopen, Request
from PIL import Image
from datetime import datetime, timedelta,timezone
import pytz
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import pylab as pl 
import numpy as np
from metpy.plots import USCOUNTIES
import matplotlib.ticker as mticker
import cartopy.mpl.gridliner 
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import os, sys, glob, os.path
from matplotlib import rcParams
from matplotlib import rc
rc('mathtext', default='regular') 
rcParams['font.family'] = 'Tahoma'
#rcParams['font.size'] = 14
rcParams['mathtext.fontset'] = 'cm'
rcParams['mathtext.rm'] = 'Tahoma'


# ## Import, Remove, Separate, Split

# In[4]:


df = pd.read_csv(r"C:\Users\C837388336\Desktop\REU\Data files\Massive Files\2012_2023_df.txt")
# inorganics
df.loc[df['ammNO3f_Val'] < 0, 'ammNO3f_Val']=np.nan
df.loc[df['ammSO4f_Val'] < 0, 'ammSO4f_Val']=np.nan
df.loc[df['SeaSaltf_Val'] < 0, 'SeaSaltf_Val']=np.nan

# organics
df.loc[df['OMCf_Val'] < 0, 'OMCf_Val']=np.nan
df.loc[df['ECf_Val'] < 0, 'ECf_Val']=np.nan
df.dropna(axis=0,how='any',inplace=True,ignore_index=True)


df['month']=None
df['year']=None
df['Date']=pd.to_datetime(df.Date).copy()
df['month'] = df['Date'].dt.month
df['year'] = df['Date'].dt.year

# get sitenames
sitenames=df['SiteCode'].unique()
print(sitenames)

# only use values from june and july
df = df[(df['month'] == 6) | (df['month'] == 7)]

# separate the years into 2011-2022 and 2023
df_others=df.loc[df.year != 2023].copy()
df_year=df.loc[df.year == 2023].copy()

# make df_climo by the site, month, year and state as well as take the mean of the monthly values. the year is also averaged, but it's fine
df_climo=df.groupby(['SiteCode','month']).mean(numeric_only=True)
df_climo.reset_index(inplace=True)

df_2023 = df_year.groupby(['SiteCode','month']).mean(numeric_only=True)
df_2023.reset_index(inplace = True)


# In[5]:


df.loc[(df.SiteCode == 'MOMO1') & (df.Date == '2023-06-08')]['OMCf_Val']


# ## Work with climo data & 2023 data

# In[7]:


# identify the months of interest across all sites from climatology (2018-2022)
df_climo_june = df_climo[df_climo['month'] == 6]
df_climo_july = df_climo[df_climo['month'] == 7]

# identify the months of interest across all sites from 2023
df_2023_june = df_2023[df_2023['month'] == 6]
df_2023_july = df_2023[df_2023['month'] == 7]


# In[8]:


# calculate climatological June & July standard deviations for each SiteCode
temp=df.groupby(['SiteCode','month', 'year']).mean(numeric_only=True)
temp.reset_index(inplace=True)

temp2 = temp.groupby(['SiteCode','month']).std(numeric_only=True)
temp2['climo_std']=temp2['OMCf_Val']

temp2.reset_index(inplace=True)
temp2.loc[temp2.SiteCode == 'MOMO1']['OMCf_Val']


# In[9]:


# merge 2023 values with temp std values. do this for june and july separately so that data is associated w/ the correct dates
df_2023_june=pd.merge(df_2023_june,temp2.loc[temp2['month'] == 6],left_on='SiteCode',right_on='SiteCode',how='left')
df_2023_july=pd.merge(df_2023_july,temp2.loc[temp2['month'] == 7],left_on='SiteCode',right_on='SiteCode',how='left')

df_2023_july


# In[10]:


temp.loc[(temp.SiteCode == 'MOMO1') & (temp.month == 7)]['OMCf_Val'].values.std()


# In[11]:


temp2.loc[(temp2.SiteCode == 'MOMO1') & (temp2.month == 7)]['OMCf_Val']


# In[12]:


# objects for the dataframe to work with
dataframe_2023 = df_2023_july
dataframe_climo = df_climo_july
# merge means from 2023 to climo to have a df built with the means and std values
temp2 = pd.merge(dataframe_climo, dataframe_2023, left_on='SiteCode', right_on='SiteCode')
temp2


# ## Transition to the computation
# *To do this, you need to sort through the sites and plot the june (or JA) anomalies* </p>
#    >**x = (x_2023 - x_climo) / sx** </p>
# x = standardized anomaly </p>
# x_2023 = 2023 mean for month </p>
# x_climo = climatological monthly mean </p>
# sx = climatological standard deviation 

# In[13]:


# make a new column in temp2 and a list to work with in the upcoming cells
temp2['Z'] = None
x_values = []

for i, sitename in enumerate(sitenames):
    # OMCf_Val_x = 2023 values
    x_2023 = temp2.loc[temp2.SiteCode == sitename]['OMCf_Val_x']
    # OMCf_Val = 2012-2023 avg values
    x_bar = temp2.loc[temp2.SiteCode == sitename]['OMCf_Val']
    # climo_std = standard deviations for 2012-2023
    sx = temp2.loc[temp2.SiteCode == sitename]['climo_std']

    
    # calculate z-scores
    x = ((x_2023 - x_bar) / sx )
    print('Standardized anomaly at ', sitename, ': ', x)

    # add these values to a list to then transition them into the df
    x_values.append(float(x))
temp2['Z'] = x_values


# In[14]:


avg_dev_NE = np.average(temp2['Z'])
avg_dev_NE


# ## Make a map
# Use what was just calculated (z score) to plot the anomalies by the IMPROVE colored boxes

# In[27]:


# This is a function that I found that allows me to spoof that this is not a Python script (this is to get a nice map background)
# I did not write this
def image_spoof(self, tile): # this function pretends not to be a Python script
    url = self._image_url(tile) # get the url of the street map API
    req = Request(url) # start request
    req.add_header('User-agent','Anaconda 3') # add user agent to request
    fh = urlopen(req) 
    im_data = io.BytesIO(fh.read()) # get image
    fh.close() # close url
    img = Image.open(im_data) # open image with PIL
    img = img.convert(self.desired_tile_form) # set image format
    return img, self.tileextent(tile), 'lower' # reformat for cartopy

# set map bounds
    #Transport and regular map bounds:
map_bounds = [-84, -65, 37, 48]
#map_bounds =[-92, -65, 32, 47]

streetmap='True'


# In[29]:


# change df_new depending on the month youre looking at
df_new = temp2

start_datetime=datetime.strptime("07-01-2023", "%m-%d-%Y")
end_datetime=datetime.strptime("07-01-2023", "%m-%d-%Y")

for x in range(0, 1+(end_datetime-start_datetime).days):
    plt.close('all')
    date2grab=start_datetime + timedelta(days=x)
    figure_title='2023 July OM Departures from 2012-2023 Average'

    
        # Plot the map with fire location and smoke plumes
    if (streetmap == 'True'):
     cimgt.OSM.get_image = image_spoof # reformat web request for street map spoofing
     osm_img = cimgt.OSM()             # spoofed, downloaded street map
     fig = plt.figure(figsize=(10,8))      # open matplotlib figure
     rect = fig.patch
     rect.set_facecolor("white")
     m = plt.axes(projection=osm_img.crs) # project using coordinate reference system (CRS) of street map
     extent = map_bounds
     m.set_extent(extent) # set extents
     scale = np.ceil(-np.sqrt(2)*np.log(np.divide((extent[1]-extent[0])/2.0,350.0))) # empirical solve for scale based on zoom
     scale = (scale<20) and scale or 19 # scale cannot be larger than 19
     m.add_image(osm_img, int(scale)) # add OSM with zoom specification

    else: 
     fig=plt.figure(figsize=(10,8))
     fig.set_facecolor('whitesmoke')
     rect = fig.patch
     rect.set_facecolor("white")
     m = plt.axes(projection=ccrs.PlateCarree())
     m.add_feature(cfeature.LAND)
     m.add_feature(cfeature.OCEAN, alpha=0.5)
     m.add_feature(cfeature.COASTLINE)
     m.set_extent(map_bounds, ccrs.PlateCarree()) 

    
    m.add_feature(cfeature.BORDERS)       
    m.add_feature(cfeature.STATES, linestyle=':')

    cs=m.scatter(df_new['Longitude_x'],df_new['Latitude_x'],c=df_new['Z'],marker='s',s=80,cmap='rainbow', \
              vmax=3,vmin=-1,edgecolor='black',transform=ccrs.PlateCarree(),label='IMPROVE',zorder=4)    

    
    plt.legend(loc=3)
    
    transform = ccrs.PlateCarree()._as_mpl_transform(m) # set transform for annotations
    cax,kw = mplt.colorbar.make_axes(m,location='right',pad=0.05,shrink=0.8)
    cbar = plt.colorbar(cs,cax=cax,**kw)
    cbar.ax.tick_params(axis='y', labelsize=10)
    cbar.set_label('Z-Score', fontsize=14, rotation = 0, labelpad=30)
    
    m.set_title(figure_title,fontsize=16)
    plt.show()

#fig.savefig('/Users/C837388336/Desktop/REU/Data files/Saved Plots/Maps/2012-2023 Departures/2023 July Departures OM.png')


# In[ ]:




