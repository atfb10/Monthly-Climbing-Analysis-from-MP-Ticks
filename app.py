import pandas as pd

from credentials import (
    test_user,
    test_user1
)

tick_data = pd.read_csv(test_user1.user_tick_export_url)
file_name = f'{test_user1.username}-ticks.csv'
tick_data.to_csv(file_name, index=False)