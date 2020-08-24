# -------------------------------- Input data ---------------------------------------- #
import os, pathfinding, IntCode, math

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
    "expected": ["169", "7001134"],
}

# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"
part_to_test = 2

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #

if part_to_test == 1:
    beam = IntCode.IntCode(puzzle_input)

    affected = 0
    for x in range(50):
        for y in range(50):
            beam.reset(puzzle_input)
            beam.add_input(x)
            beam.add_input(y)
            beam.run()
            affected += beam.outputs.pop()

    puzzle_actual_result = affected


else:
    beam = IntCode.IntCode(puzzle_input)
    known_points = {}

    def check_tractor(position):
        if position not in known_points:
            beam.reset(puzzle_input)
            beam.add_input(position.real)
            beam.add_input(-position.imag)
            beam.run()
            known_points[position] = beam.outputs.pop()
        return known_points[position] == 1

    # If we call alpha the angle from vertical to the lowest part of the beam
    # And beta the angle from vertical to the highest part of the beam
    # And x, y the target position
    # Then we have:
    # x + 100 = y*tan(beta)
    # x = (y+100)*tan(alpha)
    # Therefore:
    # y = 100*(tan (alpha) - 1) / (tan(beta) - tan(alpha))
    # x = y * tan(beta) - 100

    # First, get an approximation of alpha and beta
    def search_x(direction):
        y = 1000
        x = 0 if direction == 1 else 10 ** 4
        resolution = 100
        while True:
            if check_tractor(x + resolution - j * y) == 1:
                if resolution == 1:
                    break
                resolution //= 2
            else:
                x += resolution * direction
        return x

    alpha = math.atan(search_x(1) / 1000)
    beta = math.atan(search_x(-1) / 1000)

    # Then, math!
    # Note: We look for size 150 as a safety
    y = 150 * (math.tan(alpha) + 1) / (math.tan(beta) - math.tan(alpha))
    x = y * math.tan(beta) - 150
    position = int(x) - int(y) * j

    def corners(position):
        # We need to check only those 2 positions
        return [position + 99, position - 99 * j]

    valid_position = 0
    checked_positions = []
    best_position = position
    resolution = 100

    while True:
        box = corners(position)
        checked_positions.append(position)

        new_position = position
        if check_tractor(box[0]) and check_tractor(box[1]):
            if manhattan_distance(0, best_position) > manhattan_distance(0, position):
                best_position = position
            # If I move the box just by 1, it fails
            if (
                not check_tractor(box[0] + 1)
                and not check_tractor(box[0] + 1 * j)
                and not check_tractor(box[1] + 1 * j)
                and not check_tractor(box[1] + 1 * j)
            ):
                break
            new_position += resolution * j
        elif check_tractor(box[0]):
            new_position += resolution
        elif check_tractor(box[1]):
            new_position -= resolution
        else:
            new_position -= resolution * j

        # This means we have already checked the new position
        # So, either we reduce the resolution, or we check closer
        if new_position in checked_positions:
            if resolution != 1:
                resolution //= 2
            else:
                # This means we are close
                # So now, check the 10*10 grid closer to the emitter
                found = False
                for dx in range(10, 0, -1):
                    for dy in range(10, 0, -1):
                        test = best_position - dx + dy * j
                        box = corners(test)
                        if check_tractor(box[0]) and check_tractor(box[1]):
                            new_position = test
                            found = True
                            break

                if not found:
                    break
        position = new_position
    puzzle_actual_result = int(best_position.real * 10 ** 4 - best_position.imag)


# -------------------------------- Outputs / results --------------------------------- #

print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
