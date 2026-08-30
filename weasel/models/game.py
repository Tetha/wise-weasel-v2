
from pydantic import Field
from weasel.models import WeaselModel

class Act(WeaselModel):
    name: str
    index: int

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

