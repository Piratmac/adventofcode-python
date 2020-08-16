# -------------------------------- Input data ---------------------------------------- #
import os, pathfinding

from complex_utils import *
from tree import Tree

test_data = {}

test = 1
test_data[test] = {
    "input": """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN""",
    "expected": ["42 (without SAN and YOU), 54 (with)", "4"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read().strip(),
    "expected": ["151345", "391"],
}

# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"
part_to_test = 2

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #

all_nodes = {"COM": Tree("COM")}
for string in puzzle_input.split("\n"):
    orbitee, orbiter = string.split(")")
    if orbitee not in all_nodes:
        all_nodes[orbitee] = Tree(orbitee)
    if orbiter not in all_nodes:
        all_nodes[orbiter] = Tree(orbiter)

    all_nodes[orbitee].add_child(all_nodes[orbiter])
    all_nodes[orbiter].parent = all_nodes[orbitee]

if part_to_test == 1:
    nb_orbits = 0
    for node in all_nodes.values():
        nb_orbits += node.count_descendants()

    puzzle_actual_result = nb_orbits


else:
    puzzle_actual_result = (
        all_nodes["SAN"].get_degree_of_separation(all_nodes["YOU"]) - 2
    )


# -------------------------------- Outputs / results --------------------------------- #

print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
