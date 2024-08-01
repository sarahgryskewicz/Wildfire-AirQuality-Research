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
from netCDF4 import Dataset 
from matplotlib import rcParams
from matplotlib import rc
rc('mathtext', default='regular') 
rcParams['font.family'] = 'Tahoma'
rcParams['mathtext.fontset'] = 'cm'
rcParams['mathtext.rm'] = 'Tahoma'

## Access the IMPROVE data
df = pd.read_csv(r'C:\Users\Desktop\REU\Data\2018_2023_df.txt')
print(df.columns)
tfile = "C:/Users/Desktop/REU/Data/ETOPO1_Bed_c_gmt4.grd"
print (os.path.isfile(tfile))

## Access the netCDF file
etopodata = Dataset(tfile)
print (etopodata.variables.keys())
print (etopodata.variables['x'])
print (etopodata.variables['y'])
print (etopodata.variables['z'])

# Get the netCDF variables
topoin = etopodata.variables['z'][:]
tlons = etopodata.variables['x'][:]
tlats = etopodata.variables['y'][:]
print (tlons.min(), tlons.max(), tlats.min(), tlats.max())


# Plot the map of the Northeast & the IMPROVE sites
fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()}, figsize=(16, 15), facecolor= 'gainsboro')
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent([-82, -66, 38, 48], crs = ccrs.PlateCarree())
fig.set_facecolor('whitesmoke')
clevs = [0,200,400,600,800,1000,1200,1400,1600]
cs=plt.contourf(tlons,tlats,topoin,clevs,cmap='YlOrRd', alpha=0.5)
gl = ax.gridlines(draw_labels=True,linewidth=1, color='gray', alpha=0.5, linestyle='--')
gl.top_labels = False
gl.xlocator = mticker.FixedLocator([-125,-115,-105,-95,-85,-75,-65])
gl.ylocator = mticker.FixedLocator([20,30,40,50,60])
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER

# Make the colorbar 
cax,kw = mplt.colorbar.make_axes(ax,location='right',pad=0.058,shrink=0.5)
cbar = fig.colorbar(cs,cax=cax,**kw)

# Add map features
ax.add_feature(cfeature.LAND, edgecolor='black', facecolor='papayawhip')
ax.add_feature(cfeature.BORDERS, edgecolor = 'black')
ax.add_feature(cfeature.OCEAN, edgecolor='none', facecolor='aliceblue')
ax.add_feature(cfeature.LAKES, edgecolor = 'black', facecolor='aliceblue')
ax.add_feature(cfeature.STATES, edgecolor = 'black')

# Plot text for each site on the map
sitenames = df['SiteCode'].unique()
for k,sitename in enumerate(sitenames):
    lon = df.loc[df.SiteCode == sitename]['Longitude']
    lat = df.loc[df.SiteCode == sitename]['Latitude']
    elevation = df[df.SiteCode == sitename]['Elevation'].iloc[0]
    ax.plot(lon, lat, 'v', color='navy', markersize=10, linestyle='-', linewidth=2.0, label = sitename +': %s' %elevation)
    ax.set_title('IMPROVE Network Locations', fontsize=25)
    
    for x, y in zip(lon, lat):
        if sitename == 'LOND1':
            ax.text(x, y+0.28, sitename, color='black', fontsize=13, ha='center', va='top', transform=ccrs.PlateCarree())
        else:
            ax.text(x, y-0.22, sitename, color='black', fontsize=13, ha='center', va='top', transform=ccrs.PlateCarree())

# Save figure
fig.savefig('/Users/Desktop/REU/Saved Plots/Maps/NE map.png', dpi =1000)





