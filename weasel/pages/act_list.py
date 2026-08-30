
from flask import Blueprint, render_template, request

from weasel.models.game import Game

def create_act_list_blueprint(games: dict[str, Game]):
    bp = Blueprint("act_list", __name__)

    @bp.route("/game/<game_id>/acts")
    def list_acts(game_id: str):
        if game_id not in games:
            return "game not found", 404

        game = games[game_id]

        if 'reached_act' in request.args:
            act_id = int(request.args['reached_act'])
            known_acts = game.acts_until_just_after(act_id)
        else:
            known_acts = [game.first_act]

        if 'HX-Request' in request.headers and 'HX-Target' in request.headers:
            raw_hx_target = request.headers.get('HX-Target')
            if '#' in raw_hx_target:
                hx_target = raw_hx_target.split("#")[-1]
            else:
                hx_target = raw_hx_target

            match hx_target:
                case 'act-list':
                    return render_template(
                        "act_list/act_list.html",
                        game_id=game_id,
                        game=game,
                        known_acts=known_acts
                    )
                case _:
                    return (f"unknown target {hx_target}", 400)

        return render_template(
            "act_list/page.html",
            game_id=game_id,
            game=game,
            known_acts=known_acts
        )

    return bp