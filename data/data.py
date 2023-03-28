'''
Author: Adam Forestier
Date: March 27, 2023
Description: data.py contains functions to cleanse and aggregate user data
'''

# TODO: Turn this into a data class with a dataframe as a parameter and all functions as a method
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

# def extract_crag(df: pd.DataFrame) -> pd.DataFrame:


#     return crag

# def extract_state(df: pd.DataFrame) -> pd.DataFrame:
#     split_locations = df

#     return state