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

# The functions for mapping city to county for runners and races

def city_to_county(inp):
    
    city = inp.City
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
    lat = cases.iloc[0]['Lat']
    long = cases.iloc[0]['Long_']
    coord = [lat,long]
    
    return coord

def city_to_county_2(inp):
    
    city = inp.RACE_City
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
    lat = cases.iloc[0]['Lat']
    long = cases.iloc[0]['Long_']
    coord = [lat,long]
    
    return coord

# Use the functions to get the coordinates for runner and race locations

rnr_coords = [city_to_county(ultradata.iloc[i]) for i in range(len(ultradata))]
race_coords = [city_to_county_2(ultradata.iloc[i]) for i in range(len(ultradata))]

# Use geopy.distances.geodesic to compute distances between runner and race for all observations

distances = [geodesic(rnr_coords[i], race_coords[i]).mi for i in range(len(rnr_coords))]

# Adding distances to the dataframe

ultradata = pd.concat([ultradata, distances], axis = 1)

# Writing the final data frame to file (again. i know, i know...)

ultradata.to_csv(filepath + 'ultradata.csv', index = False)

