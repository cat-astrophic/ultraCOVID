# This script finds the county for each race city in the ultraCOVID data

# Importing required modules

import pandas as pd
import addfips

# Project directory

direc = 'D:/ultraCOVID/'

# Read in the data

ud = pd.read_csv(direc + 'ultradata.csv')
ccmap = pd.read_csv(direc + 'ccmap.csv', sep = '|') # The city to county map from before
death = pd.read_csv(direc + 'time_series_covid19_deaths_US.csv')

# Update ccmap

ccmap = ccmap.replace(to_replace = 'Washington, D.C.', value = 'District of Columbia') # Update DC naming convention
ccmap.City = ccmap.City.str.lower()
ccmap.County = ccmap.County.str.lower()

# A function to find the race county

def junk(inp):
    
    city = inp.RACE_City.lower()
    state = inp.RACE_State.upper().strip('"')
    
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
            
    return county

# Get the county for each race

rc = [junk(ud.iloc[i]) for i in range(len(ud))]

# Add this to the data

ud = pd.concat([ud, pd.Series(rc, name = 'RACE_County')], axis = 1)

# Get race FIPS with addfips

af = addfips.AddFIPS()

rfips = [af.get_county_fips(ud.RACE_County[i], state = ud.RACE_State[i]) for i in range(len(ud))]

# Use rfips to get race county population data

def ff(j):
    
    if death.FIPS[j] > 0:
        
        fu = str(int(death.FIPS[j]))
        
        if len(fu) == 4:
            
            fu = '0' + fu
        
    else:
        
        fu = None
    
    return fu

f = [ff(i) for i in range(len(death))]

death.f = f

pops = [death.Population[f.index(r)] for r in rfips]

# Add pops to data

ud = pd.concat([ud, pd.Series(pops, name = 'RACE_County_Population')], axis = 1)

# Compute per million values

racecc7 = [1000000 * ud.Race_City_Cases_MA7[i] / ud.RACE_County_Population[i] for i in range(len(ud))]
racecc14 = [1000000 * ud.Race_City_Cases_MA14[i] / ud.RACE_County_Population[i] for i in range(len(ud))]
racecc30 = [1000000 * ud.Race_City_Cases_MA30[i] / ud.RACE_County_Population[i] for i in range(len(ud))]

racecd7 = [1000000 * ud.Race_City_Deaths_MA7[i] / ud.RACE_County_Population[i] for i in range(len(ud))]
racecd14 = [1000000 * ud.Race_City_Deaths_MA14[i] / ud.RACE_County_Population[i] for i in range(len(ud))]
racecd30 = [1000000 * ud.Race_City_Deaths_MA30[i] / ud.RACE_County_Population[i] for i in range(len(ud))]

rnrcc7 = [1000000 * ud.Runner_City_Cases_MA7[i] / ud.County_Population[i] for i in range(len(ud))]
rnrcc14 = [1000000 * ud.Runner_City_Cases_MA14[i] / ud.County_Population[i] for i in range(len(ud))]
rnrcc30 = [1000000 * ud.Runner_City_Cases_MA30[i] / ud.County_Population[i] for i in range(len(ud))]

rnrcd7 = [1000000 * ud.Runner_City_Deaths_MA7[i] / ud.County_Population[i] for i in range(len(ud))]
rnrcd14 = [1000000 * ud.Runner_City_Deaths_MA14[i] / ud.County_Population[i] for i in range(len(ud))]
rnrcd30 = [1000000 * ud.Runner_City_Deaths_MA30[i] / ud.County_Population[i] for i in range(len(ud))]

# Add these to the data

racecc7 = pd.Series(racecc7, name = 'Race_City_Cases_MA7_PC')
racecc14 = pd.Series(racecc14, name = 'Race_City_Cases_MA14_PC')
racecc30 = pd.Series(racecc30, name = 'Race_City_Cases_MA30_PC')

racecd7 = pd.Series(racecd7, name = 'Race_City_Cases_MA7_PC')
racecd14 = pd.Series(racecd14, name = 'Race_City_Deaths_MA14_PC')
racecd30 = pd.Series(racecd30, name = 'Race_City_Deaths_MA30_PC')

rnrcc7 = pd.Series(rnrcc7, name = 'Runner_City_Cases_MA7_PC')
rnrcc14 = pd.Series(rnrcc14, name = 'Runner_City_Cases_MA14_PC')
rnrcc30 = pd.Series(rnrcc30, name = 'Runner_City_Cases_MA30_PC')

rnrcd7 = pd.Series(rnrcd7, name = 'Runner_City_Deaths_MA7_PC')
rnrcd14 = pd.Series(rnrcd14, name = 'Runner_City_Deaths_MA14_PC')
rnrcd30 = pd.Series(rnrcd30, name = 'Runner_City_Deaths_MA30_PC')

ud = pd.concat([racecc7, racecc14, racecc30, racecd7, racecd14, racecd30, rnrcc7, rnrcc14, rnrcc30, rnrcd7, rnrcd14, rnrcd30], axis = 1)

# Save the data

ud.to_csv(direc + 'ultradata.csv', index = False)

