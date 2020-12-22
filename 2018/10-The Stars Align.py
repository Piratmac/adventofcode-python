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
stars_init = [star.copy() for star in stars]
min_galaxy_size = 10 ** 15
min_i_galaxy_size = 0
for i in range(2 * 10 ** 4):
    stars = [(x + i * vx, y + i * vy, vx, i * vy) for x, y, vx, vy in stars_init]

    # This gives a very rough idea of the galaxy's size
    coords = list(zip(*stars))
    galaxy_size = max(coords[0]) - min(coords[0]) + max(coords[1]) - max(coords[1])

    if i == 0:
        min_galaxy_size = galaxy_size

    if galaxy_size < min_galaxy_size:
        min_i_galaxy_size = i
        min_galaxy_size = galaxy_size
    elif galaxy_size > min_galaxy_size:
        vertices = [
            x + vx * min_i_galaxy_size - (y + vy * min_i_galaxy_size) * 1j
            for x, y, vx, vy in stars_init
        ]
        star_map.vertices = vertices
        puzzle_actual_result = "See above, the galaxy is of size", min_i_galaxy_size
        print(star_map.vertices_to_grid(wall=" "))
        break


# -------------------------------- Outputs / results -------------------------------- #

print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
