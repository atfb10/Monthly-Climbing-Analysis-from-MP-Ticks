from database.mp_db import get_users
from helpers.email import send_mail
from helpers.files import (
    get_user_ticks,
    zip_user_folder
    )
from data.plotly_graph import PlotlyGraph
from data.statistics import MpUserStatistics
from users.user import MpUser

users = [MpUser(user[0], user[1], user[2]) for user in get_users()]
[get_user_ticks(user) for user in users]
adam = users[0]
adam_stats = MpUserStatistics(adam)
adam_graph = PlotlyGraph(adam)
adam_stats.stats()
adam_graph.graph()

# [zip_user_folder(user) for user in users]
# [send_mail(user) for user in users]
zip_user_folder(adam)
send_mail(adam)