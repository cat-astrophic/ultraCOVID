# This script blends the covidata and racedata (d) dataframes

# Importing required modules

import pandas as pd
import datetime

# Specifying the path to the data -- update this accordingly!

username = ''
filepath = 'C:/Users/' + username + '/Documents/Data/ultraCOVID/'

# Reading in the COVID data sets

racedata = pd.read_csv(filepath + 'd.csv')
covidata = pd.read_csv(filepath + 'covidata.csv')

# Reading in the city to county map

ccmap = pd.read_csv(filepath + 'ccmap.csv', sep = '|')

# Updating state names in ccmap to match naming conventions

ccmap = ccmap.replace(to_replace = 'Washington, D.C.', value = 'District of Columbia')

# Establishing a naming convention for counties across data sets

covidata['County'] = covidata['County'].str.lower()
ccmap['County'] = ccmap['County'].str.lower()

# Drop Canadian runners from the data since the covid data is for the US

racedata = racedata[racedata.Country == 'USA'].reset_index(drop = True)

# Drop events which occured twice in the pre-covid period

racedata['Next_Year_Event_Date'] = pd.to_datetime(racedata['Next_Year_Event_Date'])
racedata['NY_Event_Date_PM1'] = pd.to_datetime(racedata['NY_Event_Date_PM1'])
racedata = racedata[racedata['NY_Event_Date_PM1'] >= datetime.datetime.strptime('2020-04-01', '%Y-%m-%d')].reset_index(drop = True)
racedata = racedata[racedata['NY_Event_Date_PM1'] < datetime.datetime.strptime('2021-04-01', '%Y-%m-%d')].reset_index(drop = True)

# Converting covidata dates to datetime format

covidata['Date'] = pd.to_datetime(covidata['Date'])

# Defining a helper function for runner location covid data

def covid_rnr(inp):
    
    city = inp.City
    state = inp.State.upper().strip('"')
    sx = list(ccmap['State short']).index(state)
    st = ccmap['State full'][sx]
    date = inp.Next_Year_Event_Date
    
    try:
        
        cc = ccmap[ccmap['City'] == city]
        cc = cc[cc['State short'] == state]
        county = cc.iloc[0]['County']
        
    except:
        
        county = 'NOPE'
    
    if county != 'NOPE':
        
        if (county[0:5] == 'saint') and (county != 'saint marys'):
            
            back = county[5:]
            county = 'st.' + back
        
        elif county == 'virginia beach city':
            
            county = 'virginia beach'
            
        elif county ==  'alexandria city':
            
            county = 'alexandria'
            
        elif county == 'norfolk city':
            
            county = 'norfolk'
            
        elif county == 'fredericksburg city':
            
            county = 'fredericksburg'
            
        elif county == 'chesapeake city':
            
            county = 'chesapeake'
        
        elif county == 'lexington city':
            
            county = 'lexington'
            
        elif county == 'falls church city':
            
            county = 'falls church'
            
        elif county == 'staunton city':
            
            county = 'staunton'
            
        elif county == 'la porte':
            
            county = 'laporte'
            
        elif county == 'suffolk city':
            
            county = 'suffolk'
            
        elif county == 'newport news city':
            
            county = 'newport news'
            
        elif county == 'hampton city':
            
            county = 'hampton'
        
        elif county == 'manassas city':
            
            county = 'manassas'
            
        elif county == 'harrisonburg city':
            
            county = 'harrisonburg'
            
        elif county == 'prince georges':
            
            county = "prince george's"
            
        elif county == 'la salle':
            
            county = 'lasalle'
            
        elif county == 'saint marys':
            
            county = "st. mary's"
            
        elif county == 'lynchburg city':
            
            county = 'lynchburg'
            
        elif county == 'portsmouth city':
            
            county = 'portsmouth'
            
        elif county == 'poquoson city':
            
            county = 'poquoson'
            
        elif county == 'queen annes':
            
            county = "queen anne's"
            
        elif county == 'matanuska susitna':
            
            county = 'matanuska-susitna'
            
        elif county == 'st joseph':
            
            county = 'st. joseph'
            
        elif county == 'de kalb':
            
            county = 'dekalb'
            
        elif county == 'waynesboro city':
            
            county = 'waynesboro'
            
        elif county == 'winchester city':
            
            county = 'winchester'
            
        elif county == 'martinsville city':
            
            county = 'martinsville'
            
        elif county == 'danville city':
            
            county = 'danville'
            
        elif county == 'bristol city':
            
            county = 'bristol'
            
        elif county == 'de witt':
            
            county = 'dewitt'
            
        elif county == 'galax city':
            
            county = 'galax'
            
        elif county == 'colonial heights city':
            
            county = 'colonial heights'
        
        tmpdf = covidata[covidata['County'] == county]
        tmpdf = tmpdf[tmpdf['State'] == st]
        tmpdf = tmpdf[tmpdf['Date'] == date]
        cased = [tmpdf.iloc[0]['Cases_MA_7'], tmpdf.iloc[0]['Cases_MA_14'], tmpdf.iloc[0]['Cases_MA_30']]
        deadd = [tmpdf.iloc[0]['Deaths_MA_7'], tmpdf.iloc[0]['Deaths_MA_14'], tmpdf.iloc[0]['Deaths_MA_30']]
        casedst = [tmpdf.iloc[0]['Cases_MA_7_State'], tmpdf.iloc[0]['Cases_MA_14_State'], tmpdf.iloc[0]['Cases_MA_30_State']]
        deaddst = [tmpdf.iloc[0]['Deaths_MA_7_State'], tmpdf.iloc[0]['Deaths_MA_14_State'], tmpdf.iloc[0]['Deaths_MA_30_State']]
    
    else:
        
        cased = [None, None, None]
        deadd = [None, None, None]
        casedst = [None, None, None]
        deaddst = [None, None, None]
        
    return cased, deadd, casedst, deaddst

# Defining a helper function for race location covid data

def covid_race(inp):
    
    city = inp.RACE_City
    state = inp.RACE_State.upper().strip('"')
    sx = list(ccmap['State short']).index(state)
    st = ccmap['State full'][sx]
    date = inp.NY_Event_Date_PM1
    
    try:
        
        cc = ccmap[ccmap['City'] == city]
        cc = cc[cc['State short'] == state]
        county = cc.iloc[0]['County']
        
    except:
        
        county = 'NOPE'
    
    if county != 'NOPE':
        
        if (county[0:5] == 'saint') and (county != 'saint marys'):
            
            back = county[5:]
            county = 'st.' + back
        
        elif county == 'virginia beach city':
            
            county = 'virginia beach'
            
        elif county ==  'alexandria city':
            
            county = 'alexandria'
            
        elif county == 'norfolk city':
            
            county = 'norfolk'
            
        elif county == 'fredericksburg city':
            
            county = 'fredericksburg'
            
        elif county == 'chesapeake city':
            
            county = 'chesapeake'
            
        elif county == 'lexington city':
            
            county = 'lexington'
            
        elif county == 'falls church city':
            
            county = 'falls church'
            
        elif county == 'staunton city':
            
            county = 'staunton'
            
        elif county == 'la porte':
            
            county = 'laporte'
            
        elif county == 'suffolk city':
            
            county = 'suffolk'
            
        elif county == 'newport news city':
            
            county = 'newport news'
            
        elif county == 'hampton city':
            
            county = 'hampton'
            
        elif county == 'manassas city':
            
            county = 'manassas'
        
        elif county == 'harrisonburg city':
            
            county = 'harrisonburg'
            
        elif county == 'prince georges':
            
            county = "prince george's"
            
        elif county == 'la salle':
            
            county = 'lasalle'
            
        elif county == 'saint marys':
            
            county = "st. mary's"
            
        elif county == 'lynchburg city':
            
            county = 'lynchburg'
            
        elif county == 'portsmouth city':
            
            county = 'portsmouth'
            
        elif county == 'poquoson city':
            
            county = 'poquoson'
            
        elif county == 'queen annes':
            
            county = "queen anne's"
            
        elif county == 'matanuska susitna':
            
            county = 'matanuska-susitna'
            
        elif county == 'st joseph':
            
            county = 'st. joseph'
            
        elif county == 'de kalb':
            
            county = 'dekalb'
            
        elif county == 'waynesboro city':
            
            county = 'waynesboro'
            
        elif county == 'winchester city':
            
            county = 'winchester'
            
        elif county == 'martinsville city':
            
            county = 'martinsville'
            
        elif county == 'danville city':
            
            county = 'danville'
            
        elif county == 'bristol city':
            
            county = 'bristol'
            
        elif county == 'de witt':
            
            county = 'dewitt'
            
        elif county == 'galax city':
            
            county = 'galax'
            
        elif county == 'colonial heights city':
            
            county = 'colonial heights'

        tmpdf = covidata[covidata['County'] == county]
        tmpdf = tmpdf[tmpdf['State'] == st]
        tmpdf = tmpdf[tmpdf['Date'] == date]
        cased = [tmpdf.iloc[0]['Cases_MA_7'], tmpdf.iloc[0]['Cases_MA_14'], tmpdf.iloc[0]['Cases_MA_30']]
        deadd = [tmpdf.iloc[0]['Deaths_MA_7'], tmpdf.iloc[0]['Deaths_MA_14'], tmpdf.iloc[0]['Deaths_MA_30']]
        casedst = [tmpdf.iloc[0]['Cases_MA_7_State'], tmpdf.iloc[0]['Cases_MA_14_State'], tmpdf.iloc[0]['Cases_MA_30_State']]
        deaddst = [tmpdf.iloc[0]['Deaths_MA_7_State'], tmpdf.iloc[0]['Deaths_MA_14_State'], tmpdf.iloc[0]['Deaths_MA_30_State']]
        
    else:
        
        cased = [None, None, None]
        deadd = [None, None, None]
        casedst = [None, None, None]
        deaddst = [None, None, None]
        
    return cased, deadd, casedst, deaddst
    
# Creating runner city and state covid data

rnr_c_c_ma7 = []
rnr_c_c_ma14 = []
rnr_c_c_ma30 = []
rnr_c_d_ma7 = []
rnr_c_d_ma14 = []
rnr_c_d_ma30 = []

rnr_s_c_ma7 = []
rnr_s_c_ma14 = []
rnr_s_c_ma30 = []
rnr_s_d_ma7 = []
rnr_s_d_ma14 = []
rnr_s_d_ma30 = []

for i in range(len(racedata)):
    
    if racedata['Next_Year_Event_Date'][i] < datetime.datetime.strptime('2020-04-01', '%Y-%m-%d'):
        
        racedata['Next_Year_Event_Date'][i] = None
    
    if pd.isnull(racedata['Next_Year_Event_Date'][i]) == False:
        
        cased, deadd, casedst, deaddst = covid_rnr(racedata.iloc[i])
        rnr_c_c_ma7.append(cased[0])
        rnr_c_c_ma14.append(cased[1])
        rnr_c_c_ma30.append(cased[2])
        rnr_c_d_ma7.append(deadd[0])
        rnr_c_d_ma14.append(deadd[1])
        rnr_c_d_ma30.append(deadd[2])
        rnr_s_c_ma7.append(casedst[0])
        rnr_s_c_ma14.append(casedst[1])
        rnr_s_c_ma30.append(casedst[2])
        rnr_s_d_ma7.append(deaddst[0])
        rnr_s_d_ma14.append(deaddst[1])
        rnr_s_d_ma30.append(deaddst[2])

    else:
        
        rnr_c_c_ma7.append(None)
        rnr_c_c_ma14.append(None)
        rnr_c_c_ma30.append(None)
        rnr_c_d_ma7.append(None)
        rnr_c_d_ma14.append(None)
        rnr_c_d_ma30.append(None)
        rnr_s_c_ma7.append(None)
        rnr_s_c_ma14.append(None)
        rnr_s_c_ma30.append(None)
        rnr_s_d_ma7.append(None)
        rnr_s_d_ma14.append(None)
        rnr_s_d_ma30.append(None)

rnr_c_c_ma7 = pd.Series(rnr_c_c_ma7, name = 'Runner_City_Cases_MA7')
rnr_c_c_ma14 = pd.Series(rnr_c_c_ma14, name = 'Runner_City_Cases_MA14')
rnr_c_c_ma30 = pd.Series(rnr_c_c_ma30, name = 'Runner_City_Cases_MA30')
rnr_c_d_ma7 = pd.Series(rnr_c_d_ma7, name = 'Runner_City_Deaths_MA7')
rnr_c_d_ma14 = pd.Series(rnr_c_d_ma14, name = 'Runner_City_Deaths_MA14')
rnr_c_d_ma30 = pd.Series(rnr_c_d_ma30, name = 'Runner_City_Deaths_MA30')
rnr_s_c_ma7 = pd.Series(rnr_s_c_ma7, name = 'Runner_State_Cases_MA7')
rnr_s_c_ma14 = pd.Series(rnr_s_c_ma14, name = 'Runner_State_Cases_MA14')
rnr_s_c_ma30 = pd.Series(rnr_s_c_ma30, name = 'Runner_State_Cases_MA30')
rnr_s_d_ma7 = pd.Series(rnr_s_d_ma7, name = 'Runner_State_Deaths_MA7')
rnr_s_d_ma14 = pd.Series(rnr_s_d_ma14, name = 'Runner_State_Deaths_MA14')
rnr_s_d_ma30 = pd.Series(rnr_s_d_ma30, name = 'Runner_State_Deaths_MA30')

racedata = pd.concat([racedata, rnr_c_c_ma7, rnr_c_c_ma14, rnr_c_c_ma30, rnr_c_d_ma7,
                      rnr_c_d_ma14, rnr_c_d_ma30, rnr_s_c_ma7, rnr_s_c_ma14,
                      rnr_s_c_ma30, rnr_s_d_ma7, rnr_s_d_ma14, rnr_s_d_ma30], axis = 1)

# Creating race city and state covid data

race_c_c_ma7 = []
race_c_c_ma14 = []
race_c_c_ma30 = []
race_c_d_ma7 = []
race_c_d_ma14 = []
race_c_d_ma30 = []

race_s_c_ma7 = []
race_s_c_ma14 = []
race_s_c_ma30 = []
race_s_d_ma7 = []
race_s_d_ma14 = []
race_s_d_ma30 = []

for i in range(len(racedata)):
    
    if racedata['Next_Year_Event_Date'][i] < datetime.datetime.strptime('2020-04-01', '%Y-%m-%d'):
        
        racedata['Next_Year_Event_Date'][i] = None
    
    if pd.isnull(racedata['Next_Year_Event_Date'][i]) == False:
        
        cased, deadd, casedst, deaddst = covid_race(racedata.iloc[i])
        race_c_c_ma7.append(cased[0])
        race_c_c_ma14.append(cased[1])
        race_c_c_ma30.append(cased[2])
        race_c_d_ma7.append(deadd[0])
        race_c_d_ma14.append(deadd[1])
        race_c_d_ma30.append(deadd[2])
        race_s_c_ma7.append(casedst[0])
        race_s_c_ma14.append(casedst[1])
        race_s_c_ma30.append(casedst[2])
        race_s_d_ma7.append(deaddst[0])
        race_s_d_ma14.append(deaddst[1])
        race_s_d_ma30.append(deaddst[2])

    else:
        
        race_c_c_ma7.append(None)
        race_c_c_ma14.append(None)
        race_c_c_ma30.append(None)
        race_c_d_ma7.append(None)
        race_c_d_ma14.append(None)
        race_c_d_ma30.append(None)
        race_s_c_ma7.append(None)
        race_s_c_ma14.append(None)
        race_s_c_ma30.append(None)
        race_s_d_ma7.append(None)
        race_s_d_ma14.append(None)
        race_s_d_ma30.append(None)

race_c_c_ma7 = pd.Series(race_c_c_ma7, name = 'Race_City_Cases_MA7')
race_c_c_ma14 = pd.Series(race_c_c_ma14, name = 'Race_City_Cases_MA14')
race_c_c_ma30 = pd.Series(race_c_c_ma30, name = 'Race_City_Cases_MA30')
race_c_d_ma7 = pd.Series(race_c_d_ma7, name = 'Race_City_Deaths_MA7')
race_c_d_ma14 = pd.Series(race_c_d_ma14, name = 'Race_City_Deaths_MA14')
race_c_d_ma30 = pd.Series(race_c_d_ma30, name = 'Race_City_Deaths_MA30')
race_s_c_ma7 = pd.Series(race_s_c_ma7, name = 'Race_State_Cases_MA7')
race_s_c_ma14 = pd.Series(race_s_c_ma14, name = 'Race_State_Cases_MA14')
race_s_c_ma30 = pd.Series(race_s_c_ma30, name = 'Race_State_Cases_MA30')
race_s_d_ma7 = pd.Series(race_s_d_ma7, name = 'Race_State_Deaths_MA7')
race_s_d_ma14 = pd.Series(race_s_d_ma14, name = 'Race_State_Deaths_MA14')
race_s_d_ma30 = pd.Series(race_s_d_ma30, name = 'Race_State_Deaths_MA30')

racedata = pd.concat([racedata, race_c_c_ma7, race_c_c_ma14, race_c_c_ma30, race_c_d_ma7,
                      race_c_d_ma14, race_c_d_ma30, race_s_c_ma7, race_s_c_ma14,
                      race_s_c_ma30, race_s_d_ma7, race_s_d_ma14, race_s_d_ma30], axis = 1)

# Need to do the same for PM1

pm1rnr_c_c_ma7 = []
pm1rnr_c_c_ma14 = []
pm1rnr_c_c_ma30 = []
pm1rnr_c_d_ma7 = []
pm1rnr_c_d_ma14 = []
pm1rnr_c_d_ma30 = []

pm1rnr_s_c_ma7 = []
pm1rnr_s_c_ma14 = []
pm1rnr_s_c_ma30 = []
pm1rnr_s_d_ma7 = []
pm1rnr_s_d_ma14 = []
pm1rnr_s_d_ma30 = []

for i in range(len(racedata)):
    
    if pd.isnull(racedata['NY_Event_Name_PM1'][i]) == False:
        
        cased, deadd, casedst, deaddst = covid_rnr(racedata.iloc[i])
        pm1rnr_c_c_ma7.append(cased[0])
        pm1rnr_c_c_ma14.append(cased[1])
        pm1rnr_c_c_ma30.append(cased[2])
        pm1rnr_c_d_ma7.append(deadd[0])
        pm1rnr_c_d_ma14.append(deadd[1])
        pm1rnr_c_d_ma30.append(deadd[2])
        pm1rnr_s_c_ma7.append(casedst[0])
        pm1rnr_s_c_ma14.append(casedst[1])
        pm1rnr_s_c_ma30.append(casedst[2])
        pm1rnr_s_d_ma7.append(deaddst[0])
        pm1rnr_s_d_ma14.append(deaddst[1])
        pm1rnr_s_d_ma30.append(deaddst[2])

    else:
        
        pm1rnr_c_c_ma7.append(None)
        pm1rnr_c_c_ma14.append(None)
        pm1rnr_c_c_ma30.append(None)
        pm1rnr_c_d_ma7.append(None)
        pm1rnr_c_d_ma14.append(None)
        pm1rnr_c_d_ma30.append(None)
        pm1rnr_s_c_ma7.append(None)
        pm1rnr_s_c_ma14.append(None)
        pm1rnr_s_c_ma30.append(None)
        pm1rnr_s_d_ma7.append(None)
        pm1rnr_s_d_ma14.append(None)
        pm1rnr_s_d_ma30.append(None)

pm1rnr_c_c_ma7 = pd.Series(pm1rnr_c_c_ma7, name = 'Runner_City_Cases_MA7_PM1')
pm1rnr_c_c_ma14 = pd.Series(pm1rnr_c_c_ma14, name = 'Runner_City_Cases_MA14_PM1')
pm1rnr_c_c_ma30 = pd.Series(pm1rnr_c_c_ma30, name = 'Runner_City_Cases_MA30_PM1')
pm1rnr_c_d_ma7 = pd.Series(pm1rnr_c_d_ma7, name = 'Runner_City_Deaths_MA7_PM1')
pm1rnr_c_d_ma14 = pd.Series(pm1rnr_c_d_ma14, name = 'Runner_City_Deaths_MA14_PM1')
pm1rnr_c_d_ma30 = pd.Series(pm1rnr_c_d_ma30, name = 'Runner_City_Deaths_MA30_PM1')
pm1rnr_s_c_ma7 = pd.Series(pm1rnr_s_c_ma7, name = 'Runner_State_Cases_MA7_PM1')
pm1rnr_s_c_ma14 = pd.Series(pm1rnr_s_c_ma14, name = 'Runner_State_Cases_MA14_PM1')
pm1rnr_s_c_ma30 = pd.Series(pm1rnr_s_c_ma30, name = 'Runner_State_Cases_MA30_PM1')
pm1rnr_s_d_ma7 = pd.Series(pm1rnr_s_d_ma7, name = 'Runner_State_Deaths_MA7_PM1')
pm1rnr_s_d_ma14 = pd.Series(pm1rnr_s_d_ma14, name = 'Runner_State_Deaths_MA14_PM1')
pm1rnr_s_d_ma30 = pd.Series(pm1rnr_s_d_ma30, name = 'Runner_State_Deaths_MA30_PM1')

racedata = pd.concat([racedata, pm1rnr_c_c_ma7, pm1rnr_c_c_ma14, pm1rnr_c_c_ma30, pm1rnr_c_d_ma7,
                      pm1rnr_c_d_ma14, pm1rnr_c_d_ma30, pm1rnr_s_c_ma7, pm1rnr_s_c_ma14,
                      pm1rnr_s_c_ma30, pm1rnr_s_d_ma7, pm1rnr_s_d_ma14, pm1rnr_s_d_ma30], axis = 1)

# Creating race city and state covid data

pm1race_c_c_ma7 = []
pm1race_c_c_ma14 = []
pm1race_c_c_ma30 = []
pm1race_c_d_ma7 = []
pm1race_c_d_ma14 = []
pm1race_c_d_ma30 = []

pm1race_s_c_ma7 = []
pm1race_s_c_ma14 = []
pm1race_s_c_ma30 = []
pm1race_s_d_ma7 = []
pm1race_s_d_ma14 = []
pm1race_s_d_ma30 = []

for i in range(len(racedata)):
    
    if pd.isnull(racedata['NY_Event_Name_PM1'][i]) == False:
        
        cased, deadd, casedst, deaddst = covid_race(racedata.iloc[i])
        pm1race_c_c_ma7.append(cased[0])
        pm1race_c_c_ma14.append(cased[1])
        pm1race_c_c_ma30.append(cased[2])
        pm1race_c_d_ma7.append(deadd[0])
        pm1race_c_d_ma14.append(deadd[1])
        pm1race_c_d_ma30.append(deadd[2])
        pm1race_s_c_ma7.append(casedst[0])
        pm1race_s_c_ma14.append(casedst[1])
        pm1race_s_c_ma30.append(casedst[2])
        pm1race_s_d_ma7.append(deaddst[0])
        pm1race_s_d_ma14.append(deaddst[1])
        pm1race_s_d_ma30.append(deaddst[2])

    else:
        
        pm1race_c_c_ma7.append(None)
        pm1race_c_c_ma14.append(None)
        pm1race_c_c_ma30.append(None)
        pm1race_c_d_ma7.append(None)
        pm1race_c_d_ma14.append(None)
        pm1race_c_d_ma30.append(None)
        pm1race_s_c_ma7.append(None)
        pm1race_s_c_ma14.append(None)
        pm1race_s_c_ma30.append(None)
        pm1race_s_d_ma7.append(None)
        pm1race_s_d_ma14.append(None)
        pm1race_s_d_ma30.append(None)

pm1race_c_c_ma7 = pd.Series(pm1race_c_c_ma7, name = 'Race_City_Cases_MA7_PM1')
pm1race_c_c_ma14 = pd.Series(pm1race_c_c_ma14, name = 'Race_City_Cases_MA14_PM1')
pm1race_c_c_ma30 = pd.Series(pm1race_c_c_ma30, name = 'Race_City_Cases_MA30_PM1')
pm1race_c_d_ma7 = pd.Series(pm1race_c_d_ma7, name = 'Race_City_Deaths_MA7_PM1')
pm1race_c_d_ma14 = pd.Series(pm1race_c_d_ma14, name = 'Race_City_Deaths_MA14_PM1')
pm1race_c_d_ma30 = pd.Series(pm1race_c_d_ma30, name = 'Race_City_Deaths_MA30_PM1')
pm1race_s_c_ma7 = pd.Series(pm1race_s_c_ma7, name = 'Race_State_Cases_MA7_PM1')
pm1race_s_c_ma14 = pd.Series(pm1race_s_c_ma14, name = 'Race_State_Cases_MA14_PM1')
pm1race_s_c_ma30 = pd.Series(pm1race_s_c_ma30, name = 'Race_State_Cases_MA30_PM1')
pm1race_s_d_ma7 = pd.Series(pm1race_s_d_ma7, name = 'Race_State_Deaths_MA7_PM1')
pm1race_s_d_ma14 = pd.Series(pm1race_s_d_ma14, name = 'Race_State_Deaths_MA14_PM1')
pm1race_s_d_ma30 = pd.Series(pm1race_s_d_ma30, name = 'Race_State_Deaths_MA30_PM1')

racedata = pd.concat([racedata, pm1race_c_c_ma7, pm1race_c_c_ma14, pm1race_c_c_ma30, pm1race_c_d_ma7,
                      pm1race_c_d_ma14, pm1race_c_d_ma30, pm1race_s_c_ma7, pm1race_s_c_ma14,
                      pm1race_s_c_ma30, pm1race_s_d_ma7, pm1race_s_d_ma14, pm1race_s_d_ma30], axis = 1)

# Updating a couple of states (CA and GA only) which pulled in a '"'

for i in range(len(racedata)):
    
    if '"' in racedata['State'][i]:
        
        racedata['State'][i] == str(racedata['State'][i]).strip('"')

# Writing tha final data frame to file

racedata.to_csv(filepath + 'ultradata.csv', index = False)

