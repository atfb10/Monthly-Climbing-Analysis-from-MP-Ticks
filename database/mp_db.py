'''
Author: Adam Forestier
Date: March 20, 2023
Description: db.py 
'''
from typing import List

from .db_connection import DatabaseConnection
from users.user import MpUser

HOST = 'data.db'

def create_user_table() -> None:
    '''
    arguments: none
    returns: none
    description: create_user_table() creates a table for user objects to be stored if the table does not yet exist
    '''
    with DatabaseConnection(HOST) as connection:
        cursor = connection.cursor()
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS USERS(username text primary key, userid int, email text, user_tick_url text, user_tick_export_url text, csv_filename text)'
        )
    return

def insert(user: MpUser) -> None:
    '''
    arguments: user object
    returns: none
    description: insert_user() inserts a new user into the database
    '''
    with DatabaseConnection(HOST) as connection:
        cursor = connection.cursor()
        cursor.execute('INSERT INTO USERS VALUES(?, ?, ?, ?, ?, ?)', (user.userid, user.username, user.email, user.user_tick_url, user.user_tick_export_url, user.csv_filename))
    return

def get_users() -> List[MpUser]:
    '''
    arguments: None
    returns: List of MpUser objects
    description: get_users() lists all users by their id and username in the terminal
    '''
    with DatabaseConnection(HOST) as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT username, userid, email FROM USERS')    
        all_users = cursor.fetchall() 
    return all_users

def list_users() -> None:
    '''
    arguments: None
    returns: None
    description: list_all_users() lists all users by their id and username in the terminal
    '''
    with DatabaseConnection(HOST) as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT username, userid FROM USERS')    
        all_users = cursor.fetchall()     
    for user in all_users:
        print(f'User {user[0]} -> {user[1]}')
    return

def delete_user(username: str) -> None:
    '''
    arguments: none
    returns: none
    description: delete() takes in a user's username and deletes that user
    '''
    with DatabaseConnection(HOST) as connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM USERS WHERE userid=?", (username,))
    return

def delete_all_users() -> None:
    '''
    aerguments: None
    returns: None
    description: delete_all_users() deletes all users from the USERS table
    '''
    with DatabaseConnection(HOST) as connection:
        cursor = connection.cursor()
        cursor.execute('DELETE FROM USERS',)