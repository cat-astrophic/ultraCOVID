# This script preps the county level COVID data for he ultraCOVID project

# Importing required modules

import pandas as pd
import numpy as np
import datetime

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
d0 = datetime.datetime.strptime('April 1, 2020', '%B %d, %Y')
dates_tmp = [[d0+datetime.timedelta(i)]*len(cases) for i in range(365)]
dates = [i for j in dates_tmp for i in j]

# Creating the dataframe for COVID data

counties = pd.Series(counties, name = 'County')
states = pd.Series(states, name = 'State')
fips = pd.Series(fips, name = 'FIPS')
lat = pd.Series(lat, name = 'Lat')
lon = pd.Series(lon, name = 'Lon')
pop = pd.Series(pop, name = 'Population')
dates = pd.Series(dates, name = 'Date')
case_vals = pd.Series(case_vals, name = 'Cumulative_Cases')
death_vals = pd.Series(death_vals, name = 'Cumulative_Deaths')

covidata = pd.concat([counties, states, fips, lat, lon, pop, dates, case_vals, death_vals], axis = 1)

# Computing moving averages for cases and deaths by county

# First is creating differenced data in the format of the input files

casesdiff = cases[[c for c in cases.columns[0:11]]]
deathdiff = death[[d for d in death.columns[0:12]]]

for c in range(51,81+365):
    
    tmp = cases[cases.columns[c]] - cases[cases.columns[c-1]]
    casesdiff = pd.concat([casesdiff, pd.Series(tmp, name = cases.columns[c])], axis = 1)

for d in range(52,82+365):
    
    tmp = death[death.columns[d]] - death[death.columns[d-1]]
    deathdiff = pd.concat([deathdiff, pd.Series(tmp, name = death.columns[d])], axis = 1)

# Second is creating 7 day MAs

cases7 = cases[[c for c in cases.columns[0:11]]]
death7 = death[[d for d in death.columns[0:12]]]

for c in range(41,41+365):
    
    tmpl = [casesdiff[casesdiff.columns[c-i]].to_list() for i in range(7)]
    tmp = [(1/7)*sum(z) for z in zip(*tmpl)]
    cases7 = pd.concat([cases7, pd.Series(tmp, name = casesdiff.columns[c])], axis = 1)

for d in range(42,42+365):
    
    tmpl = [deathdiff[deathdiff.columns[d-i]] for i in range(7)]
    tmp = [(1/7)*sum(z) for z in zip(*tmpl)]
    death7 = pd.concat([death7, pd.Series(tmp, name = deathdiff.columns[d])], axis = 1)

# Third is creating 14 day MAs

cases14 = cases[[c for c in cases.columns[0:11]]]
death14 = death[[d for d in death.columns[0:12]]]

for c in range(41,41+365):
    
    tmpl = [casesdiff[casesdiff.columns[c-i]].to_list() for i in range(14)]
    tmp = [(1/14)*sum(z) for z in zip(*tmpl)]
    cases14 = pd.concat([cases14, pd.Series(tmp, name = casesdiff.columns[c])], axis = 1)

for d in range(42,42+365):
    
    tmpl = [deathdiff[deathdiff.columns[d-i]] for i in range(14)]
    tmp = [(1/14)*sum(z) for z in zip(*tmpl)]
    death14 = pd.concat([death14, pd.Series(tmp, name = deathdiff.columns[d])], axis = 1)
    
# Fourth is creating 30 day MAs

cases30 = cases[[c for c in cases.columns[0:11]]]
death30 = death[[d for d in death.columns[0:12]]]

for c in range(41,41+365):
    
    tmpl = [casesdiff[casesdiff.columns[c-i]].to_list() for i in range(30)]
    tmp = [(1/30)*sum(z) for z in zip(*tmpl)]
    cases30 = pd.concat([cases30, pd.Series(tmp, name = casesdiff.columns[c])], axis = 1)

for d in range(42,42+365):
    
    tmpl = [deathdiff[deathdiff.columns[d-i]] for i in range(30)]
    tmp = [(1/30)*sum(z) for z in zip(*tmpl)]
    death30 = pd.concat([death30, pd.Series(tmp, name = deathdiff.columns[d])], axis = 1)

# Coverting this into covidata formatting

# NOTE: Since some of the original JHU time series data contains decreases in total cases
#       in a given county, a floor of 0 is put in place for all moving averages as,
#       essentially, a means of data smoothing

case_vals7 = []
death_vals7 = []
case_vals14 = []
death_vals14 = []
case_vals30 = []
death_vals30 = []

for i in range(11,11+365):
    
    tmp7 = cases7[list(cases7.columns)[i]].to_list()
    tmp14 = cases14[list(cases14.columns)[i]].to_list()
    tmp30 = cases30[list(cases30.columns)[i]].to_list()
    
    for t in tmp7:
        
        case_vals7.append(max(t,0))
        
    for t in tmp14:
        
        case_vals14.append(max(t,0))
        
    for t in tmp30:
        
        case_vals30.append(max(t,0))

for i in range(12,12+365):
    
    tmp7 = death7[list(death7.columns)[i]].to_list()
    tmp14 = death14[list(death14.columns)[i]].to_list()
    tmp30 = death30[list(death30.columns)[i]].to_list()
    
    for t in tmp7:
        
        death_vals7.append(max(t,0))
        
    for t in tmp14:
        
        death_vals14.append(max(t,0))
        
    for t in tmp30:
        
        death_vals30.append(max(t,0))

# Expanding the dataframe for COVID data

case_vals7 = pd.Series(case_vals7, name = 'Cases_MA_7')
death_vals7 = pd.Series(death_vals7, name = 'Deaths_MA_7')
case_vals14 = pd.Series(case_vals14, name = 'Cases_MA_14')
death_vals14 = pd.Series(death_vals14, name = 'Deaths_MA_14')
case_vals30 = pd.Series(case_vals30, name = 'Cases_MA_30')
death_vals30 = pd.Series(death_vals30, name = 'Deaths_MA_30')

covidata = pd.concat([covidata, case_vals7, death_vals7, case_vals14, death_vals14, case_vals30, death_vals30], axis = 1)

# Repeating the above computations at the state level

# Reading in the city to county map

ccmap = pd.read_csv(filepath + 'ccmap.csv', sep = '|')

# Updating state names in ccmap to match naming conventions

ccmap = ccmap.replace(to_replace = 'Washington, D.C.', value = 'District of Columbia')

# Create lists of state names from the two data frames

allstates_cases = list(sorted(list(cases.Province_State.unique())))
tempstates = list(ccmap['State full'].unique())
tempstates.remove(np.nan)
allstates_ccmap = list(sorted(tempstates))

# Removing extra data from the two dataframes (e.g., non-state entries that appear in only one df)

ccmap = ccmap[ccmap['State full'].isin(allstates_cases)].reset_index(drop = True)
covidata = covidata[covidata['State'].isin(allstates_ccmap)].reset_index(drop = True)

# Initialize the lists for state data

states = list(covidata.State.unique())
state_cum_cases = []
state_cum_deaths = []
state_7_cases = []
state_7_deaths = []
state_14_cases = []
state_14_deaths = []
state_30_cases = []
state_30_deaths = []

# Fill the raw_state_data lists with differenced data for each state-day

for s in range(len(states)):
    
    tmpc = covidata[covidata['State'] == states[s]]
    tmp1 = []
    tmp2 = []
    tmp3 = []
    tmp4 = []
    tmp5 = []
    tmp6 = []
    tmp7 = []
    tmp8 = []
    
    for day in list(tmpc.Date.unique()):
        
        tmpc2 = tmpc[tmpc['Date'] == day]
        tmp1.append(sum(tmpc2['Cumulative_Cases']))
        tmp2.append(sum(tmpc2['Cumulative_Deaths']))
        tmp3.append(sum(tmpc2['Cases_MA_7']))
        tmp4.append(sum(tmpc2['Deaths_MA_7']))
        tmp5.append(sum(tmpc2['Cases_MA_14']))
        tmp6.append(sum(tmpc2['Deaths_MA_14']))
        tmp7.append(sum(tmpc2['Cases_MA_30']))
        tmp8.append(sum(tmpc2['Deaths_MA_30']))
        
    state_cum_cases.append(tmp1)
    state_cum_deaths.append(tmp2)
    state_7_cases.append(tmp3)
    state_7_deaths.append(tmp4)
    state_14_cases.append(tmp5)
    state_14_deaths.append(tmp6)
    state_30_cases.append(tmp7)
    state_30_deaths.append(tmp8)
    
# Adding this data to the covidata dataframe

days = list(dates.unique())

st_cum_cases = []
st_cum_deaths = []
st_ma7_cases = []
st_ma7_deaths = []
st_ma14_cases = []
st_ma14_deaths = []
st_ma30_cases = []
st_ma30_deaths = []

for row in range(len(covidata)):
    
    st = covidata.State[row]
    dt = covidata.Date[row]
    
    sti = states.index(st)
    dti = days.index(dt)
    
    st_cum_cases.append(state_cum_cases[sti][dti])
    st_cum_deaths.append(state_cum_deaths[sti][dti])
    st_ma7_cases.append(state_7_cases[sti][dti])
    st_ma7_deaths.append(state_7_deaths[sti][dti])
    st_ma14_cases.append(state_14_cases[sti][dti])
    st_ma14_deaths.append(state_14_deaths[sti][dti])
    st_ma30_cases.append(state_30_cases[sti][dti])
    st_ma30_deaths.append(state_30_deaths[sti][dti])
    
st_cum_cases = pd.Series(st_cum_cases, name = 'Cumulative_Cases_State')
st_cum_deaths = pd.Series(st_cum_deaths, name = 'Cumulative_Deaths_State')
st_ma7_cases = pd.Series(st_ma7_cases, name = 'Cases_MA_7_State')
st_ma7_deaths = pd.Series(st_ma7_deaths, name = 'Deaths_MA_7_State')
st_ma14_cases = pd.Series(st_ma14_cases, name = 'Cases_MA_14_State')
st_ma14_deaths = pd.Series(st_ma14_deaths, name = 'Deaths_MA_14_State')
st_ma30_cases = pd.Series(st_ma30_cases, name = 'Cases_MA_30_State')
st_ma30_deaths = pd.Series(st_ma30_deaths, name = 'Deaths_MA_30_State')

covidata = pd.concat([covidata, st_cum_cases, st_cum_deaths, st_ma7_cases, st_ma7_deaths, st_ma14_cases, st_ma14_deaths, st_ma30_cases, st_ma30_deaths], axis = 1)

# Writing the dataframe as a csv

covidata.to_csv(filepath + 'covidata.csv', index = False)

