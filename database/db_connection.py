'''
Author: Adam Forestier
Date: March 20, 2023
Description: db_connection contains a context manager for the projects SQLite3 database
'''

import sqlite3 as sql

class DatabaseConnection:
    def __init__(self, host) -> None:
        self.connection = None
        self.host = host
    def __enter__(self) -> sql.Connection:
        self.connection = sql.connect(self.host)
        return self.connection
    def __exit__(self, exc_type, exc_val, exc_tb) -> None: # exc = exception. type = type. val = value. tb = traceback
        if exc_type or exc_val or exc_tb:
            self.connection.close()
        else:
            self.connection.commit()
            self.connection.close()

        