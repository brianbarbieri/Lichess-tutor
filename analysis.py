import berserk
import datetime as dt

with open("secret.csv", "r") as r:
    data = [line.replace("\n","").split(",") for line in r.readlines()]
    username = data[0][1]
    token = data[1][1]

session = berserk.TokenSession(token)
client = berserk.Client(session=session)

start = berserk.utils.to_millis(dt.datetime(2018, 12, 8))
end = berserk.utils.to_millis(dt.datetime(2020, 12, 9))
games = client.games.export_by_player(username, since=start, until=end, rated=False, max=300, perf_type="blitz", moves=False, opening=True)
print(list(games)[0])
