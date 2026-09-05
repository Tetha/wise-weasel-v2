import pytest

import sys
print(sys.path)

from weasel.models.game import Game, Act, Puzzle

@pytest.fixture
def sample_game() -> Game:
    return Game(
        name="Our sample Adventure",
        acts=[
            Act(
                name="Introduction",
                index=0,
                puzzles={
                    "coffemaker": Puzzle(name="The broken coffemaker",
                           keywords=["kitchen", "coffee", "tired"]),
                    "cat": Puzzle(name="The crazy cat",
                           keywords=["cat", "angry", "front door"])
                }),
            Act(name="Build Up", index=1),
            Act(name="Climax", index=2)
        ]
    )


def test_first_act(sample_game):
    assert sample_game.first_act.name == "Introduction"

def test_acts_until_just_after(sample_game):
    acts = sample_game.acts_until_just_after(0)
    act_names = [act.name for act in acts]
    assert act_names == ["Introduction", "Build Up"]

def test_act_keywords(sample_game):
    first_act = sample_game.first_act
    assert first_act.keywords == set([
        "kitchen", "coffee", "tired",
        "cat", "angry", "front door"
    ])

def test_act_keywords_including(sample_game):
    first_act = sample_game.first_act
    assert first_act.keywords_considering(["coffee"]) == set([
        "kitchen", "coffee", "tired"
    ])