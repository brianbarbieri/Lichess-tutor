import requests
import json, ndjson
from tqdm import tqdm
from collections import Counter
import os

from app.config import Config   

def get_top_games(username):
    url = "https://lichess.org/api"
    print(f"Gathering data for {username}")
    response = requests.get(f'{url}/games/user/{username}',
        params={
            "perfType" : "blitz",
            "rated" :  "true",
            "opening" : "true",
            "moves" : "false"
        },
        headers={
            'Authorization': f'Bearer {Config.token}', # need this or you will get a 401: Not Authorized response
            "Accept": "application/x-ndjson"    # required to recieve data as ndjson format
        })

    # parse application/x-ndjson into list of JSON objects
    games = []
    ndjson = response.content.decode().split('\n')

    for json_obj in ndjson:
        if json_obj:
            games.append(json.loads(json_obj))

    # seperate games for black and white games
    white_games, black_games = [], []
    for game in games:
        if game.get("opening"):
            if game.get("players").get("white").get("user").get("name") == username:
                white_games.append(game)
            else:
                black_games.append(game)

    top = 5
    return_dict = {"username" : username}
    for colour, col_games in zip(["white", "black"],[white_games, black_games]):
        wins, lost, draws = [], [], []
        for game in col_games:
            if game.get("winner") == colour:
                wins.append(game)
            elif game.get("winner") == None:
                draws.append(game)
            else:
                lost.append(game)
        return_dict[colour] = {}
        
        for conc, str_conc in zip([wins, lost, draws],["win", "lost", "draw"]):
            return_dict[colour][str_conc] = []
            most_common = Counter([game["opening"]["name"] for game in conc]).most_common()
            most_common_percentage = [(opening[0], round(opening[1]/len(conc)*100,2)) for opening in most_common]
            for i, opn in enumerate(most_common_percentage):
                if i == top:
                    break
                return_dict[colour][str_conc].append(opn)
    print(return_dict)
    return return_dict
