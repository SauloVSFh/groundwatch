"""
Mohid post-processing
Copyright 2021 Saulo da Silva Filho - SauloVSFh
"""

#code to contrast 4 different node timeseries in 3 different scenarios accumulated by month

import numpy as np
import pandas as pd
from glob import glob
import os
import matplotlib.pyplot as plt


#fill directories as text
basefolder = 'E:/OneDrive/0_IST_GroundwatCh/IRBM/Assignment_2' 
resultsfolder = ['Results_SVSF']
folders = {'Run1' : 'Reference', 'Run2' : 'Pristine', 'Run3': 'Irrigation'} #scenarios
fn_extension= {7: '.srn', 8: '.srvg', 9: '.srvg', 11: '.srp'}  #header is the key and extension the value
figs_folder = 'E:/OneDrive/0_IST_GroundwatCh/IRBM/Assignment_2/Figures - Report'


plotting = {'.srn' : {7 : {'channel_flow':['hm³',[0,150]]}},
            '.srvg' : {8 : {'WaterStressFactor': ['', [0,1.2]], 'leaf_area_index': ['m²/m²',[0,5]], 'total_plant_biomass': ['kg/ha',[0,7e4]] }},  #adimensional units
            '.srb' : {9 : {'EvapoTranspiration_Rate_[mm/hour]': ['mm/hour',[0,0.3]]}},
            '.srp' : {11: {'water_table_depth_[m]' : ['m',[0,3]]}}}   
   
#choose extension of directory
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
                # database.to_csv(fn+'.csv')
            os.chdir('../')
        #database with the aimed extension and containing all the scenarios is ready
        
        os.chdir(figs_folder) #folder to save it
        #loop through the data to plot it
        for k2,v2 in v1.items():
            for k3,v3 in v2.items():
                #choose column to plot
                column = k3
                units = v3[0] #choose limits of y_axis
                limits = v3[1]

                fig, axs = plt.subplots(2,2, figsize=(20, 10), facecolor='w', edgecolor='k')
                fig.subplots_adjust(hspace = .25, wspace=.15)
                axs = axs.ravel()
                colors = {'Irrigation' : 'blue', 'Pristine' : 'green', 'Reference' : 'red'}
                dates = database.YY.astype('str').str[0:4] + '-' + database.MM.astype('str').str[:-2] + '-' + database.DD.astype('str').str[:-2] + '-'+ database.hh.astype('str').str[:-2]
                database['dates'] = pd.to_datetime(dates, format = '%Y-%m-%d-%H')

                for i, veg in enumerate (database.id.unique()):
                    df = database.loc [database.id == veg]
                    df1=df
                    if df.extension.unique()[0] != '.srvg':
                        df1 = df.groupby(['scenario','id',df['dates'].dt.month])[column].mean().to_frame().reset_index()
                    

                    for j,sce in enumerate(df1.scenario.unique()):
                        df_ = df1.loc [ df1.scenario == sce]
                        g = axs[i].plot(df_['dates'], df_[column], color = colors[sce], linewidth = 3.5, label = sce, alpha = 0.60)
                        axs[i].tick_params(axis = 'x', labelrotation=0)
                        title = veg.split('_')[0]
                        if title == 'Node':
                            title = veg
                        axs[i].set_title(title, fontsize = 18)  
                        axs[i].set_xlabel('')
                        axs[i].set_ylabel(units, fontsize=16)
                        axs[i].set_ylim(limits)
                        axs[i].legend ()
                        if df.extension.unique()[0] != '.srvg':
                            axs[i].set_xlabel('Month',fontsize=16)
                        if i in [1,3]:
                            axs[i].set_ylabel('')
                        if i<3:
                            axs[i].get_legend().remove()
                        

                    fig_fn = member + '_' + column.split('[')[0] + '.jpg'

                    os.chdir('E:\\OneDrive\\0_IST_GroundwatCh\\IRBM\\Assignment_2\\Figures - Report')
                    
                    fig.savefig(fig_fn, dpi = 300)
                    print(os.getcwd())
        #finish plotting the given extension. Go back to the member folder to get other extension
        os.chdir(basefolder+'/'+member)
    os.chdir('../') #change to basefolder again
    print('\n\n\nNext member\n\n\n')