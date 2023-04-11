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

ROCK_CLIMBING_GRADES_TO_NUMERIC = {
    '5.6': 0,
    '5.7': 1,
    '5.7+': 2,
    '5.8-': 3,
    '5.8': 4,
    '5.8+': 5,
    '5.9-': 6,
    '5.9': 7,
    '5.9+': 8,
    '5.10a': 9,
    '5.10a/b': 10,
    '5.10-': 11,
    '5.10b': 12,
    '5.10b/c': 13,
    '5.10': 14,
    '5.10c': 15,
    '5.10c/d': 16,
    '5.10+': 17,
    '5.10d': 18,
    '5.11a': 19,
    '5.11a/b': 20,
    '5.11-': 21, 
    '5.11b': 22, 
    '5.11b/c': 23, 
    '5.11': 24, 
    '5.11c': 25, 
    '5.11c/d': 26, 
    '5.11+': 27, 
    '5.11d': 28, 
    '5.12a': 29, 
    '5.12a/b': 30, 
    '5.12-': 31, 
    '5.12b': 32, 
    '5.12b/c': 33, 
    '5.12': 34, 
    '5.12c': 35, 
    '5.12c/d': 36, 
    '5.12+': 37, 
    '5.12d': 38, 
    '5.13a': 39, 
    '5.13a/b': 40, 
    '5.13-': 41, 
    '5.13b/c': 42, 
    '5.13': 43, 
    '5.13c': 44, 
    '5.13c/d': 45, 
    '5.13+': 46, 
    '5.13d': 47, 
    '5.14a': 48, 
    '5.14a/b': 49, 
    '5.14-': 50, 
    '5.14b': 51, 
    '5.14b/c': 52, 
    '5.14': 53, 
    '5.14c': 54, 
    '5.14c/d': 55, 
    '5.14+': 56, 
    '5.14d': 57, 
    '5.15a': 58, 
    '5.15a/b': 59, 
    '5.15-': 60, 
    '5.15b': 61, 
    '5.15b/c': 62, 
    '5.15': 63, 
    '5.15': 64, 
    '5.15c': 65, 
    '5.15c/d': 66, 
    '5.15+': 67, 
    '5.15d': 68
}

BOULDERING_GRADES = [
    'V-Easy', 
    'V1',
    'V1+',
    'V2',
    'V2+',
    'V3', 
    'V3+',
    'V4',
    'V4+',
    'V5',
    'V5+', 
    'V6',
    'V6+',
    'V7',
    'V7+',
    'V8', 
    'V8+',
    'V9',
    'V9+',
    'V10',
    'V10+',
    'V11',
    'V12',
    'V13', 
    'V14',
    'V15',
    'V16',
    'V17',
]

BOULDERING_GRADES_TO_NUMERIC = {
    'V-Easy':0, 
    'V1':1,
    'V1+':2,
    'V2':3,
    'V2+':4,
    'V3':5, 
    'V3+':6,
    'V4':7,
    'V4+':8,
    'V5':9,
    'V5+':10, 
    'V6':11,
    'V6+':12,
    'V7':13,
    'V7+':14,
    'V8':15, 
    'V8+':16,
    'V9':17,
    'V9+':18,
    'V10':19,
    'V10+':20,
    'V11':21,
    'V12':22,
    'V13':23, 
    'V14':24,
    'V15':25,
    'V16':26,
    'V17':27,
}

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
    df['Length'] = df.groupby('Route Type')['Length'].transform(lambda val: val.fillna(val.mean)) # missing route length is determined by calculating the average length of that route type
    # single_p_mean = round(df[df['Pitches'] == 1]['Length'].mean())
    # df['Length'] = df['Length'].fillna(single_p_mean)
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