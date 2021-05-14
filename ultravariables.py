# This script transforms variables into a usable format for regressing

# Importing required modules

import pandas as pd
from geopy.distance import geodesic

# Specifying the path to the data -- update this accordingly!

username = ''
filepath = 'C:/Users/' + username + '/Documents/Data/ultraCOVID/'

# Reading in the data

ultradata = pd.read_csv(filepath + 'ultradata.csv')

# First is to add a month variable for use as a fixed effect

mons = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
mon_num = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

ultradata['NY_Event_Date_PM1'] = pd.to_datetime(ultradata['NY_Event_Date_PM1'])

MONTHS = [mons[mon_num.index(str(ultradata['NY_Event_Date_PM1'][i])[5:7])] for i in range(len(ultradata['NY_Event_Date_PM1']))]
MONTHS = pd.Series(MONTHS, name = 'NY_RACE_Month')
ultradata = pd.concat([ultradata, MONTHS], axis = 1)

# Next is creating a fixed effect for in-state runners

instate = [1 if ultradata['RACE_State'][i] == ultradata['State'][i] else 0 for i in range(len(ultradata['RACE_State']))]
instate = pd.Series(instate, name = 'In_State')
ultradata = pd.concat([ultradata, instate], axis = 1)

# Next is creating a variable for a course specific fixed

courses = [str(ultradata['RACE_Name'][i]) + str(ultradata['RACE_Distance'][i]) for i in range(len(ultradata))]
courses = pd.Series(courses, name = 'Course')
ultradata = pd.concat([ultradata, courses], axis = 1)

# Last is determining the distance between runner and event

cases = pd.read_csv(filepath + 'time_series_covid19_confirmed_US.csv') # Contains lattitude and longitude
ccmap = pd.read_csv(filepath + 'ccmap.csv', sep = '|') # The city to county map from before
ccmap = ccmap.replace(to_replace = 'Washington, D.C.', value = 'District of Columbia') # Update DC naming convention
ccmap.City = ccmap.City.str.lower()
ccmap.County = ccmap.County.str.lower()
cases.Admin2 = cases.Admin2.str.lower()

# The functions for mapping city to county for runners and races

def city_to_county(inp):
    
    city = inp.City.lower()
    state = inp.State.upper().strip('"')
    sx = list(ccmap['State short']).index(state)
    st = ccmap['State full'][sx]
    
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
            
    tmp = cases[cases.Province_State == st]
    tmp = tmp[tmp.Admin2 == county]
    
    if len(tmp) > 0:
        
        lat = tmp.iloc[0]['Lat']
        long = tmp.iloc[0]['Long_']
        coord = [lat,long]
        
    else:
        
        coord = [None,None]
    
    return coord

def city_to_county_2(inp):
    
    city = inp.RACE_City.lower()
    state = inp.RACE_State.upper().strip('"')
    sx = list(ccmap['State short']).index(state)
    st = ccmap['State full'][sx]
    
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
            
    tmp = cases[cases.Province_State == st]
    tmp = tmp[tmp.Admin2 == county]
    
    if len(tmp) > 0:
        
        lat = tmp.iloc[0]['Lat']
        long = tmp.iloc[0]['Long_']
        coord = [lat,long]
        
    else:
        
        coord = [None,None]
    
    return coord

# Use the functions to get the coordinates for runner and race locations

rnr_coords = [city_to_county(ultradata.iloc[i]) for i in range(len(ultradata))]
race_coords = [city_to_county_2(ultradata.iloc[i]) for i in range(len(ultradata))]

# Use geopy.distances.geodesic to compute distances between runner and race for all observations

distances = []

for i in range(len(rnr_coords)):
    
    if (rnr_coords[i] != [None,None]) and (race_coords[i] != [None,None]):
        
        distances.append(geodesic(rnr_coords[i], race_coords[i]).mi)
        
    else:
        
        distances.append(None)

# Adding distances to the dataframe

distances = pd.Series(distances, name = 'Travel_Distance')
ultradata = pd.concat([ultradata, distances], axis = 1)

# Creating proxy variables for runner ability - mean of function of gender place in all races

runners = ultradata.Runner_ID.to_list() # Runners
gplace = ultradata.Gender_Place.to_list() # Gender places
genders = ultradata.Gender.to_list() # Gender
rids = ultradata.RACE_ID.to_list() # Races

# Create per race score

g_score = []

for i in range(len(runners)):
    
    tmp = ultradata[ultradata['RACE_ID'] == rids[i]]
    tmp = tmp[tmp['Gender'] == genders[i]]
    gp = min(gplace[i], len(tmp)) - 1
    g_score.append(1 - (gp/len(tmp)))

# Aggregate scores into an average score per runner

ability = []

for i in range(len(runners)):
    
    ids = [j for j in range(len(runners)) if runners[j] == runners[i]]
    vals = [g_score[j] for j in ids]
    ability.append(sum(vals)/len(vals))

# Adding this ability proxy score to the data frame

ability = pd.Series(ability, name = 'Ability')
ultradata = pd.concat([ultradata, ability], axis = 1)

# Creating an explicit dependent variable for the full data set regressions

y = [max(ultradata['Attended_Next_Year_Race'][i],ultradata['PM_1_Month'][i]) for i in range(len(ultradata))]
y = pd.Series(y, name = 'Y')
ultradata = pd.concat([ultradata, y], axis = 1)

# Writing the final data frame to file (again. i know, i know...)

ultradata.to_csv(filepath + 'ultradata.csv', index = False)

