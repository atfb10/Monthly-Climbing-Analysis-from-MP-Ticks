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
        self.__distrubtion_of_quality_routes()
        self.__lead_style_count_graphed()
        self.__boulder_style_count_graphed()
        return
    
    def __move_graph_to_user_folder(self, filename) -> None:
        '''
        arguments: self, name of file to move
        returns: none
        description: moves graph file to proper folder
        '''
        old_path = f'{PATH_TO_PROJECT}\\{filename}' 
        new_path = f'{PATH_TO_PROJECT}\\user_files\\{self.user.username}\\{filename}'
        if os.path.isfile(new_path):
            os.remove(new_path)
        os.rename(old_path, new_path)
        return
    
    def __distrubtion_of_quality_routes(self) -> None:
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
        self.__move_graph_to_user_folder(filename)
        return
    
    def __change_to_tr_if_no_lead(self, style: str) -> str:
        '''
        arguments: self, string of style type
        returns: original string if not "Not Led", else returns Toprope
        description: changes "Not Led" to toprope
        '''
        if style == 'Not Led':
            style = 'Toprope'
        return style
    
    def __change_to_boulder_terms(self, style: str) -> str:
        '''
        arguments: self, string of style type
        returns: original string if not onsight or redpoint. Else corrects to boulder terminology of flash or send
        '''
        if style == 'onsight':
            style == 'flash'
        elif style == 'redpoint' or style == 'Lead':
            style == 'send'
        return style
    
    def __lead_style_count_graphed(self):
        '''
        arguments: self
        returns: None
        description: countplot of number of each leadstyle
        '''
        df = self.user.df
        df = df[df['Route Type'] != 'Boulder']
        df['Lead Style'] = np.vectorize(self.__change_to_tr_if_no_lead)(df['Lead Style'])
        fig = px.histogram(df, x='Lead Style', color='Style', title='Roped Climb Style Count', text_auto=True)
        filename =  'Roped Climb Style Count.html'
        pyo.plot(fig, filename=filename)
        self.__move_graph_to_user_folder(filename)
        return
    
    def __boulder_style_count_graphed(self):
        '''
        arguments: self
        returns: None
        description: countplot of number of each boulder style
        '''
        df = self.user.df
        df = df[df['Route Type'] == 'Boulder']
        df['Style'] = np.vectorize(self.__change_to_boulder_terms)(df['Style'])
        fig = px.histogram(df, x='Style', color='Style', title='Boulder Style Count', text_auto=True)
        filename =  'Boulder Style Count.html'
        pyo.plot(fig, filename=filename)
        self.__move_graph_to_user_folder(filename)
        return