# -------------------------------- Input data ---------------------------------------- #
import os, pathfinding, IntCode

from complex_utils import *

test_data = {}

test = 1
test_data[test] = {
    "input": """""",
    "expected": ["Unknown", "Unknown"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read().strip(),
    "expected": ["1934", "RKURGKGK"],
}

# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"
part_to_test = 2

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #

position = 0
direction = north
if part_to_test == 1:
    panels = {0: 0}
else:
    panels = {0: 1}


computer = IntCode.IntCode(puzzle_input)

while computer.state != "Stopped":
    if position in panels:
        computer.add_input(panels[position])
    else:
        computer.add_input(0)
    computer.restart()
    computer.run()
    color, dir = computer.outputs[-2:]
    panels[position] = color
    direction *= (
        relative_directions["left"] if dir == 0 else relative_directions["right"]
    )
    position += direction

if part_to_test == 1:
    puzzle_actual_result = len(panels)
else:
    grid = pathfinding.Graph()
    grid.vertices = {x: "X" if panels[x] == 1 else " " for x in panels}
    puzzle_actual_result = "\n" + grid.vertices_to_grid(wall=" ")


# -------------------------------- Outputs / results --------------------------------- #

print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
