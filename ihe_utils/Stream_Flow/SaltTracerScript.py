import os
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt


'''This code is made to analyse salt tracer tests on stream using the dillution and the slug injection method.
    What it does:
        1 - find linear relationship between CE and concentration with field calibration data
        2 - convert field reading of CE into concentration of tracers
        3 - calculates the stream flow
        4 - calculates the velocities
        5 - plot calibration data
        6 - plot breakthrough curves
    '''
    
    
# start by filling variables
#stream data
L = 65 #m
salt_mass = 1e6 #mg
#data for calibration 
V0 = 500 #starting volume in mL
dV = 5 #volume added in each time step in mL
dC = 2 #concentration of tracer added in each time step in g/L
dt = 10 #time step in second


#program starts here
dir_ = 'C:/Users/svi002/OneDrive/GroundwatCh/IHE/THFSA/TH/Ex2' #folder with data
os.chdir(dir_)

fn1 = '02_calibration.csv' #.csv data for calibration
fn2 = '02_data.csv' #.csv database


V0 = 500 #starting volume in mL
dV = 5 #volume added in each time step in mL
dC = 2 #concentration of tracer added in each time step in g/L
''' dC = dm / dV -> dm = dC * dV
(g*1000)/(L/1000) * mL = (mg / mL * mL) = mg'''
dm = dV * dC # in mg

cal_df = pd.read_csv (fn1, sep = ';')
cal_df['Vt'] =  cal_df['Added_volume_mL'] + V0 #total volume in each time step
cal_df['mt'] = np.arange(0,cal_df.shape[0] * dm,dm) #total mass in mg
cal_df['Concentration_mgL-1'] = 1000 * cal_df['mt'] / cal_df['Vt']  


#linear regression to find linear equation parameters
x = np.array(cal_df['El_Cond_μScm-1']).reshape((-1, 1))
'''x because this array is required to be two-dimensional, or to be more precise, to have one column and as many rows as necessary.'''
y = np.array(cal_df['Concentration_mgL-1'])

#create a linear regression model and fit to the new arrays
model = LinearRegression().fit(x, y)
intercept = model.intercept_ 
slope = model.coef_

#open dataset with CE values and convert it to concentration
ds_df = pd.read_csv (fn2, sep =';')

ds_df['Concentration_mgL-1'] = slope*ds_df['El_Cond_μScm-1'] + intercept
ds_df.loc[ds_df['Concentration_mgL-1'] < 0, 'Concentration_mgL-1'] = 0


#recovery rate
ds_df['Acc_Concentration_mgL-1'] = ds_df['Concentration_mgL-1'].cumsum()

ds_df['Recovery'] = 100 * ds_df['Acc_Concentration_mgL-1'] / ds_df['Acc_Concentration_mgL-1'].max()


#runoff
integral = np.sum(ds_df['Concentration_mgL-1'] * dt) #mg*s / L
streamflow = salt_mass / integral #mg * L / (mg*s) = mg / s


#Vmax
firstreading = ds_df.loc [ds_df['Concentration_mgL-1'] > 0]['time_s'].iloc[0]
Vmax = L / firstreading

# #Vavg - wrong
# Vavg = L / ds_df['Concentration_mgL-1'].mean()

#Vmedian
Vmedian = L / ds_df['time_s'].median()


#outputs
ds_df.to_csv('Run_output.csv', sep=';')
f = open("run_output.txt", "w+")
f.write('Stream flow = {} L/s'.format(np.round(streamflow,2)))
f.write('\nMedian velocity = {} m/s'.format(np.round(Vmedian,2)))
f.write('\nMaximum velocity ={} m/s'.format(np.round(Vmax,2)))

f.write('\nHow to compute average velocity?')
f.close()



  
#plotting

#calibration
plt.scatter(x,y, marker ='x' , label = 'Field calibration')
xmodel = np.arange(500,900,10)
ymodel = slope*xmodel + intercept
plt.plot(xmodel, ymodel, color = 'black', linestyle ='--', label = 'Linear Regression')
plt.xlabel ('Electical conductivity [μS/cm]')
plt.ylabel ('Concentration [mg/L]')
plt.title('Field calibration data')
plt.show()

#BTC
fig = plt.figure(figsize = (15,7))

ax1 = fig.add_subplot(121)
ax1.plot(ds_df['time_s'], ds_df['El_Cond_μScm-1'], color = 'black', linestyle ='-')
fig.savefig('Calibration curve.jpg', dpi = 300)

ax2 = fig.add_subplot(122)
ax2.plot(ds_df['time_s'], ds_df['Concentration_mgL-1'], color = 'black', linestyle ='-', label = 'Breakthrough curve of tracer concentration')
ax3 = ax2.twinx()  # instantiate a second axes that shares the same x-axis
ax3.plot(ds_df['time_s'], ds_df['Recovery'], label = 'Recovery curve')


ax1.set_xlabel ('Time')
ax1.set_ylabel ('Electical conductivity [μS/cm]')
ax2.set_xlabel ('Time')
ax2.set_ylabel ('Concentration [mg/L]')
ax3.set_ylabel ('Recovery rate or trace %')
fig.suptitle('Breakthrough curves')
fig.savefig('Breakthrough curves.jpg', dpi = 300)







