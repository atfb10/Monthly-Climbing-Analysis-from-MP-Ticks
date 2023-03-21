'''
Author: Adam Forestier
Date: March 20, 2023
Description: user_addition_removal.py allows an administrator to add, list and remove users from the database
'''

from database import db
from helpers.files import make_user_files_folder
from users.user import MpUser

USER_OPTIONS = '''
Enter:
- 'a' to add a new user
- 'l' to list all users
- 'd' to delete a user
- 'q' to quit
'''

def menu(menu_options=USER_OPTIONS) -> None:
    '''
    arguments: options displayed to the user. Defaulted to user options
    returns: none
    description: menu gives an admin a menu to control the addition, listing and deletion of users in the terminal
    '''
    admin_selection = input(menu_options)
    while admin_selection != 'q':
        if admin_selection == 'a':
            username = input('Enter username: ')
            userid = input('Enter user id: ')
            user_email = input('Enter user email: ')
            new_user = MpUser(userid=userid, username=username, email=user_email)
            db.insert(new_user)
            make_user_files_folder(new_user)
        elif admin_selection == 'l':
            db.list_users()
        elif admin_selection == 'd':
            user_to_delete = input('Enter username of user to delete: ')
            db.delete(user_to_delete)
        else:
            print('Invalid operation. Select again')
        admin_selection = input(menu_options)
    return

db.create_user_table()
menu()