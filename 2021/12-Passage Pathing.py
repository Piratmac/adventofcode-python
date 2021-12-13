# -------------------------------- Input data ---------------------------------------- #
import os, grid, graph, dot, assembly, re, itertools
from collections import Counter, deque, defaultdict

from compass import *


# This functions come from https://github.com/mcpower/adventofcode - Thanks!
def lmap(func, *iterables):
    return list(map(func, *iterables))


def ints(s: str):
    return lmap(int, re.findall(r"-?\d+", s))  # thanks mserrano!


def positive_ints(s: str):
    return lmap(int, re.findall(r"\d+", s))  # thanks mserrano!


def floats(s: str):
    return lmap(float, re.findall(r"-?\d+(?:\.\d+)?", s))


def positive_floats(s: str):
    return lmap(float, re.findall(r"\d+(?:\.\d+)?", s))


def words(s: str):
    return re.findall(r"[a-zA-Z]+", s)


test_data = {}

test = 1
test_data[test] = {
    "input": """start-A
start-b
A-c
A-b
b-d
A-end
b-end""",
    "expected": ["10", "36"],
}

test += 1
test_data[test] = {
    "input": """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc""",
    "expected": ["19", "103"],
}

test += 1
test_data[test] = {
    "input": """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW""",
    "expected": ["226", "3509"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read(),
    "expected": ["4011", "108035"],
}


# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"
part_to_test = 2

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #

# Conver integer to 36-character binary
#  str_value = "{0:>036b}".format(value)
# Convert binary string to number
#  value = int(str_value, 2)


if part_to_test == 1:
    edges = {}
    vertices = set()
    for string in puzzle_input.split("\n"):
        a, b = string.split("-")
        if not a in edges:
            edges[a] = {}
        if a != "end":
            edges[a].update({b: 1})
        if b not in edges:
            edges[b] = {}
        if b != "end":
            edges[b].update({a: 1})
        vertices.add(a)
        vertices.add(b)

    caves = graph.Graph(vertices, edges)
    caves.is_vertex_valid_for_path = (
        lambda path, vertex: vertex.isupper() or not vertex in path
    )
    caves.find_all_paths("start", "end")
    puzzle_actual_result = len(caves.paths)


else:
    edges = {}
    vertices = set()
    for string in puzzle_input.split("\n"):
        a, b = string.split("-")
        if not a in edges:
            edges[a] = {}
        if a != "end":
            edges[a].update({b: 1})
        if b not in edges:
            edges[b] = {}
        if b != "end":
            edges[b].update({a: 1})
        vertices.add(a)
        vertices.add(b)

    caves = graph.Graph(vertices, edges)
    small_caves = [a for a in edges if a.islower()]

    def is_vertex_valid_for_path(path, vertex):
        if vertex.isupper():
            return True

        if vertex == "start":
            return False

        if vertex in path:
            visited = Counter(path)

            return all([visited[a] < 2 for a in small_caves])

        return True

    caves.is_vertex_valid_for_path = is_vertex_valid_for_path
    caves.find_all_paths("start", "end")
    puzzle_actual_result = len(caves.paths)

print("Case :", case_to_test, "- Part", part_to_test)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
# Date created: 2021-12-12 09:16:38.023299
# Part 1: 2021-12-12 09:57:38
# Part 2: 2021-12-12 10:07:46
