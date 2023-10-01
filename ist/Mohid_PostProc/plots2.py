# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 15:01:03 2022
@author: Saulo da Silva Filho - SauloVSFh
"""

#alternative plotting option, check which one is the right: plot or plot 2

import numpy as np
import pandas as pd
from glob import glob
import os
import matplotlib.pyplot as plt
import seaborn as sns


#fill directories as text
basefolder = 'E:/OneDrive/0_IST_GroundwatCh/IRBM/Assignment_2'
resultsfolder = ['Results_NGS']
folders = {'Run4' : 'Reference Water Quality', 'Run5' : 'Water quality after irrigation '}
fn_extension= {7: '.srn', 8: '.srvg', 9: '.srvg', 11: '.srp'}  #header is the key and extension the value
figs_folder = 'E:/OneDrive/0_IST_GroundwatCh/IRBM/Assignment_2/Figures - Report'


os.chdir('E:/OneDrive/0_IST_GroundwatCh/IRBM/Assignment_2/Results_NGS/')


database = pd.read_csv('Run4-5_srpp.csv')
column = 'nitrate[mg/l]'

df = database.groupby(['scenario','id','YY','MM'])[column].mean().to_frame().reset_index()



# colors = ['b','r']
# column = 'nitrate_in_InfilColumn[mg/l]'


# fig, axs = plt.subplots(2,2, figsize=(20, 10), facecolor='w', edgecolor='k')
# fig.subplots_adjust(hspace = .5, wspace=.15)
# axs = axs.ravel()
# colors = ['b','r']

# for i, veg in enumerate (database.id.unique()):
#     df = database.loc [database.id == veg]
#     df = df.groupby(['scenario','id','YY','MM'])[column].mean().to_frame().reset_index()
#     dates = df.YY.astype('str').str[0:4] + '-' + df.MM.astype('str').str[:-2] + '-01'
#     df['dates'] = dates
#     df['dates'] = pd.to_datetime(df.dates, format = '%Y-%m-%d')

#     for j,sce in enumerate(df.scenario.unique()):
#         df_ = df.loc [ df.scenario == sce]
#         g = axs[i].plot(df_['dates'], df_[column], color = colors[j], linewidth = 3.5, label = sce, alpha = 0.75)
#         plt.xticks(rotation=45)
#         axs[i].tick_params(labelrotation=45)
#         title = veg.split('_')[0]
#         if title == 'Node':
#             title = veg
#         axs[i].set_title(title)  
#         axs[i].set_xlabel('')
#         # axs[i].set_ylabel(units, fontsize=16)
#         # axs[i].set_ylim(limits)
#         axs[i].legend ()
#     plt.xticks(rotation=45)
# plt.show()

