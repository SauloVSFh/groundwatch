import pandas as pd
import seaborn as sns
import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st

'''
Script to calculate the idf Intensity-duration-frequency curves based on a given input that is present on the folder 
data. It inverts the function for a given return period, calculates and plots the IDF.
'''

os.chdir('E:/OneDrive/git/hydrology/data')
database_df = pd.read_csv('YearlyMaximumDailyPrecipitation.csv')
Pmx_df = pd.read_csv('Pmx.csv')
savefig_fn = 'E:/OneDrive/0_IST_GroundwatCh/HWR/Assignment 5'

#Natural logarithm and statistical parameters
database_df['Ln_YearlyMaxDailyP'] = np.log(database_df.YearlyMaxDailyP)
Average_YearlyMaxDailyP = np.mean(database_df.YearlyMaxDailyP)
SD_YearlyMaxDailyP = np.std(database_df.YearlyMaxDailyP)
Average_Ln_YearlyMaxDailyP = np.mean(database_df.Ln_YearlyMaxDailyP)
SD_Ln_YearlyMaxDailyP = np.std(database_df.Ln_YearlyMaxDailyP)
skew = database_df['YearlyMaxDailyP'].skew()

#ECDF 
database_df = database_df.sort_values(by = 'YearlyMaxDailyP').iloc[:,1:].reset_index(drop = True)
database_df['F(X)'] = (database_df.index + 1) / (database_df.shape[0]+ 1) #probability of non-excedance

#Z-scores
'''z-scores are calculated considering that the data has a normal distribution,
which is not a common behavior to precipitation data. F(x) represents the cumulative
distribution function, also understood as the area undearneath the probability density
function. Z score values are computed passing the finding by passing the probability, 
(the area under the pdf or the F(x)) into the inverse cumulative distribution function
normalized with a standard deviation of 1 and a mean of 0. 

The same logics applies if we normalize our distribution first. We can later compute the
z-score values with the following formula:
    z = x - mi / sd
    
Below, after normalizing the data using scipy.stats, this formula is applied to check the
python codes. A conventional plot is also made to check the differences between the ECDF and 
Normalized distribution function.'''


database_df['InverseNormal'] = st.norm.ppf(database_df['F(X)'], loc = Average_YearlyMaxDailyP, scale = SD_YearlyMaxDailyP) 
database_df['Z-score'] = st.norm.ppf(database_df['F(X)']) 
#formula from class
# x = z * sd + mean
database_df['Z-score2'] = (database_df['InverseNormal'] - Average_YearlyMaxDailyP) / SD_YearlyMaxDailyP
database_df['InverseNormal2'] = database_df['Z-score'] * SD_YearlyMaxDailyP + Average_YearlyMaxDailyP



'''Modelling the functions

In hydrology, the plots to model the functions are based on the z-score values.
We plot the z-score values in the x-axis.
Then in the y-axis, we plot the actual precipitation values.
We also plot in the y-axis the values that are calculated according to the 
statistical laws we want to use to model our data. We compute than in the same way we find
the inverse normal values, but this time using other statistical laws'''

#Log-normal
equation_lognormal = SD_Ln_YearlyMaxDailyP * database_df['Z-score'] + Average_Ln_YearlyMaxDailyP
database_df['LogNormal'] = np.exp(equation_lognormal) 

#Gumbel
kp = (-np.sqrt(6) / np.pi) * (0.5772 + np.log(-np.log(database_df['F(X)'])))
database_df ['Gumbel'] = kp * SD_YearlyMaxDailyP + Average_YearlyMaxDailyP

#Pearson III
zp = database_df['Z-score']
kp = (2/skew)*(((1 + (zp * skew / 6) - (skew**2)/36))**3) - 2/skew
database_df['PearsonIII'] =  Average_YearlyMaxDailyP + kp * SD_YearlyMaxDailyP



'''deploying a log-normal function'''

#computing the precipitation values for given return periods (T)
T = np.array([2.33,20,50,100,1000])
FX = 1 - 1/T
Zscore = st.norm.ppf(FX)
#P = exp (mi + z * sigma)
LogNormalPrecipitation = np.exp(Average_Ln_YearlyMaxDailyP + Zscore * SD_Ln_YearlyMaxDailyP)
LogNormalPrecipitation_df = pd.DataFrame([T, LogNormalPrecipitation]).T.rename(columns = {0:'T',1:'P_mm'})

''' 
The downloaded data is correspondent to daily measurements colected 
from 9am. In order to find the peaks of precipitation with different duration
we check the following reference:
    
    Brandão, C., Rodrigues, R., & Costa, J. P. (2001).
    Análise de fenómenos extremos precipitações intensas em Portugal continental.
    Direcção dos serviços de recursos hıdricos, DSRH-INAG, Lisboa.
    
There we can find the ratios relative to daily precipitation for different durations
and return periods. We observe that the ratios don't change between the two return periods.
That means that no matter the intensity of the event, the ratio of precipitation
will be the same.

'''

Pmx_df[['Numerator','Denominator']] = Pmx_df.Ratios.str.split('/', expand = True)#.iloc[:,1:]
Pmx_df = Pmx_df.iloc[:,1:]

''''we need to break the dataframe into two pieces. The first one we'll use daily data to compute 
the precipitation maxima for different durations. The second one, we'll use the get the precipitation
for the duration computed with the previous step and then compute to durations lower than 1 hour
'''


Pmx_D_df = Pmx_df.loc [ Pmx_df.Denominator == 'Pmx_D']#get only the values referring to Day
Pmx_1_df = Pmx_df.loc [ Pmx_df.Denominator == 'Pmx_1h']#get only the values referring to 1 hour

#get the values for pre-established return periods
Daily_P_T100 = LogNormalPrecipitation_df.P_mm.loc[LogNormalPrecipitation_df['T'] == 100].values[0]
Daily_P_T1000 = LogNormalPrecipitation_df.P_mm.loc[LogNormalPrecipitation_df['T'] == 1000].values[0]
Pmx_D_df['T100_P_mm'] = Pmx_D_df.T100 * Daily_P_T100
Pmx_D_df['T1000_P_mm'] = Pmx_D_df.T1000 * Daily_P_T1000

# reminiscent durations using the same return period
# get the 1-hour precipitation value to compute the precipitation
Hourly_P_T100 = Pmx_D_df.T100_P_mm.loc[Pmx_D_df['Numerator'] == 'Pmx_1h'].values[0]
Hourly_P_T1000 = Pmx_D_df.T1000_P_mm.loc[Pmx_D_df['Numerator'] == 'Pmx_1h'].values[0]
Pmx_1_df['T100_P_mm'] = Pmx_1_df.T100 * Hourly_P_T100
Pmx_1_df['T1000_P_mm'] = Pmx_1_df.T1000 * Hourly_P_T1000

Pmx_df = Pmx_D_df.append(Pmx_1_df)
Pmx_df['Durations'] = [1, 6, 14, 5/60, 10/60, 0.25, .5]


# =============================================================================
# =============================================================================
# =============================================================================
# plotting data
# =============================================================================
# =============================================================================
# =============================================================================

#ECDF
fig = plt.figure(figsize = (10,10))
fig.add_subplot(111)
sns.scatterplot(x = 'YearlyMaxDailyP', y= 'F(X)', data = database_df)
plt.title('Empirical Cumulative Distribution')
plt.xlabel('Yearly maximum daily precipitation from 9 am (mm)')
fig.savefig(savefig_fn +'/Empirical Cumulative Distribution.jpg', dpi = 300)


#distribution of precipitation
fig.add_subplot(111)
g = sns.histplot(database_df['YearlyMaxDailyP'], bins = 20, stat = 'density', kde =True, label = 'Precipitation Record')
plt.xlim(30, 200)
plt.title('Distribution')
plt.xlabel('Yearly maximum daily precipitation from 9 am (mm)')
plt.vlines(x =Average_YearlyMaxDailyP, ymin = 0, ymax = 0.025, color = 'red', label = 'Average')
plt.legend()
fig.savefig(savefig_fn+'/Distribution.jpg', dpi = 300)
plt.show()


# =============================================================================
# #plotting z-score histogram
# =============================================================================
fig = plt.figure(figsize = (10,10))
fig.add_subplot(111)
sns.histplot(database_df['Z-score'], bins = 20, stat = 'density', kde =True, label = 'Precipitation Record')
fig.savefig(savefig_fn+'/Z-score Distribution.jpg', dpi = 300)

# =============================================================================
# #plotting ECDF and Normalized cumulative distribution function
# =============================================================================
fig = plt.figure(figsize = (10,10))
fig.add_subplot(111)
sns.scatterplot(x = 'YearlyMaxDailyP', y= 'F(X)', data = database_df, label = 'Yearly maximum daily precipitation')
sns.scatterplot(x = 'InverseNormal', y= 'F(X)', data = database_df, label = 'Normalized Yearly maximum daily precipitation')
plt.title('Empirical and Normalized Cumulative Distribution')
plt.xlabel('Yearly maximum daily precipitation from 9 am (mm)')
plt.show()


# =============================================================================
# Plotting the statistical laws
# =============================================================================
fig = plt.figure(figsize = (10,10))
fig.add_subplot(111)
sns.scatterplot(x = 'Z-score', y = 'YearlyMaxDailyP', data = database_df, label = 'Yearly maximum daily precipitation')
colors = ['r','b','g','y']
for i,model in enumerate(database_df.iloc[:,-4:].columns):
    sns.lineplot(x = 'Z-score2', y = model, data = database_df, label = model, color = colors[i])
fig.savefig(savefig_fn+'/StatisticalLaws.jpg', dpi = 300)
plt.show()


# =============================================================================
# Plotting the pdf curves
# =============================================================================

#plotting normal scale
fig, ax = plt.subplots(figsize=(10,10))
sns.scatterplot(x = 'Durations', y = 'T100_P_mm', data = Pmx_df,
                label = 'T = 100 years', color = 'b', ax=ax)
sns.scatterplot(x = 'Durations', y = 'T1000_P_mm', data = Pmx_df,
                label = 'T = 1000 years', color = 'g', ax=ax)
plt.title( 'Rainfall depth-duration-frequency curves')
fig.savefig(savefig_fn+'Rainfall depth-duration-frequency curves.jpg', dpi = 300)
plt.show()

#plotting bi-log scale
fig, ax = plt.subplots(figsize=(10,10))
ax.set(xscale="log", yscale="log")

sns.scatterplot(x = 'Durations', y = 'T100_P_mm', data = Pmx_df,
                label = 'T = 100 years', color = 'b', ax=ax)
sns.scatterplot(x = 'Durations', y = 'T1000_P_mm', data = Pmx_df,
                label = 'T = 1000 years', color = 'g', ax=ax)
plt.title( 'Rainfall depth-duration-frequency curves - Bilog')
fig.savefig(savefig_fn+'Rainfall depth-duration-frequency curves - Bilog.jpg', dpi = 300)
plt.show()


# =============================================================================



