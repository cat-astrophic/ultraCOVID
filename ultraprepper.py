# This script preps the data for a paper on the impact of COVID on ultramarathoning

# Importing required modules

import pandas as pd
import numpy as np
import datetime

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

data = pd.concat([data, pd.Series(pnyrace, name = 'Attended_Next_Year_Race')], axis = 1)

# Calculate consecutive appearances by an individual at an event

# First, determine the sample used in the analysis :: 1 April 2019 - 31 March 2020

d = data[data['RACE_Year'].isin([2019, 2020])].reset_index(drop = True)
check = [1 if ((d['RACE_Year'][i] == 2020) and (d['RACE_Month'][i] in ['Jan', 'Feb', 'Mar'])) or ((d['RACE_Year'][i] == 2019) and (d['RACE_Month'][i] not in ['Jan', 'Feb', 'Mar'])) else 0 for i in range(len(d))]
d = pd.concat([d, pd.Series(check, name = 'Check')], axis = 1)
d = d[d['Check'] == 1].reset_index(drop = True)

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
    
all_past = pd.Series(all_past, name = 'Total Appearances')
consec_past = pd.Series(consec_past, name = 'Consecutive Appearances')
d = pd.concat([d, all_past, consec_past], axis = 1)

# If next year's race is not held, did they run a new race \pm a month?

# First, add datetime data to the dataframes d and data (we'll need both)

nastydates = [d.iloc[i]['RACE_Month'] + ' ' + str(int(d.iloc[i]['RACE_Date'])) + ', ' + str(int(d.iloc[i]['RACE_Year'])) for i in range(len(d))] # Dates as formatted strings
cleandates = [datetime.datetime.strptime(nd, '%b %d, %Y') for nd in nastydates] # Cleaned dates in datetime format
d = pd.concat([d, pd.Series(cleandates, name = 'Clean_Race_Date')], axis = 1) # Add cleandates to the dataframe

nastydates2 = [data.iloc[i]['RACE_Month'] + ' ' + str(int(data.iloc[i]['RACE_Date'])) + ', ' + str(int(data.iloc[i]['RACE_Year'])) for i in range(len(data))] # Dates as formatted strings
cleandates2 = [datetime.datetime.strptime(nd, '%b %d, %Y') for nd in nastydates2] # Cleaned dates in datetime format
data = pd.concat([data, pd.Series(cleandates2, name = 'Clean_Race_Date')], axis = 1) # Add cleandates to the dataframe

# Creating the data for whether or not an athlete competed in an event within the time window for cancelled events

unomo = []
dosmos = []

for i in range(len(d)):
    
    rid = d.iloc[i]['Runner_ID'] # Get Runner_ID
    tempdf1 = data[data['Clean_Race_Date'] >= d.iloc[i]['Clean_Race_Date'] + datetime.timedelta(365-30)] # Subset for all races this individual ran \pm one month
    tempdf2 = data[data['Clean_Race_Date'] >= d.iloc[i]['Clean_Race_Date'] + datetime.timedelta(365-60)] # Subset for all races this individual ran \pm two months
    tempdf1 = tempdf1[tempdf1['Clean_Race_Date'] <= d.iloc[i]['Clean_Race_Date'] + datetime.timedelta(365+30)] # Subset for all races this individual ran \pm one month
    tempdf2 = tempdf2[tempdf2['Clean_Race_Date'] <= d.iloc[i]['Clean_Race_Date'] + datetime.timedelta(365+60)] # Subset for all races this individual ran \pm two months
    unomo.append(np.int(rid in list(tempdf1['Runner_ID'])))
    dosmos.append(np.int(rid in list(tempdf2['Runner_ID'])))
    
d = pd.concat([d, pd.Series(unomo, name = 'PM_1_Month')], axis = 1) # Add unomo to dataframe
d = pd.concat([d, pd.Series(dosmos, name = 'PM_2_Months')], axis = 1) # Add dosmos to dataframe

# Getting the date of the future race if held

future_dates = []

for i in range(len(d)):
    
    tmpdf = data[data['RACE_Name'] == d.iloc[i]['RACE_Name']]
    tmpdf = tmpdf[tmpdf['RACE_Distance'] == d.iloc[i]['RACE_Distance']]
    tmpdf = tmpdf[tmpdf['RACE_Year'] == d.iloc[i]['RACE_Year']+1].reset_index(drop = True)
    
    if len(tmpdf) > 0:
        
        future_dates.append(tmpdf['Clean_Race_Date'][0])
        
    else:
        
        future_dates.append(np.nan)

# Adding this data to the dataframe

d = pd.concat([d, pd.Series(future_dates, name = 'Next_Year_Event_Date')], axis = 1) # Add future_dates to dataframe

# Getting the date of the \pm races if they exist (use closest date to expected event date)

future_dates1 = []
future_dates2 = []

for i in range(len(d)):
    
    if pd.isnull(d['Next_Year_Event_Date'][i]) == False:
        
        future_dates1.append(d['Clean_Race_Date'][i])
        future_dates2.append(d['Clean_Race_Date'][i])
        
    elif d.iloc[i]['PM_1_Month'] == 1:
        
        rid = d.iloc[i]['Runner_ID'] # Get Runner_ID
        tmpdf1 = data[data['Clean_Race_Date'] <= d['Clean_Race_Date'][i]+datetime.timedelta(365+30)]
        tmpdf1 = tmpdf1[tmpdf1['Clean_Race_Date'] >= d['Clean_Race_Date'][i]+datetime.timedelta(365-30)]
        tmpdf1 = tmpdf1[tmpdf1['Runner_ID'] == rid].reset_index(drop = True)
        tmpdf2 = data[data['Clean_Race_Date'] <= d['Clean_Race_Date'][i]+datetime.timedelta(365+60)]
        tmpdf2 = tmpdf2[tmpdf2['Clean_Race_Date'] >= d['Clean_Race_Date'][i]+datetime.timedelta(365-60)]
        tmpdf2 = tmpdf2[tmpdf2['Runner_ID'] == rid].reset_index(drop = True)
        diffs1 = [abs(date - d['Clean_Race_Date'][i]) for date in tmpdf1['Clean_Race_Date']]
        diffs2 = [abs(date - d['Clean_Race_Date'][i]) for date in tmpdf2['Clean_Race_Date']]
        min1 = diffs1.index(min(diffs1))
        min2 = diffs2.index(min(diffs2))
        future_dates1.append(tmpdf1.iloc[min1]['Clean_Race_Date'])
        future_dates2.append(tmpdf2.iloc[min2]['Clean_Race_Date'])
        
    elif d.iloc[i]['PM_2_Months'] == 1:
        
        rid = d.iloc[i]['Runner_ID'] # Get Runner_ID
        tmpdf2 = data[data['Clean_Race_Date'] <= d['Clean_Race_Date'][i]+datetime.timedelta(365+60)]
        tmpdf2 = tmpdf2[tmpdf2['Clean_Race_Date'] >= d['Clean_Race_Date'][i]+datetime.timedelta(365-60)]
        tmpdf2 = tmpdf2[tmpdf2['Runner_ID'] == rid].reset_index(drop = True)
        diffs2 = [abs(date - d['Clean_Race_Date'][i]) for date in tmpdf2['Clean_Race_Date']]
        min2 = diffs2.index(min(diffs2))
        future_dates1.append(np.nan)
        future_dates2.append(tmpdf2.iloc[min2]['Clean_Race_Date'])
        
    else:
        
        future_dates1.append(np.nan)
        future_dates2.append(np.nan)
        
# Adding these to the dataframe d

future_dates1 = pd.Series(future_dates1, name = 'Next_Year_Event_Date_PM1')
future_dates2 = pd.Series(future_dates2, name = 'Next_Year_Event_Date_PM2')
d = pd.concat([d, future_dates1, future_dates2], axis = 1) # Add future_dates1&2 to dataframe

# only other thing to do would be to find the dates and locations of the pm1/2 races

# First is to initialize two new columns for next years event details

nyeven = [d['RACE_Name'][i] if d['Attended_Next_Year_Race'][i] == 1 else None for i in range(len(d))]
nydist = [d['RACE_Distance'][i] if d['Attended_Next_Year_Race'][i] == 1 else None for i in range(len(d))]

nyeven = pd.Series(nyeven, name = 'Next_Year_Event')
nydist = pd.Series(nydist, name = 'Next_Year_Distance')
nyeven1 = pd.Series(nyeven, name = 'Next_Year_Event_PM1')
nydist1 = pd.Series(nydist, name = 'Next_Year_Distance_PM1')
nyeven2 = pd.Series(nyeven, name = 'Next_Year_Event_PM2')
nydist2 = pd.Series(nydist, name = 'Next_Year_Distance_PM2')

d = pd.concat([d, nyeven1, nydist1, nyeven2, nydist2], axis = 1)

d1 = d[d['PM_1_Month'] == 1]
d2 = d[d['PM_2_Months'] == 1]
d1 = d1[d1['Race_Held_Next_Year'] == 0]
d2 = d2[d2['Race_Held_Next_Year'] == 0]

for i in d1.index.to_list():
    print(str(d1.index.to_list().index(i)+1) + ' of  4221.......')
    rid = d['Runner_ID'][i] # Get runner id
    pydate = d['Clean_Race_Date'][i] # Get PY event date
    tmpdf = data[data['Clean_Race_Date'] >= d['Clean_Race_Date'][i]+datetime.timedelta(365-30)] # Subset data
    tmpdf = tmpdf[tmpdf['Clean_Race_Date'] <= d['Clean_Race_Date'][i]+datetime.timedelta(365+30)] # Subset data
    tmpdf = tmpdf[tmpdf['Runner_ID'] == rid] # All races ran in window by runner
    tmpdf2 = data[data['Clean_Race_Date'] >= d['Clean_Race_Date'][i]+datetime.timedelta(30)] # Look for these races PY
    tmpdf2 = tmpdf2[tmpdf2['Clean_Race_Date'] <= d['Clean_Race_Date'][i]-datetime.timedelta(30)] # Look for these races PY
    tmpdf2 = tmpdf2[tmpdf2['Runner_ID'] == rid] # All races ran in window by runner
    
    for row in range(len(tmpdf)):
        
        en = tmpdf.iloc[row]['RACE_Name']
        ed = tmpdf.iloc[row]['RACE_Distance']
        
        for row2 in range(len(tmpdf2)):
            
            if (tmpdf2.iloc[row2]['RACE_Name'] == en) and (tmpdf2.iloc[row2]['RACE_Distance'] == ed):
                
                tmpdf = tmpdf.drop([list(tmpdf.index)[row]]) # Remove the row from tmpdf because they ran it in PY
                
    # Finally, find the median entry
    
    if len(tmpdf) == 0:
        
        d['PM_1_Month'][i] = 0
        d['Next_Year_Event_Date_PM1'][i] = None
        
    else:
        
        datediffs = [abs(pydate+datetime.timedelta(365) - xx) for xx in tmpdf['Clean_Race_Date']]
        newdate = datediffs.index(min(datediffs))
        d['Next_Year_Event_Date_PM1'][i] = tmpdf.iloc[newdate]['Clean_Race_Date']
        d['Next_Year_Event_PM1'][i] = tmpdf.iloc[newdate]['RACE_Name']
        d['Next_Year_Distance_PM1'][i] = tmpdf.iloc[newdate]['RACE_Distance']
        
for i in d2.index.to_list():
    print(str(d2.index.to_list().index(i)+1) + ' of  7773.......')
    rid = d['Runner_ID'][i] # Get runner id
    pydate = d['Clean_Race_Date'][i] # Get PY event date
    tmpdf = data[data['Clean_Race_Date'] >= d['Clean_Race_Date'][i]+datetime.timedelta(365-30)] # Subset data
    tmpdf = tmpdf[tmpdf['Clean_Race_Date'] <= d['Clean_Race_Date'][i]+datetime.timedelta(365+30)] # Subset data
    tmpdf = tmpdf[tmpdf['Runner_ID'] == rid] # All races ran in window by runner
    tmpdf2 = data[data['Clean_Race_Date'] >= d['Clean_Race_Date'][i]+datetime.timedelta(30)] # Look for these races PY
    tmpdf2 = tmpdf2[tmpdf2['Clean_Race_Date'] <= d['Clean_Race_Date'][i]-datetime.timedelta(30)] # Look for these races PY
    tmpdf2 = tmpdf2[tmpdf2['Runner_ID'] == rid] # All races ran in window by runner
    
    for row in range(len(tmpdf)):
        
        en = tmpdf.iloc[row]['RACE_Name']
        ed = tmpdf.iloc[row]['RACE_Distance']
        
        for row2 in range(len(tmpdf2)):
            
            if (tmpdf2.iloc[row2]['RACE_Name'] == en) and (tmpdf2.iloc[row2]['RACE_Distance'] == ed):
                
                tmpdf = tmpdf.drop([list(tmpdf.index)[row]]) # Remove the row from tmpdf because they ran it in PY
                
    # Finally, find the median entry
    
    if len(tmpdf) == 0:
        
        d['PM_2_Months'][i] = 0
        d['Next_Year_Event_Date_PM2'][i] = None
        
    else:
        
        datediffs = [abs(pydate+datetime.timedelta(365) - xx) for xx in tmpdf['Clean_Race_Date']]
        newdate = datediffs.index(min(datediffs))
        d['Next_Year_Event_Date_PM2'][i] = tmpdf.iloc[newdate]['Clean_Race_Date']
        d['Next_Year_Event_PM1'][i] = tmpdf.iloc[newdate]['RACE_Name']
        d['Next_Year_Distance_PM1'][i] = tmpdf.iloc[newdate]['RACE_Distance']

# Write the final version of the dataframe d to file 

d.to_csv('C:/Users/' + username + '/Documents/Data/ultraCOVID/d.csv', index = False, encoding = 'utf-8-sig')

# Write data to csv just in case

data.to_csv('C:/Users/' + username + '/Documents/Data/ultraCOVID/large_d.csv', index = False, encoding = 'utf-8-sig')

