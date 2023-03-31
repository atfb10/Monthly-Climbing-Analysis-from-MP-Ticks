'''
author: Adam Forestier
date: March 31, 2023
description: test_stats.py tests is here to test the app's statistics functionality without waiting for the scheduler
'''

from database.mp_db import get_users
from helpers.email import send_mail
from helpers.files import (
    get_user_ticks,
    zip_user_folder
    )
from data.plotly_graph import PlotlyGraph
from users.user import MpUser