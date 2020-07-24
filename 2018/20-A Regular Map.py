# -------------------------------- Input data ---------------------------------------- #
import os

test_data = {}

test = 1
test_data[test] = {
    "input": """^WNE$""",
    "expected": ["3", "Unknown"],
}

test += 1
test_data[test] = {
    "input": """^W(N|W)E$""",
    "expected": ["3", "Unknown"],
}

test += 1
test_data[test] = {
    "input": """^ENWWW(NEEE|SSE(EE|N))$""",
    "expected": ["10", "Unknown"],
}

test += 1
test_data[test] = {
    "input": """^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$""",
    "expected": ["18", "Unknown"],
}

test += 1
test_data[test] = {
    "input": """^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$""",
    "expected": ["23", "Unknown"],
}

test += 1
test_data[test] = {
    "input": """^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$""",
    "expected": ["31", "Unknown"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read().strip(),
    "expected": ["3207", "8361"],
}

# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"
part_to_test = 2

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #


forks = [{0: 0}]

positions = {0: 0}
dir = {"N": -1j, "S": 1j, "E": 1, "W": -1}
movement = 0
length = 0

all_positions = tuple()
positions_below_1000 = tuple()
for letter in puzzle_input[1:-1]:
    if letter in "NSEW":
        # Move !
        positions = {pos + dir[letter]: positions[pos] + 1 for pos in positions}
        positions_below_1000 += tuple(x for x in positions if positions[x] < 1000)
        all_positions += tuple(x for x in positions)
    elif letter == "(":
        # Put current positions in the queue (= start of fork)
        forks.append(positions)
        # Initiate the "last fork targets" that'll get updated later
        forks.append({})
    elif letter == "|":
        # Update the "last fork targets" (forks[-1]), then reset to forks[-2]
        forks[-1] = {
            pos: min(forks[-1][pos], positions.get(pos, 10 ** 6)) for pos in forks[-1]
        }
        forks[-1].update(
            {pos: positions[pos] for pos in positions if pos not in forks[-1]}
        )
        positions = forks[-2]
    elif letter == ")":
        # Merge the current positions, the last fork targets (forks[-1]) and the positions before forking (forks[-2])
        positions.update(
            {pos: min(forks[-1][pos], positions.get(pos, 10 ** 6)) for pos in forks[-1]}
        )
        positions.update(
            {pos: min(forks[-2][pos], positions.get(pos, 10 ** 6)) for pos in forks[-2]}
        )
        # Then go back to before the forking
        forks.pop()
        forks.pop()

# Merge all forks with the most recent positions
for fork in forks:
    positions.update({pos: min(fork[pos], positions.get(pos, 10 ** 6)) for pos in fork})


if part_to_test == 1:
    puzzle_actual_result = max(positions.values())

else:
    puzzle_actual_result = len(set(all_positions)) - len(set(positions_below_1000))


# -------------------------------- Outputs / results --------------------------------- #

print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
