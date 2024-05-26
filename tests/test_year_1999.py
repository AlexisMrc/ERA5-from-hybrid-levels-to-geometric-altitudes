import os
import subprocess
import datetime
import calendar
import xarray as xr
import numpy as np
import sys
sys.path.append(sys.path[0]+"/../Scripts")
#sys.path.append("/Users/mariaccia/Documents/Projects/ERA5-from-hybrid-levels-to-geometric-altitudes/Scripts")
#print(sys.path)

from get_data_geopotential_on_ml import get_data
from Convert_and_Interpolate_Geopo_to_km import sort_files, convert_geopo_to_km_and_interpolate
from Save_to_Netcdf import save_to_netcdf

"""
    Description:
    This script will download the requested data (see script
    get_data_geopotential_on_ml.py)
    on the desired grid and 137 levels for all days of the 12 months of the year 1999.

    Outputs :
    tq_ml_Year_Month: temperature and humidity on the grid and 137 levels
                        for all days of a month in a year
    zlnsp_ml_Year_Month: surface geopotential and logarithm of surface pressure on the grid

    The script executes the compute_geopotential_on_ml.py script (inputs: Temp and Humidity and Lnsp)
    to create z_on_ml.grib files containing the geopotential height for each day
    on 137 levels on all lon and lat.

    Script to convert geopotential levels to geometric altitudes (in km)
    Then, to interpolate these levels on a specified altitude range
    Finally, the new fields are saved in a netcdf file
    
"""

if __name__ == '__main__':
    t0 = datetime.datetime.now()

    Year = 1999 # valid from 1940 to the present
    Grid = [5.0, 5.0] # min = 0.25
    Area = [60, -180, 50, 180] # North, West, South, East.
    Time = "12:00:00" # or a range as "00:00:00/01:00:00/02:00:00" or "00:00:00/to/23:00:00/by/1"
    path_repertory = "../Data/"+str(Year)
    try:
        os.mkdir(path_repertory)
    except:
        print("already exist")


    for Month in range(4, 13): # from January to December
        num_days = calendar.monthrange(Year, Month)[1]
        days = [datetime.date(Year, Month, day) for day in range(1, num_days+1)]
        Day1 = days[0].day
        Day2 = days[-1].day
        if Month < 10:
            Month = "0"+str(Month)
        else:
            Month = str(Month)
        Day1 = "0"+str(Day1)
        Day2 = str(Day2)
        Year = str(Year)

        print('Extraction between: ')
        print(Year+'-'+Month+'-'+Day1+'-'+Time)
        print(' and ')
        print(Year+'-'+Month+'-'+Day2+'-'+Time)

        path1 = path_repertory+"/tq_ml_"+Year+"-"+Month+".grib"
        path2 = path_repertory+'/zlnsp_ml_'+Year+'-'+Month+'.grib'
        get_data(Year, Month, Day1, Day2, Time, Grid, Area, path1, path2)

        print('Computation of geopotential on 137 levels')
        path3 = path_repertory+"/z_on_ml_"+Year+"-"+Month+".grib"
        path_fonction = "../Scripts/compute_geopotential_on_ml.py"
        subprocess.run(["python", path_fonction, path1, path2, "-o", path3])
        Year = int(Year)

    print('done')

    """ First, we sort downloaded ERA5 files (from Jan to Dec) """
    z_on_ml_files, zlnsp_files, tq_ml_files = sort_files(str(Year))
    print('Files are sorted')

    ds = xr.open_dataset(path_repertory+"/"+zlnsp_files[0], engine="cfgrib", indexpath='')
    lats = ds['latitude'].values
    lons = ds['longitude'].values

    """ Set the new altitude range in km """
    new_lz = np.arange(0, 80.5, 0.5)  # in km (can be modified)

    """ Converting 137 geopotential levels to geometric altitudes (in km)
    and then interpolating data over the new altitude range: new_lz """
    Matrix_T, Matrix_P = convert_geopo_to_km_and_interpolate(str(Year), new_lz, lats, lons,
                                                            z_on_ml_files, zlnsp_files, tq_ml_files)
    print('T and P are interpolated')
    """ Saving interpolated data on a netcdf file in Interpolated_Data repertory"""
    save_to_netcdf(str(Year), lats, lons, new_lz, Matrix_T, Matrix_P)
    print(datetime.datetime.now() - t0)
