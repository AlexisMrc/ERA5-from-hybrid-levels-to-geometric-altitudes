#!/usr/bin/env python
import xarray as xr
import numpy as np
import datetime
import pandas as pd
import os


def sort_files(year):
    """
    To Sort lists containing files of geopotential, log of surface pressure and temperature.
    From January to December
    :param year: str of the studied year (ex: '1999')
    :return:
    - z_on_ml_files
    - zlnsp_files
    - tq_ml_files
    """
    
    ERA5_data_rep = '../Data/' + year + '/'
    ERA5_files = os.listdir(ERA5_data_rep)

    z_on_ml_files = []
    zlnsp_files = []
    tq_ml_files = []

    for m in range(1, 13):
        if m < 10:
            m = year + "-0" + str(m)
        else:
            m = year + "-" + str(m)
        for f in ERA5_files:
            if "z_on_ml" in f and m in f:
                z_on_ml_files.append(f)
            if "zlnsp" in f and m in f:
                zlnsp_files.append(f)
            if "tq_ml" in f and m in f:
                tq_ml_files.append(f)

    return z_on_ml_files, zlnsp_files, tq_ml_files


def convert_geopo_to_km_and_interpolate(year, new_lz, lats, lons, z_on_ml_files, zlnsp_files, tq_ml_files):
    """
    Conversion of geopotential into geometric altitude (km) on 137 levels,
    then interpolation of variables (Temperature and Pressure)
    on altitudes from 0 to 80 km every 500 m.
    :param year:
    :param new_lz:
    :param z_on_ml_files:
    :param zlnsp_files:
    :param tq_ml_files:
    :return:
    - Array of Pressure
    - Array of Temperature
    """
    ERA5_data_rep = '../Data/' + year + '/'
    file = '../Data/table.csv'
    df = pd.read_csv(file, sep=',', header=0)

    a = df['a [Pa]'].values
    b = df['b'].values

    dates = pd.date_range(start=year + '-01-01', end=year + '-12-31')

    Matrix_P = np.ndarray((len(dates), len(lats), len(lons), len(new_lz)), dtype=float)
    Matrix_T = np.ndarray((len(dates), len(lats), len(lons), len(new_lz)), dtype=float)
    Matrix_P[:, :, :, :] = np.nan
    Matrix_T[:, :, :, :] = np.nan
    count = 0
    for (f, f2, f3) in zip(z_on_ml_files, zlnsp_files, tq_ml_files):
        ds = xr.open_dataset(ERA5_data_rep + f, engine="cfgrib", indexpath='')
        ds2 = xr.open_dataset(ERA5_data_rep + f2, engine="cfgrib", indexpath='')
        ds3 = xr.open_dataset(ERA5_data_rep + f3, engine="cfgrib", indexpath='')
        Z_ON_ML = ds['z'].values
        Lnsp = ds2['lnsp'].values
        T_ML = ds3['t'].values
        for i, day in enumerate(Z_ON_ML):
            for j, lat in enumerate(lats):
                g_phi = 9.80665
                Re = 6371229
                for l, lon in enumerate(lons):
                    P_half = np.ndarray((138), dtype=float)
                    for k in range(138):
                        P_half[k] = a[k] + b[k] * np.exp(Lnsp[i, j, l])
                    P_ml = np.ndarray((137), dtype=float)
                    MZ = np.ndarray((137), dtype=float)
                    for k in range(0, 137):
                        MZ[k] = Z_ON_ML[i, k, j, l] / g_phi * (Re) / (Re - Z_ON_ML[i, k, j, l] / g_phi) / 1000
                        P_ml[k] = (P_half[k] + P_half[k + 1]) / 2
                    Matrix_T[count, j, l, :] = np.interp(new_lz, np.flip(MZ), np.flip(T_ML[i, :, j, l]))
                    Matrix_P[count, j, l, :] = np.interp(new_lz, np.flip(MZ), np.flip(P_ml))
            count += 1

    return Matrix_T, Matrix_P
