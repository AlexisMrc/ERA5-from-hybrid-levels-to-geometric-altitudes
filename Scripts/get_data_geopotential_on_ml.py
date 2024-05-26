#!/usr/bin/env python
"""
    Function to download ERA5 data with indicated specifications.
    Here, data are extracted at 12:00:00 over the  specified period.
    The period can't exceed one month of a year.
    It is noteworthy that other other variables can be downloaded
    in addition to those here necessary for computing the geopotential
    on each hybrid level.
"""
import cdsapi


def get_data(Year, Month, Day1, Day2, Time, Grid, Area, path1, path2):
    """
    :param Year: str containing the year (ex: '1999')
    :param Month: str containing the month (ex: '01' for January)
    :param Day1: str containing the first day (ex: '01' for January 1st)
    :param Day2: str containing the last day (ex: '31' for January 31st)
    :param Time: str containing the hour (ex: '12:00:00')
    :param path1: path where temperature and specific humidity are saved
    :param path2: path where geopotential and logarithm of surface pressure are saved
    :return:
    - a first file containing temperature and specific humidity over 137 vertical hybrid levels (path1)
    - a second file containing geopotential and logarithm of surface pressure (path2)
    """

    c = cdsapi.Client()
    # data download specifications:
    cls     = "ea"         # do not change
    expver  = "1"          # do not change
    levtype = "ml"         # do not change
    stream  = "oper"       # do not change
    date    = Year+'-'+Month+'-'+Day1+"/to/"+Year+'-'+Month+'-'+Day2 # date: Specify a single date as "2018-01-01" or a period as "2018-08-01/to/2018-01-31". For periods > 1 month see https://software.ecmwf.int/wiki/x/l7GqB
    tp      = "an"         ## type: Use "an" (analysis) unless you have a particular reason to use "fc" (forecast).
    time    = Time   # time: ERA5 data is hourly. Specify a single time as "00:00:00", or a range as "00:00:00/01:00:00/02:00:00" or "00:00:00/to/23:00:00/by/1".

    if 2006 >= int(Year) >= 2000:

        c.retrieve('reanalysis-era5.1-complete', {
            'class': cls,
            'date': date,
            'expver': expver,
            'levelist': '1/2/3/4/5/6/7/8/9/10/11/12/13/14/15/16/17/18/19/20/21/22/23/24/25/26/27/28/29/30/31/32/33/34/35/36/37/38/39/40/41/42/43/44/45/46/47/48/49/50/51/52/53/54/55/56/57/58/59/60/61/62/63/64/65/66/67/68/69/70/71/72/73/74/75/76/77/78/79/80/81/82/83/84/85/86/87/88/89/90/91/92/93/94/95/96/97/98/99/100/101/102/103/104/105/106/107/108/109/110/111/112/113/114/115/116/117/118/119/120/121/122/123/124/125/126/127/128/129/130/131/132/133/134/135/136/137',
            # For each of the 137 model levels
            'levtype': 'ml',
            'param': '130/133',  # Temperature (t) and specific humidity (q)
            'stream': stream,
            'time': time,
            'type': tp,
            'grid': Grid,
            # Latitude/longitude grid: east-west (longitude) and north-south resolution (latitude). Default: 0.25 x 0.25
            'area': Area,  # example: [60, -10, 50, 2], # North, West, South, East. Default: global
        }, path1)

        c.retrieve('reanalysis-era5.1-complete', {
            'class': cls,
            'date': date,
            'expver': expver,
            'levelist': '1',
            # Geopotential (z) and Logarithm of surface pressure (lnsp) are 2D fields, archived as model level 1
            'levtype': levtype,
            'param': '129/152',  # Geopotential (z) and Logarithm of surface pressure (lnsp)
            'stream': stream,
            'time': time,
            'type': tp,
            'grid': Grid,
            # Longitude/latitude grid: east-west (longitude) and north-south resolution (latitude). Default: 0.25 x 0.25
            'area': Area,  # example: [60, -10, 50, 2], # North, West, South, East. Default: global
        }, path2)

    else:
        c.retrieve('reanalysis-era5-complete', {
            'class'   : cls,
            'date'    : date,
            'expver'  : expver,
            'levelist': '1/2/3/4/5/6/7/8/9/10/11/12/13/14/15/16/17/18/19/20/21/22/23/24/25/26/27/28/29/30/31/32/33/34/35/36/37/38/39/40/41/42/43/44/45/46/47/48/49/50/51/52/53/54/55/56/57/58/59/60/61/62/63/64/65/66/67/68/69/70/71/72/73/74/75/76/77/78/79/80/81/82/83/84/85/86/87/88/89/90/91/92/93/94/95/96/97/98/99/100/101/102/103/104/105/106/107/108/109/110/111/112/113/114/115/116/117/118/119/120/121/122/123/124/125/126/127/128/129/130/131/132/133/134/135/136/137',         # For each of the 137 model levels
            'levtype' : 'ml',
            'param'   : '130/133', # Temperature (t) and specific humidity (q)
            'stream'  : stream,
            'time'    : time,
            'type'    : tp,
            'grid'    : Grid, # longitude/latitude grid: east-west (longitude) and north-south resolution (latitude). Default: 0.25 x 0.25
            'area'    : Area, #example: [60, -10, 50, 2], # North, West, South, East. Default: global
        }, path1)

        c.retrieve('reanalysis-era5-complete', {
            'class'   : cls,
            'date'    : date,
            'expver'  : expver,
            'levelist': '1',       # Geopotential (z) and Logarithm of surface pressure (lnsp) are 2D fields, archived as model level 1
            'levtype' : levtype,
            'param'   : '129/152', # Geopotential (z) and Logarithm of surface pressure (lnsp)
            'stream'  : stream,
            'time'    : time,
            'type'    : tp,
            'grid'    : Grid, # longitude/latitude grid: east-west (longitude) and north-south resolution (latitude). Default: 0.25 x 0.25
            'area'    : Area, #example: [60, -10, 50, 2], # North, West, South, East. Default: global
        }, path2)

