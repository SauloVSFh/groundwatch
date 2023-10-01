import os
import numpy as np
from osgeo import gdal
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import rioxarray
from scipy import stats as st
folder = 'D:/My Documents/RemoteSensing/Data'

os.chdir(folder)

zones_fn = 'final_Topic2_Croptype_2019_32638.tif'
ndvi_fn = 'final_NDVIAverage.tif'
temp_fn = 'final_TemperatureAverage.tif'


zones_ds = gdal.Open(zones_fn)
ndvi_ds = gdal.Open(ndvi_fn)
temp_ds = gdal.Open(temp_fn)


zones_arr = zones_ds.GetRasterBand(1).ReadAsArray()
ndvi_arr = ndvi_ds.GetRasterBand(1).ReadAsArray()
temp_arr = temp_ds.GetRasterBand(1).ReadAsArray()

minX, xres, xskew, maxY, yskew, yres  = zones_ds.GetGeoTransform()
pixelArea = np.abs(xres * yres)
RasterArea = (zones_arr[np.isin(zones_arr , np.arange(1,11,1))]).shape[0] * pixelArea / 1e6

area_dict = {}
labels_dict = {1: 'Builtup', 2: 'Alfalfa', 3 : 'Apple and Pear', 4 : 'Grapes', 5 : 'Sugar beet', 
               6 : 'Wheat and Barley', 7 : 'Fall Irrigated vegetable', 8 : 'Bareland', 9: 'Others', 10 : 'Water'}

# report function
zones = np.arange(1,11)
output= 'CropType2019Report.txt'
def RasterReport (Raster, zones, LabelsDict, output):
    zones_fn = Raster
    zones_ds = gdal.Open(zones_fn)
    zones_arr = zones_ds.GetRasterBand(1).ReadAsArray()
    for zone in zones:
        label = LabelsDict[zone]
        index_arr = np.where(zones_arr == zone , 1, np.nan)
        index_size = index_arr[index_arr==1].size
        zone_area = index_size * pixelArea
        area_dict[label] = zone_area
    with open (output, '+w') as f:
        for k, v in area_dict.items():
            f.write(k + ' : ' + str(v)+ '\n')  


def ZonalStatRastertoRaster (ZoningArray, MapArray, CsvOutputName, LabelsDict):
    #arrays must have the same shape!!!
    zone_stat_dict = {}
    for zone in np.arange(1,11):
        index_arr = np.where(ZoningArray == zone , 1, np.nan)
        arr_ = np.where ( index_arr == 1, MapArray, np.nan)
        arr_2 = MapArray[~np.isnan(arr_)]
        zone_stat_dict [LabelsDict[zone]]  = [np.min (arr_2),
                                               np.round(arr_2.max(),3),
                                               np.round(arr_2.mean(),3),
                                               np.round(np.abs(arr_2).mean(),3),
                                               np.round(arr_2.var(),3),
                                               np.round(arr_2.std(),3)]
        
    columns = ['min', 'max', 'mean' , 'mean_of_abs', 'var', 'std']
    df = pd.DataFrame.from_dict(zone_stat_dict).T
    df.columns = columns
    df.to_csv(CsvOutputName)


#workflow
RasterReport(zones_fn, zones, labels_dict, output)
ZonalStatRastertoRaster(zones_arr, ndvi_arr, 'NDVI_ZonalStat.csv', labels_dict)
ZonalStatRastertoRaster(temp_arr, ndvi_arr, 'Temp_ZonalStat.csv', labels_dict)    

