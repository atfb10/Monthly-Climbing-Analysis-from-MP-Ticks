'''
author: Adam Forestier
date: March 28, 2023
description: app.py manages function calls and object creation to run the project
'''

from database.mp_db import get_users
from helpers.email import send_mail
from helpers.files import (
    get_user_ticks,
    zip_user_folder
    )
from users.user import MpUser

# Run the Application
users = [MpUser(user[0], user[1], user[2]) for user in get_users()]
dataframes = []
[dataframes.append(get_user_ticks(user)) for user in users]
[zip_user_folder(user) for user in users]
[send_mail(user) for user in users]

# TODO: REMAINING STEPS
# 1. data
#    a. NOTE (1): filter out to only previous 30 days
#    b. plotly graphs (generate all graphs using per user @ "once" using threading [not really parallel, but you know what you mean]) 
#    c. NOTE (2): txt file with data aggregated
# 2. NOTE (3): schedule when it should run
# 3. Logging to txt file


'''
Graph Ideas
- Sends vs Fell/Hung
- Count of days climbing outside vs not
- Pitches by day
- crags visited
- States climbed in
- Total feet climbed
- Feet climbed by day
'''