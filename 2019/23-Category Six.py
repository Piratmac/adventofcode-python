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
    "input": open(input_file, "r+").read(),
    "expected": ["23266", "17493"],
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

computers = [0] * 50
queue = []
nat_queue = []
nat_y_values_sent = []
for i in range(len(computers)):
    computers[i] = IntCode.IntCode(puzzle_input, i)
    computers[i].add_input(i)
    computers[i].reception_duration = 0


total_outputs = 0
while puzzle_actual_result == "Unknown":
    for computer in computers:
        computer.run(1)

        if computer.outputs:
            computer.reception_duration = 0

        if len(computer.outputs) == 3:
            total_outputs += len(computer.outputs)
            queue += [computer.outputs]
            computer.outputs = []

    if verbose_level >= 1 and queue:
        print("Queue contains", queue)
        print("# outputs from computers", total_outputs)

    while queue:
        packet = queue.pop(0)
        if packet[0] == 255 and part_to_test == 1:
            puzzle_actual_result = packet[2]
            break
        elif packet[0] == 255:
            nat_queue = packet[1:]
        else:
            computers[packet[0]].add_input(packet[1:])
            computers[packet[0]].restart()

    for computer in computers:
        if computer.state == "Paused":
            computer.reception_duration += 1

    senders = [
        computer.reference for computer in computers if computer.reception_duration < 5
    ]
    inputs = [computer.reference for computer in computers if len(computer.inputs) != 0]

    if (
        all(
            [
                computer.reception_duration > 5 and len(computer.inputs) == 0
                for computer in computers
            ]
        )
        and nat_queue
    ):
        computers[0].add_input(nat_queue)
        y_sent = nat_queue[-1]

        if verbose_level >= 1:
            print(
                "NAT sends", nat_queue, "- Previous Y values sent:", nat_y_values_sent
            )
        nat_queue = []
        if nat_y_values_sent and y_sent == nat_y_values_sent[-1]:
            puzzle_actual_result = y_sent
        nat_y_values_sent.append(y_sent)
    else:
        for computer in computers:
            if computer.state == "Paused":
                computer.add_input(-1)
                computer.restart()


# -------------------------------- Outputs / results --------------------------------- #

print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
