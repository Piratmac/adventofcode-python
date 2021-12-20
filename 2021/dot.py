from compass import *
import math


def get_dot_position(element):
    if isinstance(element, Dot):
        return element.position
    else:
        return element


# Defines all directions that can be used (basically, are diagonals allowed?)
all_directions = directions_straight


class Dot:
    # The first level is the actual terrain
    # The second level is, in order: is_walkable, is_waypoint
    # Walkable means you can get on that dot and leave it
    # Waypoints are just cool points (it's meant for reducting the grid to a smaller graph)
    # Isotropic means the direction doesn't matter
    terrain_map = {
        ".": [True, False],
        "#": [False, False],
        " ": [False, False],
        "^": [True, True],
        "v": [True, True],
        ">": [True, True],
        "<": [True, True],
        "+": [True, False],
        "|": [True, False],
        "-": [True, False],
        "/": [True, False],
        "\\": [True, False],
        "X": [True, True],
    }
    terrain_default = "X"

    # Override for printing
    terrain_print = {
        "^": "|",
        "v": "|",
        ">": "-",
        "<": "-",
    }

    # Defines which directions are allowed
    # The first level is the actual terrain
    # The second level is the direction taken to reach the dot
    # The third level are the directions allowed to leave it
    allowed_direction_map = {
        ".": {dir: all_directions for dir in all_directions},
        "#": {},
        " ": {},
        "+": {dir: all_directions for dir in all_directions},
        "|": {north: [north, south], south: [north, south]},
        "^": {north: [north, south], south: [north, south]},
        "v": {north: [north, south], south: [north, south]},
        "-": {east: [east, west], west: [east, west]},
        ">": {east: [east, west], west: [east, west]},
        "<": {east: [east, west], west: [east, west]},
        "\\": {north: [east], east: [north], south: [west], west: [south]},
        "/": {north: [west], east: [south], south: [east], west: [north]},
        "X": {dir: all_directions for dir in all_directions},
    }
    # This has the same format, except the third level has only 1 option
    # Anisotropic grids allow only 1 direction for each (position, source_direction)
    # Target direction is the direction in which I'm going
    allowed_anisotropic_direction_map = {
        ".": {dir: [-dir] for dir in all_directions},
        "#": {},
        " ": {},
        "+": {dir: [-dir] for dir in all_directions},
        "|": {north: [south], south: [north]},
        "^": {north: [south], south: [north]},
        "v": {north: [south], south: [north]},
        "-": {east: [west], west: [east]},
        ">": {east: [west], west: [east]},
        "<": {east: [west], west: [east]},
        "\\": {north: [east], east: [north], south: [west], west: [south]},
        "/": {north: [west], east: [south], south: [east], west: [north]},
        "X": {dir: [-dir] for dir in all_directions},
    }
    # Default allowed directions
    direction_default = all_directions

    # How to sort those dots
    sorting_map = {
        "xy": lambda self, a: (a.real, a.imag),
        "yx": lambda self, a: (a.imag, a.real),
        "reading": lambda self, a: (-a.imag, a.real),
        "manhattan": lambda self, a: (abs(a.real) + abs(a.imag)),
        "*": lambda self, a: (a.imag ** 2 + a.real ** 2) ** 0.5,
    }
    sort_value = sorting_map["*"]

    def __init__(self, grid, position, terrain, source_direction=None):
        self.position = position
        self.grid = grid
        self.set_terrain(terrain)
        self.neighbors = {}
        if self.grid.is_isotropic:
            self.set_directions()
        else:
            if source_direction:
                self.source_direction = source_direction
                self.set_directions()
            else:
                raise ValueError("Anisotropic dots need a source direction")

        self.neighbors_obsolete = True

    # Those functions allow sorting for various purposes
    def __lt__(self, other):
        ref = get_dot_position(other)
        return self.sort_value(self.position) < self.sort_value(ref)

    def __le__(self, other):
        ref = get_dot_position(other)
        return self.sort_value(self.position) <= self.sort_value(ref)

    def __gt__(self, other):
        ref = get_dot_position(other)
        return self.sort_value(self.position) > self.sort_value(ref)

    def __ge__(self, other):
        ref = get_dot_position(other)
        return self.sort_value(self.position) >= self.sort_value(ref)

    def __repr__(self):
        if self.grid.is_isotropic:
            return str(self.terrain) + "@" + complex(self.position).__str__()
        else:
            return (
                str(self.terrain)
                + "@"
                + complex(self.position).__str__()
                + direction_to_text[self.source_direction]
            )

    def __str__(self):
        return str(self.terrain)

    def __add__(self, direction):
        if not direction in self.allowed_directions:
            raise ValueError("Can't add a Dot with forbidden direction")
        position = self.position + direction
        if self.grid.is_isotropic:
            return self.get_dot(position)
        else:
            # For the target dot, I'm coming from the opposite direction
            return self.get_dot((position, -self.allowed_directions[0]))

    def __sub__(self, direction):
        return self.__add__(-direction)

    def phase(self, reference=0):
        ref = get_dot_position(reference)
        return math.atan2(self.position.imag - ref.imag, self.position.real - ref.real)

    def amplitude(self, reference=0):
        ref = get_dot_position(reference)
        return (
            (self.position.imag - ref.imag) ** 2 + (self.position.real - ref.real) ** 2
        ) ** 0.5

    def manhattan_distance(self, reference=0):
        ref = get_dot_position(reference)
        return abs(self.position.imag - ref.imag) + abs(self.position.real - ref.real)

    def set_terrain(self, terrain):
        self.terrain = terrain or self.terrain_default
        self.is_walkable, self.is_waypoint = self.terrain_map.get(
            self.terrain, self.terrain_map[self.terrain_default]
        )

    def set_directions(self):
        terrain = (
            self.terrain
            if self.terrain in self.allowed_direction_map
            else self.terrain_default
        )
        if self.grid.is_isotropic:
            self.allowed_directions = self.allowed_direction_map[terrain].copy()
        else:
            self.allowed_directions = self.allowed_anisotropic_direction_map[
                terrain
            ].get(self.source_direction, [])

    def get_dot(self, dot):
        return self.grid.dots.get(dot, None)

    def get_neighbors(self):
        if self.neighbors_obsolete:
            self.neighbors = {
                self + direction: 1
                for direction in self.allowed_directions
                if (self + direction) and (self + direction).is_walkable
            }

        self.neighbors_obsolete = False
        return self.neighbors

    def set_trap(self, is_trap):
        self.grid.reset_pathfinding()
        if is_trap:
            self.allowed_directions = []
            self.neighbors = {}
            self.neighbors_obsolete = False
        else:
            self.set_directions()

    def set_wall(self, is_wall):
        self.grid.reset_pathfinding()
        if is_wall:
            self.allowed_directions = []
            self.neighbors = {}
            self.neighbors_obsolete = False
            self.is_walkable = False
        else:
            self.set_terrain(self.terrain)
            self.set_directions()
