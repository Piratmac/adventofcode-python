# -------------------------------- Input data ---------------------------------------- #
import os, re

test_data = {}

test = 1
test_data[test] = {
    "input": """Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4""",
    "expected": ["5216", "Unknown"],
}


test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read().strip(),
    "expected": ["22676", "4510"],
}

# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"
part_to_test = 2
verbose = False

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #


def choose_target(opponents, unit, ignore_targets):
    targets = []
    for opponent in opponents:
        # Same team
        if opponent[-2] == unit[-2]:
            continue
        # target is already targetted
        if opponent[-2:] in ignore_targets:
            continue

        # Determine multipliers
        if unit[3] in opponent[5]:
            multiplier = 0
        elif unit[3] in opponent[6]:
            multiplier = 2
        else:
            multiplier = 1

        # Order: damage, effective power, initiative
        target = (
            unit[0] * unit[2] * multiplier,
            opponent[0] * opponent[2],
            opponent[4],
            opponent,
        )
        targets.append(target)

    targets.sort(reverse=True)

    if len(targets) > 0:
        return targets[0]


def determine_damage(attacker, defender):
    # Determine multipliers
    if attacker[3] in defender[5]:
        multiplier = 0
    elif attacker[3] in defender[6]:
        multiplier = 2
    else:
        multiplier = 1

    return attacker[0] * attacker[2] * multiplier


def attack_order(units):
    # Decreasing order of initiative
    units.sort(key=lambda unit: unit[4], reverse=True)
    return units


def target_selection_order(units):
    # Decreasing order of effective power then initiative
    units.sort(key=lambda unit: (unit[0] * unit[2], unit[4]), reverse=True)
    return units


def teams(units):
    teams = set([unit[-2] for unit in units])
    return teams


def team_size(units):
    teams = {
        team: len([unit for unit in units if unit[-2] == team])
        for team in ("Immune System:", "Infection:")
    }
    return teams


regex = "([0-9]*) units each with ([0-9]*) hit points (?:\((immune|weak) to ([a-z]*)(?:, ([a-z]*))*(?:; (immune|weak) to ([a-z]*)(?:, ([a-z]*))*)?\))? ?with an attack that does ([0-9]*) ([a-z]*) damage at initiative ([0-9]*)"
units = []
for string in puzzle_input.split("\n"):
    if string == "":
        continue

    if string == "Immune System:" or string == "Infection:":
        team = string
        continue

    matches = re.match(regex, string)
    if matches is None:
        print(string)
    items = matches.groups()

    # nb_units, hitpoints, damage, damage type, initative, immune, weak, team, number
    unit = [
        int(items[0]),
        int(items[1]),
        int(items[-3]),
        items[-2],
        int(items[-1]),
        [],
        [],
        team,
        team_size(units)[team] + 1,
    ]
    for item in items[2:-3]:
        if item is None:
            continue
        if item in ("immune", "weak"):
            attack_type = item
        else:
            if attack_type == "immune":
                unit[-4].append(item)
            else:
                unit[-3].append(item)

    units.append(unit)


boost = 0
min_boost = 0
max_boost = 10 ** 9
winner = "Infection:"
base_units = [unit.copy() for unit in units]
while True:
    if part_to_test == 2:
        # Update boost for part 2
        if winner == "Infection:" or winner == "None":
            min_boost = boost
            if max_boost == 10 ** 9:
                boost += 20
            else:
                boost = (min_boost + max_boost) // 2
        else:
            max_boost = boost
            boost = (min_boost + max_boost) // 2
        if min_boost == max_boost - 1:
            break

        units = [unit.copy() for unit in base_units]
        for uid in range(len(units)):
            if units[uid][-2] == "Immune System:":
                units[uid][2] += boost
        print("Applying boost", boost)

    while len(teams(units)) > 1:
        units_killed = 0
        if verbose:
            print()
            print("New Round")
            print([(x[-2:], x[0], "units") for x in units])
        order = target_selection_order(units)
        targets = {}
        for unit in order:
            target = choose_target(units, unit, [x[3][-2:] for x in targets.values()])
            if target:
                if target[0] != 0:
                    targets[unit[-2] + str(unit[-1])] = target

        order = attack_order(units)
        for unit in order:
            if unit[-2] + str(unit[-1]) not in targets:
                continue
            target = targets[unit[-2] + str(unit[-1])]
            position = units.index(target[3])
            damage = determine_damage(unit, target[3])
            kills = determine_damage(unit, target[3]) // target[3][1]
            units_killed += kills
            target[3][0] -= kills
            if target[3][0] > 0:
                units[position] = target[3]
            else:
                del units[position]

            if verbose:
                print(
                    unit[-2:],
                    "attacked",
                    target[3][-2:],
                    "dealt",
                    damage,
                    "damage and killed",
                    kills,
                )

        if units_killed == 0:
            break

    puzzle_actual_result = sum([x[0] for x in units])
    if part_to_test == 1:
        break
    else:
        if units_killed == 0:
            winner = "None"
        else:
            winner = units[0][-2]
        print("Boost", boost, " - Winner:", winner)
    if verbose:
        print([unit[0] for unit in units])


# -------------------------------- Outputs / results --------------------------------- #

print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
