#!/usr/bin/env python
"""
    Interpolated data are then saved in a netcdf files in Interpolated_Data directory
"""

import netCDF4 as nc
from netCDF4 import date2num
import datetime as dt

def save_to_netcdf(year, lats, lons, new_lz, Matrix_T, Matrix_P):
    start = dt.datetime.strptime("01-01-"+year+"-12", "%d-%m-%Y-%H")
    end = dt.datetime.strptime("01-01-"+str(int(year)+1)+"-12", "%d-%m-%Y-%H")
    date_generated = [start + dt.timedelta(days=x) for x in range(0, (end-start).days)]

    fn = '../Outputs/'+year+'.nc'
    ds = nc.Dataset(fn, 'w', format='NETCDF4')

    time = ds.createDimension('time', None)
    lat = ds.createDimension('lat', None)
    lon = ds.createDimension('lon', None)
    alt = ds.createDimension('alt', None)

    time = ds.createVariable('time', 'f4', ('time',))
    time.units = 'days since 1900-01-01'
    time.long_name = 'time'

    latitudes = ds.createVariable('lat', 'f4', ('lat',))
    latitudes.units = 'degrees_north'
    latitudes.long_name = 'latitude'

    longitudes = ds.createVariable('lon', 'f4', ('lon',))
    longitudes.units = 'degrees_east'
    longitudes.long_name = 'longitude'

    altitudes = ds.createVariable('alt', 'f4', ('alt',))
    altitudes.units = 'km'
    altitudes.long_name = 'altitude'

    temperature = ds.createVariable('t', 'f4', ('time', 'lat', 'lon', 'alt',))
    temperature.units = 'K' # degrees Kelvin
    temperature.standard_name = 'temperature' # this is a CF standard name

    pressure = ds.createVariable('p', 'f4', ('time', 'lat', 'lon', 'alt',))
    pressure.units = 'Pa' # degrees Kelvin
    pressure.standard_name = 'pressure' # this is a CF standard name

    times = date2num(date_generated, time.units)
    time[:] = times
    latitudes[:] = lats
    longitudes[:] = lons
    altitudes[:] = new_lz
    temperature[:, :, :] = Matrix_T[:, :, :, :]
    pressure[:, :, :] = Matrix_P[:, :, :, :]
    ds.close()
    print('done')
