# This script harvests the data for a paper on the impact of COVID on ultramarathoning

# Importing required modules

import urllib
from bs4 import BeautifulSoup as bs
import pandas as pd

# Specifiying your username

username = ''

# Defining the url base

base = 'https://calendar.ultrarunning.com/race-results?page='

# Scraping data from the races

goToRace = []
names = []
events = []
months = []
dates = []
years = []
finishers = []
cities = []
states = []

# As of February 5, 2021 this more than ensures all races since January 1, 2010 are included
# This will eventually need updating :: check this and update manually if using!

page_count = 900

for x in range(1,page_count):
    
    print('Retrieving data from search page ' + str(x) + ' of ' + str(page_count) + '.......')
    
    # Scraping the webpage
    
    url = base + str(x)
    page = urllib.request.Request(url, headers = {'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(page)
    soup = bs(response, 'html.parser')
    data = soup.find_all('tr')[0:20]
    data = [str(d) for d in data]
    
    # Parsing the meaningful information from the raw data
    
    for d in data:
        
        # The link to the race specific data page
        
        link_id1 = d.index('goToRace')
        link_id2 = d.index(')">')
        link = d[link_id1+9:link_id2]
        goToRace.append(link)
        
        # Month of event
        
        d = d[link_id2+5:]
        month_id1 = d.index('month">')
        month_id2 = d.index('</div>')
        month = d[month_id1+7:month_id2]
        months.append(month)
        
        # Date of event
        
        d = d[month_id2+8:]
        date_id1 = d.index('day')
        date_id2 = d.index('</div>')
        date = d[date_id1+5:date_id2]
        dates.append(date)
        
        # Year of event
        
        d = d[date_id2+1:]
        skip = d.index('<div')
        d = d[skip+1:]
        yr_id1 = d.index('year">')
        yr_id2 = d.index('</div>')
        yr = d[yr_id1+6:yr_id2]
        years.append(int(yr))
        
        # Event type / distance
        
        d = d[yr_id2+9:]
        name_id1 = d.index('bold">')
        name_id2 = d.index('</a>')
        name = d[name_id1+6:name_id2]
        names.append(name)
        
        # Event type / distance
        
        d = d[name_id2+18:]
        event_id1 = d.index('location">')
        event_id2 = d.index('/')
        event = d[event_id1+10:event_id2-2]
        events.append(event)
        
        # Finisher count
        
        d = d[event_id2+2:]
        fin_id2 = d.index('finishers')
        fin = d[:fin_id2-1]
        finishers.append(fin)
        
        # City of race
        
        skip = d.index('/')
        d = d[skip:]
        city_id2 = d.index(',')
        city = d[2:city_id2]
        cities.append(city)
        
        # State of race
        
        d = d[city_id2+2:]
        state_id2 = d.index('</div>')
        state = d[:state_id2]
        states.append(state)
        
# Cleaning this data before saving as a df

names = [n.replace('&amp;','&') for n in names]
splits = [int('split' in e) for e in events] # A list of indices for splits (not actual races)

# Creating the dataframe

ultra_df = pd.DataFrame({'Name': names, 'Distance': events, 'City': cities,
                         'State': states, 'Finishers': finishers, 'Month': months,
                         'Date': dates, 'Year': years, 'ID': goToRace, 'Split': splits})

us = ['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA', 'HI', 'IA',
      'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MS',
      'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA',
      'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY'] # A list of states in the US
canada = ['AB', 'BC', 'MB', 'NB', 'NL', 'ON', 'PE', 'QC', 'SK', 'YT'] # A list of territories in Canada
usca = us + canada # A list of states/territories in the US & Canada

ultra_df = ultra_df[ultra_df.Year >= 2010].reset_index(drop = True) # Subset for year >= 2010
ultra_df = ultra_df[ultra_df.Split == 0].reset_index(drop = True) # Subset for full races only (no split times)
ultra_df = ultra_df[ultra_df.State.isin(usca)].reset_index(drop = True) # Subset for races in US & Canada only

nation = ['US' if ultra_df.State[i] in us else 'CAN' for i in range(len(ultra_df))] # Nation identifier
ultra_df = pd.concat([ultra_df, pd.Series(nation, name = 'Nation')], axis = 1) # Append to df
ultra_df = ultra_df.drop('Split', axis = 1) # Remove Split from df

# Saving the dataframe to file

ultra_df.to_csv('C:/Users/' + username + '/Documents/Data/ultraCOVID/race_data.csv', index = False, encoding = 'utf-8-sig')

