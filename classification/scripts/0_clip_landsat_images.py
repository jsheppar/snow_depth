#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Import and clip Landsat 8 imagery to basin.

"""

# Import modules
import glob
import subprocess
import os

# Define filepath
filepath = './landsat/'

# Define directory with images
images_winter = sorted(glob.glob(filepath + '*.TIF'))
#images_summer = sorted(glob.glob(filepath + 'LC80450312020149LGN00/analytic/*.TIF'))

#  Define mask
mask = './belknap_roi.shp'

# Define destination to save
dest = './landsat_clipped/'

def raster_clip(raster, shapefile, destination):
    """
    Function to clip raster(s) using a shapefile(s).
      
    """
    # Get path and filename seperately 
    rasterfilepath, rasterfilename = os.path.split(raster)
    # Get file name without extension            
    rasterfileshortname, rasterextension = os.path.splitext(rasterfilename)
    
    # Get path and filename seperately 
    shapefilepath, shapefilename = os.path.split(shapefile)
    # Get file name without extension            
    shapefileshortname, shapefileextension = os.path.splitext(shapefilename)
    
    print ('Clipping %s with %s' % (rasterfilename, shapefilename))
    
    subprocess.call(['gdalwarp', '-cutline', '--config', 'GDALWARP_IGNORE_BAD_CUTLINE', 
                     'YES', shapefile, '-crop_to_cutline', raster, 
                     destination + rasterfileshortname + '.tif'])
    
    return 1

for i in images_winter:
    raster_clip(i, mask, dest)

#for i in images_summer:
#    raster_clip(i, mask, dest)


