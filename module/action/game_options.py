import pygame
from module.constant import DISPLAY, STATS_PATH, LOGIN_URL, SAVE_STATS_URL
import random
import json
from requests import post as post_request
from requests.exceptions import ConnectionError as connectionError


SURFACE = None
LEVEL = None


def init_game():
    global SURFACE
    pygame.init()
    random.seed()
    SURFACE = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption("TypeTrainer: kill by words")
    pygame.display.update()


def surface():
    global SURFACE
    return SURFACE


def set_level(level):
    global LEVEL
    LEVEL = level


def get_level():
    global LEVEL
    return LEVEL


def send_stats():
    with open(STATS_PATH, "r") as stats_file:
        player_info = json.load(stats_file)
    request_to_send = player_info
    answer = post_request(SAVE_STATS_URL, json=request_to_send).json()


def save_stats(stats):
    with open(STATS_PATH, "w") as stats_file:
        json.dump(stats, stats_file)


def send_login_request(name, password):
    request_to_send = {"name": name,
                       "pass": password }
    try:
        result = post_request(LOGIN_URL, json=request_to_send).json()
        save_stats({**result["stats"], "id": result["id"]})
        result = result["status"]
    except connectionError as e:
        return False
    else:
        return result
