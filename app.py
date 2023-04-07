'''
author: Adam Forestier
date: March 28, 2023
description: app.py manages function calls and object creation to run the project
'''
from datetime import date
import schedule

from database.mp_db import get_users
from helpers.email import send_mail
from helpers.files import (
    get_user_ticks,
    zip_user_folder
    )
from data.plotly_graph import PlotlyGraph
from data.statistics import MpUserStatistics
from users.user import MpUser

# Scheduling
def job() -> None:
    '''
    arguments: 
    returns: None
    description: job() runs all functions to make the app perform intended functionality. But only if the day is the first of the month
    '''
    if date.today().day != 1:
        return

    # Create objects
    users = [MpUser(user[0], user[1], user[2]) for user in get_users()]
    [get_user_ticks(user) for user in users]
    users_stats = [MpUserStatistics(user) for user in users]
    users_graphs = [PlotlyGraph(user) for user in users]

    # Get stats, graph, zip and send email for objects
    [user.stats() for user in users_stats]
    [user.graph() for user in users_graphs]
    [zip_user_folder(user) for user in users]
    [send_mail(user) for user in users]

# Job will run every day at 6am. It will do nothing except on the first of the month
schedule.every().day.at('06:00').do(job)
while True:
    schedule.run_pending()