import xarray
import matplotlib.pyplot as plt
import cartopy
import cartopy.feature as cfeature
import cartopy.crs as ccrs
import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib as mplt
import pylab as pl
import os, sys, glob, os.path
import pandas as pd
import numpy as np
from matplotlib import rcParams
from matplotlib import rc
rc('mathtext', default='regular') 
rcParams['font.family'] = 'Tahoma'
rcParams['mathtext.fontset'] = 'cm'
rcParams['mathtext.rm'] = 'Tahoma'

# Access data
snppdata=xarray.open_dataset("/Users/C837388336/Desktop/REU/Data files/AOD/AOD JJA/AOD_data_2023_JJA.nc")
snppdata

# Create a dates dictionary to use for plot titles
    # be mindful that if you download any date outside of these dates, you must add to this dictionary and change the corresponding numbers
dates = {
    '0': '1 June 2023', '1': '2 June 2023', '2': '3 June 2023', '3': '4 June 2023', '4': '5 June 2023', 
    '5': '6 June 2023', '6': '7 June 2023', '7': '8 June 2023', '8': '9 June 2023', '9': '10 June 2023',
    '10': '11 June 2023', '11': '12 June 2023', '12': '13 June 2023', '13': '14 June 2023', '14': '15 June 2023',
    '15': '16 June 2023', '16': '17 June 2023', '17': '18 June 2023','18': '19 June 2023','19': '20 June 2023', 
    '20': '21 June 2023','21': '22 June 2023', '22': '23 June 2023', '23': '24 June 2023', '24': '25 June 2023', 
    '25': '26 June 2023','26': '27 June 2023', '27': '28 June 2023', '28': '29 June 2023','29': '30 June 2023',
    
    '30': '1 July 2023', '31': '2 July 2023', '32': '3 July 2023', '33': '4 July 2023', '34': '5 July 2023',
    '35': '6 July 2023', '36': '7 July 2023', '37': '8 July 2023', '38': '9 July 2023', '39': '10 July 2023', 
    '40': '11 July 2023', '41': '12 July 2023', '42': '13 July 2023', '43': '14 July 2023', '44': '15 July 2023', 
    '45': '16 July 2023', '46': '17 July 2023', '47': '18 July 2023', '48': '19 July 2023','49': '20 July 2023',
    '50': '21 July 2023', '51': '22 July 2023', '52': '23 July 2023', '53': '24 July 2023', '54': '25 July 2023', 
    '55': '26 July 2023', '56': '27 July 2023', '57': '28 July 2023', '58': '29 July 2023', '59': '30 July 2023',
    '60': '31 July 2023',

    '61': '1 August 2023', '62': '2 August 2023', '63': '3 August 2023', '64': '4 August 2023', '65': '5 August 2023',
    '66': '6 August 2023', '67': '7 August 2023', '68': '8 August 2023', '69': '9 August 2023', '70': '10 August 2023', 
    '71': '11 August 2023', '72': '12 August 2023', '73': '13 August 2023', '74': '14 August 2023', '75': '15 August 2023', 
    '76': '16 August 2023', '77': '17 August 2023', '78': '18 August 2023', '79': '19 August 2023','80': '20 August 2023',
    '81': '21 August 2023', '82': '22 August 2023', '83': '23 August 2023', '84': '24 August 2023', '85': '25 August 2023', 
    '86': '26 August 2023', '87': '27 August 2023', '88': '28 August 2023', '89': '29 August 2023', '90': '30 August 2023',
    '91': '31 August 2023'
}


# Make the figure
fig=plt.figure(figsize=(10,8))
fig.set_facecolor('whitesmoke')
ax = plt.axes(projection=ccrs.PlateCarree())

# Set bounds for North America or ...
ax.set_extent([-130, -68, 30,65], ccrs.PlateCarree())
# ... set bounds for NE
#ax.set_extent([-98, -61, 31, 60], ccrs.PlateCarree())

# Plot data
cs=plt.pcolormesh(snppdata['Longitude'],snppdata['Latitude'],snppdata['Aerosol_Optical_Thickness_550_Land_Mean'][45,:,:],cmap='jet',vmin=0,vmax=1, zorder = 1)
ax.add_feature(cfeature.STATES, zorder=3)
ax.add_feature(cfeature.COASTLINE)

# Make a colorbar 
cax,kw = mplt.colorbar.make_axes(ax,location='right',pad=0.05,shrink=0.6)
cbar = fig.colorbar(cs,cax=cax,**kw)

# Put a title on the plot
ax.set_title(dates['45'] + ' AOD 550nm Land Mean', fontsize=17)

# Save figure
#fig.savefig('/Users/Desktop/REU/Saved Plots/AOD/july19.png')
