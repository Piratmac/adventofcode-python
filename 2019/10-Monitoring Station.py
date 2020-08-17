# -------------------------------- Input data ---------------------------------------- #
import os, pathfinding

from complex_utils import *
from math import pi

test_data = {}

test = 1
test_data[test] = {
    "input": """.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##""",
    "expected": ["210", "802"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read().strip(),
    "expected": ["256", "1707"],
}

# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"
part_to_test = 2

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #

grid = pathfinding.Graph()
grid.grid_to_vertices(puzzle_input, wall=".")

visible_count = []
for asteroid in grid.vertices:
    visible = set()
    for other in grid.vertices:
        if other == asteroid:
            continue
        visible.add(SuperComplex(other - asteroid).phase())
    visible_count.append((len(visible), SuperComplex(asteroid)))

if part_to_test == 1:
    puzzle_actual_result = max(visible_count)[0]


else:
    station = max(visible_count)[1]
    targets = {}

    for target in grid.vertices:
        if target == station:
            continue
        vector = SuperComplex(target - station)
        order = (
            pi / 2 - vector.phase()
            if vector.phase() <= pi / 2
            else 10 * pi / 4 - vector.phase()
        )
        try:
            targets[order].append((vector.amplitude(), target))
        except:
            targets[order] = [(vector.amplitude(), target)]

    phases = list(targets.keys())
    phases.sort()
    destroyed = 0
    while destroyed < 200:
        for phase in phases:
            if phase in targets and len(targets[phase]) > 0:
                targets[phase].sort(key=lambda a: a[0])
                target = targets[phase][0][1]
                del targets[phase][0]
                destroyed += 1
                if destroyed == 200:
                    break

    puzzle_actual_result = int(target.real * 100 - target.imag)


# -------------------------------- Outputs / results --------------------------------- #

print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
