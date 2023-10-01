import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#fill directories as text
basefolder = 'E:/OneDrive/0_IST_GroundwatCh/IRBM/Assignment_2/Results_NGS'
folders = {'Run4' : 'Reference Water Quality', 'Run5' : 'Water quality after fertilization '}
header = 7 #header is the key and extension the value
extension = '.srn'
figs_folder = 'E:/OneDrive/0_IST_GroundwatCh/IRBM/Assignment_2/Figures - Report'

files = os.listdir()

database = pd.DataFrame()

os.chdir(basefolder)
for folder, scenario in folders.items():
    os.chdir(folder)            
    files = [ file for file in os.listdir() if file.endswith(extension)] #select extensions         
    #iterate through the files within a certain extension to open it and append to dataframe
    for file in files:
        df = pd.read_csv(file, header = header, delim_whitespace=True)
        df = df.loc [~np.isnan(df.YY)]
        df['scenario'] = scenario
        df['extension'] = extension
        ID = file.split('.')[0]
        df['id'] = ID
        database = database.append(df)
    os.chdir('../')
dates = df.YY.astype('str').str[0:4] + '-' + df.MM.astype('str').str[:-2] + '-01'
database['dates'] = dates
database['dates'] = pd.to_datetime(database.dates, format = '%Y-%m-%d')
# database = database.iloc[:,7:]
print('database')
database = database.loc [database.MM < 7]
database.to_csv('E:\\OneDrive\\0_IST_GroundwatCh\\IRBM\\Assignment_2\\Results_NGS\\Run4-5_{}.csv'.format(extension[1:]))
