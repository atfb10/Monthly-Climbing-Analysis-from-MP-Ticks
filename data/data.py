'''
Author: Adam Forestier
Date: March 27, 2023
Description: data.py contains functions to cleanse and aggregate user data
'''

# TODO: Turn this into a data class with a dataframe as a parameter and all functions as a method
import numpy as np
import pandas as pd

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