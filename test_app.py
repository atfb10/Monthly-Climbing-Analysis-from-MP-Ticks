'''
author: Adam Forestier
date: April 7, 2023
description: test_app.py tests the app's graphing and statistical functionality without waiting for the scheduler
'''

from database.mp_db import get_users
from helpers.email import send_mail
from helpers.files import (
    get_user_ticks,
    zip_user_folder
    )
from data.plotly_graph import PlotlyGraph
from data.statistics import MpUserStatistics
from users.user import MpUser

# Create objects
users = [MpUser(user[0], user[1], user[2]) for user in get_users()]
# [get_user_ticks(user) for user in users]

for user in users:
    get_user_ticks(user)
    print(f'Ticks gotten for {user.username}')


users_stats = [MpUserStatistics(user) for user in users]
users_graphs = [PlotlyGraph(user) for user in users]

for user in users_stats:
    user.stats()
    print(f'Stats gotten for {user.user.username}')


for user in users_graphs:
    user.graph()
    print(f'graphs produced for {user.user.username}')


# Get stats, graph, zip and send email for objects
# [user.stats() for user in users_stats]
# [user.graph() for user in users_graphs]
[zip_user_folder(user) for user in users]
# [send_mail(user) for user in users]