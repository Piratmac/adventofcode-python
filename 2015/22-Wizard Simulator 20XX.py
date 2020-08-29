# -------------------------------- Input data -------------------------------- #
import os, heapq

test_data = {}

test = "real"
test_data[test] = {
    "input": "",
    "expected": ["900", "1216"],
}

# -------------------------------- Control program execution -------------------------------- #

case_to_test = "real"
part_to_test = 2
verbose_level = 0

# -------------------------------- Initialize some variables -------------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution -------------------------------- #


spells = {
    # Cost, Duration, Damage, Heal, Armor, Mana
    "M": [53, 1, 4, 0, 0, 0],
    "D": [73, 1, 2, 2, 0, 0],
    "S": [113, 6, 0, 0, 7, 0],
    "P": [173, 6, 3, 0, 0, 0],
    "R": [229, 5, 0, 0, 0, 101],
}


# Order:
# Player mana, HP, Armor
# Boss HP and damage
# Counters for the 3 spells: Shield, Poison, Recharge
state = ["", 500, 50, 0, 51, 9, 0, 0, 0]
i_moves, i_mana, i_hp, i_armor, i_bhp, i_bdamage, i_cs, i_cp, i_cr = range(len(state))


def apply_effects(state):
    # Shield
    if state[i_cs] > 0:
        state[i_armor] = 7
        state[i_cs] -= 1
    else:
        state[i_armor] = 0
    # Poison
    if state[i_cp] > 0:
        state[i_bhp] -= 3
    # Recharge
    if state[i_cr] > 0:
        state[i_mana] += 101

    state[-2:] = [0 if x <= 1 else x - 1 for x in state[-2:]]


def player_turn(state, spell):
    if spell in "MD":
        state[i_mana] -= spells[spell][0]
        state[i_bhp] -= spells[spell][2]
        state[i_hp] += spells[spell][3]
    else:
        state[i_mana] -= spells[spell][0]
        state[-3 + "SPR".index(spell)] = spells[spell][1]


def boss_move(state):
    state[i_hp] -= max(state[i_bdamage] - state[i_armor], 1)


min_mana = 10 ** 6
frontier = [(0, state)]
heapq.heapify(frontier)

while frontier:
    mana_used, state = heapq.heappop(frontier)

    if mana_used > min_mana:
        continue

    if part_to_test == 2:
        state[i_hp] -= 1
        if state[i_hp] <= 0:
            continue

    # Apply effects before player turn
    apply_effects(state)
    if state[i_bhp] <= 0:
        min_mana = min(min_mana, mana_used)
        continue

    for spell in spells:
        # Exclude if mana < 0
        if spells[spell][0] > state[i_mana]:
            continue
        # Exclude if mana > max mana found
        if mana_used + spells[spell][0] > min_mana:
            continue
        # Exclude if spell already active
        if spell in "SPR":
            if state[-3 + "SPR".index(spell)] != 0:
                continue

        neighbor = state.copy()
        neighbor[0] += spell

        # Player moves
        player_turn(neighbor, spell)
        if neighbor[i_bhp] <= 0:
            min_mana = min(min_mana, mana_used + spells[spell][0])
            continue

        # Apply effects
        apply_effects(neighbor)
        if neighbor[i_bhp] <= 0:
            min_mana = min(min_mana, mana_used + spells[spell][0])
            continue

        # Boss moves
        boss_move(neighbor)
        if neighbor[i_hp] <= 0:
            continue

        # Adding for future examination
        heapq.heappush(frontier, (mana_used + spells[spell][0], neighbor))

puzzle_actual_result = min_mana


# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
    print("Input : " + puzzle_input)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
