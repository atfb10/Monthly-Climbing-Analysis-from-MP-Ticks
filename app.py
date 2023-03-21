from concurrent.futures import ThreadPoolExecutor
import time

from helpers.files import (
    get_user_ticks
)
from credentials import (
    test_user,
    test_user1
)

# Utilizing threading 
with ThreadPoolExecutor(max_workers=2) as pool:
    t = time.time()
    pool.submit(get_user_ticks(test_user))
    pool.submit(get_user_ticks(test_user1))
    print(f'time to get ticks with theading = {time.time() - t}')