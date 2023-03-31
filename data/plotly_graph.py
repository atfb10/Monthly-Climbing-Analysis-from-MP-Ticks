'''
Author: Adam Forestier
Date: March 31, 2023
Description: plotly_graph.py contains the PlotlyGraph class
'''

import numpy as np
import pandas as pd
import plotly.express as px
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
        self.lead_style_count_graphed()
        return
    
    def move_graph_to_user_folder(self, filename) -> None:
        '''
        arguments: self, name of file to move
        returns: none

        '''
        old_path = f'{PATH_TO_PROJECT}\\{filename}' 
        new_path = f'{PATH_TO_PROJECT}\\user_files\\{self.user.username}\\{filename}'
        if os.path.isfile(new_path):
            os.remove(new_path)
        os.rename(old_path, new_path)
        return
    
    def distrubtion_of_quality_routes(self) -> None:
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
    
    def change_to_tr_if_no_lead(self, style: str) -> str:
        '''
        arguments: self
        returns: original string if not "Not Led", else returns Toprope
        description: changes "Not Led" to toprope
        '''
        if style == 'Not Led':
            style = 'Toprope'
        return style
    
    def lead_style_count_graphed(self):
        '''
        arguments: self
        returns: None
        description: countplot of number of each leadstyle
        '''
        df = self.user.df
        df = df[df['Route Type'] != 'Boulder']
        df['Lead Style'] = np.vectorize(self.change_to_tr_if_no_lead)(df['Lead Style'])
        fig = px.histogram(df, x='Lead Style', color='Lead Style', title='Roped Climb Style Count', text_auto=True)
        filename =  'Roped Climb Style Count.html'
        pyo.plot(fig, filename=filename)
        self.move_graph_to_user_folder(filename)
        return