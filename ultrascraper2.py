# This script harvests the data for a paper on the impact of COVID on ultramarathoning

# Importing required modules

import urllib
from bs4 import BeautifulSoup as bs
import pandas as pd

# Specifiying your username

username = 'Michael'

# Defining the url

base = 'https://calendar.ultrarunning.com/event/'
mid = '/race/'
end = '/results'

# Defining a helper function for converting the race name to url format

def race_name(name):
    
    new_name = name.lower().replace(' ', '-').replace(':', '').replace('(', '').replace(')', '').replace(',', '-').replace("'", '-').replace('/', '-').replace('&', '-').replace('---', '-').replace('--', '-')
    
    return new_name

# Defining a helper function for parsing individual results

def result_parser(dat, year, race, dist, cit, st, fins, mon, date, nat):
        
    flag = False
    output = []
    
    while flag == False:
        
        try:
            
            x = dat.index('runner_id')
            dat = dat[x+11:]
            x = dat.index(',')
            runner_id = dat[:x]
            
            x = dat.index('finish_time')
            dat = dat[x+13:]
            x = dat.index(',')
            fin_time = dat[:x]
            
            x = dat.index('overall_place')
            dat = dat[x+15:]
            x = dat.index(',')
            overall_place = dat[:x]
            
            x = dat.index('age')
            dat = dat[x+5:]
            x = dat.index(',')
            age = dat[:x]
            
            x = dat.index('age_group_place')
            dat = dat[x+17:]
            x = dat.index(',')
            age_group_place = dat[:x]
            
            x = dat.index('gender')
            dat = dat[x+9:]
            x = dat.index('",')
            gender = dat[:x]
            
            x = dat.index('gender_place')
            dat = dat[x+14:]
            x = dat.index(',')
            gender_place = dat[:x]
            
            x = dat.index('total_distance')
            dat = dat[x+17:]
            x = dat.index('",')
            total_distance = dat[:x]
            
            x = dat.index('fullName')
            dat = dat[x+11:]
            x = dat.index('",')
            athlete = dat[:x]
            
            x = dat.index('city')
            dat = dat[x+7:]
            x = dat.index('",')
            city = dat[:x]
            
            x = dat.index('state')
            dat = dat[x+8:]
            x = dat.index('",')
            state = dat[:x]
            
            x = dat.index('country')
            dat = dat[x+10:]
            x = dat.index('",')
            country = dat[:x]
            
            x = dat.index('oldest_result_date')
            dat = dat[x+21:]
            x = dat.index('",')
            oldest_race = dat[:x]
            
            x = dat.index('latest_result_date')
            dat = dat[x+21:]
            x = dat.index('",')
            latest_race = dat[:x]
            
            x = dat.index('active_years')
            dat = dat[x+15:]
            x = dat.index('},')
            time_series = dat[:x]
            
            x = dat.index('result_count')
            dat = dat[x+14:]
            x = dat.index(',')
            total_races = dat[:x]
            
            out = [race, dist, year, mon, date, cit, st, nat, fins, runner_id,
                   athlete, fin_time, overall_place, age, age_group_place,
                   gender, gender_place, total_distance, city, state, country,
                   oldest_race, latest_race, time_series, total_races]
            
            output.append(out)
            
        except:
            
            flag = True
    
    return output

# Loading the data from ultrascraper1.py

ultra_df = pd.read_csv('C:/Users/' + username + '/Documents/Data/ultraCOVID/race_data.csv')

# Scraping the results data for each race

scraped = []
missed = []
race_dat = []

for i in range(len(ultra_df)):
    
    print('Harvesting data from race ' + str(i+1) + ' of ' + str(len(ultra_df)) + '.......')
    
    try:
        
        url = base + race_name(ultra_df.Name[i]) + mid + str(ultra_df.ID[i]) + end # Create the url
        page = urllib.request.Request(url, headers = {'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(page)
        soup = bs(response, 'html.parser')
        data = str(soup.find_all('race-results')).replace('&quot;', '"')
        scrape = result_parser(data, ultra_df.Year[i], ultra_df.Name[i], ultra_df.Distance[i],
                               ultra_df.City[i], ultra_df.State[i], ultra_df.Finishers[i],
                               ultra_df.Month[i], ultra_df.Date[i], ultra_df.Nation[i])
        scraped.append(scrape)
        racedat = [list(ultra_df.iloc[i]) for j in range(len(scrape))]
        race_dat.append(racedat)
        
    except:
        
        missed.append(i)
    
# Create a dataframe (eventually)

event_names = [s[i][0] for s in scraped for i in range(len(s))]
event_types = [s[i][1] for s in scraped for i in range(len(s))]
years = [s[i][2] for s in scraped for i in range(len(s))]
mons = [s[i][3] for s in scraped for i in range(len(s))]
dates = [s[i][4] for s in scraped for i in range(len(s))]
host_cities = [s[i][5] for s in scraped for i in range(len(s))]
host_states = [s[i][6] for s in scraped for i in range(len(s))]
host_nats = [s[i][7] for s in scraped for i in range(len(s))]
finishers = [s[i][8] for s in scraped for i in range(len(s))]

r_ids = [s[i][9] for s in scraped for i in range(len(s))]
names = [s[i][10] for s in scraped for i in range(len(s))]
times = [s[i][11] for s in scraped for i in range(len(s))]
places = [s[i][12] for s in scraped for i in range(len(s))]
ages = [s[i][13] for s in scraped for i in range(len(s))]
age_places = [s[i][14] for s in scraped for i in range(len(s))]
gender = [s[i][15] for s in scraped for i in range(len(s))]
gender_places = [s[i][16] for s in scraped for i in range(len(s))]
distances = [s[i][17] for s in scraped for i in range(len(s))]
cities = [s[i][18] for s in scraped for i in range(len(s))]
states = [s[i][19] for s in scraped for i in range(len(s))]
countries = [s[i][20] for s in scraped for i in range(len(s))]
first_race = [s[i][21] for s in scraped for i in range(len(s))]
last_race = [s[i][22] for s in scraped for i in range(len(s))]
history = [s[i][23] for s in scraped for i in range(len(s))]
race_counts = [s[i][24] for s in scraped for i in range(len(s))]

RACEname = [dat[i][0] for dat in race_dat for i in range(len(dat))]
RACEdistance = [dat[i][1] for dat in race_dat for i in range(len(dat))]
RACEcity = [dat[i][2] for dat in race_dat for i in range(len(dat))]
RACEstate = [dat[i][3] for dat in race_dat for i in range(len(dat))]
RACEfinishers = [dat[i][4] for dat in race_dat for i in range(len(dat))]
RACEmonth = [dat[i][5] for dat in race_dat for i in range(len(dat))]
RACEdate = [dat[i][6] for dat in race_dat for i in range(len(dat))]
RACEyear = [dat[i][7] for dat in race_dat for i in range(len(dat))]
RACEid = [dat[i][8] for dat in race_dat for i in range(len(dat))]
RACEnation = [dat[i][9] for dat in race_dat for i in range(len(dat))]

# Cleaning the data

# Helper function for some rare (and manually validated) gender notational mixups

def gender_update(g):
    
    domain = ['M', 'F', 'N', 'W', 'A']
    codomain = ['M', 'F', 'M', 'F', 'M']
    
    try:
        
        g_new = codomain[domain.index(g)]
        
    except:
        
        g_new = 'U'
    
    return g_new

# Cleaning gender data

gender = [gender_update(g) for g in gender]

# Cleaning first and previous race data

first_race = [f[0:10] for f in first_race]
first_race = ['' if f[0:3] == 'ull' else f for f in first_race]
last_race = [l[0:10] for l in last_race]
last_race = ['' if l[0:3] == 'ull' else l for l in last_race]

# Cleaning results data (time and distance)

times = [t.replace('"', '') for t in times]
times = ['' if str(t)[0] in ['n', 'u'] else t for t in times]

distances = [d.replace('"', '') for d in distances]
distances = ['' if str(d)[0] in ['n', 'u'] else d for d in distances]

# Cleaning athlete location data

cities = ['' if c[0:3] == 'ull' else c for c in cities]
states = ['' if s[0:3] == 'ull' else s for s in states]
states = [s.replace('state":"', '').replace('\\u00a0', '') for s in states]
countries = ['' if c[0:3] == 'ull' else c for c in countries]

# Cleaning names

names = ['' if 'Unknown' in n else n for n in names]

# Making the dataframe

scraped_df = pd.DataFrame({'Runner_ID': r_ids, 'Name': names, 'Time': times,
                           'Overall': places, 'Age': ages, 'Age_Place': age_places,
                           'Gender': gender, 'Gender_Place': gender_places,
                           'Distance': distances, 'City': cities, 'State': states,
                           'Country': countries, 'First_Race_Date': first_race,
                           'Previous_Race_Date': last_race, 'Race_History': history,
                           'Total_Races': race_counts, 'RACE_ID': RACEid,
                           'RACE_Name': RACEname, 'RACE_Distance': RACEdistance,
                           'RACE_Date': RACEdate, 'RACE_Month': RACEmonth,
                           'RACE_Year': RACEyear, 'RACE_City': RACEcity,
                           'RACE_State': RACEstate, 'RACE_Nation': RACEnation,
                           'RACE_Finisher_Count': RACEfinishers})

# Dropping observations with missing data

scraped_df = scraped_df[scraped_df.Gender != 'U'].reset_index(drop = True)
scraped_df = scraped_df[scraped_df.Age != 'null'].reset_index(drop = True)
scraped_df.Age = pd.to_numeric(scraped_df.Age)
scraped_df = scraped_df[scraped_df.Age < 100].reset_index(drop = True)
scraped_df = scraped_df[scraped_df.Time != 'DNF'].reset_index(drop = True)
scraped_df = scraped_df[scraped_df.Overall != '0'].reset_index(drop = True)
scraped_df = scraped_df[scraped_df.City != ''].reset_index(drop = True)
scraped_df = scraped_df[scraped_df.State != ''].reset_index(drop = True)
scraped_df = scraped_df[scraped_df.Country != ''].reset_index(drop = True)
scraped_df = scraped_df[scraped_df.First_Race_Date != ''].reset_index(drop = True)

# Save dataframe to file

scraped_df.to_csv('C:/Users/' + username + '/Documents/Data/ultraCOVID/raw_results_data.csv', index = False, encoding = 'utf-8-sig')

