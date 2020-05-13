import json
import uuid
from datetime import datetime


_HIGHSCORES_CATEGORIES = ["best_time", "best_score"]
_LEVELS = ["level1"]
_NEW_PLAYER = {"name": "",
               "registration_date": "",
               "highscores": {"best_time": {"level1": 100000},
                              "best_score": {"level1": 10}
                              },
               "time_in_game": 0}


def update_highscores(player_id, player_highscores):
    with open("resources/players.json", "r") as highscores_data:
        highscores = json.load(highscores_data)
    for category in _HIGHSCORES_CATEGORIES:
        for level in highscores[category].keys():
            table = highscores["best_time"][level]
            table.append((player_id, player_highscores[category][level]))
            highscores[category][level].sort()
            if len(table) > 10:
                del table[-1]
            highscores[category][level] = table

    with open("resources/highscores.json", "w") as highscores_data:
        json.dump(highscores, highscores_data)


def update_statistics(player_id, player_statistics, player_highscores):
    with open("resources/players.json", "r") as players_data:
        players = json.load(players_data)
    players[player_id]["highscores"] = player_highscores
    players[player_id]["statistics"] = player_statistics
    with open("resources/players.json", "r") as players_data:
        json.dump(players, players_data)


def create_player(player_name, player_password):
    with open("resources/base.json", "r+") as base_data:
        base = json.load(base_data)
        new_id = str(uuid.uuid4())
        while base["name_by_id"].get(new_id, None) is not None:
            new_id = str(uuid.uuid4())
        base["name_by_id"][new_id] = player_name
        base["id_by_name"][player_name] = new_id

        base_data.seek(0)
        json.dump(base, base_data)
        base_data.truncate()

    with open("resources/security.json", "r+") as secure_data:
        security = json.load(secure_data)

        security[new_id] = {}
        security[new_id]["name"] = player_name
        security[new_id]["pass"] = player_password

        secure_data.seek(0)
        json.dump(security, secure_data)
        secure_data.truncate()

    with open("resources/player.json", "r+") as players_data:
        players = json.load(players_data)

        players[new_id] = _NEW_PLAYER
        players[new_id]["name"] = player_name
        players[new_id]["registration_date"] = str(datetime.now())

        players_data.seek(0)
        json.dump(players, players_data)
        players_data.truncate()


def check_login(player_name, player_password):
    with open("resources/base.json", "r") as base_data:
        base = json.load(base_data)
    player_id = base["id_by_name"].get(player_name, None)
    if player_id is not None:
        with open("resources/security.json", "r") as secure_data:
            security = json.load(secure_data)
        if security[player_id]["pass"] == player_password:
            return player_id
    return None


def get_stats(player_id):
    with open("resources/players.json", "r+") as players_data:
        players = json.load(players_data)
    player_stats = players.get("player_id", None)
    if player_stats is not None:
        return player_stats
    else:
        raise TypeError("There is no player with such id")
