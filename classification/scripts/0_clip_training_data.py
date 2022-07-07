#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
DESCRIPTION

Clip the Landsat imagery with training data.

"""

# Import modules
import glob
import subprocess
import os

# Define filepath
filepath = '../shapes/'

# Define directory with images ([:-1] because we don't need BQA band)
rasters = sorted(glob.glob(filepath + '../landsat/LC08_L2SP_045029_20200901_20200906_02_T1/LC08_L2SP_045029_20200901_20200906_02_T1_SR_B*.TIF'))

print(rasters)

# Define destination
dest = '../training_rasters/'

# Shapefiles
water = filepath + 'water_shape.shp'
ice = filepath + 'ice_shape.shp'
forest = filepath + 'evergreen_shape.shp'
grassland = filepath + 'grasslands_shape.shp'
shrub = filepath + 'shrub_shape.shp'
barren = filepath + 'barren_shape.shp'

def raster_clip(raster, shapefile):
    """
    Function to clip raster(s) using a shapefile.

    """
    # Get path and filename seperately
    rasterfilepath, rasterfilename = os.path.split(raster)
    # Get file name without extension
    rasterfileshortname, rasterextension = os.path.splitext(rasterfilename)

    # Get path and filename seperately
    shapefilepath, shapefilename = os.path.split(shapefile)
    # Get file name without extension
    shapefileshortname, shapefileextension = os.path.splitext(shapefilename)

    print ('Clipping %s.tif with %s.shp' % (rasterfileshortname, shapefileshortname))

    subprocess.call(['gdalwarp', '-cutline', shapefile, '-crop_to_cutline',
                     raster, dest + rasterfileshortname + '_' + shapefileshortname + '.tif'])

    return 1

for i in range(len(rasters)):
    raster_clip(rasters[i], water)
    raster_clip(rasters[i], ice)
    raster_clip(rasters[i], forest)
    raster_clip(rasters[i], grassland)
    raster_clip(rasters[i], shrub)
    raster_clip(rasters[i], barren)





