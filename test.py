'''
author: Adam Forestier
date: March 31, 2023
description: test.py tests is here to test the app functionality without waiting for the scheduler
'''

from database.mp_db import get_users
from helpers.email import send_mail
from helpers.files import (
    get_user_ticks,
    zip_user_folder
    )
from users.user import MpUser

users = [MpUser(user[0], user[1], user[2]) for user in get_users()]
dataframes = []
[dataframes.append(get_user_ticks(user)) for user in users]
[zip_user_folder(user) for user in users]







# [send_mail(user) for user in users]