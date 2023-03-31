'''
Author: Adam Forestier
Date: March 31, 2023
Description: statistics.py contains the MpUserStatistics class
'''

import numpy as np
import pandas as pd

from data.data import (
    ROCK_CLIMBING_GRADES,
    ROCK_CLIMBING_GRADES_TO_NUMERIC
)
from users.user import MpUser

class MpUserStatistics:
    '''
    objects of the PlotlyGraph class contains: 
    parameters: a user object
    methods: performs building of statistical table files for user dataframe. Moves files to user's filepath 
    '''
    def __init__(self, user: MpUser):
        self.user = user
    
    def stats(self) -> None:
        '''
        arguments: self
        returns: none
        description: stats() gathers statistical information and writes it a csv file
        '''
        hardest_attempt_string = self.__hardest_route_attempt()
        hardest_send_string = self.__hardest_route_sent()
        total_feet_climbed_string = self.__total_feet_climbed()
        total_pitches_climbed_string = self.__total_pitches_climbed()
        best_mp_rated_route_string = self.__best_mp_rated_climb()
        worst_mp_rated_route_string = self.__worst_mp_rated_climb()
        four_star_routes_string = self.__four_star_climbs()
        bomb_climbs_string = self.__bomb_climbs()
        return
    
    def __assign_climbing_grade_numeric(self, grade: str, climbing_grade_dict: dict = ROCK_CLIMBING_GRADES_TO_NUMERIC) -> int:
        '''
        arguments: self, grade, dictionary of climbing grades assigned to numeric
        returns: an integer value associated with a climbing grade
        description: __assign_climbing_grade_numeric utilizes a dicionary to associate a Yosemite Decimal System climbing with an integer 
        '''
        for key, value in climbing_grade_dict.items():
            if key == grade:
                return value
        return -1 # Something went wrong
    
    def __order_by_climbing_grades(self) -> pd.DataFrame:
        '''
        arguments: self
        returns: ordered dataframe with only rock climbs
        description: __order_by_climbing_grades orders a dataframe by climbing difficulty in ascending order
        '''
        df = self.__only_rock_climbing()
        df['Numeric Grade'] = np.vectorize(self.__assign_climbing_grade_numeric)(df['Rating'])
        df = df.sort_values(by=['Numeric Grade'])
        return df
    
    def __only_rock_climbing(self) -> pd.DataFrame:
        '''
        arguments: self
        returns: ordered dataframe with only rock climbs
        description: __only_rock_climbing returns a dataframe with only rock climbs
        '''
        df = self.user.df
        df = df[df['Rating'].isin(ROCK_CLIMBING_GRADES)]
        return df
    
    def __only_sends_rock_climbing(self) -> pd.DataFrame:
        '''
        arguments: self
        returns: dataframe with only sends while roped
        description: __only_sends_rock_climbing filters out unsent lead climbing
        '''
        df = self.__order_by_climbing_grades()
        df = df[df['Lead Style'].isin(['Onsight', 'Flash', 'Redpoint'])]
        return df
    
    def __hardest_route_attempt(self) -> str:
        '''
        arguments: self
        returns: dictionary of route name and its grade
        description: __highest_climbing_send returns a tuple with hardest route attempted 
        '''
        df = self.__order_by_climbing_grades()
        num_rows = len(df) - 1
        hardest_route = df.iloc[num_rows,]
        route_name = hardest_route['Route']
        route_grade = hardest_route['Rating']
        return f'Hardest Route Attempted - {route_name}: {route_grade}'

    def __hardest_route_sent(self) -> str:
        '''
        arguments: self
        returns: dictionary of route name and its grade
        description: __highest_climbing_send returns a tuple with hardest route attempted 
        '''
        df = self.__only_sends_rock_climbing()
        num_rows = len(df) - 1
        hardest_route = df.iloc[num_rows,]
        route_name = hardest_route['Route']
        route_grade = hardest_route['Rating']
        return f'Hardest Send - {route_name}: {route_grade}'
    
    def __total_feet_climbed(self):
        '''
        arguments: self
        returns: string of feet climbed
        description: __total_feet_climbed returns total feet climbed as a string
        '''
        df = self.user.df
        feet = df['Length'].sum()
        return str(f'Total Feet Climbed: {feet}')
    
    def __total_pitches_climbed(self) -> str:
        '''
        arguments: self
        returns: string of pitches climbed
        description: __total_pitches_climbed returns total feet climbed as a string
        '''
        df = self.user.df
        p = int(df['Pitches'].sum())
        return str(f'Total Feet Climbed: {p}')
    
    def __best_mp_rated_climb(self) -> str:
        '''
        arguments: self
        returns: string of best climb
        description: __best_mp_rated_climb returns highest rated mountain project climb
        '''
        df = self.user.df
        df = df.sort_values(by=['Avg Stars'])
        best_climb = df.iloc[0,]
        best_climb_name = best_climb['Route']
        best_climb_stars = best_climb['Avg Stars']
        return f'Highest Rated MP Route Climbed - {best_climb_name}: {best_climb_stars}'
    
    def __worst_mp_rated_climb(self) -> str:
        '''
        arguments: self
        returns: string of worst climb
        description: __worst_mp_rated_climb returns lowed rated mountain project climb
        '''
        df = self.user.df
        df = df.sort_values(by=['Avg Stars'], ascending=False)
        worst = df.iloc[0,]
        worst_climb_name = worst['Route']
        worst_climb_stars = worst['Avg Stars']
        return f'Lowest Rated MP Route Climbed - {worst_climb_name}: {worst_climb_stars}'
    
    def __four_star_climbs(self) -> str:
        '''
        arguments: self
        returns: string with list of routes user has given 4 stars
        description: __four_star_climbs shows a user their 4 star climbs
        '''
        df = self.user.df
        df = df[df['Your Stars'] == 4]
        four_star_routes = df['Route'].tolist()
        four_star_routes = str(four_star_routes)
        return f'Your 4 Star Routes: {four_star_routes}'
    
    def __bomb_climbs(self) -> str:
        '''
        arguments: self
        returns: string with list of routes user has given 4 stars
        description: __four_star_climbs shows a user their 4 star climbs
        '''
        df = self.user.df
        df = df[df['Your Stars'] == 0]
        bombs = df['Route'].tolist()
        bombs = str(bombs)
        return f'Your least favorite climbs: {bombs}'