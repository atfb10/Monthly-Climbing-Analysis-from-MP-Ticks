'''
Author: Adam Forestier
Date: March 28, 2023
Description: files contains various functions regarding files
'''
import os
import pandas as pd
import shutil as sh
from typing import List

from data.data import (
    add_cols,
    clean_data
    )
from my_credentials import PATH_TO_PROJECT
from users.user import MpUser

# For testing only

def get_user_ticks(user: MpUser) -> List[pd.DataFrame]:
    '''
    arguments: MpUser object
    returns: nothing
    description: get_user_ticks() downloads a user's ticks as a csv from mountainproject.com and then moves the csv to the appropriate folder
                 additionally, it cleans the sets the data field to a pd.datetime field and returns the cleansed dataframe
    '''
    df = pd.read_csv(user.user_tick_export_url)
    df = clean_data(df)
    df = add_cols(df)
    df.to_csv(user.csv_filename, index=False)
    move_user_csv(user)
    return df

def move_user_csv(user: MpUser) -> None:
    '''
    arguments: an MpUser object
    returns: None
    description: move_user_csv() moves the csv files in the parent directory into a users subfolder under the user_files directory
    '''
    old_path = f'{PATH_TO_PROJECT}\\{user.csv_filename}'
    new_path = f'{PATH_TO_PROJECT}\\user_files\\{user.username}\\{user.csv_filename}'
    if os.path.isfile(new_path):
        os.remove(new_path)
    os.rename(old_path, new_path)
    return

def make_user_files_folder(user: MpUser):
    '''
    arguments: an MpUser object
    returns: none
    description: make_user_files_folder creates a folder under the user_files directory for each user that will store their data files
    '''
    parent_dir = "user_files/"
    user_folder = str(user.username)
    path = os.path.join(parent_dir, user_folder)
    os.mkdir(path)
    return

def zip_user_folder(user: MpUser):
    '''
    arguments: an MpUser object
    returns: None
    description: zip_user_folder creates a zip folder that contains a users graph and data files
    '''
    parent_dir = 'user_files/'
    user_folder = str(user.username)
    path = os.path.join(parent_dir, user_folder)
    sh.make_archive(f'{path}', 'zip', path)
    return