"""
Created on Wed Feb 16 14:56:42 2022
Mohid post-processing
@author: Saulo da Silva Filho - SauloVSFh
"""

#code to contrast 4 different node timeseries in 3 different scenarios accumulated by month

import numpy as np
import pandas as pd
from glob import glob
import os
import matplotlib.pyplot as plt


#fill directories as text
basefolder = 'E:/OneDrive/0_IST_GroundwatCh/IRBM/Assignment_2'
resultsfolder = ['Results_NGS'] 
folders = {'Run4' : 'Reference Water Quality', 'Run5' : 'Water quality after irrigation '}
fn_extension= {7: '.srn', 8: '.srvg', 9: '.srvg', 11: '.srp'}  #header is the key and extension the value
figs_folder = 'E:/OneDrive/0_IST_GroundwatCh/IRBM/Assignment_2/Figures - Report'

plotting = {'.srpp' : {9 : {'channel_flow':['m³/s',[0,200]]}},
            '.srrp' : {8 : {'WaterStressFactor': ['', [0,1.2]], 'leaf_area_index': ['m²/m²',[0,5]],
                            'total_plant_biomass': ['kg/ha',[0,7e4]] }}}
   


os.chdir(basefolder)

#iterate through resultsfolder
for member in resultsfolder:
    os.chdir(member)
    #iterate through extensions
    for k1,v1 in plotting.items():
        fn_extension = k1 #choosing one extension
        header = list(v1.items())[0][0] #header to locate the column
        database = pd.DataFrame() #dataframe to append different runs of the model with the same extension
        #iterate through results
        for folder, scenario in folders.items():
            os.chdir(folder)            
            files = [ file for file in os.listdir() if file.endswith(fn_extension)] #select extensions         
            #iterate through the files within a certain extension to open it and append to dataframe
            for file in files:
                df = pd.read_csv(file, header = header, delim_whitespace=True)
                df.head()
                df = df.loc [~np.isnan(df.YY)]
                df['scenario'] = scenario
                df['extension'] = fn_extension
                ID = file.split('.')[0]
                df['id'] = ID
                df = df.loc[df.YY <=2006.0] #select period of interest
                database = database.append(df)
                fn = member+ fn_extension+ folder+ file
                print(fn)
            os.chdir('../')
        dates = df.YY.astype('str').str[0:4] + '-' + df.MM.astype('str').str[:-2] + '-01'
        database['dates'] = dates
        database['dates'] = pd.to_datetime(database.dates, format = '%Y-%m-%d')
        # database = database.iloc[:,7:]
        database.to_csv('E:\\OneDrive\\0_IST_GroundwatCh\\IRBM\\Assignment_2\\Results_NGS\\Run4-5_{}.csv'.format(fn_extension[1:]))
                
                