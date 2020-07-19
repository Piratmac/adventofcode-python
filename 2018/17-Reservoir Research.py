# -------------------------------- Input data ---------------------------------------- #
import os

test_data = {}

test = 1
test_data[test] = {
    "input": """x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504""",
    "expected": ["Unknown", "Unknown"],
}

test += 1
test_data[test] = {
    "input": """x=496, y=2..8
x=499, y=3..5
x=501, y=3..5
y=5, x=499..501
x=505, y=2..8""",
    "expected": ["Unknown", "Unknown"],
}

test += 1
test_data[test] = {
    "input": """x=491, y=2..8
x=497, y=4..8
x=504, y=3..8
y=8, x=497..504
x=508, y=2..8""",
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
    "expected": ["39877", "33291"],
}

# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"
part_to_test = 2

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #


walls = []
min_y, max_y = 0, -(10 ** 6)
min_x, max_x = 500, 500

for string in puzzle_input.split("\n"):
    a, b = string.split(", ")
    dim1, val1 = a.split("=")
    val1 = int(val1)

    dim2, val2 = b.split("=")
    val2 = val2.split("..")
    val2, val3 = int(val2[0]), int(val2[1])

    if dim1 == "x":
        min_y = min(min_y, -val3)
        max_y = max(max_y, -val2)
        min_x = min(min_x, val1)
        max_x = max(max_x, val1)
    else:
        min_y = min(min_y, -val1)
        max_y = max(max_y, -val1)
        min_x = min(min_x, val2)
        max_x = max(max_x, val3)

    for spot in range(val2, val3 + 1):
        if dim1 == "x":
            dot = val1 - spot * 1j
        else:
            dot = spot - val1 * 1j
        walls.append(dot)

walls = set(walls)

current_position = 500
wet_positions = set()
pools = set()
flowing = [current_position]
settled = set()

i = 0
while flowing:
    current_position = flowing.pop()
    #        print ('--------------')
    #        print ('now', current_position, current_position - 1j not in walls, current_position - 1j not in pools)
    #        print ('pools', pools)

    if current_position.imag <= min_y:
        settled.add(current_position)
        position = current_position + 1j

        while position in flowing:
            settled.add(position)
            flowing.remove(position)
            position += 1j
        continue

    if current_position - 1j in settled:
        settled.add(current_position)
        continue
    if current_position - 1j not in walls and current_position - 1j not in pools:
        flowing.append(current_position)
        flowing.append(current_position - 1j)
        current_position -= 1j
        if current_position.imag >= min_y and current_position.imag <= max_y:
            wet_positions.add(current_position)
    else:

        pooling = True
        settling = False
        pool = set([current_position])
        # fill horizontally

        for direction in [-1, 1]:
            position = current_position
            while True:
                # Extend to the right
                position += direction
                if position in walls:
                    break
                elif position in settled:
                    settling = True
                    break
                else:
                    wet_positions.add(position)
                    pool.add(position)
                    if position - 1j not in walls and position - 1j not in pools:
                        pooling = False
                        flowing.append(position)
                        break

        if settling:
            settled = settled.union(pool)
        elif pooling:
            pools = pools.union(pool)

    # print ('pools', pools)
    # print ('flowing', flowing)

    # This limit is totally arbitrary
    if i == 10 ** 4:
        print("stop")
        break
    i += 1

print("step", i)
for y in range(max_y + 1, min_y - 1, -1):
    for x in range(min_x - 2, max_x + 3):
        if x + y * 1j in pools:
            print("~", end="")
        elif x + y * 1j in settled:
            print("S", end="")
        elif x + y * 1j in flowing:
            print("F", end="")
        elif x + y * 1j in pools:
            print("~", end="")
        elif x + y * 1j in wet_positions:
            print("|", end="")
        elif x + y * 1j in walls:
            print("#", end="")
        else:
            print(".", end="")
    print("")


if part_to_test == 1:
    puzzle_actual_result = len(wet_positions)
else:
    puzzle_actual_result = len(pools)
# 33556 too high


# -------------------------------- Outputs / results --------------------------------- #

print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
