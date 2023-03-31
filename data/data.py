'''
Author: Adam Forestier
Date: March 27, 2023
Description: data.py contains functions to cleanse and aggregate user data
'''

import numpy as np
import pandas as pd

US_STATE_TO_ABBREVIATION = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY"
}

US_STATE_LIST = [
    "Alabama",
    "Alaska",
    "Arizona",
    "Arkansas",
    "California",
    "Colorado",
    "Connecticut",
    "Delaware",
    "Florida",
    "Georgia",
    "Hawaii",
    "Idaho",
    "Illinois",
    "Indiana",
    "Iowa",
    "Kansas",
    "Kentucky",
    "Louisiana",
    "Maine",
    "Maryland",
    "Massachusetts",
    "Michigan",
    "Minnesota",
    "Mississippi",
    "Missouri",
    "Montana",
    "Nebraska",
    "Nevada",
    "New Hampshire",
    "New Jersey",
    "New Mexico",
    "New York",
    "North Carolina",
    "North Dakota",
    "Ohio",
    "Oklahoma",
    "Oregon",
    "Pennsylvania",
    "Rhode Island",
    "South Carolina",
    "South Dakota",
    "Tennessee",
    "Texas",
    "Utah",
    "Vermont",
    "Virginia",
    "Washington",
    "West Virginia",
    "Wisconsin",
    "Wyoming"
]

ROCK_CLIMBING_GRADES = [
    '5.6',
    '5.7',
    '5.7+',
    '5.8-',
    '5.8',
    '5.8+',
    '5.9-',
    '5.9',
    '5.9+',
    '5.10a',
    '5.10a/b',
    '5.10-',
    '5.10b',
    '5.10b/c',
    '5.10',
    '5.10c',
    '5.10c/d',
    '5.10+',
    '5.10d',
    '5.11a',
    '5.11a/b',
    '5.11-', 
    '5.11b', 
    '5.11b/c', 
    '5.11', 
    '5.11c', 
    '5.11c/d', 
    '5.11+', 
    '5.11d', 
    '5.12a', 
    '5.12a/b', 
    '5.12-', 
    '5.12b', 
    '5.12b/c', 
    '5.12', 
    '5.12c', 
    '5.12c/d', 
    '5.12+', 
    '5.12d', 
    '5.13a', 
    '5.13a/b', 
    '5.13-', 
    '5.13b/c', 
    '5.13', 
    '5.13c', 
    '5.13c/d', 
    '5.13+', 
    '5.13d', 
    '5.14a', 
    '5.14a/b', 
    '5.14-', 
    '5.14b', 
    '5.14b/c', 
    '5.14', 
    '5.14c', 
    '5.14c/d', 
    '5.14+', 
    '5.14d', 
    '5.15a', 
    '5.15a/b', 
    '5.15-', 
    '5.15b', 
    '5.15b/c', 
    '5.15', 
    '5.15', 
    '5.15c', 
    '5.15c/d', 
    '5.15+', 
    '5.15d'
]

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    '''
    arguments: uncleansed dataframe of mountain project user ticks
    returns: cleansed dataframe of mountain project user ticks
    description: clean_data() cleans a mountain project data frame to 
    ''' 
    df = df.drop('Rating Code', axis=1)
    df = df.rename(columns={'Your Rating': 'Your Grade'})
    df['Your Grade'] = df['Your Grade'].fillna('Not Assigned')
    df['Notes'] = df['Notes'].fillna('No Notes')
    df['Date'] = pd.to_datetime(df['Date'])
    df['Lead Style'] = df['Lead Style'].fillna('Not Led')
    df['Style'] = df['Style'].fillna('Not Specified')
    single_p_mean = round(df[df['Pitches'] == 1]['Length'].mean())
    df['Length'] = df['Length'].fillna(single_p_mean)
    return df

def extract_crag(location: str) -> str:
    '''
    arguments: dataframe of user data
    returns: the state
    description: extract_state is a helper method to create th state columns
    '''
    split_locations = location.split(' > ')
    return split_locations[len(split_locations) - 1]

def extract_state(location: str) -> str:
    '''
    arguments: dataframe of user data
    returns: the state
    description: extract_state is a helper method to create th state columns
    '''
    split_locations = location.split(' > ')
    return split_locations[0]

def add_cols(df: pd.DataFrame) -> pd.DataFrame:
    '''
    arguments: dataframe of user data
    returns: dataframe of user data with columns added
    description: add_cols() creates new columns for the dataframe to be analyzed
    '''
    df['Route Crag'] = np.vectorize(extract_crag)(df['Location'])
    df['Route State'] = np.vectorize(extract_state)(df['Location'])
    return df