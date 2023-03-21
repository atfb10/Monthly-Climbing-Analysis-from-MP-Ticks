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
# 1. Create users for the database
# 2. Get all users from the database
# 3. call get_user_ticks
# 4. data
#    a. plotly graphs
#    b. txt file with data aggregated
# 5. zip the username folder under the user_files directory
# 6. email the user the zip file
# 7. schedule when it should run