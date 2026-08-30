
from flask import Blueprint, render_template

def create_blueprint(games) -> Blueprint:
    bp = Blueprint("games_list", __name__, url_prefix="/")

    @bp.route("/games")
    def list_games():
        return render_template("game_list/page.html", games=games)

    return bp