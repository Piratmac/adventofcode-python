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
    score = 0

    while computer.state != "Stopped":
        computer.run()

        ball_x = 0
        paddle_x = 0
        for i in range(len(computer.outputs) // 3):
            # Ball position
            if computer.outputs[i * 3 + 2] == 4:
                ball_x = computer.outputs[i * 3]
            # Paddle position
            elif computer.outputs[i * 3 + 2] == 3:
                paddle_x = computer.outputs[i * 3]

            # Check the score
            elif computer.outputs[i * 3] == -1 and computer.outputs[i * 3 + 1] == 0:
                score = computer.outputs[i * 3 + 2]
        computer.outputs = []

        if computer.state == "Stopped":
            break

        # Move paddle
        if paddle_x < ball_x:
            joystick = 1
        elif paddle_x > ball_x:
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

    puzzle_actual_result = score


# -------------------------------- Outputs / results --------------------------------- #

print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
