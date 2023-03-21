'''
Author: Adam Forestier
Date: March 2-, 2023
Description: files contains various functions regarding files
'''
import pandas as pd

from users.user import MpUser

def get_user_ticks(user: MpUser) -> None:
    '''
    arguments: MpUser object
    returns: nothing
    description: get_user_ticks() takes in a user object and returns
    '''
    df = pd.read_csv(user.user_tick_export_url)
    df.to_csv(user.csv_filename, index=False)
    return

# TODO: Create function to remove user files from within their directory prior to adding the new ones each month

# TODO: Add user files to their respective folder after they have been generated for the month & the previous months have been removed

# TODO: Create user folder within files directory whenever a new user is added to the database