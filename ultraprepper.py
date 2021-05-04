# This script preps the data for a paper on the impact of COVID on ultramarathoning

# Importing required modules

import pandas as pd
import numpy as np
import datetime
from matplotlib import pyplot as plt

# Specifiying your username

username = ''

# Reading in the race data and results data

data = pd.read_csv('C:/Users/' + username + '/Documents/Data/ultraCOVID/raw_results_data.csv')

# Define a function for indicating COVID era races

def covidfunc(inp):
    
    if inp['RACE_Year'] == 2021:
        
        coval = 1
        
    elif (inp['RACE_Year'] == 2021) and (inp['RACE_Month'] not in ['Jan', 'Feb', 'Mar']):
        
        coval = 1
        
    else:
        
        coval = 0
        
    return coval

# Add a COVID variable to indicate which races took places during COVID

cid = [covidfunc(data.iloc[row]) for row in range(np.shape(data)[0])]
data = pd.concat([data, pd.Series(cid, name = 'COVID')], axis = 1)

# Is next year's race held?

nyrace = []

for i in range(len(data)):
    
    dy = data[data['RACE_Year'] == data.iloc[i]['RACE_Year']+1] # Subset for next year's data
    dy = dy[dy['RACE_Name'] == data.iloc[i]['RACE_Name']] # Subset for the event
    dy = dy[dy['RACE_Distance'] == data.iloc[i]['RACE_Distance']] # Subset for the event
    nyrace.append(min(1,len(dy))) # Append 1 if df non-empty, 0 otherwise
    
data = pd.concat([data, pd.Series(nyrace, name = 'Race_Held_Next_Year')], axis = 1)

# Do individuals run next year's race?

pnyrace = []

for i in range(len(data)):
    
    idx = data.iloc[i]['Runner_ID'] # Get Runner_ID
    dy = data[data['RACE_Year'] == data.iloc[i]['RACE_Year']+1] # Subset for next year's data
    dy = dy[dy['RACE_Name'] == data.iloc[i]['RACE_Name']] # Subset for the event
    dy = dy[dy['RACE_Distance'] == data.iloc[i]['RACE_Distance']] # Subset for the event
    dylist = dy['Runner_ID'].to_list() # Creating a list to make this work
    pnyrace.append(np.int(idx in dylist)) # Append 1 if ran next year's race, 0 otherwise

data = pd.concat([data, pd.Series(nyrace, name = 'Attended_Next_Year_Race')], axis = 1)

# Calculate consecutive appearances by an individual at an event

# First, determine the sample used in the analysis :: 1 April 2019 - 31 March 2020

d = data[data['RACE_Year'].isin([2019, 2020])].reset_index(drop = True)
check = [1 if ((d['RACE_Year'][i] == 2020) and (d['RACE_Month'][i] in ['Jan', 'Feb', 'Mar'])) or ((d['RACE_Year'][i] == 2019) and (d['RACE_Month'][i] not in ['Jan', 'Feb', 'Mar'])) else 0 for i in range(len(d))]
d = pd.concat([d, pd.Series(check, name = 'Check')], axis = 1)

# Next, this is a helper function

def yearsies_shmearsies(yick):
    
    for ick in range(len(yick)):
        
        if yick[0] - yick[ick] == ick: # Ensure consecutive years
            
            blah = ick + 1 # Increase the value of consecutive years ran
    
    return blah

# For races in the pre-COVID portion of the sample, determine race history for each individual

all_past = []
consec_past = []

for i in range(len(d)):
    
    idx = d.iloc[i]['Runner_ID'] # Get Runner_ID
    tempdf = data[data['RACE_Year'] <= d.iloc[i]['RACE_Year']] # Subset for past race history
    tempdf = tempdf[tempdf['RACE_Name'] == d.iloc[i]['RACE_Name']] # Subset for the event
    tempdf = tempdf[tempdf['RACE_Distance'] == d.iloc[i]['RACE_Distance']] # Subset for the event    
    tempdf = tempdf[tempdf['Runner_ID'] == idx] # Subset for the runner
    templist = tempdf['Runner_ID'].to_list() # Creating a list to make this work
    yearsies = tempdf['RACE_Year'].to_list() # A list of all years they competed
    all_past.append(len(yearsies)) # Total past appearances at the event
    consec_past.append(yearsies_shmearsies(yearsies)) # Consecutive past appearances at the event
    
d = pd.concat([d, pd.Series(all_past, name = 'Total Appearances')], axis = 1)
d = pd.concat([d, pd.Series(consec_past, name = 'Consecutive Appearances')], axis = 1)

# If next year's race is not held, did they run a new race \pm a month?

# First, add datetime data to the dataframes d and data (we'll need both)

nastydates = [d.iloc[i]['RACE_Month'] + ' ' + str(d.iloc[i]['RACE_Date']) + ', ' + str(d.iloc[i]['RACE_Year']) for i in range(len(d))] # Dates as formatted strings
cleandates = [datetime.datetime.strptime(nd, '%b %d, %Y') for nd in nastydates] # Cleaned dates in datetime format
d = pd.concat([d, pd.Series(cleandates, name = 'Clean_Race_Date')], axis = 1) # Add cleandates to the dataframe

nastydates2 = [data.iloc[i]['RACE_Month'] + ' ' + str(data.iloc[i]['RACE_Date']) + ', ' + str(data.iloc[i]['RACE_Year']) for i in range(len(data))] # Dates as formatted strings
cleandates2 = [datetime.datetime.strptime(nd, '%b %d, %Y') for nd in nastydates2] # Cleaned dates in datetime format
data = pd.concat([data, pd.Series(cleandates2, name = 'Clean_Race_Date')], axis = 1) # Add cleandates to the dataframe

# Creating the data for whether or not an athlete competed in an event within the time window for cancelled events

unomo = []
dosmos = []

for i in range(len(d)):
    
    idx = d.iloc[i]['Runner_ID'] # Get Runner_ID
    tempdf1 = data[data['Clean_Race_Date'] >= d.iloc[i]['Clean_Race_Date'] - datetime.timedelta(30)] # Subset for all races this individual ran \pm one month
    tempdf2 = data[data['Clean_Race_Date'] >= d.iloc[i]['Clean_Race_Date'] - datetime.timedelta(60)] # Subset for all races this individual ran \pm two months
    tempdf1 = tempdf1[tempdf1['Clean_Race_Date'] <= d.iloc[i]['Clean_Race_Date'] + datetime.timedelta(30)] # Subset for all races this individual ran \pm one month
    tempdf2 = tempdf2[tempdf2['Clean_Race_Date'] <= d.iloc[i]['Clean_Race_Date'] + datetime.timedelta(60)] # Subset for all races this individual ran \pm two months
    unomo.append(np.int(idx in tempdf1['Runner_ID']))
    dosmos.append(np.int(idx in tempdf2['Runner_ID']))
    

    







# can also look at impact on race counts for events (as a summary statistic)
# also get unique runner counts by year, race and event counts by year, total runners count by year