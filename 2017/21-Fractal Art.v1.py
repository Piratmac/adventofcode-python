# -------------------------------- Input data -------------------------------- #
import os, drawing, itertools, math

test_data = {}

test = 1
test_data[test] = {
    "input": """../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#""",
    "expected": ["12", "Unknown"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read().strip(),
    "expected": ["139", "1857134"],
}

# -------------------------------- Control program execution -------------------------------- #

case_to_test = "real"
part_to_test = 2
verbose_level = 1

# -------------------------------- Initialize some variables -------------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution -------------------------------- #

pattern = """.#.
..#
###"""

grid = drawing.text_to_grid(pattern)
parts = drawing.split_in_parts(grid, 2, 2)
merged_grid = drawing.merge_parts(parts, 2, 2)


if case_to_test == 1:
    iterations = 2
elif part_to_test == 1:
    iterations = 5
else:
    iterations = 18


enhancements = {}
for string in puzzle_input.split("\n"):
    if string == "":
        continue

    source, _, target = string.split(" ")
    source = source.replace("/", "\n")
    target = target.replace("/", "\n")

    source_grid = drawing.text_to_grid(source)
    enhancements[source] = target

    for rotated_source in drawing.rotate(source_grid):
        rotated_source_text = drawing.grid_to_text(rotated_source)
        enhancements[rotated_source_text] = target

        for flipped_source in drawing.flip(rotated_source):
            flipped_source_text = drawing.grid_to_text(flipped_source)
            enhancements[flipped_source_text] = target

pattern_grid = drawing.text_to_grid(pattern)
for i in range(iterations):

    grid_x, grid_y = zip(*pattern_grid.keys())
    grid_width = max(grid_x) - min(grid_x) + 1

    if grid_width % 2 == 0:
        parts = drawing.split_in_parts(pattern_grid, 2, 2)
    else:
        parts = drawing.split_in_parts(pattern_grid, 3, 3)

    grid_size = int(math.sqrt(len(parts)))

    new_parts = []
    for part in parts:
        part_text = drawing.grid_to_text(part)
        new_parts.append(drawing.text_to_grid(enhancements[part_text]))

    new_grid = drawing.merge_parts(new_parts, grid_size, grid_size)

    pattern_grid = new_grid

grid_text = drawing.grid_to_text(pattern_grid)

puzzle_actual_result = grid_text.count("#")


# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
    print("Input : " + puzzle_input)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
