# -------------------------------- Input data ---------------------------------------- #
import os, pathfinding

from complex_utils import *

test_data = {}

test = 1
test_data[test] = {
    "input": """R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83""",
    "expected": ["159", "610"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read().strip(),
    "expected": ["308", "12934"],
}

# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"
part_to_test = 2

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #

wires = []
for i in range(len(puzzle_input.split("\n"))):
    wire = puzzle_input.split("\n")[i]
    position = 0
    wires.append(list())
    for line in wire.split(","):
        direction = {"U": north, "D": south, "L": west, "R": east}[line[0]]
        for step in range(int(line[1:])):
            position += direction
            wires[i].append(position)

common = list(set(wires[0]).intersection(set(wires[1])))


if part_to_test == 1:
    common = complex_sort(common, "manhattan")
    puzzle_actual_result = int(manhattan_distance(0, common[0]))


else:
    min_distance = 10 ** 20
    for spot in common:
        distance = (
            wires[0].index(spot) + wires[1].index(spot) + 2
        )  # 2 because start is not included
        min_distance = min(min_distance, distance)

    puzzle_actual_result = min_distance


# -------------------------------- Outputs / results --------------------------------- #

print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
