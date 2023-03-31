'''
Author: Adam Forestier
Date: March 31, 2023
Description: statistics.py contains the MpUserStatistics class
'''

import numpy as np
import pandas as pd
from users.user import MpUser

class PlotlyGraphMpUserStatistics:
    '''
    objects of the PlotlyGraph class contains: 
    parameters: a user object
    methods: performs building of statistical table files for user dataframe. Moves files to user's filepath 
    '''
    def __init__(self, user: MpUser):
        self.user = user