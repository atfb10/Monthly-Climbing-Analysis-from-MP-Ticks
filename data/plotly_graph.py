'''
Author: Adam Forestier
Date: March 31, 2023
Description: plotly_graph.py contains the PlotlyGraph class
'''
import json
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.offline as pyo
import plotly.graph_objs as go
import plotly.figure_factory as ff
import os

from data.data import (
    ROCK_CLIMBING_GRADES,
    US_STATE_TO_ABBREVIATION,
    US_STATE_LIST
)
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
        self.__map_pitches_by_state()
        self.__pitches_by_crag()
        self.__feet_by_crag()
        self.__map_feet_by_state()
        self.__feet_by_date()
        self.__pitches_by_date()
        self.__routes_by_style()
        self.__rock_routes_by_grade()
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
        elif style == 'redpoint':
            style == 'send'
        elif style == 'Lead':
            style = 'send'
        return style
    
    def __lead_style_count_graphed(self) -> None:
        '''
        arguments: self
        returns: None
        description: countplot of number of each leadstyle
        '''
        df = self.user.df
        df = df[df['Route Type'] != 'Boulder']
        df['Lead Style'] = np.vectorize(self.__change_to_tr_if_no_lead)(df['Lead Style'])
        fig = px.histogram(df, x='Lead Style', color='Lead Style', title='Roped Climb Style Count', text_auto=True)
        filename =  'Roped Climb Style Count.html'
        pyo.plot(fig, filename=filename)
        self.__move_graph_to_user_folder(filename)
        return
    
    def __boulder_style_count_graphed(self) -> None:
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
    
    def __map_pitches_by_state(self) -> None:
        '''
        arguments: self
        returns: none
        description: __map_pitches_by_state displays a heat map on a US map by number of pitches done in each state
        '''
        with open('D:\\coding\\projects\\mp-user-tick-analysis\\us-states.json') as response:
            states = json.load(response)
        df = self.user.df
        df = df.groupby('Route State').sum()['Pitches']
        df = df.reset_index()
        df.columns = ['State', 'Pitches']
        df = df[df['State'].isin(US_STATE_LIST)]
        df['State'] = df['State'].map(US_STATE_TO_ABBREVIATION)
        max_pitches = df['Pitches'].max()
        fig = px.choropleth(df, geojson=states, locations='State', color='Pitches', color_continuous_scale='Viridis', range_color=(0, max_pitches), scope='usa', title='Pitches Climbed by State')
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        filename =  'Climbing Map Pitches.html'
        pyo.plot(fig, filename=filename)
        self.__move_graph_to_user_folder(filename)
        return
    
    def __map_feet_by_state(self) -> None:
        '''
        arguments: self
        returns: none
        description: __map_feet_by_state displays a heat map on a US map by number of feet climbed in each state
        '''
        with open('D:\\coding\\projects\\mp-user-tick-analysis\\us-states.json') as response:
            states = json.load(response)
        df = self.user.df
        df = df.groupby('Route State').sum()['Length']
        df = df.reset_index()
        df.columns = ['State', 'Feet Climbed']
        df = df[df['State'].isin(US_STATE_LIST)]
        df['State'] = df['State'].map(US_STATE_TO_ABBREVIATION)
        max_pitches = df['Feet Climbed'].max()
        fig = px.choropleth(df, geojson=states, locations='State', color='Feet Climbed', color_continuous_scale='Turbo', range_color=(0, max_pitches), scope='usa', title='Feet Climbed by State')
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        filename =  'Climbing Map Feet.html'
        pyo.plot(fig, filename=filename)
        self.__move_graph_to_user_folder(filename)
        return
    
    def __pitches_by_crag(self) -> None:
        '''
        arguments: self
        returns: none
        description: __pitches_by_crag graphs the total number of pitches by crag
        '''
        df = self.user.df
        df = df.groupby('Route Crag').sum()['Pitches']
        df = df.reset_index()
        df.columns = ['Crag', 'Pitch Count']
        fig = px.histogram(df, x='Crag', y='Pitch Count', color='Crag', title='Pitches by Crag', text_auto=True)
        filename =  'Pitches by Crag.html'
        pyo.plot(fig, filename=filename)
        self.__move_graph_to_user_folder(filename)
        return
    
    def __feet_by_crag(self) -> None:
        '''
        arguments: self
        returns: none
        description: __feet_by_crag graphs the total number of feet climbed by crag
        '''
        df = self.user.df
        df = df.groupby('Route Crag').sum()['Length']
        df = df.reset_index()
        df.columns = ['Crag', 'Feet Climbed']
        fig = px.histogram(df, x='Crag', y='Feet Climbed', color='Crag', title='Feet Climbed by Crag')
        filename =  'Feet by Crag.html'
        pyo.plot(fig, filename=filename)
        self.__move_graph_to_user_folder(filename)
        return
    
    def __pitches_by_date(self) -> None:
        '''
        arguments: self
        returns: none
        description: __pitches_by_date graphs the total number of pitches by date
        '''
        df = self.user.df
        df = df.groupby('Date').sum()['Pitches']
        df = df.reset_index()
        df.columns = ['Date', 'Pitch Count']
        fig = px.histogram(df, x='Date', y='Pitch Count', title='Pitches by Date', text_auto=True)
        filename =  'Pitches by Date.html'
        pyo.plot(fig, filename=filename)
        self.__move_graph_to_user_folder(filename)
        return
    
    def __feet_by_date(self) -> None:
        '''
        arguments: self
        returns: none
        description: __pitches_by_state graphs the total number of feet climbed by date
        '''
        df = self.user.df
        df = df.groupby('Date').sum()['Length']
        df = df.reset_index()
        df.columns = ['Date', 'Feet Climbed']
        fig = px.histogram(df, x='Date', y='Feet Climbed', title='Feet Climbed by Date')
        filename =  'Feet by Date.html'
        pyo.plot(fig, filename=filename)
        self.__move_graph_to_user_folder(filename)
        return
    
    def __routes_by_style(self) -> None:
        '''
        arguments: self
        returns: none
        description: __routes_by_style graphs the total number of routes by style
        '''
        df = self.user.df
        routes_by_style = df['Route Type'].value_counts()
        routes_by_style = routes_by_style.to_frame()
        routes_by_style = routes_by_style.reset_index()
        routes_by_style.columns = ['Type', 'Route Count']
        fig = px.histogram(routes_by_style, x='Type', y='Route Count', color='Type', title='Routes Climbed by Route Type')
        filename =  'Route Counts by Route Type.html'
        pyo.plot(fig, filename=filename)
        self.__move_graph_to_user_folder(filename)
        return
    
    def __rock_routes_by_grade(self) -> None:
        '''
        arguments: self
        returns: None
        description: __rock_routes_by_grade shows the number of rock climbs done by grade is ascending order of difficulty on the x-axis
        '''
        df = self.user.df
        df['Rating'] = np.vectorize(lambda rating: rating.strip())(df['Rating'])
        df = df[df['Rating'].isin(ROCK_CLIMBING_GRADES)]
        grades = df['Rating'].value_counts()
        grades = grades.reset_index()
        grades.columns = ['Grade', 'Number of Routes']
        fig = px.histogram(grades, x='Grade', y='Number of Routes', color='Grade', title='Number of Rock Routes Climbed by Grade', category_orders={'Grade': ROCK_CLIMBING_GRADES})
        filename = 'Rock Climb Count by Grade.html'
        pyo.plot(fig, filename=filename)
        self.__move_graph_to_user_folder(filename)
        return