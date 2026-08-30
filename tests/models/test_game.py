import pytest

from weasel.models.game import Game, Act

@pytest.fixture
def sample_game() -> Game:
    return Game(
        name="Our sample Adventure",
        acts=[
            Act(name="Introduction", index=0),
            Act(name="Build Up", index=1),
            Act(name="Climax", index=2)
        ]
    )


def test_first_act(sample_game):
    assert sample_game.first_act == Act(name="Introduction", index=0)

def test_acts_until_just_after(sample_game):
    assert sample_game.acts_until_just_after(0) == [
        Act(name="Introduction", index=0),
        Act(name="Build Up", index=1)
    ]