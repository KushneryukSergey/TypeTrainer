import json
import os
from app import app
from requests import request
from flask import Flask, render_template, request, url_for, redirect, jsonify, send_from_directory
from modules.data_handling import check_login, create_player, update_highscores, update_statistics,\
    get_highscores, get_stats, HIGHSCORES_CATEGORIES, LEVELS


@app.route('/request/client_endpoint/save_stats', methods=['POST'])
def save_stats_endpoint():
    player_stats = request.get_json(force=True)
    with open("resources/players.json", "r") as players_data:
        players = json.load(players_data)
        if players.get(player_stats["id"]) is None:
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
        if base["id_by_name"].get(register_info["name"]) is not None:
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
        print(login_info)
    else:
        answer = {"status": "success", "stats": get_stats(player_id)}
    return jsonify(answer)


@app.route('/homepage')
def homepage():
    return render_template('homepage.html', title='Home')


# пока что фавикон нормально не появлятся ((
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/')
def redirection():
    # здесь у нас главная страница проекта
    return redirect(url_for("homepage"))


@app.route('/player_statistics')
def player_statistics():
    print(get_highscores()["best_time"])
    return render_template('highscores.html',
                           title='Highscores',
                           categories=HIGHSCORES_CATEGORIES,
                           levels=LEVELS,
                           highscores=get_highscores())
