# This script preps the county level COVID data for he ultraCOVID project

# Importing required modules

import pandas as pd

# Specifying the path to the data -- update this accordingly!

username = ''
filepath = 'C:/Users/' + username + '/Documents/Data/ultraCOVID/'

# Reading in the COVID data sets

cases = pd.read_csv(filepath + 'time_series_covid19_confirmed_US.csv')
death = pd.read_csv(filepath + 'time_series_covid19_deaths_US.csv')

# Creating a list of all county level cases and deaths cumulative totals by day

case_vals = []
death_vals = []

for i in range(81,81+365):
    
    tmp = cases[list(cases.columns)[i]].to_list()
    
    for t in tmp:
        
        case_vals.append(t)

for i in range(82,82+365):
    
    tmp = cases[list(death.columns)[i]].to_list()
    
    for t in tmp:
        
        death_vals.append(t)

# Creating lists of other variables that will go into the dataframe

counties = cases['Admin2'].to_list()*365
states = cases['Province_State'].to_list()*365
fips = cases['FIPS'].to_list()*365
lat = cases['Lat'].to_list()*365
lon = cases['Long_'].to_list()*365
pop = death['Population'].to_list()*365

# Creating the dataframe for COVID data

counties = pd.Series(counties, name = 'County')
states = pd.Series(states, name = 'State')
fips = pd.Series(fips, name = 'FIPS')
lat = pd.Series(lat, name = 'Lat')
lon = pd.Series(lon, name = 'Lon')
pop = pd.Series(pop, name = 'Population')
case_vals = pd.Series(case_vals, name = 'Cumulative_Cases')
death_vals = pd.Series(death_vals, name = 'Cumulative_Deaths')

covidata = pd.concat([counties, states, fips, lat, lon, pop, case_vals, death_vals], axis = 1)

# Writing the dataframe as a csv

covidata.to_csv(filepath + 'covidata.csv', index = False)

