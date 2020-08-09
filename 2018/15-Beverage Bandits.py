# -------------------------------- Input data -------------------------------- #
import os, pathfinding, complex_utils, copy

test_data = {}

test = 1
test_data[test] = {
    "input": """#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
#######""",
    "expected": ["36334 (37, 982, E)", "Unknown"],
}

test += 1
test_data[test] = {
    "input": """#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######""",
    "expected": ["39514 (46 rounds, 859 HP, E)", "Unknown"],
}

test += 1
test_data[test] = {
    "input": """#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######""",
    "expected": ["27755 (35 rounds, 793 HP, G)", "Unknown"],
}

test += 1
test_data[test] = {
    "input": """#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######""",
    "expected": ["Unknown", "15 attack power, 4988 (29 rounds, 172 HP)"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read().strip(),
    "expected": ["207542", "64688"],
}

# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"
part_to_test = 2
verbose_level = 1

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Player class definition --------------------------- #


class Player:
    position = 0
    type = ""
    HP = 200
    graph = ""
    alive = True
    attack_power = 3

    def __init__(self, type, position, attack_power=3):
        self.position = position
        self.type = type
        if self.type == "E":
            self.attack_power = attack_power

    def __lt__(self, other):
        if self.position.imag < other.position.imag:
            return True
        else:
            return self.position.real < other.position.real

    def move(self, graph, creatures):
        """
        Searches for the closest ennemy

        :param Graph graph: The game map
        :param list creatures: A list of creatures
        :return: The target position
        """

        # Modify graph so that allies are walls, ennemies are traps
        self.graph = copy.deepcopy(graph)
        verbose = False
        if False:
            verbose = True
        allies = [
            c.position
            for c in creatures
            if c.type == self.type and c != self and c.alive
        ]
        ennemies = [c.position for c in creatures if c.type != self.type and c.alive]

        # Check if there is an ennemy next to me => no movement in this case
        ennemy_next_to_me = [
            self.position
            for dir in complex_utils.directions_straight
            if self.position + dir in ennemies
        ]
        if ennemy_next_to_me:
            return

        self.graph.add_traps(ennemies)
        self.graph.add_walls(allies)

        # Run BFS from my position to determine closest target
        self.graph.breadth_first_search(self.position)

        # Determine all target positions (= cells next to the ennemies), then choose closest
        target_positions = [
            (self.graph.distance_from_start[e + dir], e + dir)
            for e in ennemies
            for dir in complex_utils.directions_straight
            if e + dir in self.graph.distance_from_start
        ]
        if not target_positions:
            return

        min_distance = min([pos[0] for pos in target_positions])
        closest_targets = [pos[1] for pos in target_positions if pos[0] == min_distance]
        target = complex_utils.complex_sort(closest_targets, "reading")[0]

        if min_distance == 0:
            return

        if verbose:
            print("before", self.position, target_positions, closest_targets, target)

        # Then we do the opposite, to know in which direction to go
        # Run BFS from the target
        self.graph.breadth_first_search(target)
        # Determine which direction to go to is best
        next_positions = [
            (self.graph.distance_from_start[self.position + dir], self.position + dir,)
            for dir in complex_utils.directions_straight
            if self.position + dir in self.graph.vertices
        ]
        min_distance = min([pos[0] for pos in next_positions])
        closest_positions = [pos[1] for pos in next_positions if pos[0] == min_distance]
        target = complex_utils.complex_sort(closest_positions, "reading")[0]
        if verbose:
            print(
                "after", self.position, next_positions, closest_positions, target, self
            )

        self.position = target

    def attack(self, creatures):
        """
        Attacks an ennemy in range

        :param Graph graph: The game map
        :param list creatures: A list of creatures
        :return: Nothing
        """

        # Find who to attack
        ennemies = [
            c
            for c in creatures
            for dir in complex_utils.directions_straight
            if self.position + dir == c.position and c.type != self.type and c.alive
        ]
        if not ennemies:
            return

        min_HP_ennemies = player_sort(
            [e for e in ennemies if e.HP == min([e.HP for e in ennemies])]
        )
        ennemy = player_sort(min_HP_ennemies)[0]

        ennemy.lose_HP(self.attack_power)

    def lose_HP(self, HP):
        """
        Loses HP following an attack

        :param int HP: How many HP to lose
        :return: Nothing
        """
        self.HP -= HP
        self.alive = self.HP > 0


def player_sort(players):
    players.sort(key=lambda a: (-a.position.imag, a.position.real))
    return players


# -------------------------------- Actual code execution ----------------------------- #


if part_to_test == 1:
    grid = puzzle_input

    # Initial grid with everything
    graph = pathfinding.Graph()
    graph.grid_to_vertices(grid)

    # Identify all creatures
    creatures = graph.grid_search(grid, ("E", "G"))

    creatures = [
        Player(type, position) for type in creatures for position in creatures[type]
    ]
    factions = set(c.type for c in creatures)

    round = 0
    if verbose_level >= 2:
        print("Start")
        print(graph.vertices_to_grid({c.position: c.type for c in creatures}))
        print([(c.type, c.position, c.HP) for c in player_sort(creatures)])
    while True:
        player_sort(creatures)
        for i, creature in enumerate(creatures):
            if not creature.alive:
                continue
            creature.move(graph, creatures)
            creature.attack(creatures)

        creatures = [c for c in creatures if c.alive]
        factions = set(c.type for c in creatures)
        if len(factions) == 1:
            break

        round += 1
        if verbose_level >= 3:
            print("round", round)
            print(graph.vertices_to_grid({c.position: c.type for c in creatures}))
            print([(c.type, c.position, c.HP, c.alive) for c in player_sort(creatures)])

    if verbose_level >= 2:
        print("End of combat")
        print(graph.vertices_to_grid({c.position: c.type for c in creatures}))
        print([(c.type, c.position, c.HP) for c in player_sort(creatures)])
        print(
            "Reached round:",
            round,
            "- Remaining HP:",
            sum(c.HP for c in creatures),
            "- Winner:",
            factions,
        )
    puzzle_actual_result = sum(c.HP for c in creatures if c.alive) * round


else:
    grid = puzzle_input

    # Initial grid with everything
    graph = pathfinding.Graph()
    graph.grid_to_vertices(grid)

    # Identify all creatures
    creatures_positions = graph.grid_search(grid, ("E", "G"))

    for attack in range(3, 100):
        creatures = [
            Player(type, position, attack)
            for type in creatures_positions
            for position in creatures_positions[type]
        ]
        factions = set(c.type for c in creatures)
        dead_elves = 0

        round = 0
        while dead_elves == 0:
            player_sort(creatures)
            for i, creature in enumerate(creatures):
                if not creature.alive:
                    continue
                creature.move(graph, creatures)
                creature.attack(creatures)

            dead_elves = len([c for c in creatures if c.type == "E" and not c.alive])
            creatures = [c for c in creatures if c.alive]
            factions = set(c.type for c in creatures)
            if len(factions) == 1:
                break

            round += 1

        if verbose_level >= 2:
            print("End of combat with attack", attack)
            if verbose_level >= 3:
                print(graph.vertices_to_grid({c.position: c.type for c in creatures}))
            print(
                "Reached round:",
                round,
                "- Remaining HP:",
                sum(c.HP for c in creatures),
                "- Winner:",
                factions,
            )
            print("Dead elves:", dead_elves)

        if factions == set("E",):
            puzzle_actual_result = sum(c.HP for c in creatures if c.alive) * round
            break

# -------------------------------- Outputs / results -------------------------------- #

print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
