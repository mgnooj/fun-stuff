"An implementation of Hagelbarger's prediction machine for playing Heads or Tails. "
## At the beginning of any play, the computer is connected to the appropriate memory register
## by the state of play relays. The memory stores two kinds of information: Should the machine
## play same or different in this state to win? Has the machine been winning in this state?
## The former is controlled by a reversible counter which...will contain the number of times
## the machine should have played the same in that state minus the number times it should have
## played different. The exact logic of the latter part of the memory....roughly corresponds
## to remembering whether the machine has won both, one, or neither of the last two places in
## that state.
##      D.W. Hagelbarger, "SEER, A Sequence Extrapolating Robot", 1955

import random

WIN, LOSE = True, False
SAME, DIFFERENT = True, False

class Seer:
    "Stores previous user input and game outcomes, detects patterns, and produces decisions."
    ## GAME STATE to record recent user behavior and game outcomes
    def __init__(self):
        self.previous_round = None
        self.previous_action = None
        self.last_round = None
        self.last_action = None

    ## MEMORY CELLS to 'remember' previous outcomes under specific conditions
        self.memory = {
            (WIN, SAME, WIN):           {"counter": 0, "previous": None, "last": None},
            (WIN, SAME, LOSE):          {"counter": 0, "previous": None, "last": None},
            (WIN, DIFFERENT, WIN):      {"counter": 0, "previous": None, "last": None},
            (WIN, DIFFERENT, LOSE):     {"counter": 0, "previous": None, "last": None},
            (LOSE, SAME, WIN):          {"counter": 0, "previous": None, "last": None},
            (LOSE, SAME, LOSE):         {"counter": 0, "previous": None, "last": None},
            (LOSE, DIFFERENT, WIN):     {"counter": 0, "previous": None, "last": None},
            (LOSE, DIFFERENT, LOSE):    {"counter": 0, "previous": None, "last": None}
        }

    def access_memory(self):
        behavior = self.previous_action == self.last_action
        return self.memory[(self.previous_round, behavior, self.last_round)]

    def decide(self):
        "Decide heads or tails based on prior user actions; or random output if no data available."
        if self.previous_round and self.last_round:
            memory_cell = self.access_memory()
            if memory_cell["previous"] and memory_cell["last"]:                 # If both wins, decision = counter > 0
                return memory_cell["counter"] > 0
            if True in (memory_cell["previous"], memory_cell["last"]):          # If one win, 3:1 odds of decision = counter > 0
                odds = random.randint(1, 100)
                return memory_cell["counter"] > 0 if odds < 75 else memory_cell["counter"] < 0
        return random.choice([True, False])                                     # If no data, or two losses, or counter is at zero, play random

    def update(self, action, result):
        "Update machine state to reflect outcome of most recent round."
        if self.previous_round and self.last_round:
            memory_cell = self.access_memory()
            memory_cell["previous"], memory_cell["last"] = memory_cell["last"], result
            if result and memory_cell["counter"] < 3:
                memory_cell["counter"] += 1
            elif not result and memory_cell["counter"] > -3:
                memory_cell["counter"] -= 1
        self.previous_round, self.previous_action = self.last_round, self.last_action
        self.last_round, self.last_action = result, action

if __name__ == "__main__":
    seer = Seer()
    play = True

    while play:
        ## MAKE DECISION
        decision = seer.decide()

        ## GAME
        current_action = input("Heads or tails?\n")[0].lower() == "h"
        outcome = current_action != decision
        print("Win\n" if outcome else "Lose\n")

        ## UPDATE MEMORY CELL AND GAME STATE
        seer.update(current_action, outcome)
        play = input("Play again? (y/n)\n")[0].lower() == "y"
