import os
import pandas as pd
import numpy as np


'''Determine the watertype, redoxlevel, and POLIN (for parameters A and B only) of a number of 
example samples given in the spreadsheet, which can be downloaded from E-Campus XL. In your 
analysis make use of the Tables and Figures in Chapter 3 of the Lecture Notes (Mapping 
Hydrochemistry)'''

#fill directory
dir_ = 'C:/Users/svi002/OneDrive/GroundwatCh/IHE/THFSA/FLS/Assignment 4'

#molecular weights and ions datasets
mw_fn = 'mw.csv' 
ions_fn = 'ions.csv' #values in mg/L

os.chdir(dir_)
ions_df = pd.read_csv(ions_fn)
mw_df = pd.read_csv(mw_fn)

Cl_types_dict = {1: [[0,5],'Fresh', 'Oligohaline', 'G'],
 				 2: [[5,30], 'Fresh', 'Oligohaline-fresh', 'g'],
 				   3: [[30,150], 'Fresh', 'Fresh', 'F'],
                    4: [[150,300], 'Fresh', 'Fresh-brackish', 'f'],
 				   5: [[300, 1000], 'Brackish','Brackish', 'B'],
 				   6: [[1000,10000], 'Brackish', 'Brackish-salt', 'b'],
 				   7: [[10000,20000], 'Salt', 'Salt', 'S'],
 				   8: [[20000,1e30], 'Hypersaline', 'Hypersaline', 'H']}

Alk_types_dict = {1: [[0,31], 'Very low', '*'],
                  2: [[31,61], 'Low', 0],
                  3: [[61,122], 'Moderately low', 1],
                  4: [[122,244], 'Moderate', 2],
                  5: [[244,488], 'Moderately high', 3],
                  6: [[488,976], 'High', 4],
                  7: [[976, 1953], 'Very high', 5],
                  8: [[1953, 3905], 'Extreme', 6],
                  9: [[3905, 1e30] , 'Very extreme', 7]}
#simplified
Redox_index_dict = {'NO3': 1, 'Mn(2)':0.5, 'Fe(2)' : 0.25 , 'SO4': 0.9}
                              
#water type
#Cl concentration
Cl = ions_df['Cl']    
Cl_type_list = []
for sample in Cl:  
    for k,j in Cl_types_dict.items():  
        interval = j[0]       
        if (sample >= interval[0]) and (sample < interval[1]):
            Cl_type_list.append(j[3])
        continue
#Alkalinity
Alk = ions_df['HCO3']    
Alk_type_list = []
for sample in Alk:  
    for k,j in Alk_types_dict.items():  
        interval = j[0]       
        if (sample >= interval[0]) and (sample < interval[1]):
            Alk_type_list.append(j[2])
        continue

#Water type
cations1 = ['Mg', 'Ca']
cations2 = ['Fe(2)', 'Mn(2)']
cations3 = ['Na', 'K','NH4']
anions1 = ['HCO3']
anions2 = ['SO4', 'NO3']
anions3 = ['Cl']

ions_mmolL_df = ions_df.copy()
ions_meqL_df = ions_df.copy()
ions_convert = ions_df.columns[2:]
for ion in ions_convert:
    mw = mw_df[ion].values[0]
    concentration = ions_df[ion]
    concentration_meqL = concentration / mw    
    ions_mmolL_df [ion] = concentration_meqL
    
    cations1_ = ions_mmolL_df[cations1].sum(axis=1) * 2 #convert  to meq/ L
    cations2_ = ions_mmolL_df[cations2].sum(axis=1) * 2
    cations3_ = ions_mmolL_df[cations3].sum(axis=1) 
    anions1_ = ions_mmolL_df[anions1].sum(axis=1)
    anions2_ = ions_mmolL_df['SO4']*2 + ions_mmolL_df['NO3']
    anions3_ = ions_mmolL_df[anions3].sum(axis=1)
    ions_groups = [cations1_, cations2_, cations3_, anions1_, anions2_, anions3_]
    
    
    cations_group_df = pd.DataFrame([cations1_, cations2_, cations3_]).T
    cations_group_df.index +=1
    cations_group_df = cations_group_df.rename(columns = {0: '_'.join(cations1),
                                                          1: '_'.join(cations2),
                                                          2: '_'.join(cations3)})
    anions_group_df = pd.DataFrame([anions1_, anions2_, anions3_]).T
    anions_group_df.index +=1
    anions_group_df = anions_group_df.rename(columns = {0: '_'.join(anions1),
                                                          1: '_'.join(anions2),
                                                          2: '_'.join(anions3)})
    
    cations_type_df = cations_group_df.idxmax(axis=1)
    anions_type_df = anions_group_df.idxmax(axis=1)

ions_meqL_df[cations1] =  ions_mmolL_df[cations1] * 2
ions_meqL_df[cations2] =  ions_mmolL_df[cations2] * 2
ions_meqL_df[cations3] =  ions_mmolL_df[cations3] * 2
Watertype_list = []
for i in ions_meqL_df.index:
    sample = ions_meqL_df.iloc[i, :]
    majorcations_list = cations_type_df.iloc[i].split("_")
    majorcations_concentrations_df = sample[majorcations_list]
    majorcation = majorcations_concentrations_df.idxmax()
    
    #anions
    majoranions_list = anions_type_df.iloc[i].split("_")
    majoranions_concentrations_df = sample[majoranions_list]
    majoranion = majoranions_concentrations_df.idxmax()       
    Watertype_list.append('{}-{}'.format(majorcation,majoranion))



#redox index
redox_list = []
for i,sample in enumerate(ions_df.Example):
    series = ions_df.iloc[i,:]
    if (series['NO3'] > Redox_index_dict['NO3']) and (series['Mn(2)'] < Redox_index_dict['Mn(2)']):
        redox_list.append(['0-2','Suboxic'])
    else:
        if (series['Mn(2)'] > Redox_index_dict['Mn(2)']) and ((series['Fe(2)'] < Redox_index_dict['Fe(2)'])):
            redox_list.append(['3','Transition'])
        else:
            if (series['Fe(2)'] > Redox_index_dict['Fe(2)']) and ((series['SO4'] > Redox_index_dict['SO4'])):
                redox_list.append(['4','Sulphate-stable'])
            else:
                if ((series['SO4'] < Redox_index_dict['SO4'])):
                    redox_list.append(['5-6','Deep anoxic'])
                else:
                    redox_list.append(['4','Sulphate-stable'])
                    
        
#pollution index
#sulphate and pH only
A = np.round(1.333 * np.absolute(ions_df.pH - 7),2)

SO4c =  0.67 * ((ions_df.SO4/96) - (0.0232 * ions_df.Cl)/35.453)
SO4c = np.round(np.where(SO4c<0, 0, SO4c),2)

B = np.log(10* ((ions_df.NO3/62) + SO4c))/np.log(2)
B = np.round(np.where(B<0, 0, B), 2)

POLIN = np.round((A + B) / (2-(2/6)),2)

# output
output_df = pd.DataFrame(index = range(0,10))
output_df['Example'] = output_df.index + 1
output_df['Cl'] = Cl_type_list
output_df['Alkalinity'] = Alk_type_list
output_df['Watertype'] = Watertype_list
output_df[['Redox number', 'Redox State']] = redox_list
output_df['POLIN'] = POLIN
output_df.to_csv('output.csv', index = False)



