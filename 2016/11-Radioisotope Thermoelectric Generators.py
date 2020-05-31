# -------------------------------- Input data -------------------------------- #
import os, itertools
import pathfinding

test_data = {}

test = 1
test_data[test] = {"input": """""",
                   "expected": ['Unknown', 'Unknown'],
                  }

test += 1
test_data[test] = {"input": """""",
                   "expected": ['Unknown', 'Unknown'],
                  }

test = 'real'
test_data[test] = {"input": '11112123333',
                   "expected": ['31', 'Unknown'],
                  }

# -------------------------------- Control program execution -------------------------------- #

case_to_test  = 'real'
part_to_test  = 2
verbose_level = 1

# -------------------------------- Initialize some variables -------------------------------- #

puzzle_input           = test_data[case_to_test]['input']
puzzle_expected_result = test_data[case_to_test]['expected'][part_to_test-1]
puzzle_actual_result   = 'Unknown'




# -------------------------------- Actual code execution -------------------------------- #



if part_to_test == 1:
    # -------------------------------- Graph-related functions -------------------------------- #
    # Re-implement the heuristic to match this graph
    def heuristic (self, current_node, target_node):
      return sum([abs(int(target_node[i]) - int(current_node[i])) for i in range (1, len(current_node))]) // 2
    pathfinding.WeightedGraph.heuristic = heuristic


    # How to determine neighbors
    def neighbors (self, state):
        global states
        E = int(state[0])
        movables = [x for x in range(1, len(state)) if state[x] == state[0]]

        # Connecting if we move 1 element only
        possible_neighbors = []
        for movable in movables:
            if E > 1:
                neighbor = str(E-1) + state[1:movable] + str(int(state[movable])-1) + state[movable+1:]
                possible_neighbors.append(neighbor)
            if E < 4:
                neighbor = str(E+1) + state[1:movable] + str(int(state[movable])+1) + state[movable+1:]
                possible_neighbors.append(neighbor)

        if len(movables) >= 2:
            for moved_objects in itertools.combinations(movables, 2):
                mov1, mov2 = moved_objects
                # No use to bring 2 items downstairs
    #            if E > 1:
    #                neighbor = str(E-1) + state[1:mov1] + str(int(state[mov1])-1) + state[mov1+1:mov2] + str(int(state[mov2])-1) + state[mov2+1:]
    #                possible_neighbors.append(neighbor)
                if E < 4:
                    neighbor = str(E+1) + state[1:mov1] + str(int(state[mov1])+1) + state[mov1+1:mov2] + str(int(state[mov2])+1) + state[mov2+1:]
                    possible_neighbors.append(neighbor)

        return [x for x in possible_neighbors if x in states]

    pathfinding.WeightedGraph.neighbors = neighbors

    def cost(self, current_node, next_node):
        return 1
    pathfinding.WeightedGraph.cost = cost


    # -------------------------------- Graph construction & execution -------------------------------- #

    # state = (E, TG, TM, PtG, PtM, SG, SM, PrG, PrM, RG, RM)
    # Forbidden states: Any G + M if G for M is absent
    # Forbidden transitions: E changes, the rest is identical

    states = set([''.join([str(E), str(TG), str(TM), str(PtG), str(PtM), str(SG), str(SM), str(PrG), str(PrM), str(RG), str(RM)])
              for E in range(1, 5)
              for TG in range(1, 5)
              for TM in range(1, 5)
              for PtG in range(1, 5)
              for PtM in range(1, 5)
              for SG in range(1, 5)
              for SM in range(1, 5)
              for PrG in range(1, 5)
              for PrM in range(1, 5)
              for RG in range(1, 5)
              for RM in range(1, 5)

              if  (TG  == TM  or TM  not in (TG, PtG, SG, PrG, RG))
              and (PtG == PtM or PtM not in (TG, PtG, SG, PrG, RG))
              and (SG  == SM  or SM  not in (TG, PtG, SG, PrG, RG))
              and (PrG == PrM or PrM not in (TG, PtG, SG, PrG, RG))
              and (RG  == RM  or RM  not in (TG, PtG, SG, PrG, RG))
           ])

    end = '4' * 11

    graph = pathfinding.WeightedGraph()
    came_from, total_cost = graph.a_star_search(puzzle_input, end)

    puzzle_actual_result = total_cost[end]

else:
    # -------------------------------- Graph-related functions -------------------------------- #
    # Part 2 was completely rewritten for performance improvements

    def valid_state (state):
        pairs = [(state[x], state[x+1]) for x in range (1, len(state), 2)]
        generators = state[1::2]

        for pair in pairs:
            if pair[0] != pair[1]: # Microchip is not with generator
                if pair[1] in generators: # Microchip is with a generator
                    return False

        return True

    def visited_state(state):
        global visited_coded_states

        pairs = [(state[x], state[x+1]) for x in range (1, len(state), 2)]

        coded_state = [(state[0], pair) for pair in sorted(pairs)]

        if coded_state in visited_coded_states:
            return True
        else:
            visited_coded_states.append(coded_state)
            return False


    # -------------------------------- BFS implementation -------------------------------- #
    start = list(map(int, puzzle_input)) + [1] * 4
    end = [4] * 15

    visited_coded_states = []
    frontier = [(start, 0)]

    for status in frontier:
        state, curr_steps = status

        # Determine potential states to go to
        elev_position = state[0]
        # The +1 ignores the elevator
        elements_at_level = [item+1 for item, level in enumerate(state[1:]) if level == elev_position]

        movables = list(itertools.combinations(elements_at_level, 2)) + elements_at_level

        if elev_position == 1:
            directions = [1]
        elif elev_position == 4:
            directions = [-1]
        else:
            directions = [1, -1]

        for direction in directions:
            for movable in movables:
                new_state = state.copy()

                new_floor = elev_position + direction
                new_state[0] = new_floor
                if isinstance(movable, tuple):
                # No point in moving 2 items downwards
                    if direction == -1:
                        continue
                    new_state[movable[0]] = new_floor
                    new_state[movable[1]] = new_floor
                else:
                    new_state[movable] = new_floor

                if valid_state(new_state):
                    if visited_state(new_state):
                        continue
                    else:
                        frontier.append((new_state, curr_steps+1))

                if new_state == end:
                    puzzle_actual_result = curr_steps + 1
                    break

            if puzzle_actual_result != 'Unknown':
                break

        if puzzle_actual_result != 'Unknown':
            break







    puzzle_actual_result = curr_steps + 1







# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
    print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : ' + str(puzzle_actual_result))




