# -------------------------------- Input data ---------------------------------------- #
import os, pathfinding, re

from complex_utils import *
from math import ceil

test_data = {}

test = 1
test_data[test] = {
    "input": """10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL
6 HTRFP, 1 FVXV, 4 JKLNF, 1 TXFCS, 2 PXBP => 4 JRBFT""",
    "expected": ["31", "Unknown"],
}

test += 1
test_data[test] = {
    "input": """157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT""",
    "expected": ["13312", "82892753"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read().strip(),
    "expected": ["1037742", "1572358"],
}

# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"
part_to_test = 2

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #


def execute_reaction(stock, reaction, required):
    global ore_required
    target = reaction[1]
    nb_reactions = ceil((required[target] - stock.get(target, 0)) / reaction[0])

    # Impact on target material
    stock[target] = stock.get(target, 0) + nb_reactions * reaction[0] - required[target]
    del required[target]

    # Impact on other materials
    for i in range(len(reaction[2]) // 2):
        nb_required, mat = reaction[2][i * 2 : i * 2 + 2]
        nb_required = int(nb_required) * nb_reactions
        if mat == "ORE" and part_to_test == 1:
            ore_required += nb_required
        elif stock.get(mat, 0) >= nb_required:
            stock[mat] -= nb_required
        else:
            missing = nb_required - stock.get(mat, 0)
            stock[mat] = 0
            required[mat] = required.get(mat, 0) + missing


reactions = {}
for string in puzzle_input.split("\n"):
    if string == "":
        continue

    source, target = string.split(" => ")
    nb, target = target.split(" ")
    nb = int(nb)

    sources = source.replace(",", "").split(" ")

    reactions[target] = (nb, target, sources)


if part_to_test == 1:
    required = {"FUEL": 1}
    ore_required = 0
    stock = {}
    while len(required) > 0:
        material = list(required.keys())[0]
        execute_reaction(stock, reactions[material], required)

    puzzle_actual_result = ore_required


else:
    below, above = 1000000000000 // 1037742, 1000000000000

    while below != above - 1:
        required = {"FUEL": (below + above) // 2}
        stock = {"ORE": 1000000000000}
        while len(required) > 0 and "ORE" not in required:
            material = list(required.keys())[0]
            execute_reaction(stock, reactions[material], required)

        if stock["ORE"] == 0 or "ORE" in required:
            above = (below + above) // 2
        else:
            below = (below + above) // 2

    puzzle_actual_result = below


# -------------------------------- Outputs / results --------------------------------- #

print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
