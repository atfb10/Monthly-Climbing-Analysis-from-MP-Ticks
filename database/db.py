'''
Author: Adam Forestier
Date: March 20, 2023
Description: db.py 
'''
import sqlite3 as sql

from .db_connection import DatabaseConnection
from ..users.user import MpUser

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
        cursor.execute(
            'INSERT INTO USERS(?, ?, ?, ?, ?, ?)', (
            user.userid, user.username, 
            user.email, user.user_tick_url, 
            user.user_tick_export_url, 
            user.csv_filename
            )
        )
    return

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
        print(f'User {all_users[user][1]} -> {all_users[user][0]}')
    return

def delete(username: str) -> None:
    '''
    arguments: none
    returns: none
    description: delete() takes in a user's username and deletes that user
    '''
    with DatabaseConnection(HOST) as connection:
        cursor = connection.cursor()
        cursor.execute('DELETE FROM USERS WHERE username=?', (username,))