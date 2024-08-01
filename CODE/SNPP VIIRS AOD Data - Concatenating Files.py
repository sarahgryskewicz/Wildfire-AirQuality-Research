# Concatenate here before plotting the data (see other file)
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
from datetime import datetime
import pandas as pd

# Access directory of downloaded files
snpp_direc = '/Users/Desktop/REU/Data/AOD/AOD nc/'
gfiles=sorted(glob.glob(snpp_direc+'AERDB_D3_VIIRS_SNPP.A2023*nc'))
# Concatenate
ds = xarray.concat([xarray.open_dataset(f) for f in gfiles],dim="time",coords="different")

dates = []
for filepath in gfiles:
    # File name example: AERDB_D3_VIIRS_SNPP.A2023152.002.2023156000957
    day_num = int(filepath[77:80]) 
    year = int(filepath[73:77])     
    date = pd.Timestamp(year=year, month=1, day=1) + pd.Timedelta(days=day_num - 1)
    # Open dataset and add date as a new coordinate
    ds = xarray.open_dataset(filepath)
    ds.coords['dates'] = date
    # Append dataset to list
    dates.append(ds)

# Concatenate datasets along 'time' dimension
ds = xarray.concat(dates, dim='time')

#Dropping variables from a dataset: (only want a few so lots are being dropped from this file)
vars_to_drop = ["Unsuitable_Pixel_Fraction_Land_Ocean", "Aerosol_Optical_Thickness_550_Land_Ocean_Count",\
              "Aerosol_Optical_Thickness_550_Land_Ocean_Maximum", "Aerosol_Optical_Thickness_550_Land_Ocean_Mean",\
              "Aerosol_Optical_Thickness_550_Land_Ocean_Minimum", "Aerosol_Optical_Thickness_550_Land_Ocean_Standard_Deviation",\
              "Aerosol_Optical_Thickness_550_Ocean_Count", "Aerosol_Type_Land_Ocean_Histogram", "Aerosol_Type_Land_Ocean_Mode",\
              "Angstrom_Exponent_Land_Ocean_Maximum", "Angstrom_Exponent_Land_Ocean_Mean", "Angstrom_Exponent_Land_Ocean_Minimum", \
              "Angstrom_Exponent_Land_Ocean_Maximum", "Angstrom_Exponent_Land_Ocean_Mean", "Angstrom_Exponent_Land_Ocean_Minimum", \
              "Angstrom_Exponent_Land_Ocean_Standard_Deviation", "Angstrom_Exponent_Ocean_Maximum", "Angstrom_Exponent_Ocean_Mean", \
              "Angstrom_Exponent_Ocean_Minimum", "Angstrom_Exponent_Ocean_Standard_Deviation", \
              "Spectral_Aerosol_Optical_Thickness_Ocean_Standard_Deviation", "Spectral_Aerosol_Optical_Thickness_Ocean_Mean", \
             "Spectral_Aerosol_Optical_Thickness_Ocean_Count", "Aerosol_Optical_Thickness_550_Ocean_Maximum",\
             "Fine_Mode_Fraction_550_Ocean_Standard_Deviation", "Fine_Mode_Fraction_550_Ocean_Mean", "Aerosol_Optical_Thickness_550_Ocean_Mean",\
             "Aerosol_Optical_Thickness_550_Ocean_Minimum", "Aerosol_Optical_Thickness_550_Ocean_Standard_Deviation"]


ds = ds.drop_vars(vars_to_drop)
output_path = os.path.join("C:/Users/Desktop/REU/Data/AOD/AOD JJA", 'AOD_data_2023_JJA.nc')
# Save out a xarray dataset into a new netcdf:
ds.to_netcdf(output_path, format='NETCDF4')
