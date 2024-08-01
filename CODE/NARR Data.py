#!/usr/bin/env python
# coding: utf-8

# ## Plot NARR Reanalysis Data for Wind and Temperature
# ### CSU REU Summer 2024 - Sarah Gryskewicz
# ***

# In[2]:


# Import necessary modules
import xarray  
import matplotlib.pyplot as plt
import pandas as pd
import cartopy
import cartopy.feature as cfeature
import cartopy.crs as ccrs
import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib as mplt
import pylab as pl
import numpy as np
import matplotlib.cm as cm


# ## Plot Temp and Wind Barbs Together

# In[3]:


# Read in the files using xarray
uwnd=xarray.open_dataset('/Users/C837388336/Desktop/REU/Weather activity/NARR/uwnd.10m.2023.nc')
vwnd=xarray.open_dataset('/Users/C837388336/Desktop/REU/Weather activity/NARR/vwnd.10m.2023.nc')
temp = xarray.open_dataset('/Users/C837388336/Desktop/REU/Weather activity/NARR/air.2m.2023.nc')


# In[4]:


# Subset files to a certain day
day=8
june_uwnd = uwnd.sel(time=slice('2023-06-%s' %day, '2023-06-%s' %day))
june_vwnd = vwnd.sel(time=slice('2023-06-%s' %day, '2023-06-%s' %day))

june_temp = temp.sel(time=slice('2023-06-%s' %day, '2023-06-%s' %day))


# In[5]:


time_arr=june_temp['time'].values
time_arr = pd.to_datetime(time_arr)

# Make wind speed for the u and v components
wspd = np.sqrt(june_uwnd['uwnd'].values**2+june_vwnd['vwnd'].values**2)
# Get temp values from K --> F
K = june_temp['air'].values
air_F = (K - 273.15)* 1.8 + 32


# In[6]:


for t, ptime in enumerate(time_arr):
    fig = plt.figure(figsize=(8, 10))
    rect = fig.patch
    rect.set_facecolor("white")
    
    ax = plt.axes(projection=ccrs.LambertConformal(central_longitude=-107.0, central_latitude=50, 
                                                   false_easting=5632642.22547, false_northing=4612545.65137, 
                                                   standard_parallels=[50, 50], globe=None, cutoff=1))
    
    ax.set_extent([-85, -65, 38, 51], ccrs.PlateCarree())
    ax.add_feature(cfeature.STATES)
    ax.add_feature(cfeature.BORDERS)
    ax.add_feature(cfeature.COASTLINE)
    
    # Plot the temperatures
    cs_temp = ax.contourf(june_temp['x'], june_temp['y'], air_F[t,:,:], 
                          levels=[35, 37.5, 40, 42.5, 45, 47.5, 50, 52.5, 55, 57.5, 60, 
                                  62.5, 65, 67.5, 70, 72.5, 75, 77.5, 80],
                          cmap='jet',
                          transform=ccrs.LambertConformal(central_longitude=-107.0, central_latitude=50, 
                                                          false_easting=5632642.22547, false_northing=4612545.65137, 
                                                          standard_parallels=[50, 50], globe=None, cutoff=1))

    # Overlay wind speed as contours
    #cs_wind = ax.contour(june_uwnd['x'], june_uwnd['y'], wspd[t,:,:], 
     #                    levels=[10, 20, 30, 40, 50], 
      #                   colors='black', linewidths=1,
       #                  transform=ccrs.LambertConformal(central_longitude=-107.0, central_latitude=50, 
        #                                                 false_easting=5632642.22547, false_northing=4612545.65137, 
         #                                                standard_parallels=[50, 50], globe=None, cutoff=1))
    
    # Plot wind direction/barbs
    qv = ax.quiver(june_uwnd['x'], june_uwnd['y'], june_uwnd['uwnd'][t,:,:], june_vwnd['vwnd'][t,:,:], 
                   scale=350, color='black', transform=ccrs.LambertConformal(central_longitude=-107.0, 
                                                                             central_latitude=50, 
                                                                             false_easting=5632642.22547, 
                                                                             false_northing=4612545.65137, 
                                                                             standard_parallels=[50, 50], 
                                                                             globe=None, cutoff=1))
    
    # Add a colorbar for temperature
    cax_temp, kw_temp = mplt.colorbar.make_axes(ax, location='bottom', pad=0.05)
    cbar_temp = fig.colorbar(cs_temp, cax=cax_temp, **kw_temp)
    cbar_temp.set_label('Temperature ($^{o}$F)', rotation = 0, horizontalalignment = 'center')

    #ax.legend([cs_wind.collections[0]], ['Wind Speed (m/s)'], loc='lower left')
    
    # Put a title on the plot
    ax.set_title(str(ptime) + ' 2m Temperature ($^{o}$F) and 10m Wind (m s$^{-1}$)', fontsize = 15)
    
    plt.show()
# Save figures if desired (here, just naming them in numeric order
    fig.savefig('/Users/C837388336/Desktop/REU/Weather activity/NARR/Plots/june8_temp&wind_'+'{0:03d}'.format(t)+'.png',bbox_inches='tight',
                dpi=600, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()


# ## Find wind between 700-500 mb as well as 700-300 mb
# 700-500 mb: Transport over a broad distance. Will use this data when assessing Quebec/June impacts </p>
# 700-300 mb: Transport across North America. Will use this data when  assessing BC/Alberta/July impacts
# ***

# In[7]:


uw = xarray.open_dataset('/Users/C837388336/Desktop/REU/Weather activity/NARR/uwnd.202306.nc')
vw = xarray.open_dataset('/Users/C837388336/Desktop/REU/Weather activity/NARR/vwnd.202306.nc')

# for july
#uw = xarray.open_dataset('/Users/C837388336/Desktop/REU/Weather activity/NARR/uwnd.202307.nc')
#vw = xarray.open_dataset('/Users/C837388336/Desktop/REU/Weather activity/NARR/uwnd.202307.nc')


# In[21]:


day = 11
june_uwn = uw.sel(time=slice('2023-06-%s' %day, '2023-06-%s' %day))
june_vwn = vw.sel(time=slice('2023-06-%s' %day, '2023-06-%s' %day))

time_arr = june_uwn['time'].values
time_arr = pd.to_datetime(time_arr)

# select levels 700 mb and 500 mb
uwn_700 = june_uwn.sel(level=700)
uwn_500 = june_uwn.sel(level=500)

vwn_700 = june_vwn.sel(level=700)
vwn_500 = june_vwn.sel(level=500)


# subtract between layers
uwn_sel = uwn_500 - uwn_700
vwn_sel = vwn_500 - vwn_700
wspd = np.sqrt(uwn_sel['uwnd'].values**2+vwn_sel['vwnd'].values**2)


# ## Plot Wind Speed and Direction from 700-500 mb

# In[24]:


for t, ptime in enumerate(time_arr):
    fig=plt.figure(figsize=(6,8))
    rect = fig.patch
    rect.set_facecolor("white")
    # This sets up the plot region with the values given in the file
    ax = plt.axes(projection=ccrs.LambertConformal(central_longitude=-107.0, central_latitude=50, false_easting=5632642.22547, 
                                                   false_northing=4612545.65137, standard_parallels=[50,50], globe=None, cutoff=1))   
    #ax.set_extent([-130, -65, 38, 51], ccrs.PlateCarree())
    ax.set_extent([-80, -65, 38, 51], ccrs.PlateCarree())

    ax.add_feature(cfeature.STATES) # Plot the state lines
    ax.add_feature(cfeature.BORDERS)
    ax.add_feature(cfeature.COASTLINE)

    # Plot the wind speeds
    cs=ax.contourf(uwn_sel['x'],uwn_sel['y'], wspd[t,:,:], levels=[0,2.5,5,7.5,10,12.5,15],cmap='jet',
                   transform=ccrs.LambertConformal(central_longitude=-107.0, central_latitude=50, 
                                                   false_easting=5632642.22547,false_northing=4612545.65137, 
                                                   standard_parallels=[50,50], globe=None, cutoff=1))
    # Plot the wind direction/barbs
    qv=ax.quiver(uwn_sel['x'],uwn_sel['y'],uwn_sel['uwnd'][t,:,:],vwn_sel['vwnd'][t,:,:],scale=350, color='k',
              transform=ccrs.LambertConformal(central_longitude=-107.0, central_latitude=50, false_easting=5632642.22547,
                                              false_northing=4612545.65137, standard_parallels=[50,50], globe=None, cutoff=1))
    
    # Make a colorbar 
    cax,kw = mplt.colorbar.make_axes(ax,location='right',pad=0.05, shrink = 0.5)
    cbar = fig.colorbar(cs,cax=cax,**kw)
    cbar.ax.tick_params(labelsize=8) 
    cbar.set_label('Wind', fontsize = 10, rotation = 0, labelpad=25)

    # Put a title on the plot
    ax.set_title(str(ptime) + ' 700-500 mb Wind', fontsize = 15)
    ax.annotate('Speed', xy=(1.24, 0.430), xycoords='axes fraction',
             fontsize=10, ha='left', va='center', rotation=0)
    ax.annotate('(m s$^{-1}$)', xy=(1.23, 0.38), xycoords='axes fraction',
             fontsize=10, ha='left', va='center', rotation=0)
    plt.show()

    # Save figures if desired (here, just naming them in numeric order
    fig.savefig('/Users/C837388336/Desktop/REU/Weather activity/NARR/Plots/june/june10_wind_'+'{0:03d}'.format(t)+'.png',bbox_inches='tight',
               dpi=600, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()


# ## Plot Wind Barbs and Temp from 700-500 mb

# In[67]:


## THIS PLOTS TEMP AND WIND BARBS
for t, ptime in enumerate(time_arr):
    fig = plt.figure(figsize=(8, 10))
    rect = fig.patch
    rect.set_facecolor("white")
    
    ax = plt.axes(projection=ccrs.LambertConformal(central_longitude=-107.0, central_latitude=50, 
                                                   false_easting=5632642.22547, false_northing=4612545.65137, 
                                                   standard_parallels=[50, 50], globe=None, cutoff=1))
    
    ax.set_extent([-85, -65, 38, 51], ccrs.PlateCarree())
    ax.add_feature(cfeature.STATES)
    ax.add_feature(cfeature.BORDERS)
    ax.add_feature(cfeature.COASTLINE)
    
    # Plot the temperatures
    cs_temp = ax.contourf(june_temp['x'], june_temp['y'], air_F[t,:,:], 
                          levels=[35, 37.5, 40, 42.5, 45, 47.5, 50, 52.5, 55, 57.5, 60, 
                                  62.5, 65, 67.5, 70, 72.5, 75, 77.5, 80],
                          cmap='jet',
                          transform=ccrs.LambertConformal(central_longitude=-107.0, central_latitude=50, 
                                                          false_easting=5632642.22547, false_northing=4612545.65137, 
                                                          standard_parallels=[50, 50], globe=None, cutoff=1))

    # Overlay wind speed as contours
    #cs_wind = ax.contour(june_uwnd['x'], june_uwnd['y'], wspd[t,:,:], 
     #                    levels=[10, 20, 30, 40, 50], 
      #                   colors='black', linewidths=1,
       #                  transform=ccrs.LambertConformal(central_longitude=-107.0, central_latitude=50, 
        #                                                 false_easting=5632642.22547, false_northing=4612545.65137, 
         #                                                standard_parallels=[50, 50], globe=None, cutoff=1))
    
    # Plot wind direction/barbs
    qv = ax.quiver(uwn_sel['x'], uwn_sel['y'], uwn_sel['uwnd'][t,:,:], vwn_sel['vwnd'][t,:,:], 
                   scale=350, color='black', transform=ccrs.LambertConformal(central_longitude=-107.0, 
                                                                             central_latitude=50, 
                                                                             false_easting=5632642.22547, 
                                                                             false_northing=4612545.65137, 
                                                                             standard_parallels=[50, 50], 
                                                                             globe=None, cutoff=1))
    
    # Add a colorbar for temperature
    cax_temp, kw_temp = mplt.colorbar.make_axes(ax, location='bottom', pad=0.05)
    cbar_temp = fig.colorbar(cs_temp, cax=cax_temp, **kw_temp)
    cbar_temp.set_label('Temperature ($^{o}$F)', rotation = 0, horizontalalignment = 'center')

    #ax.legend([cs_wind.collections[0]], ['Wind Speed (m/s)'], loc='lower left')
    
    # Put a title on the plot
    ax.set_title(str(ptime) + ' 2m Temperature ($^{o}$F) and 700-500 mb Wind (m/s)', fontsize = 15)
    
    plt.show()
# Save figures if desired (here, just naming them in numeric order
    #fig.savefig('/Users/C837388336/Desktop/REU/Weather activity/NARR/Plots/700_500/june7_temp&wind_'+'{0:03d}'.format(t)+'.png',bbox_inches='tight',
              # dpi=600, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()


# ## Code to Plot Wind and Temp Individually
# You'll need the above code to do this

# In[46]:


# Loop through all the times and make a plot for each. (wind)

for t, ptime in enumerate(time_arr):
    fig=plt.figure(figsize=(6,8))
    rect = fig.patch
    rect.set_facecolor("white")
    # This sets up the plot region with the values given in the file
    ax = plt.axes(projection=ccrs.LambertConformal(central_longitude=-107.0, central_latitude=50, false_easting=5632642.22547, 
                                                   false_northing=4612545.65137, standard_parallels=[50,50], globe=None, cutoff=1))   
    #ax.set_extent([-123, -113, 32, 43], ccrs.PlateCarree())
#    ax.set_extent([-85, -65, 38, 51], ccrs.PlateCarree())
    ax.set_extent([-75, -65, 38, 51], ccrs.PlateCarree())

    ax.add_feature(cfeature.STATES) # Plot the state lines
    ax.add_feature(cfeature.BORDERS)
    ax.add_feature(cfeature.COASTLINE)

    # Plot the wind speeds
    cs=ax.contourf(june_uwnd['x'],june_uwnd['y'], wspd[t,:,:], levels=[0,2.5,5,7.5,10,12.5,15],cmap='jet',
                   transform=ccrs.LambertConformal(central_longitude=-107.0, central_latitude=50, 
                                                   false_easting=5632642.22547,false_northing=4612545.65137, 
                                                   standard_parallels=[50,50], globe=None, cutoff=1))
    # Plot the wind direction/barbs
    qv=ax.quiver(june_uwnd['x'],june_uwnd['y'],june_uwnd['uwnd'][t,:,:],june_vwnd['vwnd'][t,:,:],scale=350, color='k',
              transform=ccrs.LambertConformal(central_longitude=-107.0, central_latitude=50, false_easting=5632642.22547,
                                              false_northing=4612545.65137, standard_parallels=[50,50], globe=None, cutoff=1))
    
    # Make a colorbar 
    cax,kw = mplt.colorbar.make_axes(ax,location='right',pad=0.05,shrink=0.5)
    cbar = fig.colorbar(cs,cax=cax,**kw)
    cbar.set_label('Wind Speed (m/s)', rotation = 90)

    # Put a title on the plot
    ax.set_title(str(ptime) + ' 10 m Wind Speed (m/s) and Direction', fontsize = 17)
    #ax.set_title('6 June 2023 at ' + ptime + ' 10 m Wind Speed (m/s) and Wind Direction ($^{o}$)', fontsize = 20)
    plt.show()

    # Save figures if desired (here, just naming them in numeric order
    fig.savefig('/Users/C837388336/Desktop/REU/Weather activity/NARR/Wind Plots/june6_wind_'+'{0:03d}'.format(t)+'.png',bbox_inches='tight',
                dpi=600, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()


# In[104]:


# Loop through all the times and make a plot for each. (temp)
for t, ptime in enumerate(time_arr):
    fig=plt.figure(figsize=(6,8))
    rect = fig.patch
    rect.set_facecolor("white")
    # This sets up the plot region with the values given in the file
    ax = plt.axes(projection=ccrs.LambertConformal(central_longitude=-107.0, central_latitude=50, false_easting=5632642.22547, 
                                                   false_northing=4612545.65137, standard_parallels=[50,50], globe=None, cutoff=1))   
    #ax.set_extent([-123, -113, 32, 43], ccrs.PlateCarree())
    ax.set_extent([-85, -65, 38, 51], ccrs.PlateCarree())
    ax.add_feature(cfeature.STATES) # Plot the state lines
    ax.add_feature(cfeature.BORDERS)
    ax.add_feature(cfeature.COASTLINE)
    
    # Plot the temperatures
    cs=ax.contourf(june_temp['x'],june_temp['y'], air_F[t,:,:], levels=[35,37.5,40,42.5,45,47.5,50,52.5,55,57.5,60,62.5,65,67.5,70,72.5,75,77.5,80],cmap='jet',
                   transform=ccrs.LambertConformal(central_longitude=-107.0, central_latitude=50, 
                                                   false_easting=5632642.22547,false_northing=4612545.65137, 
                                                   standard_parallels=[50,50], globe=None, cutoff=1))
    
    # Make a colorbar 
    cax,kw = mplt.colorbar.make_axes(ax,location='right',pad=0.05,shrink=0.5)
    cbar = fig.colorbar(cs,cax=cax,**kw)
    cbar.set_label('Temperature')
    
    # Put a title on the plot
    ax.set_title(ptime)
    plt.show()
    
    # Save figures if desired (here, just naming them in numeric order
    fig.savefig('/Users/C837388336/Desktop/REU/Weather activity/NARR/Temp Plots/june5_temp_'+'{0:03d}'.format(t)+'.png',bbox_inches='tight',
                dpi=600, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()


# In[ ]:




