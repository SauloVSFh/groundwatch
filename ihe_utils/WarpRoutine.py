import os
import numpy as np
from osgeo import gdal
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import rioxarray

folder = 'D:/My Documents/RemoteSensing/Data'

os.chdir(folder)

zones_fn = 'Topic2_Croptype_2019_32638.tif'
finalzones_fn = 'final_'+ zones_fn
ndvi_fn = 'NDVIAverage.tif'
temp_fn = 'TemperatureAverage.tif'
finalndvi_fn = 'final_'+ndvi_fn
finaltemp_fn = 'final_'+temp_fn

mis_fn = 'scheme_bdry.shp'


zones_ds = gdal.Open(zones_fn)
ndvi_ds = gdal.Open(ndvi_fn)
zones_ds = gdal.Open(zones_fn)

#getting data to warp rasters
minX, xres, xskew, maxY, yskew, yres  = zones_ds.GetGeoTransform()
maxX = minX + (zones_ds.RasterXSize * xres)
minY = maxY + (zones_ds.RasterXSize * yres)
newxRes = 30
newyRes = 30

gdal.Warp(finalndvi_fn, ndvi_fn,  outputBounds = (minX, minY, maxX, maxY) , 
          cutlineDSName=mis_fn,  dstNodata = np.nan, 
          xRes = newxRes, yRes = newyRes, resampleAlg = 'average') 

gdal.Warp(finaltemp_fn, temp_fn,  outputBounds = (minX, minY, maxX, maxY) , 
          cutlineDSName=mis_fn,  dstNodata = np.nan, 
          xRes = newxRes, yRes = newyRes, resampleAlg = 'average') 

gdal.Warp(finalzones_fn, zones_fn, outputBounds = (minX, minY, maxX, maxY) , 
          cutlineDSName=mis_fn,  dstNodata = np.nan, 
          xRes = newxRes, yRes = newyRes, resampleAlg = 'average') 





# gdal.Warp(finalndvi_fn, ndvi_fn,  cutlineDSName=mis_fn, dstNodata = 0)  
# zones_arr = zones_ds.GetRasterBand(1).ReadAsArray()
# ndvi_arr = ndvi_ds.GetRasterBand(1).ReadAsArray()

# print(gdf_.crs)
# print(zones_arr.shape [0] / zones_arr.shape [1] , ndvi_arr.shape [0] / ndvi_arr.shape [1])
# print(zones_arr.shape , ndvi_arr.shape )
print(maxX, maxY)
# plt.imshow(ndvi_arr)