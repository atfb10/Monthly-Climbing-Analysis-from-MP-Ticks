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
from users.user import MpUser

# Testing only
users = [MpUser(user[0], user[1], user[2]) for user in get_users()]
dataframes = []
[dataframes.append(get_user_ticks(user)) for user in users]
[zip_user_folder(user) for user in users]
[send_mail(user) for user in users]

# Scheduling
def job() -> None:
    '''
    arguments: 
    returns: None
    description: job() runs all functions to make the app perform intended functionality. But only if the day is the first of the month
    '''
    if date.today().day != 1:
        return
    users = [MpUser(user[0], user[1], user[2]) for user in get_users()]
    dataframes = []
    [dataframes.append(get_user_ticks(user)) for user in users]
    [zip_user_folder(user) for user in users]
    [send_mail(user) for user in users]
    return

# Job will run every day at 6am. It will do nothing except on the first of the month
schedule.every().day.at('06:00').do(job)
while True:
    schedule.run_pending()

'''
TODO: REMAINING STEPS
1. data
    a. NOTE (1): filter out to only previous 30 days
    b. plotly graphs (generate all graphs using per user @ "once" using threading [not really parallel, but you know what you mean]) 
    c. NOTE (2): txt file with data aggregated
 2. Logging to txt file
'''

'''
Graph Ideas
- Lead Style graphed (onsight, flash, redpoint, fell/hung)
- Boulder style graphed (flash, send, attempt)
- Count of days climbing outside vs not
- Pitches by day
- crags visited
- States climbed in
- Total feet climbed
- Feet climbed by day
- Word cloud taken from notes
- Histogram w/ Kernal Density Estimation plot by climbing grades. NOTE: Go to saved url under "coding" folder titled sort column in pandas by specific order for how to do this. Function that creates a dataframe that is sorted by route grade 
- Histogram w/ Kernal Density Estimation plot by bouldering grades. NOTE: Go to saved url under "coding" folder titled sort column in pandas by specific order for how to do this. Function that creates a dataframe that is sorted by bouldering grade
'''

'''
Text Data Ideas (.txt -> .html) Iteration 1 = data in a text file. Iteration 2 = table in html file. Iteration 3 -> in a bootstrap styled html file
- Number of feet climbed
- Hardest pitch sent
- Hardest pitch attempted
- Route climbed the most
- Boulder climbed the most
- Hardest boulder sent
- Hardest boulder climbed
- List of routes given four stars (your favorites of the month)
- List of routes given 1 star or a bomb (your least favorite climbs of the month)
- state where most pitches were climbed
- state with most days climbing at
- crag where most pitches were climbed
- crag with most days climbing at
- Longest route (by vertical feet)
- Biggest day of climbing (by vertical feet)
- likelihood (percentage) of onsighting/flashing a route of a specific grade
'''

'''
how I want to do HTML file.
1. Create dataframe with all the text data: do this by 
    a) extracting the values from the dataframe. 
    b) creating a dictionary object with each key as what the category and each value as the value for that category (example 'num_feet_climbed': length_variable) 
    c. Pass that dictionary into a dataframe object
2. Write the dataframe as a .html (iteration 2 = done)
3. Write the table to a pre-styled html file, and then save that html file for each user
'''