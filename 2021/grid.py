from compass import *
from dot import Dot
from graph import WeightedGraph
import heapq


class Grid:
    # For anisotropic grids, this provides which directions are allowed
    possible_source_directions = {
        ".": directions_straight,
        "#": [],
        " ": [],
        "^": [north, south],
        "v": [north, south],
        ">": [east, west],
        "<": [east, west],
        "+": directions_straight,
        "|": [north, south],
        "-": [east, west],
        "/": directions_straight,
        "\\": directions_straight,
    }
    direction_default = directions_straight
    all_directions = directions_straight

    def __init__(self, dots=[], edges={}, isotropic=True):
        """
        Creates the grid based on the list of dots and edges provided

        :param sequence dots: Either a list of positions or a dict position:terrain
        :param dict edges: Dict of format source:target:distance
        :param Boolean isotropic: Whether directions matter
        """

        self.is_isotropic = bool(isotropic)

        if dots:
            if isinstance(dots, dict):
                if self.is_isotropic:
                    self.dots = {x: Dot(self, x, dots[x]) for x in dots}
                else:
                    self.dots = {x: Dot(self, x[0], dots[x], x[1]) for x in dots}
            else:
                if self.is_isotropic:
                    self.dots = {x: Dot(self, x, None) for x in dots}
                else:
                    self.dots = {x: Dot(self, x[0], None, x[1]) for x in dots}
        else:
            self.dots = {}

        self.edges = edges.copy()
        if edges:
            self.set_edges(self.edges)

        self.width = None
        self.height = None

    def set_edges(self, edges):
        """
        Sets up the edges as neighbors of Dots

        """
        for source in edges:
            if not self.dots[source].neighbors:
                self.dots[source].neighbors = {}
            for target in edges[source]:
                self.dots[source].neighbors[self.dots[target]] = edges[source][target]
            self.dots[source].neighbors_obsolete = False

    def reset_pathfinding(self):
        """
        Resets the pathfinding (= forces recalculation of all neighbors if relevant)

        """
        if self.edges:
            self.set_edges(self.edges)
        else:
            for dot in self.dots.values():
                dot.neighbors_obsolete = True

    def text_to_dots(self, text, ignore_terrain="", convert_to_int=False):
        """
        Converts a text to a set of dots

        The text is expected to be separated by newline characters
        The dots will have x - y * 1j as coordinates

        :param string text: The text to convert
        :param sequence ignore_terrain: Types of terrain to ignore (useful for walls)
        """
        self.dots = {}

        y = 0
        for line in text.splitlines():
            for x in range(len(line)):
                if line[x] not in ignore_terrain:
                    if convert_to_int:
                        value = int(line[x])
                    else:
                        value = line[x]
                    if self.is_isotropic:
                        self.dots[x - y * 1j] = Dot(self, x - y * 1j, value)
                    else:
                        for dir in self.possible_source_directions.get(
                            value, self.direction_default
                        ):
                            self.dots[(x - y * 1j, dir)] = Dot(
                                self, x - y * 1j, value, dir
                            )
            y += 1

    def words_to_dots(self, text, convert_to_int=False):
        """
        Converts a text to a set of dots

        The text is expected to be separated by newline characters
        The dots will have x - y * 1j as coordinates
        Dots are words (rather than letters, like in text_to_dots)

        :param string text: The text to convert
        :param sequence ignore_terrain: Types of terrain to ignore (useful for walls)
        """
        self.dots = {}

        y = 0
        for line in text.splitlines():
            for x in line.split(" "):
                for dir in self.possible_source_directions.get(
                    x, self.direction_default
                ):
                    if convert_to_int:
                        self.dots[(x - y * 1j, dir)] = Dot(
                            self, x - y * 1j, int(x), dir
                        )
                    else:
                        self.dots[(x - y * 1j, dir)] = Dot(self, x - y * 1j, x, dir)
            y += 1

    def dots_to_text(self, mark_coords={}, void=" "):
        """
        Converts dots to a text

        The text will be separated by newline characters

        :param dict mark_coords: List of coordinates to mark, with letter to use
        :param string void: Which character to use when no dot is present
        :return: the text
        """
        text = ""

        min_x, max_x, min_y, max_y = self.get_box()

        # The imaginary axis is reversed compared to reading order
        for y in range(max_y, min_y - 1, -1):
            for x in range(min_x, max_x + 1):
                try:
                    text += str(mark_coords[x + y * 1j])
                except (KeyError, TypeError):
                    if x + y * 1j in mark_coords:
                        text += "X"
                    else:
                        if self.is_isotropic:
                            text += str(self.dots.get(x + y * 1j, void))
                        else:
                            dots = [dot for dot in self.dots if dot[0] == x + y * 1j]
                            if dots:
                                text += str(self.dots.get(dots[0], void))
                            else:
                                text += str(void)
            text += "\n"

        return text

    def get_size(self):
        """
        Gets the width and height of the grid

        :return: the width and height
        """

        if not self.width:
            min_x, max_x, min_y, max_y = self.get_box()

            self.width = max_x - min_x + 1
            self.height = max_y - min_y + 1

        return (self.width, self.height)

    def get_box(self):
        """
        Gets the min/max x and y values

        :return: the minimum and maximum for x and y values
        """

        if not self.dots:
            return (0, 0, 0, 0)
        x_vals = set(dot.position.real for dot in self.dots.values())
        y_vals = set(dot.position.imag for dot in self.dots.values())

        min_x, max_x = int(min(x_vals)), int(max(x_vals))
        min_y, max_y = int(min(y_vals)), int(max(y_vals))
        return (min_x, max_x, min_y, max_y)

    def add_traps(self, traps):
        """
        Adds traps
        """

        for dot in traps:
            if self.is_isotropic:
                self.dots[dot].set_trap(True)
            else:
                # print (dot, self.dots.values())
                if dot in self.dots:
                    self.dots[dot].set_trap(True)
                else:
                    for direction in self.all_directions:
                        if (dot, direction) in self.dots:
                            self.dots[(dot, direction)].set_trap(True)

    def add_walls(self, walls):
        """
        Adds walls
        """

        for dot in walls:
            if self.is_isotropic:
                self.dots[dot].set_wall(True)
            else:
                if dot in self.dots:
                    self.dots[dot].set_wall(True)
                else:
                    for direction in self.all_directions:
                        if (dot, direction) in self.dots:
                            self.dots[(dot, direction)].set_wall(True)

    def get_borders(self):
        """
        Gets the borders of the image

        Only the terrain of the dot will be sent back
        This will be returned in left-to-right, up to bottom reading order
        Newline characters are not included

        :return: a text representing a border
        """

        if not self.dots:
            return (0, 0, 0, 0)
        x_vals = set(map(int, (dot.position.real for dot in self.dots.values())))
        y_vals = set(map(int, (dot.position.imag for dot in self.dots.values())))

        min_x, max_x = int(min(x_vals)), int(max(x_vals))
        min_y, max_y = int(min(y_vals)), int(max(y_vals))

        borders = []
        borders.append([self.dots[x + 1j * max_y] for x in sorted(x_vals)])
        borders.append([self.dots[max_x + 1j * y] for y in sorted(y_vals)])
        borders.append([self.dots[x + 1j * min_y] for x in sorted(x_vals)])
        borders.append([self.dots[min_x + 1j * y] for y in sorted(y_vals)])

        borders_text = []
        for border in borders:
            borders_text.append("".join(dot.terrain for dot in border))

        return borders, borders_text

    def get_columns(self):
        """
        Gets the columns of the image

        :return: a dict of dots
        """

        if not self.dots:
            return (0, 0, 0, 0)
        x_vals = set(map(int, (dot.position.real for dot in self.dots.values())))
        y_vals = set(map(int, (dot.position.imag for dot in self.dots.values())))

        min_x, max_x = int(min(x_vals)), int(max(x_vals))
        min_y, max_y = int(min(y_vals)), int(max(y_vals))

        columns = {}
        for x in x_vals:
            columns[x] = [x + 1j * y for y in y_vals if x + 1j * y in self.dots]

        return columns

    def get_rows(self):
        """
        Gets the rows of the image

        :return: a dict of dots
        """

        if not self.dots:
            return (0, 0, 0, 0)
        x_vals = set(map(int, (dot.position.real for dot in self.dots.values())))
        y_vals = set(map(int, (dot.position.imag for dot in self.dots.values())))

        min_x, max_x = int(min(x_vals)), int(max(x_vals))
        min_y, max_y = int(min(y_vals)), int(max(y_vals))

        rows = {}
        for y in y_vals:
            rows[y] = [x + 1j * y for x in x_vals if x + 1j * y in self.dots]

        return rows

    def rotate(self, angles):
        """
        Rotates clockwise a grid and returns a list of rotated grids

        :param tuple angles: Which angles to use for rotation
        :return: The dots
        """

        rotated_grids = []

        x_vals = set(dot.position.real for dot in self.dots.values())
        y_vals = set(dot.position.imag for dot in self.dots.values())

        min_x, max_x, min_y, max_y = self.get_box()
        width, height = self.get_size()

        if isinstance(angles, int):
            angles = {angles}

        for angle in angles:
            if angle == 0:
                rotated_grids.append(self)
            elif angle == 90:
                rotated_grids.append(
                    Grid(
                        {
                            height - 1 + pos.imag - 1j * pos.real: dot.terrain
                            for pos, dot in self.dots.items()
                        }
                    )
                )
            elif angle == 180:
                rotated_grids.append(
                    Grid(
                        {
                            width
                            - 1
                            - pos.real
                            - 1j * (height - 1 + pos.imag): dot.terrain
                            for pos, dot in self.dots.items()
                        }
                    )
                )
            elif angle == 270:
                rotated_grids.append(
                    Grid(
                        {
                            -pos.imag - 1j * (width - 1 - pos.real): dot.terrain
                            for pos, dot in self.dots.items()
                        }
                    )
                )

        return rotated_grids

    def flip(self, flips):
        """
        Flips a grid and returns a list of grids

        :param tuple flips: Which flips to perform
        :return: The dots
        """

        flipped_grids = []

        x_vals = set(dot.position.real for dot in self.dots.values())
        y_vals = set(dot.position.imag for dot in self.dots.values())

        min_x, max_x, min_y, max_y = self.get_box()
        width, height = self.get_size()

        if isinstance(flips, str):
            flips = {flips}

        for flip in flips:
            if flip == "N":
                flipped_grids.append(self)
            elif flip == "H":
                flipped_grids.append(
                    Grid(
                        {
                            pos.real - 1j * (height - 1 + pos.imag): dot.terrain
                            for pos, dot in self.dots.items()
                        }
                    )
                )
            elif flip == "V":
                flipped_grids.append(
                    Grid(
                        {
                            width - 1 - pos.real + 1j * pos.imag: dot.terrain
                            for pos, dot in self.dots.items()
                        }
                    )
                )

        return flipped_grids

    def crop(self, corners=[], size=0):
        """
        Gets the list of dots within a given area

        :param sequence corners: Either one or 2 corners to use
        :param int or sequence size: The size (width + height, or simply length) to use
        :return: a dict of matching dots
        """

        delta = size - 1
        # top left corner + size are provided
        if delta and len(corners) == 1:
            # The corner is a Dot
            if isinstance(corners[0], Dot):
                min_x, max_x = (
                    int(corners[0].position.real),
                    int(corners[0].position.real) + delta,
                )
                min_y, max_y = (
                    int(corners[0].position.imag) - delta,
                    int(corners[0].position.imag),
                )
            # The corner is a tuple position, direction
            elif isinstance(corners[0], tuple):
                min_x, max_x = int(corners[0][0].real), int(corners[0][0].real + delta)
                min_y, max_y = int(corners[0][0].imag - delta), int(corners[0][0].imag)
            # The corner is a complex number
            else:
                min_x, max_x = int(corners[0].real), int(corners[0].real + delta)
                min_y, max_y = int(corners[0].imag - delta), int(corners[0].imag)

        # Multiple corners are provided
        else:
            # Dots are provided as a Dot instance
            if isinstance(corners[0], Dot):
                x_vals = set(dot.position.real for dot in corners)
                y_vals = set(dot.position.imag for dot in corners)
            # Dots are provided as complex numbers
            else:
                x_vals = set(pos.real for pos in corners)
                y_vals = set(pos.imag for pos in corners)

            min_x, max_x = int(min(x_vals)), int(max(x_vals))
            min_y, max_y = int(min(y_vals)), int(max(y_vals))

        if self.is_isotropic:
            cropped = Grid(
                {
                    x + y * 1j: self.dots[x + y * 1j].terrain
                    for y in range(min_y, max_y + 1)
                    for x in range(min_x, max_x + 1)
                    if x + y * 1j in self.dots
                }
            )
        else:
            cropped = Grid(
                {
                    (x + y * 1j, dir): self.dots[(x + y * 1j, dir)].terrain
                    for y in range(min_y, max_y + 1)
                    for x in range(min_x, max_x + 1)
                    for dir in self.all_directions
                    if (x + y * 1j, dir) in self.dots
                }
            )

        return cropped

    def dijkstra(self, start):
        """
        Applies the Dijkstra algorithm to a given search

        This algorithm is appropriate for "One source, multiple targets"
        It takes into account positive weigths / costs of travelling.
        Negative weights will make the algorithm fail.

        The exploration path is based on concentric shapes
        The frontier elements have identical / similar cost from start
        It'll yield exact result for the path-finding, but it's quite slow

        :param Dot start: The start dot to consider
        """
        current_distance = 0
        if not isinstance(start, Dot):
            start = self.dots[start]
        frontier = [(0, start)]
        heapq.heapify(frontier)
        visited = {start: 0}

        while frontier:
            current_distance, dot = frontier.pop(0)
            neighbors = dot.get_neighbors()
            if not neighbors:
                continue

            for neighbor, weight in neighbors.items():
                if neighbor in visited and visited[neighbor] <= (
                    current_distance + weight
                ):
                    continue
                # Adding for future examination
                frontier.append((current_distance + weight, neighbor))

                # Adding for final search
                visited[neighbor] = current_distance + weight
                start.neighbors[neighbor] = current_distance + weight

    def convert_to_graph(self):
        """
        Converts the grid in a reduced graph for pathfinding

        :return: a WeightedGraph containing all waypoints and links
        """

        waypoints = [
            self.dots[dot_key]
            for dot_key in self.dots
            if self.dots[dot_key].is_waypoint
        ]
        edges = {}

        for waypoint in waypoints:
            self.dijkstra(waypoint)
            distances = waypoint.get_neighbors()
            edges[waypoint] = {
                wp: distances[wp]
                for wp in distances
                if wp != waypoint and wp.is_waypoint
            }

        graph = WeightedGraph(waypoints, edges)
        graph.neighbors = lambda vertex: vertex.get_neighbors()

        return graph


def merge_grids(grids, width, height):
    """
    Merges different grids in a single grid

    All grids are assumed to be of the same size

    :param dict grids: The grids to merge
    :param int width: The width, in number of grids
    :param int height: The height, in number of grids
    :return: The merged grid
    """

    final_grid = Grid()

    part_width, part_height = grids[0].get_size()
    if any([not grid.is_isotropic for grid in grids]):
        print("This works only for isotropic grids")
        return

    grid_nr = 0
    for part_y in range(height):
        for part_x in range(width):
            offset = part_x * part_width - 1j * part_y * part_height
            final_grid.dots.update(
                {
                    (pos + offset): Dot(
                        final_grid, pos + offset, grids[grid_nr].dots[pos].terrain
                    )
                    for pos in grids[grid_nr].dots
                }
            )
            grid_nr += 1

    return final_grid
