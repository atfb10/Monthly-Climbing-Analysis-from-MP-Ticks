'''
author: Adam Forestier
date: March 31, 2023
description: test_graphs.py tests is here to test the app's graphing functionality without waiting for the scheduler
'''

from database.mp_db import get_users
from helpers.email import send_mail
from helpers.files import (
    get_user_ticks,
    zip_user_folder
    )
from data.plotly_graph import PlotlyGraph
from users.user import MpUser

users = [MpUser(user[0], user[1], user[2]) for user in get_users()]
[get_user_ticks(user) for user in users]
# here I need to do the stats and graph calls
justin = users[2]
justin_graph = PlotlyGraph(justin)
justin_graph.graph()



[zip_user_folder(user) for user in users]




# [send_mail(user) for user in users]