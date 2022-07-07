# -*- coding: utf-8 -*-

"""

DESCRIPTION

Format training data,

"""

# Import modulesn
import numpy as np
import pandas as pd
import glob
import os
from osgeo import gdal

# Define filepath
filepath = '../'

# Define destination
dest = '../training_data/'

# Get a list of training rasters
water = sorted(glob.glob(filepath + 'training_rasters/*water_shape.tif'))
ice = sorted(glob.glob(filepath + 'training_rasters/*ice_shape.tif'))
forest = sorted(glob.glob(filepath + 'training_rasters/*evergreen_shape.tif'))
grassland = sorted(glob.glob(filepath + 'training_rasters/*grasslands_shape.tif'))
shrub = sorted(glob.glob(filepath + 'training_rasters/*shrub_shape.tif'))
barren = sorted(glob.glob(filepath + 'training_rasters/*barren_shape.tif'))

# Define some functions
def geotiff_read(infile):
    """
    Function to read a Geotiff file and convert to numpy array.

    """
    # Allow GDAL to throw Python exceptions
    gdal.UseExceptions()

    # Read tiff and convert to a numpy array
    tiff = gdal.Open(infile)

    if tiff.RasterCount == 1:
        array = tiff.ReadAsArray()

    if tiff.RasterCount > 1:
        array = np.zeros((tiff.RasterYSize, tiff.RasterXSize, tiff.RasterCount))
        for i in range(tiff.RasterCount):
            band = tiff.GetRasterBand(i + 1)
            array[:, :, i] = band.ReadAsArray()

    # Get parameters
    geotransform = tiff.GetGeoTransform()
    projection = tiff.GetProjection()
    band = tiff.GetRasterBand(1)
    nodata = band.GetNoDataValue()

    return array, geotransform, projection, nodata


def make_training_data(band_list, label):

    """
    Function to format clipped raster training data for sci-kit learn

    """

    samples = []
    labels = []

    for i in band_list:
        # Read training rasters
        array, geotransform, projection, nodata = geotiff_read(i)

        # Put data into the right shape
        samples.append(list(np.ravel(array[array > 0])))

        # Add labels
        labels.append(np.repeat(label, len(list(np.ravel(array[array > 0])))))

    # Put into DataFrame
    samples_df = pd.DataFrame(samples).transpose()
#    samples_df.columns = ['B10', 'B11', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B9']
    samples_df.columns = ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7']
    labels_df = pd.DataFrame(labels[0])
    labels_df.columns = ['label']
    df = pd.merge(left=labels_df, right=samples_df, left_index=True, right_index=True)

    return df

water_df = make_training_data(water, 1)
ice_df = make_training_data(ice, 2)
forest_df = make_training_data(forest, 3)
grassland_df = make_training_data(grassland, 4)
shrub_df = make_training_data(shrub, 5)
barren_df = make_training_data(barren, 6)

#null_df = pd.DataFrame(np.zeros((200, 11)))
#null_df.columns = ['label', 'B10', 'B11', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B9']
null_df = pd.DataFrame(np.zeros((200, 8)))
null_df.columns = ['label', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7']

# Stack DataFrames
df = pd.concat((water_df, ice_df, forest_df, grassland_df, shrub_df, barren_df, null_df))

# Save to csv
df.to_csv(dest + 'training_data.csv', index=False)



























