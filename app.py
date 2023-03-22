'''
author: Adam Forestier
date: March 22, 2023
description: app.py manages function calls and object creation to run the project
'''
from database.mp_db import get_users
from helpers.files import get_user_ticks
from users.user import MpUser

users = [MpUser(user[0], user[1], user[2]) for user in get_users()]

for user in users:
    get_user_ticks(user)

# TODO: REMAINING STEPS
# 1. data
#    a. plotly graphs (generate all graphs using per user @ "once" using threading [not really parallel, but you know what you mean]) 
#    b. txt file with data aggregated
# 2. zip the username folder under the user_files directory
# 3. email the user the zip file
# 4. schedule when it should run
# 5. Logging to txt file