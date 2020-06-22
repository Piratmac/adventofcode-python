# -------------------------------- Input data -------------------------------- #
import os, parse, pathfinding

test_data = {}

test = 1
test_data[test] = {
    "input": """position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>""",
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
    "expected": ["RLEZNRAN", "10240"],
}

# -------------------------------- Control program execution -------------------------------- #

case_to_test = "real"
part_to_test = 1

# -------------------------------- Initialize some variables -------------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution -------------------------------- #
stars = []
for string in puzzle_input.split("\n"):
    if string == "":
        continue
    r = parse.parse("position=<{:>d},{:>d}> velocity=<{:>d},{:>d}>", string)
    stars.append(list(map(int, r)))

star_map = pathfinding.Graph()
for i in range(2 * 10 ** 4):
    stars = [(x + vx, y + vy, vx, vy) for x, y, vx, vy in stars]
    vertices = [x - y * 1j for x, y, vx, vy in stars]

    # This was solved a bit manually
    # I noticed all coordinates would converge around 0 at some point
    # That point was around 10300 seconds
    # Then made a limit: all coordinates should be within 300 from zero
    # (my first test was actually 200, but that was gave no result)
    # This gave ~ 20 seconds of interesting time
    # At the end it was trial and error to find 10 240
    coords = [v.real in range(-300, 300) for v in vertices] + [
        v.imag in range(-300, 300) for v in vertices
    ]

    if all(coords) and i == 10239:
        star_map.vertices = vertices
        print(i + 1)
        print(star_map.vertices_to_grid(wall=" "))


# -------------------------------- Outputs / results -------------------------------- #

print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
