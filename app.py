from concurrent.futures import ThreadPoolExecutor
import time

from helpers.files import (
    get_user_ticks
)

# Utilizing threading 
# with ThreadPoolExecutor(max_workers=2) as pool:
#     t = time.time()
#     pool.submit(get_user_ticks(test_user))
#     pool.submit(get_user_ticks(test_user1))
#     print(f'time to get ticks with theading = {time.time() - t}')

# TODO: REMAINING STEPS
# 1. Get all users from the database
# 2. call get_user_ticks
# 3. data
#    a. plotly graphs
#    b. txt file with data aggregated
# 4. zip the username folder under the user_files directory
# 5. email the user the zip file
# 6. schedule when it should run