# -------------------------------- Input data ---------------------------------------- #
import os, drawing
from complex_utils import *

test_data = {}

test = 1
test_data[test] = {
    "input": """.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.""",
    "expected": ["1147", "Unknown"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read().strip(),
    "expected": ["483840", "219919"],
}

# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"
part_to_test = 2
verbose_level = 2

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #


def text_to_grid(text):
    """
    Converts a text to a set of coordinates

    The text is expected to be separated by newline characters
    Each character will have its coordinates as keys

    :param string text: The text to convert
    :return: The converted grid, its height and width
    """
    grid = {}
    lines = text.splitlines()
    height = len(lines)
    width = 0
    for y in range(len(lines)):
        width = max(width, len(lines[y]))
        for x in range(len(lines[y])):
            grid[x - 1j * y] = lines[y][x]

    return grid


def grid_to_text(grid, blank_character=" "):
    """
    Converts the grid to a text format

    :param dict grid: The grid to convert, in format (x, y): value
    :param string blank_character: What to use for cells with unknown value
    :return: The grid in text format
    """

    text = ""

    min_y, max_y = int(max_imag(grid.keys())), int(min_imag(grid.keys()))
    min_x, max_x = int(min_real(grid.keys())), int(max_real(grid.keys()))

    for y in range(min_y, max_y + 1, -1):
        for x in range(min_x, max_x + 1):
            if x + 1j * y in grid:
                text += str(grid[x + 1j * y])
            else:
                text += blank_character
        text += os.linesep
    text = text[: -len(os.linesep)]

    return text


if part_to_test == 1:
    end = 10
else:
    end = 1000000000


graph = text_to_grid(puzzle_input)

if verbose_level == 3:
    print("Initial state")
    print(grid_to_text(graph))

i = 1
scores = []
while i <= end:
    new_graph = graph.copy()

    for space in graph:
        neighbors = [
            graph[space + direction]
            for direction in directions_diagonals
            if space + direction in graph
        ]
        if graph[space] == ".":
            if len([x for x in neighbors if x == "|"]) >= 3:
                new_graph[space] = "|"
        elif graph[space] == "|":
            if len([x for x in neighbors if x == "#"]) >= 3:
                new_graph[space] = "#"
        elif graph[space] == "#":
            if (
                len([x for x in neighbors if x == "#"]) >= 1
                and len([x for x in neighbors if x == "|"]) >= 1
            ):
                new_graph[space] = "#"
            else:
                new_graph[space] = "."

    graph = new_graph.copy()
    if verbose_level == 3:
        print("step", i)
        print(grid_to_text(new_graph))

    score = len([1 for x in graph if graph[x] == "#"]) * len(
        [1 for x in graph if graph[x] == "|"]
    )
    if i > 800 and i < 10 ** 8 and score in scores:
        repeats_every = i - scores.index(score) - 1 - 800
        i += (end - i) // repeats_every * repeats_every
        # print(
        # "repeats_every",
        # repeats_every,
        # "score",
        # score,
        # "index",
        # scores.index(score),
        # i,
        # )

    if i > 800:
        scores.append(score)
    # print(i, score)

    i += 1

puzzle_actual_result = len([1 for x in graph if graph[x] == "#"]) * len(
    [1 for x in graph if graph[x] == "|"]
)

# -------------------------------- Outputs / results --------------------------------- #

print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
