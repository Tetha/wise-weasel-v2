import json
from pathlib import Path

from flask import Flask, g

from weasel.models.game import Game
from weasel.pages.game_list import create_blueprint as create_game_list_blueprint
from weasel.pages.act_list import create_act_list_blueprint
def load_walkthroughs() -> dict[str, Game]:
    source_folder = Path("walkthroughs")

    games = {}
    for file in source_folder.glob("*.json"):
        with file.open("r", encoding="UTF-8") as f:
            game_data_raw = json.load(f)
            game_data = Game.model_validate(game_data_raw)
            games[file.name.replace(".json", "")] = game_data
    
    return games


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    games = load_walkthroughs()

    @app.route("/")
    def index():
        return "Hello World"

    app.register_blueprint(create_act_list_blueprint(games))
    app.register_blueprint(create_game_list_blueprint(games))

    return app