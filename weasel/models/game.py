
from pydantic import Field
from weasel.models import WeaselModel

class Puzzle(WeaselModel):
    """The display name of the puzzle.
    
    This will be used e.g. as headers for the puzzle page, or as
    an identifier on the puzzle discovery page. This shuold make
    a player recognize that this is the puzzle they are stuck on."""
    name: str

    keywords: set[str] = Field(default_factory=set)

    def has_some_keyword_of(self, given_keywords: set[str]) -> bool:
        return not self.keywords.isdisjoint(given_keywords)

class Act(WeaselModel):
    name: str
    index: int
    
    """The puzzles in this act.
    
    The index will be used in URLs and will be handled as an identifier
    for the puzzle, so it should be short, not contain special characters
    and ideally be a kebab-case string ("locked-study-door").
    
    Spoilers are acceptable in this string, as the player will only
    see it once they have discovered this puzzle for a solution"""
    puzzles: dict[str, Puzzle] = Field(default_factory=dict)

    @property
    def keywords(self) -> set[str]:
        words = set()
        for puzzle in self.puzzles.values():
            for word in puzzle.keywords:
                words.add(word)
        return words

    def puzzles_considering(self, given_keywords=list[str]) -> list[Puzzle]:
        return [
            puzzle 
            for puzzle in self.puzzles.values()
            if puzzle.has_some_keyword_of(given_keywords)
        ]

    def keywords_considering(self, given_keywords=list[str]) -> set[str]:
        words = set()
        for puzzle in self.puzzles_considering(given_keywords):
            words = words.union(puzzle.keywords)
        return words

class Game(WeaselModel):
    name: str
    acts: list[Act] = Field(default_factory=list)

    @property
    def first_act(self):
        if len(self.acts) == 0:
            raise ValueError("Game has no acts defined")
        return self.acts[0]

    def acts_until_just_after(self, last_seen_act_index):
        for idx, act in enumerate(self.acts):
            if act.index == last_seen_act_index:
                return self.acts[:idx+2]

        raise ValueError(f"No act with id {last_seen_act_index} known")

