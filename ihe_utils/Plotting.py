import os 
import rioxarray as rxr
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def PlotCatRaster(TifFile, Labels_dict):
    zones_ds = rxr.open_rasterio(zones_fn, masked = True)
    zones_arr = zones_ds.to_numpy()
    zones_arr_im = zones_arr[0]
    values = np.unique(zones_arr_im.ravel())
    values = values[~np.isnan(values)]
    xmin = zones_ds.x.min().values
    xmax = zones_ds.x.max().values
    ymin = zones_ds.y.min().values
    ymax = zones_ds.y.max().values
    extent = [xmin, xmax, ymin, ymax]
    im = plt.imshow(zones_arr_im, extent = extent)
    # get the colors of the values, according to the 
    # colormap used by imshow
    colors = [ im.cmap(im.norm(value)) for value in values]
    # create a patch (proxy artist) for every color 
    patches = [ mpatches.Patch(color=colors[k], label= v) for k,v in labels_dict.items() ]
    # patches = [ mpatches.Patch(color=colors[i], label= labels_dict.items()[i] ) for i in range(len(values))]
    # put those patched as legend-handles into the legend
    plt.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0. )  
    plt.show()