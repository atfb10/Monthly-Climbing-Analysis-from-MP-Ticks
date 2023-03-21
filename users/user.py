'''
Author: Adam Forestier
Date: March 20, 2023
Description: user contains the User class that ticks are downloaded for
'''

class MpUser:
    BASE_URL = 'https://www.mountainproject.com/user/'
    TICK = '/ticks'
    TICK_EXPORT = '/tick-export'

    def __init__(self, userid: int, username: str, email: str):
        '''
        every mountain project user has a userid and username
        '''
        self.userid = userid
        self.username = username
        self.email = email
        self.user_tick_url = f'{self.BASE_URL}{userid}/{username}{self.TICK}'
        self.user_tick_export_url = f'{self.BASE_URL}{userid}/{username}{self.TICK_EXPORT}'
        self.csv_filename = f'{username}-monthly-ticks.csv'

    def __repr__(self) -> str:
        '''
        prints the user's id and name 
        '''
        return f'User ID: {self.userid}. Username: {self.username}'