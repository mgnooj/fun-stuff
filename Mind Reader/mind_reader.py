"An implementation of Shannon's prediction machine for playing Heads or Tails."
##  Basically, the machine looks for certain types of patterns in the behavior of its human
##  opponent. If it can find these patterns it remembers them and assumes that the player
##  will follow the patterns the next time the same situation arises. The machine also
##  contains a random element. Until patterns have been found, or if an assumed pattern
##  is not repeated at least twice by the player, the machine chooses its move at random.
##  The types of patters remembered involve the outcome of two successive plays (that is,
##  whether or not the player won on those players) and whether he changed his choice
##  between them and after them. There are eight possible situations, and for each of these,
##  two things the player can do.
##      Claude Shannon, "A Mind-Reading (?) Machine", 1953

import random

HEADS, TAILS = True, False
WIN, LOSE = True, False
REPEAT, DIFFERENT = True, False

class Mindreader:
    "Stores previous user input and game outcomes, detects patterns, and produces decisions."
    ## GAME STATE reflecting prior two rounds to store recent user behavior and game outcomes
    def __init__(self):
        self.previous_round = None
        self.previous_action = None
        self.last_round = None
        self.last_action = None

    ## MEMORY CELLS to 'remember' previous behavior under specific conditions
        self.memory = {
            (WIN, REPEAT, WIN):         {"last_instance": None, "previous": None},
            (WIN, REPEAT, LOSE):        {"last_instance": None, "previous": None},
            (WIN, DIFFERENT, WIN):      {"last_instance": None, "previous": None},
            (WIN, DIFFERENT, LOSE):     {"last_instance": None, "previous": None},
            (LOSE, REPEAT, WIN):        {"last_instance": None, "previous": None},
            (LOSE, REPEAT, LOSE):       {"last_instance": None, "previous": None},
            (LOSE, DIFFERENT, WIN):     {"last_instance": None, "previous": None},
            (LOSE, DIFFERENT, LOSE):    {"last_instance": None, "previous": None}
        }

    def decide(self):
        "Decide heads or tails based on prior user actions; or random output if no data available."
        try:
            behavior = self.previous_action == self.last_action                           ## True = SAME, False = DIFFERENT
            memory_cell = self.memory[(self.previous_round, behavior, self.last_round)]   ## Find relevant memory cell
            pattern_detected = memory_cell["last_instance"] == memory_cell["previous"]    ## If pattern is detected,
            follow_pattern = memory_cell["last_instance"] == self.last_action             ## follow pattern
            return follow_pattern if pattern_detected else random.choice([HEADS, TAILS])  ## else random
        except (ValueError, IndexError) as _:                                             ## If no state, play random
            return random.choice([HEADS, TAILS])

    def update(self, player_action, result):
        "Update machine state to reflect outcome of most recent round."
        if self.previous_round and self.last_round:
            behavior = self.previous_action == self.last_action                           ## True = SAME, False = DIFFERENT
            memory_cell = self.memory[(self.previous_round, behavior, self.last_round)]   ## Find relevant memory cell
            memory_cell["previous"] = memory_cell["last_instance"]
            memory_cell["last_instance"] = player_action == self.last_action
        self.previous_round, self.previous_action = self.last_round, self.last_action
        self.last_round, self.last_action = result, player_action

if __name__ == "__main__":
    shannon = Mindreader()
    play = True

    while play:
        ## MAKE DECISION
        decision = shannon.decide()

        ## PLAY ROUND
        current_action = input("Heads or tails?\n")[0].lower() == "h"
        outcome = current_action != decision
        print("Win\n" if outcome else "Lose\n")

        # UPDATE STATE
        shannon.update(current_action, outcome)
        play = input("Play again? (y/n)\n")[0].lower() == "y"
