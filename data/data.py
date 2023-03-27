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
    df['Your Grade'] = df['Your Grade'].fillna('Not assigned')
    df['Notes'] = df['Notes'].fillna('No Notes')
    df['Date'] = pd.to_datetime(df['Date'])
    return df