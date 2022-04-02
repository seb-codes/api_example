# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 15:53:44 2022

@author: Sebastian
"""

API_KEY = 't8TRqDt25mWFseYc979amOTfgVTkFOyZ3zCKJ9C2'

import requests
import pandas as pd

# Using the feed parameter 
response = requests.get('https://api.nasa.gov/neo/rest/v1/feed?start_date=2022-01-01&end_date=2022-01-07&api_key='+API_KEY)

data = response.json()

# arranging data from api response
num_of_neos = data['element_count']

prev_range_request_link = data['links']['prev']
next_range_request_link = data['links']['next']

df = pd.DataFrame()

# grabbing data needed, and manipulating to be able to put data into dataframe
for key in data['near_earth_objects']:
    # print(key)
    for i in range(len(data['near_earth_objects'][key])):
        close_approach_date = data['near_earth_objects'][key][i]['close_approach_data'][0]['close_approach_date']
        miss_distance_miles = data['near_earth_objects'][key][i]['close_approach_data'][0]['miss_distance']['miles']
        relative_velocity_mph = data['near_earth_objects'][key][i]['close_approach_data'][0]['relative_velocity']['miles_per_hour']
        estimated_diameter_max_ft = data['near_earth_objects'][key][i]['estimated_diameter']['feet']['estimated_diameter_max']
        estimated_diameter_min_ft = data['near_earth_objects'][key][i]['estimated_diameter']['feet']['estimated_diameter_min']
        
        data['near_earth_objects'][key][i].pop('close_approach_data')
        data['near_earth_objects'][key][i].pop('links')
        data['near_earth_objects'][key][i].pop('estimated_diameter')
        
        data['near_earth_objects'][key][i].update({"estimated_diameter_max_ft": estimated_diameter_max_ft, 
                                                   "estimated_diameter_min_ft": estimated_diameter_min_ft,
                                                   "close_approach_date":close_approach_date,
                                                   "miss_distance_miles":miss_distance_miles,
                                                   "relative_velocity_mph":relative_velocity_mph})
    
        df_holder = pd.DataFrame(data['near_earth_objects'][key][i],index=[0])
        df = df.append(df_holder,ignore_index=True)
        
# can output this data into database or csv

df.to_csv('neos_feed_data.csv')

# Using Lookup id paramater

response = requests.get('https://api.nasa.gov/neo/rest/v1/neo/2001036?api_key='+API_KEY)

data = response.json()

# same logic to organizing data as before, just on 1 record
close_approach_date = data['close_approach_data'][0]['close_approach_date']
miss_distance_miles = data['close_approach_data'][0]['miss_distance']['miles']
relative_velocity_mph = data['close_approach_data'][0]['relative_velocity']['miles_per_hour']
estimated_diameter_max_ft = data['estimated_diameter']['feet']['estimated_diameter_max']
estimated_diameter_min_ft = data['estimated_diameter']['feet']['estimated_diameter_min']

data.pop('close_approach_data')
data.pop('links')
data.pop('estimated_diameter')

data.update({"estimated_diameter_max_ft": estimated_diameter_max_ft, 
                                           "estimated_diameter_min_ft": estimated_diameter_min_ft,
                                           "close_approach_date":close_approach_date,
                                           "miss_distance_miles":miss_distance_miles,
                                           "relative_velocity_mph":relative_velocity_mph})

df2 = pd.DataFrame(data,index=[0])

df2.to_csv('lookup_data.csv')

# Using Browse Parameter 

response = requests.get('https://api.nasa.gov/neo/rest/v1/neo/browse?api_key='+API_KEY)

data = response.json()

# similar process as above would go here, just saving time from redundancy.