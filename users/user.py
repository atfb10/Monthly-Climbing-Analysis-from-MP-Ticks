'''
Author: Adam Forestier
Date: March 17, 2023
Description: user contains the User class that ticks are downloaded for
'''

class MpUser:
    BASE_URL = 'https://www.mountainproject.com/user/'

    def __init__(self, username: str, userid=int):
        '''
        every mountain project user has a userid and username
        '''
        self.username = username
        self.userid = userid
        self.user_tick_url = f'{self.BASE_URL}{userid}/{username}/ticks'

    def __repr__(self) -> str:
        '''
        prints the user's id and name 
        '''
        return f'User ID: {self.userid}. Username: {self.username}'