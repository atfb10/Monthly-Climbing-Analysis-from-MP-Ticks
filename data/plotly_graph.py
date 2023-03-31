'''
Author: Adam Forestier
Date: March 31, 2023
Description: plotly_graph.py contains the PlotlyGraph class
'''

import numpy as np
import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go
import plotly.figure_factory as ff
import os

from my_credentials import PATH_TO_PROJECT
from users.user import MpUser

class PlotlyGraph:
    '''
    objects of the PlotlyGraph class contains: 
    parameters: a user object
    methods: performs building of graphs files for user dataframe. Moves files to user's filepath 
    '''
    def __init__(self, user: MpUser):
        self.user = user

    def graph(self) -> None:
        '''
        arguments: self
        returns: none
        description: graph() calls the graphing methods of self
        '''
        self.distrubtion_of_quality_routes()
        return
    
    def move_graph_to_user_folder(self, filename):
        old_path = f'{PATH_TO_PROJECT}\\{filename}'
        new_path = f'{PATH_TO_PROJECT}\\user_files\\{self.user.username}\\{filename}'
        if os.path.isfile(new_path):
            os.remove(new_path)
        os.rename(old_path, new_path)
        return
    
    def distrubtion_of_quality_routes(self):
        '''
        arguments: self
        returns: None
        description: avg_stars_vs_user_stars() creates a scatterplot showing this relationship
        '''
        df = self.user.df
        data = [df['Avg Stars'], df['Your Stars']]
        labels = ['Mountain Project Stars', 'Your Stars']
        fig = ff.create_distplot(data, labels, bin_size=.5, show_hist=False, show_rug=False,)
        fig.update_layout(
            title_text='Distribution of Quality of Routes Climbed',
            xaxis_title='Stars',
            yaxis_title='Density'
            )
        filename = 'Distribution of Route Quality.html'
        pyo.plot(fig, filename=filename)
        self.move_graph_to_user_folder(filename)
        return
