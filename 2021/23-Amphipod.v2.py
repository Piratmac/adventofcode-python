# -------------------------------- Input data ---------------------------------------- #
import os, grid, graph, dot, assembly, re, itertools, copy, functools
from collections import Counter, deque, defaultdict
from functools import reduce, lru_cache
import heapq

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
    "input": """#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########""",
    "expected": ["12521", "44169"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read(),
    "expected": ["18170", "Unknown"],
}


# -------------------------------- Control program execution ------------------------- #

case_to_test = 1
part_to_test = 2


# This is attempt 2, where no parsing happens (hardcoded input)
# It works for part 1, but has no optimization so it's too slow for part 2


# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #


class StateGraph(graph.WeightedGraph):
    final_states = []
    valid_states = []
    estimate = []

    def neighbors(self, state):
        neighbors = {}
        if is_state_final(state):
            return {}
        for i in range(len(state)):
            for target, distance in amphipods_edges[state[i]].items():
                new_state = list(state)
                new_state[i] = target
                new_state = tuple(new_state)
                if is_state_valid(new_state) and is_movement_valid(state, new_state, i):
                    neighbors[new_state] = (
                        distance * amphipod_costs[amphipod_targets[i]]
                    )
                    # if state not in self.edges:
                    #    self.edges[state] = {}
                    # self.edges[state][new_state] = distance * amphipod_costs[i]

        # print (state, neighbors)

        return neighbors

    def path(self, target_vertex):
        """
        Reconstructs the path followed to reach a given vertex

        :param Any target_vertex: The vertex to be reached
        :return: A list of vertex from start to target
        """
        path = [target_vertex]
        while self.came_from[target_vertex]:
            distance = self.edges[self.came_from[target_vertex]][target_vertex]
            target_vertex = self.came_from[target_vertex]
            path.append((target_vertex, distance))

        path.reverse()

        return path

    def estimate_to_complete(self, state):
        if state in self.estimate:
            return self.estimate[state]
        estimate = 0
        for i in range(len(state)):
            source = state[i]
            target = amphipod_targets[i]
            estimate += estimate_to_complete_amphipod(source, target)

        return estimate

    def a_star_search(self, start, end=None):
        current_distance = 0
        frontier = [(0, start, 0)]
        heapq.heapify(frontier)
        self.distance_from_start = {start: 0}
        self.came_from = {start: None}
        self.min_distance = float("inf")

        while frontier:
            estimate_at_completion, vertex, current_distance = heapq.heappop(frontier)
            if (len(frontier)) % 10000 == 0:
                print(
                    len(frontier),
                    self.min_distance,
                    estimate_at_completion,
                    current_distance,
                )

            if current_distance > self.min_distance:
                continue

            if estimate_at_completion > self.min_distance:
                continue

            neighbors = self.neighbors(vertex)
            if not neighbors:
                continue

            for neighbor, weight in neighbors.items():
                # We've already checked that node, and it's not better now
                if neighbor in self.distance_from_start and self.distance_from_start[
                    neighbor
                ] <= (current_distance + weight):
                    continue

                if current_distance + weight > self.min_distance:
                    continue

                # Adding for future examination
                priority = current_distance + self.estimate_to_complete(neighbor)
                heapq.heappush(
                    frontier, (priority, neighbor, current_distance + weight)
                )

                # Adding for final search
                self.distance_from_start[neighbor] = current_distance + weight
                self.came_from[neighbor] = vertex

                if is_state_final(neighbor):
                    self.min_distance = min(
                        self.min_distance, current_distance + weight
                    )
                    print("Found", self.min_distance, "at", len(frontier))
                    # Example, part 1:
                    # Trouvé vers 340000
                    # Commence à converger vers 570000

                    # Real, part 1:
                    # Trouvé 1e valeur vers 1 290 000
                    # Trouvé valeur correcte à 1 856 807

        return end in self.distance_from_start


@lru_cache
def is_state_final(state):
    return all(amphipod_targets[i] == state[i][0] for i in range(8))


@lru_cache
def is_state_valid(state):
    # print (state)
    # Can't have 2 amphipods in the same place
    if len(set(state)) != len(state):
        # print ('Amphipod superposition')
        return False

    for i in range(len(state)):
        if state[i][0] in "ABCD":

            # Moved to a room
            if state[i][0] != start[i][0]:
                # Moved to a room that is not ours
                if state[i][0] != amphipod_targets[i]:
                    # print ('Moved to other room', state, i, start)
                    return False

                # Moved to a room where there is someone else
                room = [
                    position
                    for position, room in enumerate(state)
                    if room == amphipod_targets[i] and position != i
                ]
                if len(state) == 8:
                    if any([position // 2 != i // 2 for position in room]):
                        # print ('Room occupied', state, i, start)
                        return False
                else:
                    if any([position // 4 != i // 4 for position in room]):
                        # print ('Room occupied', state, i, start)
                        return False

    return True


@lru_cache
def estimate_to_complete_amphipod(source, target):
    estimate = 0
    amphipod_cost = amphipod_costs[target[0]]
    # Not in target place
    if target[0] != source[0]:
        if source in ("LL", "RR"):
            estimate += amphipod_cost
            source = "LR" if source[0] == "L" else "RL"
            # print ('LL/RR', i, source, amphipod_cost)

        if source[0] in "LX":
            # print ('LX', i, source, amphipods_edges[source][target[0]+'1'] * amphipod_cost)
            estimate += amphipods_edges[source][target[0] + "1"] * amphipod_cost
        else:
            # From one room to the other, just count 2 until hallway + 2 per room distance
            # print ('Room', i, source, (2+2*abs(ord(source[0])-ord('A') - i//2)) * amphipod_cost)
            estimate += (2 + 2 * abs(ord(source[0]) - ord(target[0]))) * amphipod_cost
    return estimate


@lru_cache
def is_movement_valid(state, new_state, changed):
    # Check there are no amphibot in the way
    # print ('Moving', changed, 'at', state[changed], 'to', new_state[changed])
    if state[changed] in amphipods_edges_conditions:
        if new_state[changed] in amphipods_edges_conditions[state[changed]]:
            # print (amphipods_edges_conditions[state[changed]][new_state[changed]])
            if any(
                amphi in amphipods_edges_conditions[state[changed]][new_state[changed]]
                for amphi in new_state
            ):
                return False

    return True


amphipod_costs = {"A": 1, "B": 10, "C": 100, "D": 1000}

if part_to_test == 1:
    amphipod_targets = ["A", "A", "B", "B", "C", "C", "D", "D"]
    amphipods_edges = {
        "LL": {"LR": 1},
        "LR": {"LL": 1, "A1": 2, "B1": 4, "C1": 6, "D1": 8},
        "A1": {"A2": 1, "LR": 2, "XAB": 2, "XBC": 4, "XCD": 6, "RL": 8},
        "A2": {"A1": 1},
        "XAB": {"A1": 2, "B1": 2, "C1": 4, "D1": 6},
        "B1": {"B2": 1, "LR": 4, "XAB": 2, "XBC": 2, "XCD": 4, "RL": 6},
        "B2": {"B1": 1},
        "XBC": {"B1": 2, "C1": 2, "A1": 4, "D1": 4},
        "C1": {"C2": 1, "LR": 6, "XAB": 4, "XBC": 2, "XCD": 2, "RL": 4},
        "C2": {"C1": 1},
        "XCD": {"C1": 2, "D1": 2, "A1": 6, "B1": 4},
        "D1": {"D2": 1, "LR": 8, "XAB": 6, "XBC": 4, "XCD": 2, "RL": 2},
        "D2": {"D1": 1},
        "RL": {"RR": 1, "A1": 8, "B1": 6, "C1": 4, "D1": 2},
        "RR": {"RL": 1},
    }

    amphipods_edges_conditions = {
        "XAB": {"C1": ["XBC"], "D1": ["XBC", "XCD"]},
        "XBC": {"A1": ["XAB"], "D1": ["XCD"]},
        "XCD": {"A1": ["XAB", "XBC"], "B1": ["XBC"]},
        "A1": {"RL": ["XAB", "XBC", "XCD"], "XBC": ["XAB"], "XCD": ["XAB", "XBC"]},
        "B1": {"LR": ["XAB"], "RL": ["XBC", "XCD"], "XCD": ["XBC"]},
        "C1": {"LR": ["XAB", "XBC"], "RL": ["XCD"], "XAB": ["XBC"]},
        "D1": {"LR": ["XAB", "XBC", "XCD"], "XAB": ["XBC", "XCD"], "XBC": ["XCD"]},
        "LR": {"B1": ["XAB"], "C1": ["XAB", "XBC"], "D1": ["XAB", "XBC", "XCD"]},
        "RL": {"A1": ["XAB", "XBC", "XCD"], "B1": ["XBC", "XCD"], "C1": ["XCD"]},
    }

    if case_to_test == 1:
        start = ("A2", "D2", "A1", "C1", "B1", "C2", "B2", "D1")
    else:
        start = ("A1", "C2", "C1", "D1", "B1", "D2", "A2", "B2")

    end = tuple("AABBCCDD")

    amphipod_graph = StateGraph()

    state = ("A2", "D2", "A1", "C1", "B1", "C2", "B2", "D1")
    assert is_state_final(state) == False
    state = ("A1", "A2", "B1", "B2", "C1", "C2", "D2", "D2")
    assert is_state_final(state) == True
    state = ("A1", "A2", "B1", "B1", "C1", "C2", "D2", "D2")
    assert is_state_valid(state) == False
    assert is_state_final(state) == True

    # Can't move from C1 to RL if XBC is occupied
    source = ("A2", "D2", "B1", "XCD", "C1", "C2", "XBC", "D1")
    target = ("A2", "D2", "B1", "XCD", "RL", "C2", "XBC", "D1")
    assert amphipod_graph.is_movement_valid(source, target, 4) == False

    # Can't move to room occupied by someone else
    target = ("A2", "B1", "A1", "D2", "C1", "C2", "B2", "D1")
    assert is_state_valid(target) == False

    state = ("A2", "D2", "A1", "XBC", "B1", "C2", "B2", "D1")
    assert amphipod_graph.estimate_to_complete(state) == 6468
    state = ("A2", "D2", "A1", "C1", "B1", "C2", "B2", "D1")
    assert amphipod_graph.estimate_to_complete(state) == 6488

    amphipod_graph.a_star_search(start)

    puzzle_actual_result = amphipod_graph.min_distance

else:
    amphipod_targets = [
        "A",
        "A",
        "A",
        "A",
        "B",
        "B",
        "B",
        "B",
        "C",
        "C",
        "C",
        "C",
        "D",
        "D",
        "D",
        "D",
    ]
    amphipods_edges = {
        "LL": {"LR": 1},
        "LR": {"LL": 1, "A1": 2, "B1": 4, "C1": 6, "D1": 8},
        "A1": {"A2": 1, "LR": 2, "XAB": 2, "XBC": 4, "XCD": 6},
        "A2": {"A1": 1, "A3": 1},
        "A3": {"A2": 1, "A4": 1},
        "A4": {"A3": 1},
        "XAB": {"A1": 2, "B1": 2, "C1": 4, "D1": 6},
        "B1": {"B2": 1, "LR": 4, "XAB": 2, "XBC": 2, "XCD": 4, "RL": 6},
        "B2": {"B1": 1, "B3": 1},
        "B3": {"B2": 1, "B4": 1},
        "B4": {"B3": 1},
        "XBC": {"B1": 2, "C1": 2, "A1": 4, "D1": 4},
        "C1": {"C2": 1, "LR": 6, "XAB": 4, "XBC": 2, "XCD": 2, "RL": 4},
        "C2": {"C1": 1, "C3": 1},
        "C3": {"C2": 1, "C4": 1},
        "C4": {"C3": 1},
        "XCD": {"C1": 2, "D1": 2, "A1": 6, "B1": 4},
        "D1": {"D2": 1, "LR": 8, "XAB": 6, "XBC": 4, "XCD": 2, "RL": 2},
        "D2": {"D1": 1, "D3": 1},
        "D3": {"D2": 1, "D4": 1},
        "D4": {"D3": 1},
        "RL": {"RR": 1, "A1": 8, "B1": 6, "C1": 4, "D1": 2},
        "RR": {"RL": 1},
    }

    amphipods_edges_conditions = {
        "XAB": {"C1": ["XBC"], "D1": ["XBC", "XCD"]},
        "XBC": {"A1": ["XAB"], "D1": ["XCD"]},
        "XCD": {"A1": ["XAB", "XBC"], "B1": ["XBC"]},
        "A1": {"RL": ["XAB", "XBC", "XCD"], "XBC": ["XAB"], "XCD": ["XAB", "XBC"]},
        "B1": {"LR": ["XAB"], "RL": ["XBC", "XCD"], "XCD": ["XBC"]},
        "C1": {"LR": ["XAB", "XBC"], "RL": ["XCD"], "XAB": ["XBC"]},
        "D1": {"LR": ["XAB", "XBC", "XCD"], "XAB": ["XBC", "XCD"], "XBC": ["XCD"]},
        "LR": {"B1": ["XAB"], "C1": ["XAB", "XBC"], "D1": ["XAB", "XBC", "XCD"]},
        "RL": {"A1": ["XAB", "XBC", "XCD"], "B1": ["XBC", "XCD"], "C1": ["XCD"]},
    }

    start_points = {
        1: (
            "A4",
            "C3",
            "D2",
            "D4",
            "A1",
            "B3",
            "C1",
            "C2",
            "B1",
            "B2",
            "C4",
            "D3",
            "A2",
            "A3",
            "B4",
            "D1",
        ),
        #############
        # ...........#
        ###B#C#B#D###
        # D#C#B#A#
        # D#B#A#C#
        # A#D#C#A#
        #########
        "real": (
            "A1",
            "C3",
            "C4",
            "D2",
            "B3",
            "C1",
            "C2",
            "D1",
            "B1",
            "B2",
            "D3",
            "D4",
            "A2",
            "A3",
            "A4",
            "B4",
        )
        #############
        # ...........#
        ###A#C#B#B###
        # D#C#B#A#
        # D#B#A#C#
        # D#D#A#C#
        #########
    }
    start = start_points[case_to_test]

    amphipod_graph = StateGraph()

    if True:
        # Check initial example start
        state = start_points[1]
        assert is_state_final(state) == False
        assert is_state_valid(state) == True

        # Check final state
        state = (
            "A1",
            "A2",
            "A1",
            "A2",
            "B1",
            "B2",
            "B1",
            "B2",
            "C1",
            "C2",
            "C1",
            "C2",
            "D2",
            "D2",
            "D2",
            "D2",
        )
        assert is_state_final(state) == True
        assert is_state_valid(state) == False

        # Can't move from C1 to RL if XBC is occupied
        source = (
            "A2",
            "D2",
            "B1",
            "XCD",
            "C1",
            "C2",
            "XBC",
            "D1",
            "A2",
            "D2",
            "B1",
            "XCD",
            "C1",
            "C2",
            "XBC",
            "D1",
        )
        target = (
            "A2",
            "D2",
            "B1",
            "XCD",
            "RL",
            "C2",
            "XBC",
            "D1",
            "A2",
            "D2",
            "B1",
            "XCD",
            "C1",
            "C2",
            "XBC",
            "D1",
        )
        assert is_movement_valid(source, target, 4) == False

        # Can't move to room occupied by someone else
        state = (
            "A4",
            "C1",
            "C3",
            "C2",
            "A1",
            "B3",
            "XAB",
            "C2",
            "B1",
            "B2",
            "C4",
            "D3",
            "A2",
            "A3",
            "B4",
            "D1",
        )
        assert is_state_valid(target) == False

        state = start_points[1]
        # print (amphipod_graph.neighbors(state))
        # print (amphipod_graph.estimate_to_complete(state))
        assert amphipod_graph.estimate_to_complete(state) == 23342

        # Estimate when on target
        state = (
            "A1",
            "A2",
            "A3",
            "A4",
            "B1",
            "B2",
            "B3",
            "B4",
            "C1",
            "C2",
            "C3",
            "C4",
            "D1",
            "D2",
            "D3",
            "D4",
        )
        assert amphipod_graph.estimate_to_complete(state) == 0

        # Estimate when 1 is missing
        state = (
            "XAB",
            "A2",
            "A3",
            "A4",
            "B1",
            "B2",
            "B3",
            "B4",
            "C1",
            "C2",
            "C3",
            "C4",
            "D1",
            "D2",
            "D3",
            "D4",
        )
        assert amphipod_graph.estimate_to_complete(state) == 2

        # Estimate for other amphipod
        state = (
            "A1",
            "A2",
            "A3",
            "A4",
            "XCD",
            "B2",
            "B3",
            "B4",
            "C1",
            "C2",
            "C3",
            "C4",
            "D1",
            "D2",
            "D3",
            "D4",
        )
        assert amphipod_graph.estimate_to_complete(state) == 40

        # Estimate when 2 are inverted
        state = (
            "A1",
            "A2",
            "A3",
            "B1",
            "A1",
            "B2",
            "B3",
            "B4",
            "C1",
            "C2",
            "C3",
            "C4",
            "D1",
            "D2",
            "D3",
            "D4",
        )
        assert amphipod_graph.estimate_to_complete(state) == 44

        # Estimate when start in LL
        state = (
            "LL",
            "A2",
            "A3",
            "A4",
            "B1",
            "B2",
            "B3",
            "B4",
            "C1",
            "C2",
            "C3",
            "C4",
            "D1",
            "D2",
            "D3",
            "D4",
        )
        assert amphipod_graph.estimate_to_complete(state) == 3

    # amphipod_graph.dijkstra(start)
    amphipod_graph.a_star_search(start)


# -------------------------------- Outputs / results --------------------------------- #

print("Case :", case_to_test, "- Part", part_to_test)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
# Date created: 2021-12-23 08:11:43.693421
# Part 1: 2021-12-24 01:44:31
