# ERA5 Reanalyses Downloader and Processor

## Overview

This repository contains scripts designed to download and process ERA5 reanalysis data. The script `test_year_1999.nc` downloads temperature (t) and specific humidity (q) on 137 hybrid levels, and geopotential (z) and log of surface pressure (lnsp) on one level for a specified grid and year. These data are first downloaded and saved in the '/Data/1999' directory. These variables are then used to compute geopotential (z) on 137 levels. The interpolated temperature and pressure fields on the chosen altitude range are saved in the `/Outputs` directory as NetCDF files.

## Contents

- `test_year_1999.nc`: Main script for downloading and processing ERA5 reanalysis data.
- `/Outputs`: Directory where the processed NetCDF files are saved.

## Installation

To run the scripts, you need to have Python installed along with the necessary libraries. You can install the required dependencies using the provided `requirements.txt` file.

```bash
pip install -r requirements.txt

## Dependencies

- Python 3.x
- Required Python libraries (listed in requirements.txt)

## Acknowledgments

This work makes use of the ERA5 reanalysis data provided by the European Centre for Medium-Range Weather Forecasts (ECMWF).