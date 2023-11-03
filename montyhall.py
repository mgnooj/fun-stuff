## montyhall.py ::  A Python simulation of the Monty Hall Problem.

from numpy.random import randint, choice

def monty_hall(switch: bool) -> bool:
    goat_door: int = randint(1, 4)
    chosen_door: int = randint(1, 4)
    open_door: int = choice([door for door in range(1, 4) if door not in (goat_door, chosen_door)])
    if switch:
        chosen_door = choice([door for door in range(1, 4) if door not in (open_door, chosen_door)])
    return chosen_door == goat_door     ## True if player wins, False if Monty wins

if __name__ == "__main__":
    switch_results: [bool] = [monty_hall(switch=True) for _ in range(10000)]
    no_switch_results: [bool] = [monty_hall(switch=False) for _ in range(10000)]
    print(f"Player switches: {len([x for x in switch_results if x]) / 100}% win percentage")
    print(f"Player does not switch: {len([x for x in no_switch_results if x]) / 100}% win percentage")
