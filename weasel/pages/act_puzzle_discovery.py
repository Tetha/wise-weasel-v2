
from flask import Blueprint, render_template, request

from weasel.models.game import Game

def create_act_puzzle_discovery_blueprint(
        games: dict[str, Game]) -> Blueprint:
    bp = Blueprint("act_puzzle_discovery", __name__)

    
    @bp.route("/game/<game_id>/act/<act_id>/puzzles")
    def discover_puzzles(game_id, act_id):
        if game_id not in games:
            return "game not found", 404

        game = games[game_id]

        for act in game.acts:
            if act.index == int(act_id):
                break
        else:
            return "act not found", 404

        given_keywords_raw = request.args.get("given_keywords")
        if given_keywords_raw is None:
            given_keywords = []
            keywords = act.keywords
            single_remaining_puzzle = None
        else:
            given_keywords = given_keywords_raw.split(",")
            keywords = act.keywords_considering(given_keywords)

            remaining_puzzles = act.puzzles_considering(given_keywords)
            if len(remaining_puzzles) == 1:
                single_remaining_puzzle = remaining_puzzles[0]

        return render_template("act_puzzle_discovery/page.html",
                               game=game,
                               game_id=game_id,
                               act=act,
                               keywords=keywords,
                               given_keywords=given_keywords,
                               single_remaining_puzzle=single_remaining_puzzle)

    return bp