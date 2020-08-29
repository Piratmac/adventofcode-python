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
    "expected": ["462", "23981"],
}

# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"
part_to_test = 2
verbose_level = 1

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #

tiles = {0: " ", 1: "#", 2: "ø", 3: "_", 4: "o"}
grid = pathfinding.Graph()
computer = IntCode.IntCode(puzzle_input)

if part_to_test == 1:
    computer.run()
    grid.vertices = {}
    for i in range(len(computer.outputs) // 3):
        position = SuperComplex(
            computer.outputs[i * 3] - j * computer.outputs[i * 3 + 1]
        )
        grid.vertices[position] = tiles[computer.outputs[i * 3 + 2]]

    puzzle_actual_result = sum([1 for val in grid.vertices.values() if val == "ø"])


else:
    computer.instructions[0] = 2
    blocks_left = 1
    score = 0

    vertices = {}

    while blocks_left > 0 and computer.state != "Failure":
        computer.run()

        # Check if we can still play
        blocks_left = 0
        ball_position = 0
        paddle_position = 0
        for i in range(len(computer.outputs) // 3):

            vertices[
                computer.outputs[i * 3] - j * computer.outputs[i * 3 + 1]
            ] = computer.outputs[i * 3 + 2]
            # The ball has not fallen
            if computer.outputs[i * 3 + 2] == 4:
                ball_position = (
                    computer.outputs[i * 3] - j * computer.outputs[i * 3 + 1]
                )
                if ball_position.imag < -21:
                    print("Failed")
                    computer.state = "Failure"
                    break
            # Check the score
            elif computer.outputs[i * 3] == -1 and computer.outputs[i * 3 + 1] == 0:
                score = computer.outputs[i * 3 + 2]

            # Store the paddle position
            elif computer.outputs[i * 3 + 2] == 3:
                paddle_position = (
                    computer.outputs[i * 3] - j * computer.outputs[i * 3 + 1]
                )

        # There are still blocks to break
        blocks_left = len([x for x in vertices if vertices[x] == 2])

        # Move paddle
        if paddle_position.real < ball_position.real:
            joystick = 1
        elif paddle_position.real > ball_position.real:
            joystick = -1
        else:
            joystick = 0
        computer.add_input(joystick)

        if verbose_level >= 2:
            print(
                "Movements",
                len(computer.all_inputs),
                " - Score",
                score,
                " - Blocks left",
                blocks_left,
                " - Ball",
                ball_position,
                " - Paddle",
                paddle_position,
                " - Direction",
                joystick,
            )

        # 'Restart' the computer to process the input
        computer.restart()

    # Outputs the grid (just for fun)
    grid.vertices = {x: tiles.get(vertices[x], vertices[x]) for x in vertices}
    print(grid.vertices_to_grid())

    puzzle_actual_result = score


# -------------------------------- Outputs / results --------------------------------- #

print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
