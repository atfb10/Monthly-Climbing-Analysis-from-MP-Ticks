'''
Author: Adam Forestier
Date: March 20, 2023
Description: user_addition_removal.py allows an administrator to add, list and remove users from the database
'''

from database import mp_db
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
    admin_selection.lower
    while admin_selection != 'q':
        if admin_selection == 'a':
            username = input('Enter username: ')
            userid = input('Enter user id: ')
            user_email = input('Enter user email: ')
            new_user = MpUser(userid=userid, username=username, email=user_email)
            mp_db.insert(new_user)
            make_user_files_folder(new_user)
        elif admin_selection == 'l':
            mp_db.list_users()
        elif admin_selection == 'd':
            username = input('Enter username of user to delete: ').strip()
            mp_db.delete_user(username)
        else:
            print('Invalid operation. Select again')
        admin_selection = input(menu_options)
        admin_selection.lower
    return

mp_db.create_user_table()
menu()