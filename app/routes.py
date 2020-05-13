from app import app
from requests import request
from flask import Flask, render_template, request, url_for, redirect, jsonify
from modules.data_handling import *
import json


@app.route('/request/client_endpoint/save_stats', methods=['POST'])
def save_stats_endpoint():
    player_stats = request.get_json(force=True)
    with open("resources/players.json", "r") as players_data:
        players = json.load(players_data)
        if players.get(player_stats["id"], None) is None:
            answer = {"status": "Player do not exist"}
            return jsonify(answer)
    update_highscores(player_stats["id"], player_stats["highscores"])
    update_statistics(player_stats["id"], player_stats["statistics"], player_stats["highscores"])
    answer = {"status": "complete"}
    return jsonify(answer)


@app.route('/request/client_endpoint/register', methods=['POST'])
def register_endpoint():
    register_info = request.get_json(force=True)
    with open("resources/base.json", "r") as base_data:
        base = json.load(base_data)
        if base["id_by_name"].get(register_info["name"], None) is not None:
            answer = {"status": "already_exist"}
        else:
            create_player(register_info["name"], register_info["pass"])
            answer = {"status": "success"}
    return jsonify(answer)


@app.route('/request/client_endpoint/login', methods=['POST'])
def login_endpoint():
    login_info = request.get_json(force=True)
    player_id = check_login(login_info["name"], login_info["pass"])
    if player_id is None:
        answer = {"status": "incorrect"}
    else:
        answer = {"status": "success", "stats": get_stats(player_id)}
    return jsonify(answer)


@app.route('/homepage')
def homepage():
    # здесь у нас главная страница проекта
    user = {'username': 'Sergey'}
    return render_template('homepage.html', title='Home', user=user)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/')
def redirection():
    # здесь у нас главная страница проекта
    return redirect(url_for("homepage"))


@app.route('/statistics')
def statistics():
    # здесь у нас статистика по игрокам
    print(get_highscores()["best_time"])
    return render_template('highscores.html',
                           title='Highscores',
                           categories=HIGHSCORES_CATEGORIES,
                           levels=LEVELS,
                           highscores=get_highscores())
