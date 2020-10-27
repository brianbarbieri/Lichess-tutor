import requests
import json, ndjson
from tqdm import tqdm
from collections import Counter

from app.config import Config   

def connect_to_API(username, params):
    url = "https://lichess.org/api"
    print(f"Gathering data for {username}")
    response = requests.get(f"{url}/games/user/{username}",
        params=params,
        headers={
            "Authorization": f"Bearer {Config.token}", # need this or you will get a 401: Not Authorized response
            "Accept": "application/x-ndjson"    # required to recieve data as ndjson format
        })

    # parse application/x-ndjson into list of JSON objects
    games = []
    ndjson = response.content.decode().split("\n")

    for json_obj in ndjson:
        if json_obj:
            games.append(json.loads(json_obj))
    return games

def get_move_tree(username, depth):
    """
    Returns move tree, which is a tree of all the moves played by the player and their ending
    """

    from app.logic.utils import set_by_path, get_by_path
    params={
        "perfType" : "blitz",
        "rated" :  "true",
        "opening" : "true",
        "moves" : "true"
    }
    games = connect_to_API(username, params)

    filtered_games = []
    for game in games:
        if game.get("winner"):
            unw = game.get("players").get("white").get("user").get("name")
            unb = game.get("players").get("black").get("user").get("name")
            if (game.get("winner") == "white" and username == unw) or (game.get("winner") == "black" and username == unb):
                conclusion = "won"
            else:
                conclusion = "lost"
        else:
            conclusion = "tie"

        filtered_game = {
            "id" : game["id"],
            "moves" : game["moves"].split(" "),
            "outcome" : conclusion
        } 
        filtered_games.append(filtered_game) 


    tree = {}
    # first create the move tree
    for i in range(1, depth):
        for game in filtered_games:
            moves = game.get("moves")[:i]
            if len(moves) == i: #else it will overwrite branches with short games
                set_by_path(tree, moves, {"score" : {
                        "won" : 0,
                        "lost" : 0,
                        "tie" : 0
                }})

    # fill the scores in the move tree
    for i in range(1, depth):
        for game in filtered_games:
            moves = game.get("moves")[:i]
            moves.append("score")
            moves.append(game["outcome"])
            set_by_path(tree, moves, get_by_path(tree, moves) + 1)
    return tree

def get_top_games(username, max_):
    """
    Returns the top x openings of a player for each possible ending and colour
    """
    params={
        "perfType" : "blitz",
        "rated" :  "true",
        "opening" : "true",
        "moves" : "false"
    }
    games = connect_to_API(username, params)

    # seperate games for black and white games
    white_games, black_games = [], []
    for game in games:
        if game.get("opening"):
            if game.get("players").get("white").get("user").get("name") == username:
                white_games.append(game)
            else:
                black_games.append(game)

    return_dict = {}
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
                if i == max_:
                    break
                return_dict[colour][str_conc].append(opn)
    return return_dict
