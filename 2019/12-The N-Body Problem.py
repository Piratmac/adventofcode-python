# -------------------------------- Input data ---------------------------------------- #
import os, pathfinding, re, math, copy

from complex_utils import *

test_data = {}

test = 1
test_data[test] = {
    "input": """<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>""",
    "expected": ["179 after 10 steps", "2772"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read().strip(),
    "expected": ["12773", "306798770391636"],
}

# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"
part_to_test = 2

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #

stars = []
for string in puzzle_input.split("\n"):
    x, y, z = map(int, re.findall("[-0-9]{1,}", string))
    stars.append([x, y, z, 0, 0, 0])

if part_to_test == 1:
    for step in range(1000):
        for star_id in range(len(stars)):
            for coord in range(3):
                stars[star_id][3 + coord] += sum(
                    [1 for other in stars if stars[star_id][coord] < other[coord]]
                )
                stars[star_id][3 + coord] += sum(
                    [-1 for other in stars if stars[star_id][coord] > other[coord]]
                )

        for star_id in range(len(stars)):
            for coord in range(3):
                stars[star_id][coord] += stars[star_id][3 + coord]

    energy = sum(
        [
            (abs(x) + abs(y) + abs(z)) * (abs(dx) + abs(dy) + abs(dz))
            for (x, y, z, dx, dy, dz) in stars
        ]
    )
    puzzle_actual_result = energy

else:

    # 1st trick: For this part, do the computation on each axis independently (since they're independent)
    # 2nd trick: the function state => next state is invertible, so any repetition will go through the initial state (we can't have 3>0>1>0>1>0>1, it has to be something like 3>0>1>3>0>1)
    repeats = []
    for coord in range(3):
        step = -1
        repeat = 0
        stars_pos_vel = [
            [stars[star_id][coord], stars[star_id][coord + 3]]
            for star_id in range(len(stars))
        ]
        init_stars_pos_vel = [
            [stars[star_id][coord], stars[star_id][coord + 3]]
            for star_id in range(len(stars))
        ]

        while repeat == 0:  # and step < 20:
            step += 1
            for star_id in range(len(stars)):
                stars_pos_vel[star_id][1] += sum(
                    [
                        1
                        for other in stars_pos_vel
                        if stars_pos_vel[star_id][0] < other[0]
                    ]
                )
                stars_pos_vel[star_id][1] -= sum(
                    [
                        1
                        for other in stars_pos_vel
                        if stars_pos_vel[star_id][0] > other[0]
                    ]
                )

            for star_id in range(len(stars)):
                stars_pos_vel[star_id][0] += stars_pos_vel[star_id][1]

            if stars_pos_vel == init_stars_pos_vel:
                repeat = step + 1

        repeats.append(repeat)

    lcm = repeats[0]
    for val in repeats:
        lcm = lcm * val // math.gcd(lcm, val)

    puzzle_actual_result = lcm

# -------------------------------- Outputs / results --------------------------------- #

print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
