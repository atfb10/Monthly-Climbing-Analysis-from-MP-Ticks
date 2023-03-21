'''
Author: Adam Forestier
Date: March 20, 2023
Description: files contains various functions regarding files
'''
import os
import pandas as pd

from users.user import MpUser

def get_user_ticks(user: MpUser) -> None:
    '''
    arguments: MpUser object
    returns: nothing
    description: get_user_ticks() downloads a user's ticks as a csv from mountainproject.com and then moves the csv to the appropriate folder
    '''
    df = pd.read_csv(user.user_tick_export_url)
    df.to_csv(user.csv_filename, index=False)
    move_user_csv(user)
    return

def move_user_csv(user: MpUser) -> None:
    '''
    arguments: an MpUser object
    returns: None
    description: move_user_csv() moves the csv files in the parent directory into a users subfolder under the user_files directory
    '''
    new_path = f'files/{user.username}/{user.csv_filename}'
    os.rename(user.csv_filename, new_path)
    return

def make_user_files_folder(user: MpUser):
    '''
    arguments: an MpUser object
    returns: none
    description: make_user_files_folder creates a folder under the user_files directory for each user that will store their data files
    '''
    user_folder = str(user.username)
    parent_dir = "/user_files/"
    path = os.path.join(parent_dir, user_folder)
    os.mkdir(path)
    return