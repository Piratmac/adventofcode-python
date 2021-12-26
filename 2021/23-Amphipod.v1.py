# -------------------------------- Input data ---------------------------------------- #
import os, grid, graph, dot, assembly, re, itertools, copy, functools
from collections import Counter, deque, defaultdict
from functools import reduce
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
    "expected": ["12521", "Unknown"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read(),
    "expected": ["Unknown", "Unknown"],
}


# -------------------------------- Control program execution ------------------------- #

case_to_test = 1
part_to_test = 1

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# This was the very first attempt to solve it
# It tries to parse the input, the run A* on it to find possible movements
# Basically it's wayyy too slow and buggy


# -------------------------------- Actual code execution ----------------------------- #

dot.Dot.sort_value = dot.Dot.sorting_map["xy"]


class NewGrid(grid.Grid):
    def text_to_dots(self, text, ignore_terrain="", convert_to_int=False):
        self.dots = {}

        y = 0
        self.amphipods = {}
        self.position_to_rooms = []
        nb_amphipods = []
        for line in text.splitlines():
            for x in range(len(line)):
                if line[x] not in ignore_terrain:
                    value = line[x]
                    position = x - y * 1j

                    if value == " ":
                        continue

                    if value in "ABCD":
                        self.position_to_rooms.append(position)
                        if value in nb_amphipods:
                            UUID = value + "2"
                        else:
                            UUID = value + "1"
                            nb_amphipods.append(value)
                        self.amphipods[UUID] = dot.Dot(self, position, value)

                        value = "."

                    self.dots[position] = dot.Dot(self, position, value)
                    # self.dots[position].sort_value = self.dots[position].sorting_map['xy']
                    if value == ".":
                        self.dots[position].is_waypoint = True
            y += 1


class StateGraph(graph.WeightedGraph):
    amphipod_state = ["A1", "A2", "B1", "B2", "C1", "C2", "D1", "D2"]

    def a_star_search(self, start, end=None):
        """
        Performs a A* search

        This algorithm is appropriate for "One source, multiple targets"
        It takes into account positive weigths / costs of travelling.
        Negative weights will make the algorithm fail.

        The exploration path is a mix of Dijkstra and Greedy BFS
        It uses the current cost + estimated cost to determine the next element to consider

        Some cases to consider:
        - If Estimated cost to complete = 0, A* = Dijkstra
        - If Estimated cost to complete <= actual cost to complete, it is exact
        - If Estimated cost to complete > actual cost to complete, it is inexact
        - If Estimated cost to complete = infinity, A* = Greedy BFS
        The higher Estimated cost to complete, the faster it goes

        :param Any start: The start vertex to consider
        :param Any end: The target/end vertex to consider
        :return: True when the end vertex is found, False otherwise
        """
        current_distance = 0
        frontier = [(0, start, 0)]
        heapq.heapify(frontier)
        self.distance_from_start = {start: 0}
        self.came_from = {start: None}
        self.visited = [tuple(dot.position for dot in start)]

        i = 0
        while frontier:  # and i < 5:
            i += 1
            priority, vertex, current_distance = heapq.heappop(frontier)
            print(len(frontier), priority, current_distance)

            neighbors = self.neighbors(vertex)
            if not neighbors:
                continue

            for neighbor, weight in neighbors.items():
                # We've already checked that node, and it's not better now
                if neighbor in self.distance_from_start and self.distance_from_start[
                    neighbor
                ] <= (current_distance + weight):
                    continue

                if any(
                    equivalent_position in self.visited
                    for equivalent_position in self.equivalent_positions(neighbor)
                ):
                    continue

                # Adding for future examination
                priority = current_distance + self.estimate_to_complete(neighbor, end)
                # print (vertex, neighbor, current_distance, priority)
                heapq.heappush(
                    frontier, (priority, neighbor, current_distance + weight)
                )

                # Adding for final search
                self.distance_from_start[neighbor] = current_distance + weight
                self.came_from[neighbor] = vertex
                self.visited.append(tuple(dot.position for dot in neighbor))

                if self.state_is_final(neighbor):
                    return self.distance_from_start[neighbor]

            # print (len(frontier))

        return end in self.distance_from_start

    def neighbors(self, state):
        if self.state_is_final(state):
            return None

        neighbors = {}
        for i, current_dot in enumerate(state):
            amphipod_code = self.amphipod_state[i]
            dots = self.area_graph.edges[current_dot]
            for dot, cost in dots.items():
                new_state = list(state)
                new_state[i] = dot
                new_state = tuple(new_state)
                # print ('Checking', amphipod_code, 'moved from', state[i], 'to', new_state[i])
                if self.state_is_valid(state, new_state, i):
                    neighbors[new_state] = (
                        cost * self.amphipods[amphipod_code].movement_cost
                    )
                    # print ('Movement costs', cost * self.amphipods[amphipod_code].movement_cost)

        return neighbors

    def state_is_final(self, state):
        for i, position in enumerate(state):
            amphipod_code = self.amphipod_state[i]
            amphipod = self.amphipods[amphipod_code]

            if not position in self.room_to_positions[amphipod.terrain]:
                return False
        return True

    def state_is_valid(self, state, new_state, changed):
        # Duplicate = 2 amphipods in the same place
        if len(set(new_state)) != len(new_state):
            # print ('Duplicate amphipod', new_state[changed])
            return False

        # Check amphipod is not in wrong room
        if new_state[i].position in self.position_to_rooms:
            room = self.position_to_rooms[new_state[i].position]
            # print ('Amphipod may be in wrong place', new_state)
            amphipod = self.amphipod_state[i]
            if room == self.amphipods[amphipod].initial_room:
                return True
            else:
                # print ('Amphipod is in wrong place', new_state)
                return False

        return True

    def estimate_to_complete(self, state, target_vertex):
        distance = 0
        for i, dot in enumerate(state):
            amphipod_code = self.amphipod_state[i]
            amphipod = self.amphipods[amphipod_code]

            if not dot.position in self.room_to_positions[amphipod.terrain]:
                room_positions = self.room_to_positions[amphipod.terrain]
                targets = [self.dots[position] for position in room_positions]
                distance += (
                    min(
                        self.area_graph.all_edges[dot][target]
                        if target in self.area_graph.all_edges[dot]
                        else 10 ** 6
                        for target in targets
                    )
                    * amphipod.movement_cost
                )

        return distance

    def equivalent_positions(self, state):
        state_positions = [dot.position for dot in state]
        positions = [
            tuple([state_positions[1]] + [state_positions[0]] + state_positions[2:]),
            tuple(
                state_positions[0:2]
                + [state_positions[3]]
                + [state_positions[2]]
                + state_positions[4:]
            ),
            tuple(
                state_positions[0:4]
                + [state_positions[5]]
                + [state_positions[4]]
                + state_positions[6:]
            ),
            tuple(state_positions[0:6] + [state_positions[7]] + [state_positions[6]]),
        ]

        for i in range(4):
            position = tuple(
                state_positions[:i]
                + state_positions[i + 1 : i]
                + state_positions[i + 2 :]
            )
            positions.append(position)

        return positions


if part_to_test == 1:
    area_map = NewGrid()
    area_map.text_to_dots(puzzle_input)

    position_to_rooms = defaultdict(list)
    room_to_positions = defaultdict(list)
    area_map.position_to_rooms = sorted(
        area_map.position_to_rooms, key=lambda a: (a.real, a.imag)
    )
    for i in range(4):
        position_to_rooms[area_map.position_to_rooms[2 * i]] = "ABCD"[i]
        position_to_rooms[area_map.position_to_rooms[2 * i + 1]] = "ABCD"[i]
        room_to_positions["ABCD"[i]].append(area_map.position_to_rooms[2 * i])
        room_to_positions["ABCD"[i]].append(area_map.position_to_rooms[2 * i + 1])
        # Forbid to use the dot right outside the room
        area_map.dots[area_map.position_to_rooms[2 * i + 1] + 1j].is_waypoint = False
    area_map.position_to_rooms = position_to_rooms
    area_map.room_to_positions = room_to_positions

    # print (list(dot for dot in area_map.dots if area_map.dots[dot].is_waypoint))

    for amphipod in area_map.amphipods:
        area_map.amphipods[amphipod].initial_room = area_map.position_to_rooms[
            area_map.amphipods[amphipod].position
        ]
        area_map.amphipods[amphipod].movement_cost = 10 ** (
            ord(area_map.amphipods[amphipod].terrain) - ord("A")
        )

    area_graph = area_map.convert_to_graph()
    area_graph.all_edges = area_graph.edges
    area_graph.edges = {
        dot: {
            neighbor: distance
            for neighbor, distance in area_graph.edges[dot].items()
            if distance <= 2
        }
        for dot in area_graph.vertices
    }
    print(len(area_graph.all_edges))

    # print (area_graph.vertices)
    # print (area_graph.edges)

    state_graph = StateGraph()
    state_graph.area_graph = area_graph
    state_graph.amphipods = area_map.amphipods
    state_graph.position_to_rooms = area_map.position_to_rooms
    state_graph.room_to_positions = area_map.room_to_positions
    state_graph.dots = area_map.dots

    state = tuple(
        area_map.dots[area_map.amphipods[amphipod].position]
        for amphipod in sorted(area_map.amphipods.keys())
    )
    # print ('area_map.amphipods', area_map.amphipods)

    print("state", state)
    # print ('equivalent', state_graph.equivalent_positions(state))
    print("estimate", state_graph.estimate_to_complete(state, None))

    print(state_graph.a_star_search(state))

    # In the example, A is already in the right place
    # In all other cases, 1 anphipod per group has to go to the bottom, so 1 move per amphipod


else:
    for string in puzzle_input.split("\n"):
        if string == "":
            continue


# -------------------------------- Outputs / results --------------------------------- #

print("Case :", case_to_test, "- Part", part_to_test)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
# Date created: 2021-12-23 08:11:43.693421
