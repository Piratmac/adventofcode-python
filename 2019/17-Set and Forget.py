# -------------------------------- Input data ---------------------------------------- #
import os, pathfinding, IntCode

from complex_utils import *

test_data = {}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read().strip(),
    "expected": ["5068", "1415975"],
}

# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"
part_to_test = 2
verbose_level = 0

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #

position = 0

droid = IntCode.IntCode(puzzle_input)
droid.run()
grid = []
for output in droid.outputs:
    if chr(output) == "#":
        grid.append(position)
    elif chr(output) in ["^", "v", ">", "<"]:
        droid_pos = [position, accent_to_dir[chr(output)]]

    if chr(output) == "\n":
        position = j * (position.imag - 1)
    else:
        position += 1


if part_to_test == 1:
    alignment_parameter = 0
    for x in range(1, int(max_real(grid))):
        for y in range(int(min_imag(grid)), -1):
            if x + y * j in grid:
                if all([x + y * j + dir in grid for dir in directions_straight]):
                    alignment_parameter += x * -y

    puzzle_actual_result = alignment_parameter


else:
    steps = []
    visited = []

    # Find the path, in the long form (L,12,R,8,.....)
    while True:
        position, direction = droid_pos
        visited.append(position)
        if position + direction in grid:
            steps[-1] += 1
            droid_pos[0] += droid_pos[1]
        else:
            option = [
                (turn[0].upper(), direction * relative_directions[turn])
                for turn in relative_directions
                if position + direction * relative_directions[turn] in grid
                if position + direction * relative_directions[turn] not in visited
            ]
            if len(option) > 1:
                print("error")
                raise Exception(position, direction, option)

            if option:
                option = option[0]
                steps += [option[0], 1]
                droid_pos[1] = option[1]
                droid_pos[0] += droid_pos[1]
            else:
                break

    steps = list(map(str, steps))
    steps_inline = ",".join(steps)

    # Shorten the path
    subprograms = []
    nb_to_letter = {0: "A", 1: "B", 2: "C"}

    offset = 0
    for i in range(3):
        while len(subprograms) == i:
            nb_steps = min(20, len(steps) - offset)
            subprogram = steps[offset : offset + nb_steps]
            subprogram_inline = ",".join(subprogram)

            # The limits of 3 is arbitrary
            while (
                steps_inline.count(subprogram_inline) < 3 or len(subprogram_inline) > 20
            ):
                # Shorten subprogram for test
                if len(subprogram) <= 2:
                    break
                else:
                    if subprogram[-1] in ("A", "B", "C"):
                        del subprogram[-1]
                    else:
                        del subprogram[-2:]

                subprogram_inline = ",".join(subprogram)

            # Found one!
            if steps_inline.count(subprogram_inline) >= 3 and len(subprogram) > 2:
                subprograms.append(subprogram_inline)
                steps_inline = steps_inline.replace(subprogram_inline, nb_to_letter[i])
                steps = steps_inline.split(",")
            else:
                if steps[offset] in ["A", "B", "C"]:
                    offset += 1
                else:
                    offset += 2
        offset = 0

    # Now send all that to the robot
    droid.instructions[0] = 2
    inputs = (
        steps_inline + "\n" + "\n".join(subprograms) + "\nn\n"
    )  # the last n is for the video
    for letter in inputs:
        droid.add_input(ord(letter))
    droid.restart()
    droid.run()

    puzzle_actual_result = droid.outputs.pop()
    if verbose_level:
        for output in droid.outputs:
            print(chr(output), end="")


# -------------------------------- Outputs / results --------------------------------- #

print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
