'''
Author: Adam Forestier
Date: March 31, 2023
Description: statistics.py contains the MpUserStatistics class
'''

import numpy as np
import pandas as pd

from data.data import (
    BOULDERING_GRADES,
    BOULDERING_GRADES_TO_NUMERIC,
    ROCK_CLIMBING_GRADES,
    ROCK_CLIMBING_GRADES_TO_NUMERIC
)
from my_credentials import PATH_TO_PROJECT
import os
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
        strings_to_write = []
        strings_to_write.append(self.__hardest_route_attempt())
        strings_to_write.append(self.__hardest_route_sent())
        # strings_to_write.append(self.__hardest_boulder_sent()) # Handle when None
        strings_to_write.append(self.__total_feet_climbed())
        strings_to_write.append(self.__total_pitches_climbed())
        strings_to_write.append(self.__best_mp_rated_climb())
        strings_to_write.append(self.__worst_mp_rated_climb())
        strings_to_write.append(self.__four_star_climbs())
        strings_to_write.append(self.__bomb_climbs())
        strings_to_write.append(self.__longest_route_climbed())
        strings_to_write.append(self.__route_climbed_most_times())
        # strings_to_write.append(self.__boulder_climbed_most_times()) # Handle when None
        filename = self.user.txt_filename
        write_file = open(filename, 'w')
        self.__write_name_by_line(write_file, strings_to_write)
        write_file.close()
        self.__move_stats_user_folder(filename)
        return
    
    def __move_stats_user_folder(self, filename) -> None:
        '''
        arguments: self, name of file to move
        returns: none
        description: moves stats file to proper folder
        '''
        old_path = f'{PATH_TO_PROJECT}\\{filename}' 
        new_path = f'{PATH_TO_PROJECT}\\user_files\\{self.user.username}\\{filename}'
        if os.path.isfile(new_path):
            os.remove(new_path)
        os.rename(old_path, new_path)
        return
    
    def __write_name_by_line(self, file, write_set) -> None:
        index = 0
        for name in write_set:
            index += 1
            if index < len(write_set):
                file.write(f'{name}\n')
            else: file.write(f'{name}')
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
    
    def __assign_bouldering_grade_numeric(self, grade: str, bouldering_grade_dict: dict = BOULDERING_GRADES_TO_NUMERIC) -> int:
        '''
        arguments: self, grade, dictionary of climbing grades assigned to numeric
        returns: an integer value associated with a climbing grade
        description: __assign_climbing_grade_numeric utilizes a dicionary to associate a Yosemite Decimal System climbing with an integer 
        '''
        for key, value in bouldering_grade_dict.items():
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
        returns: dataframe with only rock climbs
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
        description: __highest_climbing_send returns a string with hardest route attempted 
        '''
        df = self.__only_sends_rock_climbing()
        num_rows = len(df) - 1
        hardest_route = df.iloc[num_rows,]
        route_name = hardest_route['Route']
        route_grade = hardest_route['Rating']
        return f'Hardest Send - {route_name}: {route_grade}'
    
    def __only_bouldering(self) -> pd.DataFrame:
        '''
        arguments: self
        returns:  dataframe with only boulders
        description: __only_rock_climbing returns a dataframe with only bouldering problems
        '''
        df = self.user.df
        df = df[df['Rating'].isin(BOULDERING_GRADES)]
        return df
    
    def __hardest_boulder_sent(self) -> str:
        '''
        arguments: self
        returns: dictionary of route name and its grade
        description: __highest_climbing_send returns a string with hardest route attempted 
        '''
        df = self.__only_bouldering()
        df['Numeric Grade'] = np.vectorize(self.__assign_bouldering_grade_numeric)(df['Rating'])
        df = df.sort_values(by=['Numeric Grade'], ascending=False)
        df = df[df['Lead Style'].isin(['Send', 'Flash', 'Lead'])]
        hardest_boulder = df.iloc[0,]
        route_name = hardest_boulder['Route']
        route_grade = hardest_boulder['Rating']
        return f'Hardest Bouldering Send - {route_name}: {route_grade}'
    
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
        df = df.sort_values(by=['Avg Stars'], ascending=False)
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
        df = df.sort_values(by=['Avg Stars'])
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
    
    def __longest_route_climbed(self) -> str:
        '''
        arguments: self
        returns: string of longest route you have climbed
        description: __longest_route_clmbed returns a string of the longest route you have climbed
        '''
        df = self.__only_rock_climbing()
        df = df.sort_values(by=['Length'], ascending=False)
        longest_route = df.iloc[0,]
        longest_route_name = longest_route['Route']
        longest_route_distance = longest_route['Length']
        return f'Your longest route - {longest_route_name}: {longest_route_distance} feet'
    
    def __route_climbed_most_times(self) -> str:
        '''
        arguments: self
        returns: string of route climbed the most time
        description: __route_climbed_most_times returns the route climbed the most times along with the laps
        '''
        df = self.__only_rock_climbing()
        most_climbed = df['Route'].value_counts().nlargest(1).to_frame()
        most_climbed = most_climbed.reset_index()
        most_climbed.columns = ['Route', 'Times Climbed']
        most_climbed = most_climbed.iloc[0,]
        most_climbed_name = most_climbed['Route']
        most_climbed_times = most_climbed['Times Climbed']
        return f'Most Climbed route - {most_climbed_name}: {most_climbed_times}x'

    def __boulder_climbed_most_times(self) -> str:
        '''
        arguments: self
        returns: string of route climbed the most time
        description: __route_climbed_most_times returns the route climbed the most times along with the laps
        '''
        df = self.__only_bouldering()
        most_climbed = df['Route'].value_counts().nlargest(1).to_frame()
        most_climbed = most_climbed.reset_index()
        most_climbed.columns = ['Boulder', 'Times Climbed']
        most_climbed = most_climbed.iloc[0,]
        most_climbed_name = most_climbed['Boulder']
        most_climbed_times = most_climbed['Times Climbed']
        return f'Most Climbed Boulder Problem - {most_climbed_name}: {most_climbed_times}x'