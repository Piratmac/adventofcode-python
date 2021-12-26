# -------------------------------- Input data ---------------------------------------- #
import os, grid, graph, dot, assembly, re, itertools, copy, functools, time, math
from collections import Counter, deque, defaultdict
from functools import reduce, lru_cache
import heapq
import cProfile


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
    "input": "",  # open(input_file, "r+").read(),
    "expected": ["18170", "50208"],
}


# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"
part_to_test = 2
check_assertions = False

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #

# Now runs in a reasonable time
# Goal is to further optimize

# Possible improvements:
# Major change:
# - Same algo: change positions to be numeric
# - Same algo: use sets for each group of amphipods (avoids having to convert them)
# - Change algo: each zone is a room, and use pop/prepend ro keep track of order

# Final numbers
# Example part 1:    275619 function calls in   0.242 seconds
# Example part 2: 354914699 function calls in 349.813 seconds
# Real    part 1:    726789 function calls in   0.612 seconds
# Real    part 2: 120184853 function calls in 112.793 seconds


# Initial durations
# Example part 1
# 771454 function calls in 0.700 seconds

# Example part 2
# About 2400 seconds


# Improvements done:
# If X is in Yn and can go to Y(n-1), force that as a neighbor (since it'll happen anyway)
# If X is in Xn and can go to X(n+1), force that as a neighbor (since it'll happen anyway)
# Doing both gave 2x gain on part 1, 8x on part 2
# Example part 1
# 500664 function calls in 0.466 seconds with the priorities (= multiple neighbors)
# 354634 function calls in 0.327 seconds with a single priority (= take 1st priority neighbor found)
# Example part 2
# 348213851 function calls in 339.382 seconds with a single priority


# Allowing to go from X1 to Y1 (with proper 'blocks' in place if someone is in the way)
# Example part 1
# 275619 function calls in 0.244 seconds
# Example part 2
# 352620555 function calls in 339.027 seconds

# Making it end as soon as a solution is found
# Example part 2
# 352337447 function calls in 356.088 seconds ==> Probably not representative...


# Other attempts
# lru_cache on both estimate to complete & get_neighbors
# Example part 2
# 352333566 function calls in 393.890 seconds ==> not a good idea

# Remove lru_cache on state_to_tuple
# Example part 2
# 354915167 function calls in 346.961 seconds


class StateGraph(graph.WeightedGraph):
    final_states = []

    def a_star_search(self, start, end=None):
        current_distance = 0
        frontier = [(0, state_to_tuple(start), start, 0)]
        heapq.heapify(frontier)
        self.distance_from_start = {state_to_tuple(start): 0}
        self.came_from = {state_to_tuple(start): None}
        self.min_distance = float("inf")

        print("Starting search")

        while frontier:
            (
                estimate_at_completion,
                vertex_tuple,
                vertex,
                current_distance,
            ) = heapq.heappop(frontier)
            if (len(frontier)) % 10000 == 0:
                print(
                    " Searching",
                    len(frontier),
                    self.min_distance,
                    estimate_at_completion,
                    current_distance,
                )

            if current_distance > self.min_distance:
                continue

            if estimate_at_completion > self.min_distance:
                continue

            neighbors = get_neighbors(vertex)
            if not neighbors:
                continue

            for neighbor, weight in neighbors.items():
                neighbor_tuple = state_to_tuple(neighbor)
                # We've already checked that node, and it's not better now
                if (
                    neighbor_tuple in self.distance_from_start
                    and self.distance_from_start[neighbor_tuple]
                    <= (current_distance + weight)
                ):
                    continue

                if current_distance + weight > self.min_distance:
                    continue

                # Adding for future examination
                priority = current_distance + estimate_to_complete(neighbor_tuple)
                heapq.heappush(
                    frontier,
                    (priority, neighbor_tuple, neighbor, current_distance + weight),
                )

                # Adding for final search
                self.distance_from_start[neighbor_tuple] = current_distance + weight
                self.came_from[neighbor_tuple] = vertex_tuple

                if is_state_final(neighbor):
                    self.min_distance = min(
                        self.min_distance, current_distance + weight
                    )
                    print(
                        "  Found",
                        self.min_distance,
                        "at",
                        len(frontier),
                        "for",
                        neighbor,
                    )
                    return neighbor
                    self.final_states.append(neighbor)

        print("Search complete!")
        return end in self.distance_from_start


# @lru_cache
def state_to_tuple(state):
    return tuple(
        tuple(sorted(state[group * group_size : (group + 1) * group_size]))
        for group in range(4)
    )


@lru_cache
def is_state_final(state):
    return all(amphipod_targets[i] == val[0] for i, val in enumerate(state))


@lru_cache
def is_state_valid(state):
    # Can't have 2 amphipods in the same place
    if len(set(state)) != len(state):
        # print ('Amphipod superposition')
        return False

    return True


@lru_cache
def estimate_to_complete_amphipod(source, target):
    estimate = 0
    amphipod_cost = amphipod_costs[target[0]]
    # print ('Estimating', source, 'to', target)
    # Not in target place
    if source in ("LL", "RR"):
        estimate += amphipod_cost
        source = "LR" if source[0] == "L" else "RL"
        # print ('Source in LL/RR, adding', amphipod_cost)
        ##print ('LL/RR', i, source, amphipod_cost)

    if source[0] in "RLX":
        ##print ('LX', i, source, amphipods_edges[source][target[0]+'1'] * amphipod_cost)
        estimate += amphipods_edges[source][target[0] + "1"] * amphipod_cost
        # print ('Source in RLX, adding', amphipods_edges[source][target[0]+'1'] * amphipod_cost)
        source = target[0] + "1"

    if target[0] != source[0]:
        # print ('Source in wrong ABCD room, adding', (2+2*abs(ord(source[0]) - ord(target[0]))) * amphipod_cost)
        # From start to top position in room
        estimate += abs(int(source[1]) - 1) * amphipod_cost
        # From one room to the other, count 2 until hallway + 2 per room distance
        estimate += (2 + 2 * abs(ord(source[0]) - ord(target[0]))) * amphipod_cost

        source = target[0] + "1"

    # Then add vertical moves within rooms
    # print ('Adding vertical movements within target', abs(int(source[1]) - int(target[1])) * amphipod_cost)
    estimate += abs(int(target[1]) - 1) * amphipod_cost
    return estimate


@lru_cache
def estimate_to_complete_group(group, positions):
    estimate = 0
    available = [x for x in amphipod_all_targets[group] if x not in positions]
    for i, source in enumerate(positions):
        if source[0] == "ABCD"[group]:
            continue
        target = available.pop()
        estimate += estimate_to_complete_amphipod(source, target)
    return estimate


def estimate_to_complete(state):
    estimate = 0

    for group in range(4):
        estimate += estimate_to_complete_group(group, state[group])

    return estimate


@lru_cache
def is_movement_valid(state, new_state, changed):
    # print ('Checking', changed, 'from', state)
    # print ('             to', new_state)
    current_position = state[changed]
    current_room = current_position[0]

    new_position = new_state[changed]
    new_room = new_position[0]

    target_room = amphipod_targets[changed]
    target_id = changed // group_size

    # Moving within a room
    if new_room == current_room:
        # Forbidden: Moving with something in between
        # Since all movements are by 1 only: If there was an obstable, 2 amphibots would be in the same place

        # Within my target room
        if new_room == target_room:
            # Room occupied by friends only (myself included)
            amphi_in_target = set(
                [
                    amphipod_targets[state.index(target_room + str(i + 1))]
                    for i in range(group_size)
                    if target_room + str(i + 1) in state
                ]
            )
            if amphi_in_target == {target_room}:
                # Allowed: Moving down in target room if full of friends
                # Forbidden: Moving down in target room if full of friends
                # print ('# Allowed: Moving down in target room if full of friends')
                return new_position[-1] > current_position[-1], False

            # Allowed: Moving up in target room if has other people
            # Forbidden: Moving down in target room if has other people
            # print ('# Allowed: Moving up in target room if has other people')
            return new_position[-1] < current_position[-1], False

        # Within a hallway
        # Forbidden: Moving from hallway to another hallway
        # Moving from X to another X is forbidden via amphipods_edges

        # Allowed: move within L or R spaces
        if current_room in "LR":
            # print ('# Allowed: move within L or R spaces')
            return True, False

        # Allowed: Moving up in other's room
        # print ('# Allowed: Moving up in other\'s room')
        return new_position[-1] < current_position[-1], True

    #######
    # Move to my room
    if new_room == target_room:
        # Forbidden: Moving to my room if there are others in it
        amphi_in_target = set(
            [
                amphipod_targets[state.index(target_room + str(i + 1))]
                for i in range(group_size)
                if target_room + str(i + 1) in state
            ]
        )
        if amphi_in_target and amphi_in_target != {target_room}:
            # print ('# Forbidden: Moving to my room if there are others in it')
            return False, False

        # Forbidden: Moving with something in between
        if current_position in amphipods_edges_conditions:
            if new_position in amphipods_edges_conditions[current_position]:
                # New position can't be blocking because it's not in the list of blocking ones
                if any(
                    position
                    in amphipods_edges_conditions[current_position][new_position]
                    for position in new_state
                ):
                    # print ('# Forbidden: Moving to my room with something in between')
                    return False, False

        # Allowed: Moving to my room if only same amphibots are in and no obstacle
        # Allowed: Moving to my room if empty and no obstacle
        # print ('# Allowed: Moving to my room if (empty OR only same amphibots are in) and no obstacle')
        return True, True

    # Move to hallway from a room
    if new_room in "XLR":
        # Forbidden: Moving out of my room if it's empty
        # Forbidden: Moving out of my room if it's full of friends
        amphi_in_target = set(
            [
                amphipod_targets[state.index(target_room + str(i + 1))]
                for i in range(group_size)
                if target_room + str(i + 1) in state
            ]
        )
        if current_room == target_room and (
            amphi_in_target == {target_room} or amphi_in_target == ()
        ):
            # print ('# Forbidden: Moving out of my room if it\'s empty OR full of friends')
            return False, False

        # Forbidden: Moving with something in between
        if current_position in amphipods_edges_conditions:
            if new_position in amphipods_edges_conditions[current_position]:
                # New position can't be blocking because it's not in the list of blocking ones
                if any(
                    position
                    in amphipods_edges_conditions[current_position][new_position]
                    for position in new_state
                ):
                    # print ('# Forbidden: Moving to hallway with something in between')
                    return False, False

        # Allowed: Moving out of my room if there are other people in it and no obstacle
        # Allowed: Moving out of other's room is there are no obstacle
        # print ('# Allowed: Moving out of my room if there are other people in it and no obstacle + # Allowed: Moving out of other\'s room is there are no obstacle')
        return True, False

    # Forbidden: Moving to other's room
    return False, False


def get_neighbors(state):
    neighbors = {}
    if is_state_final(state):
        # print ('Final state')
        return {}

    for i in range(len_state):
        # Forbidden: Moving from hallway to another hallway ==> Through amphipods_edges
        for target, distance in amphipods_edges[state[i]].items():
            new_state = state[:i] + (target,) + state[i + 1 :]
            # print (i, 'moves from', state[i], 'to', target)
            # print ('new state', new_state)
            if is_state_valid(new_state):
                # print ('State valid')
                is_valid, is_priority = is_movement_valid(state, new_state, i)
                if is_valid:  # is_movement_valid(state, new_state, i):
                    # print ('Movement valid')
                    if is_priority:
                        return {
                            new_state: distance * amphipod_costs[amphipod_targets[i]]
                        }
                    neighbors[new_state] = (
                        distance * amphipod_costs[amphipod_targets[i]]
                    )

    # print (state, neighbors)

    return neighbors


def tuple_replace(init, source, target):
    position = init.index(source)
    return position, init[:position] + (target,) + init[position + 1 :]


def state_to_text(state):
    rows = [
        "#############",
        ["#", "LL", "LR", ".", "XAB", ".", "XBC", ".", "XCD", ".", "RL", "RR", "#"],
        ["#", "#", "#", "A1", "#", "B1", "#", "C1", "#", "D1", "#", "#", "#"],
        [" ", " ", "#", "A2", "#", "B2", "#", "C2", "#", "D2", "#", " ", " "],
        [" ", " ", "#", "A3", "#", "B3", "#", "C3", "#", "D3", "#", " ", " "],
        [" ", " ", "#", "A4", "#", "B4", "#", "C4", "#", "D4", "#", " ", " "],
        [" ", " ", "#", "#", "#", "#", "#", "#", "#", "#", "#", " ", " "],
    ]
    if group_size == 2:
        del rows[4:6]

    text = ""
    for row in rows:
        text += "".join(
            "ABCD"[state.index(i) // group_size]
            if i in state
            else i
            if i in ".# "
            else "."
            for i in row
        )
        text += "\n"

    return text


amphipod_costs = {"A": 1, "B": 10, "C": 100, "D": 1000}


if part_to_test == 1:
    len_state = 8
    group_size = len_state // 4

    amphipod_targets = ["A", "A", "B", "B", "C", "C", "D", "D"]
    amphipod_all_targets = [["A1", "A2"], ["B1", "B2"], ["C1", "C2"], ["D1", "D2"]]
    amphipods_edges = {
        "LL": {"LR": 1},
        "LR": {"LL": 1, "A1": 2, "B1": 4, "C1": 6, "D1": 8},
        "A1": {
            "B1": 4,
            "C1": 6,
            "D1": 8,
            "A2": 1,
            "LR": 2,
            "XAB": 2,
            "XBC": 4,
            "XCD": 6,
            "RL": 8,
        },
        "A2": {"A1": 1},
        "XAB": {"A1": 2, "B1": 2, "C1": 4, "D1": 6},
        "B1": {
            "A1": 4,
            "C1": 4,
            "D1": 6,
            "B2": 1,
            "LR": 4,
            "XAB": 2,
            "XBC": 2,
            "XCD": 4,
            "RL": 6,
        },
        "B2": {"B1": 1},
        "XBC": {"B1": 2, "C1": 2, "A1": 4, "D1": 4},
        "C1": {
            "A1": 6,
            "B1": 4,
            "D1": 4,
            "C2": 1,
            "LR": 6,
            "XAB": 4,
            "XBC": 2,
            "XCD": 2,
            "RL": 4,
        },
        "C2": {"C1": 1},
        "XCD": {"C1": 2, "D1": 2, "A1": 6, "B1": 4},
        "D1": {
            "A1": 8,
            "B1": 6,
            "C1": 4,
            "D2": 1,
            "LR": 8,
            "XAB": 6,
            "XBC": 4,
            "XCD": 2,
            "RL": 2,
        },
        "D2": {"D1": 1},
        "RL": {"RR": 1, "A1": 8, "B1": 6, "C1": 4, "D1": 2},
        "RR": {"RL": 1},
    }

    amphipods_edges_conditions = {
        "XAB": {"C1": ["XBC"], "D1": ["XBC", "XCD"]},
        "XBC": {"A1": ["XAB"], "D1": ["XCD"]},
        "XCD": {"A1": ["XAB", "XBC"], "B1": ["XBC"]},
        "A1": {
            "B1": ["XAB"],
            "C1": ["XAB", "XBC"],
            "D1": ["XAB", "XBC", "XCD"],
            "RL": ["XAB", "XBC", "XCD"],
            "XBC": ["XAB"],
            "XCD": ["XAB", "XBC"],
        },
        "B1": {
            "A1": ["XAB"],
            "C1": ["XBC"],
            "D1": ["XBC", "XCD"],
            "LR": ["XAB"],
            "RL": ["XBC", "XCD"],
            "XCD": ["XBC"],
        },
        "C1": {
            "A1": ["XAB", "XBC"],
            "B1": ["XBC"],
            "D1": ["XCD"],
            "LR": ["XAB", "XBC"],
            "RL": ["XCD"],
            "XAB": ["XBC"],
        },
        "D1": {
            "A1": ["XAB", "XBC", "XCD"],
            "B1": ["XBC", "XCD"],
            "C1": ["XCD"],
            "LR": ["XAB", "XBC", "XCD"],
            "XAB": ["XBC", "XCD"],
            "XBC": ["XCD"],
        },
        "LR": {"B1": ["XAB"], "C1": ["XAB", "XBC"], "D1": ["XAB", "XBC", "XCD"]},
        "RL": {"A1": ["XAB", "XBC", "XCD"], "B1": ["XBC", "XCD"], "C1": ["XCD"]},
    }

    start_points = {
        1: ("A2", "D2", "A1", "C1", "B1", "C2", "B2", "D1"),
        #############
        # ...........#
        ###B#C#B#D###
        # A#D#C#A#
        #########
        "real": ("A1", "C2", "C1", "D1", "B1", "D2", "A2", "B2")
        #############
        # ...........#
        ###A#C#B#B###
        # D#D#A#C#
        #########
    }
    start = start_points[case_to_test]

    if case_to_test == 1:

        ######is_state_valid
        if check_assertions:
            state = start_points[case_to_test]
            assert is_state_valid(state) == True

            state = ("A1", "A2", "A1", "A2", "B4", "B2", "B3", "B2")
            assert is_state_valid(state) == False

        ######is_state_final
        if check_assertions:
            state = start_points[case_to_test]
            assert is_state_final(state) == False

            state = ("A1", "A2", "B4", "B2", "C4", "C2", "D2", "D3")
            assert is_state_final(state) == True

        ######is_movement_valid
        if check_assertions:
            # Rule set:
            # Move within room
            # Allowed: Moving down in target room if full of friends
            # Forbidden: Moving down in target room if full of friends
            # Allowed: Moving up in target room if has other people
            # Forbidden: Moving down in target room if has other people
            # Forbidden: Moving from hallway to another hallway : Prevented by amphipods_edges (not tested here)
            # Forbidden: Moving from X to another X is forbidden : Prevented by amphipods_edges (not tested here)
            # Allowed: move within L or R spaces
            # Allowed: Moving up in other's room
            # Move to target
            # Forbidden: Moving to my room if there are others in it
            # Forbidden: Moving to my room with something in between
            # Allowed: Moving to my room if only same amphibots are in and no obstacle
            # Allowed: Moving to my room if empty and no obstacle
            # Move to hallway from a room
            # Forbidden: Moving out of my room if it's empty
            # Forbidden: Moving out of my room if it's full of friends
            # Allowed: Moving out of my room if there are other people in it and no obstacle
            # Allowed: Moving out of other's room if there are no obstacle
            # Forbidden: Moving to other's room

            # Move within room

            # Allowed: Moving down in target room if full of friends
            # Forbidden: Moving down in target room if full of friends
            # Allowed: Moving up in target room if has other people
            # Forbidden: Moving down in target room if has other people
            # Technically not feasible because there are 2 places only

            # Allowed: move within L or R spaces
            _, source = tuple_replace(start, "A2", "LL")
            changed, target = tuple_replace(source, "LL", "LR")
            assert is_movement_valid(source, target, changed) == (True, False)

            # Allowed: Moving up in other's room
            _, source = tuple_replace(start, "B1", "LL")
            changed, target = tuple_replace(source, "B2", "B1")
            assert is_movement_valid(source, target, changed) == (True, True)

            # state = ('A2', 'D2', 'A1', 'C1', 'B1', 'C2', 'B2', 'D1')

            # Move to target

            # Forbidden: Moving to my room if there are others in it
            _, source = tuple_replace(start, "D1", "LR")
            changed, target = tuple_replace(source, "LR", "D1")
            assert is_movement_valid(source, target, changed) == (False, False)

            # Forbidden: Moving to my room with something in between
            _, source = tuple_replace(start, "D1", "XAB")
            _, source = tuple_replace(source, "A2", "XBC")
            changed, target = tuple_replace(source, "XAB", "D1")
            assert is_movement_valid(source, target, changed) == (False, False)

            # Allowed: Moving to my room if only same amphibots are in and no obstacle
            source = ("A2", "XAB", "LR", "C1", "B1", "C2", "B2", "D1")
            changed, target = tuple_replace(source, "XAB", "A1")
            assert is_movement_valid(source, target, changed) == (True, True)

            # Allowed: Moving to my room if empty and no obstacle
            source = ("LR", "XAB", "LR", "C1", "B1", "C2", "B2", "D1")
            changed, target = tuple_replace(source, "XAB", "A1")
            assert is_movement_valid(source, target, changed) == (True, True)

            # Move to hallway from a room

            # Forbidden: Moving out of my room if it's empty
            source = ("A2", "LL", "A1", "C1", "B1", "C2", "B2", "D1")
            changed, target = tuple_replace(source, "D1", "XAB")
            assert is_movement_valid(source, target, changed) == (False, False)

            # Forbidden: Moving out of my room if it's full of friends
            source = ("A2", "LL", "A1", "C1", "B1", "C2", "D2", "D1")
            changed, target = tuple_replace(source, "D1", "XCD")
            assert is_movement_valid(source, target, changed) == (False, False)

            # Allowed: Moving out of my room if there are other people in it and no obstacle
            source = ("A2", "D2", "A1", "C1", "B1", "C2", "B2", "D1")
            changed, target = tuple_replace(source, "D1", "XAB")
            assert is_movement_valid(source, target, changed) == (True, False)

            # Allowed: Moving out of other's room if there are no obstacle
            source = start
            changed, target = tuple_replace(source, "A1", "XAB")
            assert is_movement_valid(source, target, changed) == (True, False)

            # Forbidden: Moving to other's room
            source = ("XAB", "D2", "A1", "C1", "LR", "C2", "B2", "D1")
            changed, target = tuple_replace(source, "XAB", "B1")
            assert is_movement_valid(source, target, changed) == (False, False)

        ######estimate_to_complete_amphipod ==> via estimate_to_complete

        ######estimate_to_complete
        if check_assertions:
            # Start ('A2', 'D2', 'A1', 'C1', 'B1', 'C2', 'B2', 'D1')

            # Estimate when on target
            state = ("A1", "A2", "B1", "B2", "C1", "C2", "D1", "D2")
            assert estimate_to_complete(state_to_tuple(state)) == 0

            # Estimate when 1 is missing
            state = ("XAB", "A2", "B1", "B2", "C1", "C2", "D1", "D2")
            assert estimate_to_complete(state_to_tuple(state)) == 2

            # Estimate when 1 is missing for B
            state = ("A1", "A2", "XCD", "B2", "C1", "C2", "D1", "D2")
            assert estimate_to_complete(state_to_tuple(state)) == 40

            # Estimate when 2 are inverted
            state = ("B1", "A2", "A1", "B2", "C1", "C2", "D1", "D2")
            assert estimate_to_complete(state_to_tuple(state)) == 44

            # Estimate when 2 are inverted in bottom pieces
            state = ("B2", "A1", "A2", "B1", "C1", "C2", "D1", "D2")
            assert estimate_to_complete(state_to_tuple(state)) == 66

            # Estimate when start in LL
            state = ("LL", "A2", "B1", "B2", "C1", "C2", "D1", "D2")
            assert estimate_to_complete(state_to_tuple(state)) == 3

        ######Manual testing of solution
        if check_assertions:
            states = [
                start,
                ("A2", "D2", "A1", "C1", "B1", "C2", "B2", "RL"),
                ("A2", "D1", "A1", "C1", "B1", "C2", "B2", "RL"),
                ("A2", "LR", "A1", "C1", "B1", "C2", "B2", "RL"),
                ("A2", "LR", "A1", "C1", "B1", "C2", "B2", "D1"),
                ("A2", "LR", "A1", "XAB", "B1", "C2", "B2", "D1"),
                ("A2", "LR", "A1", "XAB", "XBC", "C2", "B2", "D1"),
                ("A2", "LR", "A1", "XAB", "C1", "C2", "B2", "D1"),
                ("A2", "LR", "A1", "XAB", "C1", "C2", "B1", "D1"),
                ("A2", "LR", "A1", "XAB", "C1", "C2", "XBC", "D1"),
                ("A2", "LR", "A1", "B1", "C1", "C2", "XBC", "D1"),
                ("A2", "LR", "A1", "B1", "C1", "C2", "XBC", "D2"),
                ("A2", "LR", "A1", "B1", "C1", "C2", "D1", "D2"),
                ("A2", "LR", "XAB", "B1", "C1", "C2", "D1", "D2"),
                ("A2", "A1", "XAB", "B1", "C1", "C2", "D1", "D2"),
                ("A2", "A1", "XAB", "B2", "C1", "C2", "D1", "D2"),
                ("A2", "A1", "B1", "B2", "C1", "C2", "D1", "D2"),
            ]

            total_cost = 0
            for i in range(len(states) - 1):
                print("Starting from", states[i])
                print(state_to_text(states[i]))
                neighbors = get_neighbors(states[i])
                print("Neighbors")
                text = ""
                neighbors_text = [
                    state_to_text(neighbor).splitlines() for neighbor in neighbors
                ]

                nb_row_per_neighbor = len(neighbors_text[0])
                for row in range(
                    math.ceil(len(neighbors_text) / 10) * nb_row_per_neighbor
                ):
                    start_neighbor = row // nb_row_per_neighbor * 10
                    text += (
                        "   ".join(
                            neighbors_text[start_neighbor + i][
                                row % nb_row_per_neighbor
                            ]
                            for i in range(10)
                            if start_neighbor + i < len(neighbors_text)
                        )
                        + "\n"
                    )
                    if row % nb_row_per_neighbor == nb_row_per_neighbor - 1:
                        text += "\n"

                print(text)
                print("Getting to   ", "\n" + state_to_text(states[i + 1]))

                assert states[i + 1] in neighbors
                assert is_state_valid(states[i + 1])
                cost = neighbors[states[i + 1]]
                print(
                    estimate_to_complete(state_to_tuple(states[i])), 44169 - total_cost
                )
                total_cost += cost
                print("Cost", cost)
                input()
            # print ('Total cost', total_cost)


else:
    len_state = 16
    group_size = len_state // 4

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
    amphipod_all_targets = [
        ["A1", "A2", "A3", "A4"],
        ["B1", "B2", "B3", "B4"],
        ["C1", "C2", "C3", "C4"],
        ["D1", "D2", "D3", "D4"],
    ]
    amphipods_edges = {
        "LL": {"LR": 1},
        "LR": {"LL": 1, "A1": 2, "B1": 4, "C1": 6, "D1": 8},
        "A1": {
            "B1": 4,
            "C1": 6,
            "D1": 8,
            "A2": 1,
            "LR": 2,
            "XAB": 2,
            "XBC": 4,
            "XCD": 6,
            "RL": 8,
        },
        "A2": {"A1": 1, "A3": 1},
        "A3": {"A2": 1, "A4": 1},
        "A4": {"A3": 1},
        "XAB": {"A1": 2, "B1": 2, "C1": 4, "D1": 6},
        "B1": {
            "A1": 4,
            "C1": 4,
            "D1": 6,
            "B2": 1,
            "LR": 4,
            "XAB": 2,
            "XBC": 2,
            "XCD": 4,
            "RL": 6,
        },
        "B2": {"B1": 1, "B3": 1},
        "B3": {"B2": 1, "B4": 1},
        "B4": {"B3": 1},
        "XBC": {"B1": 2, "C1": 2, "A1": 4, "D1": 4},
        "C1": {
            "A1": 6,
            "B1": 4,
            "D1": 4,
            "C2": 1,
            "LR": 6,
            "XAB": 4,
            "XBC": 2,
            "XCD": 2,
            "RL": 4,
        },
        "C2": {"C1": 1, "C3": 1},
        "C3": {"C2": 1, "C4": 1},
        "C4": {"C3": 1},
        "XCD": {"C1": 2, "D1": 2, "A1": 6, "B1": 4},
        "D1": {
            "A1": 8,
            "B1": 6,
            "C1": 4,
            "D2": 1,
            "LR": 8,
            "XAB": 6,
            "XBC": 4,
            "XCD": 2,
            "RL": 2,
        },
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
        "A1": {
            "B1": ["XAB"],
            "C1": ["XAB", "XBC"],
            "D1": ["XAB", "XBC", "XCD"],
            "RL": ["XAB", "XBC", "XCD"],
            "XBC": ["XAB"],
            "XCD": ["XAB", "XBC"],
        },
        "B1": {
            "A1": ["XAB"],
            "C1": ["XBC"],
            "D1": ["XBC", "XCD"],
            "LR": ["XAB"],
            "RL": ["XBC", "XCD"],
            "XCD": ["XBC"],
        },
        "C1": {
            "A1": ["XAB", "XBC"],
            "B1": ["XBC"],
            "D1": ["XCD"],
            "LR": ["XAB", "XBC"],
            "RL": ["XCD"],
            "XAB": ["XBC"],
        },
        "D1": {
            "A1": ["XAB", "XBC", "XCD"],
            "B1": ["XBC", "XCD"],
            "C1": ["XCD"],
            "LR": ["XAB", "XBC", "XCD"],
            "XAB": ["XBC", "XCD"],
            "XBC": ["XCD"],
        },
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

    if case_to_test == 1:

        ######is_state_valid
        if check_assertions:

            state = start_points[case_to_test]
            assert is_state_valid(state) == True

            state = (
                "A1",
                "A2",
                "A1",
                "A2",
                "B4",
                "B2",
                "B3",
                "B2",
                "C1",
                "C2",
                "C1",
                "C2",
                "D2",
                "D3",
                "D2",
                "D4",
            )
            assert is_state_valid(state) == False

        ######is_state_final
        if check_assertions:
            state = start_points[case_to_test]
            assert is_state_final(state) == False

            state = (
                "A1",
                "A2",
                "A4",
                "A3",
                "B4",
                "B2",
                "B3",
                "B1",
                "C4",
                "C2",
                "C1",
                "C3",
                "D2",
                "D3",
                "D1",
                "D4",
            )
            assert is_state_final(state) == True

        ######is_movement_valid
        if check_assertions:
            # Rule set:
            # Move within room
            # Allowed: Moving down in target room if full of friends
            # Forbidden: Moving down in target room if full of friends
            # Allowed: Moving up in target room if has other people
            # Forbidden: Moving down in target room if has other people
            # Forbidden: Moving from hallway to another hallway : Prevented by amphipods_edges (not tested here)
            # Forbidden: Moving from X to another X is forbidden : Prevented by amphipods_edges (not tested here)
            # Allowed: move within L or R spaces
            # Allowed: Moving up in other's room
            # Move to target
            # Forbidden: Moving to my room if there are others in it
            # Forbidden: Moving to my room with something in between
            # Allowed: Moving to my room if only same amphibots are in and no obstacle
            # Allowed: Moving to my room if empty and no obstacle
            # Move to hallway from a room
            # Forbidden: Moving out of my room if it's empty
            # Forbidden: Moving out of my room if it's full of friends
            # Allowed: Moving out of my room if there are other people in it and no obstacle
            # Allowed: Moving out of other's room if there are no obstacle
            # Forbidden: Moving to other's room

            # Move within room

            # Allowed: Moving down in target room if full of friends
            source = (
                "A4",
                "A2",
                "D2",
                "D4",
                "LR",
                "B3",
                "C1",
                "C2",
                "B1",
                "B2",
                "C4",
                "D3",
                "LR",
                "LL",
                "B4",
                "D1",
            )
            changed, target = tuple_replace(source, "A2", "A3")
            assert is_movement_valid(source, target, changed) == (True, False)
            # Forbidden: Moving down in target room if full of friends
            changed, target = tuple_replace(source, "A2", "A1")
            assert is_movement_valid(source, target, changed) == (False, False)

            # Allowed: Moving up in target room if has other people
            source = (
                "A3",
                "LR",
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
                "A1",
                "LL",
                "B4",
                "D1",
            )
            changed, target = tuple_replace(source, "A3", "A2")
            assert is_movement_valid(source, target, changed) == (True, False)
            # Forbidden: Moving down in target room if has other people
            source = (
                "A3",
                "LR",
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
                "A1",
                "LL",
                "B4",
                "D1",
            )
            changed, target = tuple_replace(source, "A3", "A4")
            assert is_movement_valid(source, target, changed) == (False, False)

            # Allowed: move within L or R spaces
            _, source = tuple_replace(start, "A4", "LL")
            changed, target = tuple_replace(source, "LL", "LR")
            assert is_movement_valid(source, target, changed) == (True, False)

            # Allowed: Moving up in other's room
            _, source = tuple_replace(start, "A1", "LL")
            changed, target = tuple_replace(source, "A2", "A1")
            assert is_movement_valid(source, target, changed) == (True, True)

            # Move to target

            # Forbidden: Moving to my room if there are others in it
            _, source = tuple_replace(start, "D1", "LR")
            changed, target = tuple_replace(source, "LR", "D1")
            assert is_movement_valid(source, target, changed) == (False, False)

            # Forbidden: Moving to my room with something in between
            _, source = tuple_replace(start, "D1", "XAB")
            _, source = tuple_replace(source, "A4", "XBC")
            changed, target = tuple_replace(source, "XAB", "D1")
            assert is_movement_valid(source, target, changed) == (False, False)

            # Allowed: Moving to my room if only same amphibots are in and no obstacle
            source = (
                "A3",
                "C3",
                "RL",
                "D4",
                "LL",
                "B3",
                "C1",
                "C2",
                "B1",
                "B2",
                "C4",
                "D3",
                "LR",
                "RR",
                "B4",
                "D1",
            )
            changed, target = tuple_replace(source, "RL", "A1")
            assert is_movement_valid(source, target, changed) == (True, True)
            source = (
                "A3",
                "A2",
                "RL",
                "D4",
                "LL",
                "B3",
                "C1",
                "C2",
                "B1",
                "B2",
                "C4",
                "D3",
                "LR",
                "RR",
                "B4",
                "D1",
            )
            changed, target = tuple_replace(source, "RL", "A1")
            assert is_movement_valid(source, target, changed) == (True, True)

            # Allowed: Moving to my room if empty and no obstacle
            source = (
                "RL",
                "C3",
                "XCD",
                "D4",
                "LL",
                "B3",
                "C1",
                "C2",
                "B1",
                "B2",
                "C4",
                "D3",
                "LR",
                "RR",
                "B4",
                "D1",
            )
            changed, target = tuple_replace(source, "XCD", "A1")
            assert is_movement_valid(source, target, changed) == (True, True)

            # Move to hallway from a room

            # Forbidden: Moving out of my room if it's empty
            source = (
                "A4",
                "C3",
                "LL",
                "LR",
                "A1",
                "B3",
                "C1",
                "C2",
                "B1",
                "B2",
                "C4",
                "RR",
                "A2",
                "A3",
                "B4",
                "D1",
            )
            changed, target = tuple_replace(source, "D1", "XAB")
            assert is_movement_valid(source, target, changed) == (False, False)

            # Forbidden: Moving out of my room if it's full of friends
            source = (
                "A4",
                "C3",
                "A2",
                "A3",
                "A1",
                "B3",
                "C1",
                "C2",
                "B1",
                "B2",
                "C4",
                "XAB",
                "D2",
                "D4",
                "LL",
                "D1",
            )
            changed, target = tuple_replace(source, "D1", "XCD")
            assert is_movement_valid(source, target, changed) == (False, False)

            # Allowed: Moving out of my room if there are other people in it and no obstacle
            source = (
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
            )
            changed, target = tuple_replace(source, "D1", "XAB")
            assert is_movement_valid(source, target, changed) == (True, False)

            # Allowed: Moving out of other's room if there are no obstacle
            source = start
            changed, target = tuple_replace(source, "A1", "XAB")
            assert is_movement_valid(source, target, changed) == (True, False)

            # Forbidden: Moving to other's room
            source = (
                "A4",
                "XAB",
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
                "LR",
            )
            changed, target = tuple_replace(source, "XAB", "D1")
            assert is_movement_valid(source, target, changed) == (False, False)

        ######estimate_to_complete_amphipod ==> via estimate_to_complete

        ######estimate_to_complete
        if check_assertions:

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
            assert estimate_to_complete(state_to_tuple(state)) == 0

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
            assert estimate_to_complete(state_to_tuple(state)) == 2

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
            assert estimate_to_complete(state_to_tuple(state)) == 40

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
            assert estimate_to_complete(state_to_tuple(state)) == 47

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
            assert estimate_to_complete(state_to_tuple(state)) == 3

        ######Manual testing of solution - Also allows to identify possible improvements
        if check_assertions:
            states = [
                start,
                (
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
                    "RL",
                ),
                (
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
                    "RR",
                ),
                (
                    "A4",
                    "C3",
                    "D1",
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
                    "RR",
                ),
                (
                    "A4",
                    "C3",
                    "LR",
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
                    "RR",
                ),
                (
                    "A4",
                    "C3",
                    "LL",
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
                    "RR",
                ),
                (
                    "A4",
                    "C3",
                    "LL",
                    "D4",
                    "A1",
                    "B3",
                    "RL",
                    "C2",
                    "B1",
                    "B2",
                    "C4",
                    "D3",
                    "A2",
                    "A3",
                    "B4",
                    "RR",
                ),
                (
                    "A4",
                    "C3",
                    "LL",
                    "D4",
                    "A1",
                    "B3",
                    "RL",
                    "C1",
                    "B1",
                    "B2",
                    "C4",
                    "D3",
                    "A2",
                    "A3",
                    "B4",
                    "RR",
                ),
                (
                    "A4",
                    "C3",
                    "LL",
                    "D4",
                    "A1",
                    "B3",
                    "RL",
                    "XCD",
                    "B1",
                    "B2",
                    "C4",
                    "D3",
                    "A2",
                    "A3",
                    "B4",
                    "RR",
                ),
                (
                    "A4",
                    "C2",
                    "LL",
                    "D4",
                    "A1",
                    "B3",
                    "RL",
                    "XCD",
                    "B1",
                    "B2",
                    "C4",
                    "D3",
                    "A2",
                    "A3",
                    "B4",
                    "RR",
                ),
                (
                    "A4",
                    "C1",
                    "LL",
                    "D4",
                    "A1",
                    "B3",
                    "RL",
                    "XCD",
                    "B1",
                    "B2",
                    "C4",
                    "D3",
                    "A2",
                    "A3",
                    "B4",
                    "RR",
                ),
                (
                    "A4",
                    "LR",
                    "LL",
                    "D4",
                    "A1",
                    "B3",
                    "RL",
                    "XCD",
                    "B1",
                    "B2",
                    "C4",
                    "D3",
                    "A2",
                    "A3",
                    "B4",
                    "RR",
                ),
                (
                    "A4",
                    "LR",
                    "LL",
                    "D4",
                    "A1",
                    "B3",
                    "RL",
                    "XCD",
                    "XBC",
                    "B2",
                    "C4",
                    "D3",
                    "A2",
                    "A3",
                    "B4",
                    "RR",
                ),
                (
                    "A4",
                    "LR",
                    "LL",
                    "D4",
                    "A1",
                    "B3",
                    "RL",
                    "XCD",
                    "C1",
                    "B2",
                    "C4",
                    "D3",
                    "A2",
                    "A3",
                    "B4",
                    "RR",
                ),
                (
                    "A4",
                    "LR",
                    "LL",
                    "D4",
                    "A1",
                    "B3",
                    "RL",
                    "XCD",
                    "C2",
                    "B2",
                    "C4",
                    "D3",
                    "A2",
                    "A3",
                    "B4",
                    "RR",
                ),
                (
                    "A4",
                    "LR",
                    "LL",
                    "D4",
                    "A1",
                    "B3",
                    "RL",
                    "XCD",
                    "C3",
                    "B2",
                    "C4",
                    "D3",
                    "A2",
                    "A3",
                    "B4",
                    "RR",
                ),
                (
                    "A4",
                    "LR",
                    "LL",
                    "D4",
                    "A1",
                    "B3",
                    "RL",
                    "XCD",
                    "C3",
                    "B1",
                    "C4",
                    "D3",
                    "A2",
                    "A3",
                    "B4",
                    "RR",
                ),
                (
                    "A4",
                    "LR",
                    "LL",
                    "D4",
                    "A1",
                    "B3",
                    "RL",
                    "XCD",
                    "C3",
                    "XBC",
                    "C4",
                    "D3",
                    "A2",
                    "A3",
                    "B4",
                    "RR",
                ),
                (
                    "A4",
                    "LR",
                    "LL",
                    "D4",
                    "A1",
                    "B3",
                    "RL",
                    "XCD",
                    "C3",
                    "C1",
                    "C4",
                    "D3",
                    "A2",
                    "A3",
                    "B4",
                    "RR",
                ),
                (
                    "A4",
                    "LR",
                    "LL",
                    "D4",
                    "A1",
                    "B3",
                    "RL",
                    "XCD",
                    "C3",
                    "C2",
                    "C4",
                    "D3",
                    "A2",
                    "A3",
                    "B4",
                    "RR",
                ),
                (
                    "A4",
                    "LR",
                    "LL",
                    "D4",
                    "A1",
                    "B2",
                    "RL",
                    "XCD",
                    "C3",
                    "C2",
                    "C4",
                    "D3",
                    "A2",
                    "A3",
                    "B4",
                    "RR",
                ),
                (
                    "A4",
                    "LR",
                    "LL",
                    "D4",
                    "A1",
                    "B1",
                    "RL",
                    "XCD",
                    "C3",
                    "C2",
                    "C4",
                    "D3",
                    "A2",
                    "A3",
                    "B4",
                    "RR",
                ),
                (
                    "A4",
                    "LR",
                    "LL",
                    "D4",
                    "A1",
                    "XBC",
                    "RL",
                    "XCD",
                    "C3",
                    "C2",
                    "C4",
                    "D3",
                    "A2",
                    "A3",
                    "B4",
                    "RR",
                ),
                (
                    "A4",
                    "LR",
                    "LL",
                    "D4",
                    "A1",
                    "XBC",
                    "RL",
                    "XCD",
                    "C3",
                    "C2",
                    "C4",
                    "D3",
                    "A2",
                    "A3",
                    "B3",
                    "RR",
                ),
                (
                    "A4",
                    "LR",
                    "LL",
                    "D4",
                    "A1",
                    "XBC",
                    "RL",
                    "XCD",
                    "C3",
                    "C2",
                    "C4",
                    "D3",
                    "A2",
                    "A3",
                    "B2",
                    "RR",
                ),
                (
                    "A4",
                    "LR",
                    "LL",
                    "D4",
                    "A1",
                    "XBC",
                    "RL",
                    "XCD",
                    "C3",
                    "C2",
                    "C4",
                    "D3",
                    "A2",
                    "A3",
                    "B1",
                    "RR",
                ),
                (
                    "A4",
                    "LR",
                    "LL",
                    "D4",
                    "A1",
                    "XBC",
                    "RL",
                    "XCD",
                    "C3",
                    "C2",
                    "C4",
                    "D3",
                    "A2",
                    "A3",
                    "XAB",
                    "RR",
                ),
                (
                    "A4",
                    "LR",
                    "LL",
                    "D4",
                    "A1",
                    "B1",
                    "RL",
                    "XCD",
                    "C3",
                    "C2",
                    "C4",
                    "D3",
                    "A2",
                    "A3",
                    "XAB",
                    "RR",
                ),
                (
                    "A4",
                    "LR",
                    "LL",
                    "D4",
                    "A1",
                    "B2",
                    "RL",
                    "XCD",
                    "C3",
                    "C2",
                    "C4",
                    "D3",
                    "A2",
                    "A3",
                    "XAB",
                    "RR",
                ),
                (
                    "A4",
                    "LR",
                    "LL",
                    "D4",
                    "A1",
                    "B3",
                    "RL",
                    "XCD",
                    "C3",
                    "C2",
                    "C4",
                    "D3",
                    "A2",
                    "A3",
                    "XAB",
                    "RR",
                ),
                (
                    "A4",
                    "LR",
                    "LL",
                    "D4",
                    "A1",
                    "B4",
                    "RL",
                    "XCD",
                    "C3",
                    "C2",
                    "C4",
                    "D3",
                    "A2",
                    "A3",
                    "XAB",
                    "RR",
                ),
                (
                    "A4",
                    "LR",
                    "LL",
                    "D4",
                    "A1",
                    "B4",
                    "RL",
                    "B1",
                    "C3",
                    "C2",
                    "C4",
                    "D3",
                    "A2",
                    "A3",
                    "XAB",
                    "RR",
                ),
                (
                    "A4",
                    "LR",
                    "LL",
                    "D4",
                    "A1",
                    "B4",
                    "RL",
                    "B2",
                    "C3",
                    "C2",
                    "C4",
                    "D3",
                    "A2",
                    "A3",
                    "XAB",
                    "RR",
                ),
                (
                    "A4",
                    "LR",
                    "LL",
                    "D4",
                    "A1",
                    "B4",
                    "RL",
                    "B3",
                    "C3",
                    "C2",
                    "C4",
                    "D3",
                    "A2",
                    "A3",
                    "XAB",
                    "RR",
                ),
                (
                    "A4",
                    "LR",
                    "LL",
                    "D4",
                    "A1",
                    "B4",
                    "B1",
                    "B3",
                    "C3",
                    "C2",
                    "C4",
                    "D3",
                    "A2",
                    "A3",
                    "XAB",
                    "RR",
                ),
                (
                    "A4",
                    "LR",
                    "LL",
                    "D4",
                    "A1",
                    "B4",
                    "B2",
                    "B3",
                    "C3",
                    "C2",
                    "C4",
                    "D3",
                    "A2",
                    "A3",
                    "XAB",
                    "RR",
                ),
                (
                    "A4",
                    "LR",
                    "LL",
                    "D4",
                    "A1",
                    "B4",
                    "B2",
                    "B3",
                    "C3",
                    "C2",
                    "C4",
                    "D2",
                    "A2",
                    "A3",
                    "XAB",
                    "RR",
                ),
                (
                    "A4",
                    "LR",
                    "LL",
                    "D4",
                    "A1",
                    "B4",
                    "B2",
                    "B3",
                    "C3",
                    "C2",
                    "C4",
                    "D1",
                    "A2",
                    "A3",
                    "XAB",
                    "RR",
                ),
                (
                    "A4",
                    "LR",
                    "LL",
                    "D4",
                    "A1",
                    "B4",
                    "B2",
                    "B3",
                    "C3",
                    "C2",
                    "C4",
                    "XCD",
                    "A2",
                    "A3",
                    "XAB",
                    "RR",
                ),
                (
                    "A4",
                    "LR",
                    "LL",
                    "D4",
                    "A1",
                    "B4",
                    "B2",
                    "B3",
                    "C3",
                    "C2",
                    "C4",
                    "C1",
                    "A2",
                    "A3",
                    "XAB",
                    "RR",
                ),
                (
                    "A4",
                    "LR",
                    "LL",
                    "D3",
                    "A1",
                    "B4",
                    "B2",
                    "B3",
                    "C3",
                    "C2",
                    "C4",
                    "C1",
                    "A2",
                    "A3",
                    "XAB",
                    "RR",
                ),
                (
                    "A4",
                    "LR",
                    "LL",
                    "D2",
                    "A1",
                    "B4",
                    "B2",
                    "B3",
                    "C3",
                    "C2",
                    "C4",
                    "C1",
                    "A2",
                    "A3",
                    "XAB",
                    "RR",
                ),
                (
                    "A4",
                    "LR",
                    "LL",
                    "D1",
                    "A1",
                    "B4",
                    "B2",
                    "B3",
                    "C3",
                    "C2",
                    "C4",
                    "C1",
                    "A2",
                    "A3",
                    "XAB",
                    "RR",
                ),
                (
                    "A4",
                    "LR",
                    "LL",
                    "RL",
                    "A1",
                    "B4",
                    "B2",
                    "B3",
                    "C3",
                    "C2",
                    "C4",
                    "C1",
                    "A2",
                    "A3",
                    "XAB",
                    "RR",
                ),
                (
                    "A4",
                    "LR",
                    "LL",
                    "RL",
                    "A1",
                    "B4",
                    "B2",
                    "B3",
                    "C3",
                    "C2",
                    "C4",
                    "C1",
                    "A2",
                    "A3",
                    "D1",
                    "RR",
                ),
                (
                    "A4",
                    "LR",
                    "LL",
                    "RL",
                    "A1",
                    "B4",
                    "B2",
                    "B3",
                    "C3",
                    "C2",
                    "C4",
                    "C1",
                    "A2",
                    "A3",
                    "D2",
                    "RR",
                ),
                (
                    "A4",
                    "LR",
                    "LL",
                    "RL",
                    "A1",
                    "B4",
                    "B2",
                    "B3",
                    "C3",
                    "C2",
                    "C4",
                    "C1",
                    "A2",
                    "A3",
                    "D3",
                    "RR",
                ),
                (
                    "A4",
                    "LR",
                    "LL",
                    "RL",
                    "A1",
                    "B4",
                    "B2",
                    "B3",
                    "C3",
                    "C2",
                    "C4",
                    "C1",
                    "A2",
                    "A3",
                    "D4",
                    "RR",
                ),
                (
                    "A4",
                    "LR",
                    "LL",
                    "RL",
                    "XAB",
                    "B4",
                    "B2",
                    "B3",
                    "C3",
                    "C2",
                    "C4",
                    "C1",
                    "A2",
                    "A3",
                    "D4",
                    "RR",
                ),
                (
                    "A4",
                    "LR",
                    "LL",
                    "RL",
                    "B1",
                    "B4",
                    "B2",
                    "B3",
                    "C3",
                    "C2",
                    "C4",
                    "C1",
                    "A2",
                    "A3",
                    "D4",
                    "RR",
                ),
                (
                    "A4",
                    "LR",
                    "LL",
                    "RL",
                    "B1",
                    "B4",
                    "B2",
                    "B3",
                    "C3",
                    "C2",
                    "C4",
                    "C1",
                    "A1",
                    "A3",
                    "D4",
                    "RR",
                ),
                (
                    "A4",
                    "LR",
                    "LL",
                    "RL",
                    "B1",
                    "B4",
                    "B2",
                    "B3",
                    "C3",
                    "C2",
                    "C4",
                    "C1",
                    "XCD",
                    "A3",
                    "D4",
                    "RR",
                ),
                (
                    "A4",
                    "LR",
                    "LL",
                    "RL",
                    "B1",
                    "B4",
                    "B2",
                    "B3",
                    "C3",
                    "C2",
                    "C4",
                    "C1",
                    "D1",
                    "A3",
                    "D4",
                    "RR",
                ),
                (
                    "A4",
                    "LR",
                    "LL",
                    "RL",
                    "B1",
                    "B4",
                    "B2",
                    "B3",
                    "C3",
                    "C2",
                    "C4",
                    "C1",
                    "D2",
                    "A3",
                    "D4",
                    "RR",
                ),
                (
                    "A4",
                    "LR",
                    "LL",
                    "RL",
                    "B1",
                    "B4",
                    "B2",
                    "B3",
                    "C3",
                    "C2",
                    "C4",
                    "C1",
                    "D3",
                    "A3",
                    "D4",
                    "RR",
                ),
                (
                    "A4",
                    "LR",
                    "LL",
                    "RL",
                    "B1",
                    "B4",
                    "B2",
                    "B3",
                    "C3",
                    "C2",
                    "C4",
                    "C1",
                    "D3",
                    "A2",
                    "D4",
                    "RR",
                ),
                (
                    "A4",
                    "LR",
                    "LL",
                    "RL",
                    "B1",
                    "B4",
                    "B2",
                    "B3",
                    "C3",
                    "C2",
                    "C4",
                    "C1",
                    "D3",
                    "A1",
                    "D4",
                    "RR",
                ),
                (
                    "A4",
                    "LR",
                    "LL",
                    "RL",
                    "B1",
                    "B4",
                    "B2",
                    "B3",
                    "C3",
                    "C2",
                    "C4",
                    "C1",
                    "D3",
                    "XAB",
                    "D4",
                    "RR",
                ),
                (
                    "A4",
                    "A1",
                    "LL",
                    "RL",
                    "B1",
                    "B4",
                    "B2",
                    "B3",
                    "C3",
                    "C2",
                    "C4",
                    "C1",
                    "D3",
                    "XAB",
                    "D4",
                    "RR",
                ),
                (
                    "A4",
                    "A2",
                    "LL",
                    "RL",
                    "B1",
                    "B4",
                    "B2",
                    "B3",
                    "C3",
                    "C2",
                    "C4",
                    "C1",
                    "D3",
                    "XAB",
                    "D4",
                    "RR",
                ),
                (
                    "A4",
                    "A3",
                    "LL",
                    "RL",
                    "B1",
                    "B4",
                    "B2",
                    "B3",
                    "C3",
                    "C2",
                    "C4",
                    "C1",
                    "D3",
                    "XAB",
                    "D4",
                    "RR",
                ),
                (
                    "A4",
                    "A3",
                    "LR",
                    "RL",
                    "B1",
                    "B4",
                    "B2",
                    "B3",
                    "C3",
                    "C2",
                    "C4",
                    "C1",
                    "D3",
                    "XAB",
                    "D4",
                    "RR",
                ),
                (
                    "A4",
                    "A3",
                    "A1",
                    "RL",
                    "B1",
                    "B4",
                    "B2",
                    "B3",
                    "C3",
                    "C2",
                    "C4",
                    "C1",
                    "D3",
                    "XAB",
                    "D4",
                    "RR",
                ),
                (
                    "A4",
                    "A3",
                    "A2",
                    "RL",
                    "B1",
                    "B4",
                    "B2",
                    "B3",
                    "C3",
                    "C2",
                    "C4",
                    "C1",
                    "D3",
                    "XAB",
                    "D4",
                    "RR",
                ),
                (
                    "A4",
                    "A3",
                    "A2",
                    "RL",
                    "B1",
                    "B4",
                    "B2",
                    "B3",
                    "C3",
                    "C2",
                    "C4",
                    "C1",
                    "D3",
                    "D1",
                    "D4",
                    "RR",
                ),
                (
                    "A4",
                    "A3",
                    "A2",
                    "RL",
                    "B1",
                    "B4",
                    "B2",
                    "B3",
                    "C3",
                    "C2",
                    "C4",
                    "C1",
                    "D3",
                    "D2",
                    "D4",
                    "RR",
                ),
                (
                    "A4",
                    "A3",
                    "A2",
                    "A1",
                    "B1",
                    "B4",
                    "B2",
                    "B3",
                    "C3",
                    "C2",
                    "C4",
                    "C1",
                    "D3",
                    "D2",
                    "D4",
                    "RR",
                ),
                (
                    "A4",
                    "A3",
                    "A2",
                    "A1",
                    "B1",
                    "B4",
                    "B2",
                    "B3",
                    "C3",
                    "C2",
                    "C4",
                    "C1",
                    "D3",
                    "D2",
                    "D4",
                    "RL",
                ),
                (
                    "A4",
                    "A3",
                    "A2",
                    "A1",
                    "B1",
                    "B4",
                    "B2",
                    "B3",
                    "C3",
                    "C2",
                    "C4",
                    "C1",
                    "D3",
                    "D2",
                    "D4",
                    "D1",
                ),
                #############
                # AA.D.....AD#
                ###B#.#C#.###
                # D#B#C#.#
                # D#B#C#.#
                # A#B#C#.#
                #########
            ]

            total_cost = 0
            for i in range(len(states) - 1):
                print("Starting from", i, states[i], "\n" + state_to_text(states[i]))
                neighbors = get_neighbors(states[i])
                print("Neighbors")
                text = ""
                neighbors_text = [
                    state_to_text(neighbor).splitlines() for neighbor in neighbors
                ]

                nb_row_per_neighbor = len(neighbors_text[0])
                for row in range(
                    math.ceil(len(neighbors_text) / 10) * nb_row_per_neighbor
                ):
                    start_neighbor = row // nb_row_per_neighbor * 10
                    text += (
                        "   ".join(
                            neighbors_text[start_neighbor + i][
                                row % nb_row_per_neighbor
                            ]
                            for i in range(10)
                            if start_neighbor + i < len(neighbors_text)
                        )
                        + "\n"
                    )
                    if row % nb_row_per_neighbor == nb_row_per_neighbor - 1:
                        text += "\n"

                print(text)
                print("Getting to   ", "\n" + state_to_text(states[i + 1]))

                assert states[i + 1] in neighbors
                assert is_state_valid(states[i + 1])
                cost = neighbors[states[i + 1]]
                print(
                    estimate_to_complete(state_to_tuple(states[i])), 44169 - total_cost
                )
                total_cost += cost
                print("Cost", cost)
                # input()
            exit()
            # print ('Total cost', total_cost)


amphipod_graph = StateGraph()

print("Estimate from start", estimate_to_complete(state_to_tuple(start)))

cProfile.run("amphipod_graph.a_star_search(start)")
# amphipod_graph.a_star_search(start)
# for final_state in amphipod_graph.final_states:
# print ('Final path', amphipod_graph.path(state_to_tuple(final_state)))


puzzle_actual_result = amphipod_graph.min_distance


# -------------------------------- Outputs / results --------------------------------- #

print("Case :", case_to_test, "- Part", part_to_test)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
# Date created: 2021-12-23 08:11:43.693421
# Part 1: 2021-12-24 01:44:31
# Part 2: 2021-12-26 15:00:00
