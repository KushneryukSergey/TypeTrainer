import json
import uuid
from datetime import datetime

_PLAYER_DATA_FILE = "resources/players.json"
_HIGHSCORES_DATA_FILE = "resources/highscores.json"
_BASE_DATA_FILE = "resources/base.json"
_SECURITY_DATA_FILE = "resources/security.json"

HIGHSCORES_CATEGORIES = ["best_time", "best_score"]
LEVELS = ["level1"]


def get_now():
    return str(datetime.now())


def _create_new_player_info(name, registration_date):
    return {"name": f"{name}",
            "registration_date": f"{registration_date}",
            "highscores": {"best_time": {"level1": 100000},
                           "best_score": {"level1": 10}},
            "statistics": {}}


def update_highscores(player_id, player_highscores):
    with open(_HIGHSCORES_DATA_FILE, "r") as highscores_data:
        highscores = json.load(highscores_data)
    for category in HIGHSCORES_CATEGORIES:
        for level in LEVELS:
            table = highscores[category][level]
            table.append([player_highscores[category][level], player_id])
            highscores[category][level].sort()
            if len(table) > 10:
                del table[-1]
            highscores[category][level] = table

    with open(_HIGHSCORES_DATA_FILE, "w") as highscores_data:
        json.dump(highscores, highscores_data)


def _update_and_download_to_json(file, by_keys, by_values, changing_key=None):
    with open(file, "r+") as data:
        base = json.load(data)
        for key, value in zip(by_keys, by_values):
            if changing_key is None:
                base[key] = value
            else:
                base[changing_key][key] = value

        data.seek(0)
        json.dump(base, data)
        data.truncate()


def update_statistics(player_id, player_statistics, player_highscores):
    _update_and_download_to_json(_PLAYER_DATA_FILE, ["highscores", "statistics"],
                                 [player_highscores, player_statistics], player_id)


def create_player(player_name, player_password):
    new_id = str(uuid.uuid4())
    _update_and_download_to_json(_BASE_DATA_FILE, [new_id], [player_name], "name_by_id")
    _update_and_download_to_json(_BASE_DATA_FILE, [player_name], [new_id], "id_by_name")

    _update_and_download_to_json(_SECURITY_DATA_FILE, [new_id],
                                 [{"name": player_name, "pass": player_password}])

    _update_and_download_to_json(_PLAYER_DATA_FILE, [new_id],
                                 [_create_new_player_info(player_name, get_now())])


def check_login(player_name, player_password):
    with open(_BASE_DATA_FILE, "r") as base_data:
        base = json.load(base_data)
    player_id = base["id_by_name"].get(player_name)
    if player_id is not None:
        with open(_SECURITY_DATA_FILE, "r") as secure_data:
            security = json.load(secure_data)
        if security[player_id]["pass"] == player_password:
            return player_id
    return None


def get_stats(player_id):
    with open(_PLAYER_DATA_FILE, "r") as players_data:
        players = json.load(players_data)
    player_stats = players.get(player_id)
    if player_stats is not None:
        return player_stats
    else:
        raise ValueError("There is no player with such id")


def get_highscores():
    with open(_HIGHSCORES_DATA_FILE, "r") as highscores_data:
        highscores = json.load(highscores_data)
    return highscores
