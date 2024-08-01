#!/usr/bin/env python
# coding: utf-8

# ## Plume Plotting
# ### CSU REU 2024 - Sarah Gryskewicz
# *This notebook will use both the Multiple Sites code as well as the added HMS smoke plume data to visualize smoke transport*
# ***

# In[37]:


# Import necessary modules
import io
import numpy as np
import pandas as pd
from zipfile import ZipFile
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
from matplotlib import rcParams
from matplotlib import rc
rc('mathtext', default='regular') 
rcParams['font.family'] = 'Tahoma'
rcParams['font.size'] = 14
rcParams['mathtext.fontset'] = 'cm'
rcParams['mathtext.rm'] = 'Tahoma'

# Put in settings
    #Transport and regular map bounds:
#map_bounds = [-129, -65, 33,60]
#map_bounds = [-82, -65, 36.8, 48]

 # Quebec fire bounds:
map_bounds = [-89, -65, 38, 54]

streetmap='True'


# In[39]:


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


# In[41]:


# Get text filer
improve_nm_daily=pd.read_csv(r"C:\Users\C837388336\Desktop\REU\Data files\Massive Files\2018_2023_df.txt",header=0)
improve_nm_daily['Date']=pd.to_datetime(improve_nm_daily['Date'])


# In[43]:


# Thank you to Dr. Bonne Ford for providing me code to work with shapefiles/plume data from the HMS fire & smoke product
# Plot shapefiles
start_datetime=datetime.strptime("06-08-2023", "%m-%d-%Y")
end_datetime=datetime.strptime("06-08-2023", "%m-%d-%Y")

for x in range(0, 1+(end_datetime-start_datetime).days):
    plt.close('all')
    date2grab=start_datetime + timedelta(days=x)
    obdate=date2grab.strftime("%Y%m%d")
    sm_dir=date2grab.strftime("%Y/%m/")
    figure_title='HMS Fires and Smoke across the United States '+date2grab.strftime("%d %B %Y")
    output_figure_file='./HMS_plots/HMS_NM_'+date2grab.strftime("%m.%d.%y")+'b.png'
    # Read in file with fire locations. First check the main directory, if not there, then check the archive
    smoke_dir="https://satepsanone.nesdis.noaa.gov/pub/FIRE/web/HMS/Smoke_Polygons/Shapefile/"+sm_dir
    fire_dir="https://satepsanone.nesdis.noaa.gov/pub/FIRE/web/HMS/Fire_Points/Text/"+sm_dir
    smoke_URL=smoke_dir+'hms_smoke'+obdate+'.zip'
    print (smoke_URL)
    request_response = requests.head(smoke_URL)
    if (request_response.status_code == 404): 
     smoke_URL=smoke_dir+'ARCHIVE/hms_smoke'+obdate+'.zip'
     request_response=requests.head(smoke_URL)
     if (request_response.status_code == 404): 
            print('Cannot find smoke file')

    fire_URL=fire_dir+'hms_fire'+obdate+'.txt'
    print (fire_URL)
    request_response = requests.head(fire_URL)
    if (request_response.status_code == 404): 
     fire_URL=fire_dir+'TXT_ARCHIVE/hms'+obdate+'.txt'
     request_response=requests.head(fire_URL)
     if (request_response.status_code == 404):
            print ('Using prelim fire file')

    # Get the fire locations
    df=pd.read_csv(fire_URL)
    # Get the smoke plumes
    response=requests.get(smoke_URL)
    with ZipFile(io.BytesIO(response.content),mode='r') as zf:  
        shpfile=io.BytesIO(zf.read('hms_smoke'+obdate+'.shp'))
        dbffile=io.BytesIO(zf.read('hms_smoke'+obdate+'.dbf'))
        shxfile=io.BytesIO(zf.read('hms_smoke'+obdate+'.shx'))
        
    shp_file = shapefile.Reader(shp=shpfile, shx=shxfile, dbf=dbffile)
    smoke_polys=[]
    polygons = shp_file.shapes() 
    for polygon in polygons:
        polygon = shapely.geometry.shape(polygon)
        smoke_polys.append(polygon)
    plumes = cfeature.ShapelyFeature(smoke_polys, ccrs.PlateCarree())  

    # Plot the map with fire location and smoke plumes
    if (streetmap == 'True'):
     cimgt.OSM.get_image = image_spoof # reformat web request for street map spoofing
     osm_img = cimgt.OSM()             # spoofed, downloaded street map
     fig = plt.figure(figsize=(8,10))  # open matplotlib figure
     rect = fig.patch
     rect.set_facecolor("white")
     m = plt.axes(projection=osm_img.crs) # project using coordinate reference system (CRS) of street map
     extent = map_bounds
     m.set_extent(extent) # set extents
     scale = np.ceil(-np.sqrt(2)*np.log(np.divide((extent[1]-extent[0])/2.0,350.0))) # empirical solve for scale based on zoom
     scale = (scale<20) and scale or 19 # scale cannot be larger than 19
     m.add_image(osm_img, int(scale)) # add OSM with zoom specification

    else: 
     fig=plt.figure(figsize=(8,10))
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
    


    # Shrink the number of fires to only include fires exceeding a certain threshold in fire radiative power (FRP) emitted from wildfires
    fire_threshold = 50         # Exceeding ___ FRP 
    filtered_df = df[df['        FRP'] >= fire_threshold]          # Filter the df so that where df[FRP] exceeds 100, the values will be 
                                                                    # Added to a new filtered df. THIS IS ONLY FOR THE HMS FIRE POINTS, NOT THE PLUMES
    if not filtered_df.empty:             # Plot sources if threshold is met
        m.scatter(filtered_df['        Lon'], filtered_df['        Lat'], color='red', transform=ccrs.PlateCarree(),
              marker='v', s=15, label='HMS Fire', zorder=3)

    # Add plumes
    m.add_feature(plumes, facecolor='gray', alpha=0.4,label='HMS Smoke',zorder=2)

    map_obdate=date2grab.strftime("%Y-%m-%d") 
    maplocs_improve = improve_nm_daily[improve_nm_daily['Date'] == map_obdate].copy()
    cs=m.scatter(maplocs_improve['Longitude'],maplocs_improve['Latitude'],c=maplocs_improve['MF_Val'],marker='s',s=60,cmap='rainbow', \
              vmax=15,vmin=0,edgecolor='black',transform=ccrs.PlateCarree(),label='IMPROVE',zorder=4)    
    plt.legend(loc=3)
    transform = ccrs.PlateCarree()._as_mpl_transform(m) # set transform for annotations
    cax,kw = mplt.colorbar.make_axes(m,location='bottom',pad=0.05,shrink=0.8)
    cbar = plt.colorbar(cs,cax=cax,**kw)
    cbar.set_label('PM$_{2.5}$ [$\mu$g m$^{-3}$]', fontsize=18, horizontalalignment='center', rotation=0)
    fig.set_facecolor('whitesmoke')
    m.set_title(figure_title,fontsize=20)
    plt.show()

# Save figure
#fig.savefig('/Users/C837388336/Desktop/REU/Data files/Saved Plots/Plumes/July/july19.png')


# ## See how many fires are small compared to larger ones

# In[18]:


less = []
for j in range(len(df[ '        FRP'])):
        if df[ '        FRP'][j] <= fire_threshold:
           # print(df[ '        FRP'][j])
            less.append(df[ '        FRP'][j])
difference = len(df[ '        FRP']) - len(less)
print('removed fires: ', len(less))
print('remaining fires: ', difference)


# In[19]:


df['        Lon']


# In[20]:


df['        Lat']


# In[21]:


df.columns


# In[22]:


df[ '        FRP']


# In[ ]:





# In[ ]:




