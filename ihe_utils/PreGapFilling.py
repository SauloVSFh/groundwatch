import os
import shutil

SEBAL_out_dir = 'D:\My Documents\RemoteSensing\Assignment\Part2\SebalData\SEBAL_Out'
vars_list = ['Output_biomass_production', 'Output_evapotranspiration', 'Output_vegetation']

prefix_list = ['L8_Biomass_prod', 'L8_ETact_', 'L8_NDVI']
output_folder = '_NDVI_'
filesout_dir = 'D:\My Documents\RemoteSensing\Assignment\Part2\SebalData\SEBAL_Out\GapFilling\{}'.format(output_folder)

os.chdir (SEBAL_out_dir)
folders_list = os.listdir()
folders_list = [folder for folder in folders_list if folder.startswith('LC')]

var = vars_list [2]
prefix = prefix_list[2] 
# for folder in folders_list:
#     path = folder+'/{}'.format(var)
#     os.chdir(path) #evapotranspiration files
#     files_list = os.listdir()
#     file = [file for file in files_list if prefix in file]
#     shutil.copy(file[0],filesout_dir )
#     os.chdir('../')
    # os.chdir('../')
    # print(path)

